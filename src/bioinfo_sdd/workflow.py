"""Deterministic local workflow runner for section SDD."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .checks import CheckResult, run_check
from .io import append_jsonl, read_yaml, utc_now, write_json
from .models import load_section
from .sections import gate_status


class WorkflowRunner:
    def __init__(self, root: Path, workflow_path: Path, section_dir: Path, run_id: str) -> None:
        self.root = root
        self.workflow_path = workflow_path
        self.workflow = read_yaml(workflow_path)
        self.section_dir = section_dir
        self.section = load_section(section_dir)
        self.run_id = run_id
        self.run_dir = section_dir / "runs" / run_id
        self.state_path = self.run_dir / "state.json"
        self.log_path = self.run_dir / "log.jsonl"
        self.checks_dir = self.run_dir / "checks"

    def _base_state(self) -> dict[str, Any]:
        return {
            "schema_version": "0.1.0",
            "section_id": self.section.section_id,
            "run_id": self.run_id,
            "workflow_id": self.workflow.get("workflow_id", "section-sdd"),
            "status": "running",
            "current_step_index": 0,
            "completed_steps": [],
            "updated_at": utc_now(),
        }

    def _load_state(self) -> dict[str, Any]:
        if self.state_path.exists():
            import json

            return json.loads(self.state_path.read_text(encoding="utf-8"))
        return self._base_state()

    def _write_state(self, state: dict[str, Any]) -> None:
        state["updated_at"] = utc_now()
        write_json(self.state_path, state)

    def _log(self, event: str, **payload: Any) -> None:
        append_jsonl(
            self.log_path,
            {
                "timestamp": utc_now(),
                "event": event,
                "section_id": self.section.section_id,
                "run_id": self.run_id,
                **payload,
            },
        )

    def _record_check(self, result: CheckResult) -> None:
        write_json(self.checks_dir / f"{result.check_id}.json", result.to_dict())

    def _record_evidence_summary(self) -> CheckResult:
        checks = []
        if self.checks_dir.exists():
            checks = sorted(path.name for path in self.checks_dir.glob("*.json"))
        evidence_path = self.section_dir / "evidence.md"
        try:
            evidence = str(evidence_path.relative_to(self.root))
        except ValueError:
            evidence = str(evidence_path)
        result = CheckResult(
            "evidence_summary",
            "pass",
            "evidence summary recorded for completed deterministic checks",
            {
                "evidence": evidence,
                "checks": checks,
            },
        )
        self._record_check(result)
        return result

    def run(self) -> dict[str, Any]:
        state = self._load_state()
        if state.get("status") in {"completed", "rejected"}:
            return state
        state["status"] = "running"
        self._write_state(state)
        self._log("workflow_started", current_step_index=state["current_step_index"])

        steps = self.workflow.get("steps") or []
        index = int(state.get("current_step_index", 0))
        while index < len(steps):
            step = steps[index]
            step_id = step["id"]
            step_type = step["type"]
            self._log("step_started", step_id=step_id, step_type=step_type)

            if step_type == "validate_section":
                result = run_check("section_schema", self.root, self.section_dir)
                self._record_check(result)
                if result.status == "fail":
                    state.update({"status": "failed", "failed_step": step_id, "failure_reason": result.summary})
                    self._write_state(state)
                    self._log("step_failed", step_id=step_id, result=result.to_dict())
                    return state

            elif step_type == "gate":
                gate = step["gate"]
                status = gate_status(self.section_dir, gate)
                if status == "pending":
                    state.update({"status": "paused", "paused_step": step_id, "paused_gate": gate})
                    self._write_state(state)
                    self._log("workflow_paused", step_id=step_id, gate=gate)
                    return state
                if status == "rejected":
                    state.update({"status": "rejected", "rejected_step": step_id, "rejected_gate": gate})
                    self._write_state(state)
                    self._log("workflow_rejected", step_id=step_id, gate=gate)
                    return state

            elif step_type == "run_check":
                result = run_check(step["check"], self.root, self.section_dir)
                self._record_check(result)
                if result.status == "fail":
                    state.update({"status": "failed", "failed_step": step_id, "failure_reason": result.summary})
                    self._write_state(state)
                    self._log("step_failed", step_id=step_id, result=result.to_dict())
                    return state

            elif step_type == "record_evidence":
                self._record_evidence_summary()

            else:
                state.update({"status": "failed", "failed_step": step_id, "failure_reason": f"unknown step type {step_type}"})
                self._write_state(state)
                self._log("step_failed", step_id=step_id, step_type=step_type)
                return state

            state.setdefault("completed_steps", []).append(step_id)
            index += 1
            state["current_step_index"] = index
            state.pop("paused_step", None)
            state.pop("paused_gate", None)
            self._write_state(state)
            self._log("step_completed", step_id=step_id)

        state["status"] = "completed"
        self._write_state(state)
        self._log("workflow_completed")
        return state
