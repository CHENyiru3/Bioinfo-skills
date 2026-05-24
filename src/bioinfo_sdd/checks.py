"""Deterministic checks used by the SDD workflow engine and CLI."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable

from .catalog import package_refs, skill_refs, stage_skills, tool_refs
from .installed_refs import active_manifest, load_selection
from .market import market_package_ref_paths, market_tool_ref_paths, sha256_file, validate_market
from .models import load_section, validate_section_file
from .packs import discover_packs, task_templates_for_section, validate_pack_file


@dataclass(frozen=True)
class CheckResult:
    check_id: str
    status: str
    summary: str
    details: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return {
            "check_id": self.check_id,
            "status": self.status,
            "summary": self.summary,
            "details": self.details,
        }


CheckFn = Callable[[Path, Path | None], CheckResult]
CHECK_REGISTRY: dict[str, CheckFn] = {}


def register_check(check_id: str) -> Callable[[CheckFn], CheckFn]:
    def decorator(func: CheckFn) -> CheckFn:
        CHECK_REGISTRY[check_id] = func
        return func

    return decorator


def run_check(check_id: str, root: Path, section_dir: Path | None = None) -> CheckResult:
    if check_id not in CHECK_REGISTRY:
        return CheckResult(check_id, "fail", f"unknown check: {check_id}", {})
    return CHECK_REGISTRY[check_id](root, section_dir)


def _frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError(f"{path}: missing YAML frontmatter")
    end = text.find("\n---\n", 4)
    if end == -1:
        raise ValueError(f"{path}: unterminated YAML frontmatter")
    data: dict[str, str] = {}
    for line in text[4:end].splitlines():
        if not line.strip() or line.startswith("#"):
            continue
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip()
    return data


def _inline_list(value: str | None) -> list[str]:
    if not value:
        return []
    text = value.strip()
    if text.startswith("[") and text.endswith("]"):
        text = text[1:-1]
    return [part.strip().strip('"').strip("'") for part in text.split(",") if part.strip()]


def _require_sections(path: Path, text: str, sections: list[str], errors: list[str]) -> None:
    for section in sections:
        if section not in text:
            errors.append(f"{path}: missing required section {section}")


def _reject_placeholder_phrases(path: Path, text: str, errors: list[str]) -> None:
    for phrase in ["To be filled", "runtime routing placeholder", "authoritative stage definition"]:
        if phrase in text:
            errors.append(f"{path}: contains unresolved placeholder phrase {phrase!r}")


@register_check("section_schema")
def check_section_schema(_root: Path, section_dir: Path | None) -> CheckResult:
    if section_dir is None:
        return CheckResult("section_schema", "fail", "section_dir is required", {})
    errors = validate_section_file(section_dir)
    status = "pass" if not errors else "fail"
    summary = "section schema is valid" if not errors else "section schema has errors"
    return CheckResult("section_schema", status, summary, {"errors": errors})


@register_check("section_artifacts")
def check_section_artifacts(_root: Path, section_dir: Path | None) -> CheckResult:
    if section_dir is None:
        return CheckResult("section_artifacts", "fail", "section_dir is required", {})
    required = ["section.yml", "spec.md", "plan.md", "tasks.md", "evidence.md", "gates.yml"]
    missing = [name for name in required if not (section_dir / name).exists()]
    status = "pass" if not missing else "fail"
    summary = "section artifacts are complete" if not missing else "section artifacts are missing files"
    return CheckResult("section_artifacts", status, summary, {"missing": missing})


@register_check("pack_manifest")
def check_pack_manifest(root: Path, _section_dir: Path | None = None) -> CheckResult:
    pack_paths = sorted((root / "sdd" / "packs").glob("*/pack.yml"))
    errors: list[str] = []
    for path in pack_paths:
        errors.extend(f"{path}: {error}" for error in validate_pack_file(path, root=root))
    status = "pass" if pack_paths and not errors else "fail"
    summary = "pack manifests are valid" if status == "pass" else "pack manifests have errors"
    return CheckResult(
        "pack_manifest",
        status,
        summary,
        {"errors": errors, "packs": [str(path.relative_to(root)) for path in pack_paths]},
    )


@register_check("market_manifest")
def check_market_manifest(root: Path, _section_dir: Path | None = None) -> CheckResult:
    errors = validate_market(root)
    status = "pass" if not errors else "fail"
    summary = "tool market manifest is valid" if status == "pass" else "tool market manifest has errors"
    return CheckResult("market_manifest", status, summary, {"errors": errors})


@register_check("installed_refs")
def check_installed_refs(_root: Path, section_dir: Path | None) -> CheckResult:
    if section_dir is None:
        return CheckResult("installed_refs", "fail", "section_dir is required", {})
    selection = load_selection(section_dir)
    manifest = active_manifest(section_dir)
    errors: list[str] = []
    if not selection.get("active_revision"):
        errors.append("no active installed-ref revision")
    if manifest is None:
        errors.append("active installed-ref manifest is missing")
    else:
        for key in ["packages", "tools"]:
            for row in manifest.get(key, []):
                rel = row.get("installed_path")
                if not rel:
                    errors.append(f"{key}: missing installed_path for {row.get('id')}")
                    continue
                path = section_dir / rel
                if not path.exists():
                    errors.append(f"{key}: installed ref does not exist: {rel}")
                    continue
                expected = row.get("sha256")
                observed = sha256_file(path)
                if expected != observed:
                    errors.append(f"{key}: checksum mismatch for {rel}")
    status = "pass" if not errors else "fail"
    summary = "installed refs are valid" if status == "pass" else "installed refs have errors"
    return CheckResult(
        "installed_refs",
        status,
        summary,
        {
            "errors": errors,
            "active_revision": selection.get("active_revision"),
            "active_bundles": selection.get("active_bundles", []),
        },
    )


@register_check("task_slots_filled")
def check_task_slots_filled(root: Path, section_dir: Path | None) -> CheckResult:
    if section_dir is None:
        return CheckResult("task_slots_filled", "fail", "section_dir is required", {})
    section = load_section(section_dir)
    resolved_tasks = task_templates_for_section(root, section.data.get("pack_refs", []), section.data.get("task_refs", []))
    manifest = active_manifest(section_dir)
    installed_slots = {
        row.get("slot_id")
        for row in (manifest or {}).get("tools", [])
        if row.get("slot_id")
    }
    required_slots = {
        slot.get("slot_id")
        for task in resolved_tasks.values()
        for slot in task.get("tool_slots", [])
        if slot.get("slot_id")
    }
    missing = sorted(required_slots - installed_slots)
    status = "pass" if not missing else "fail"
    summary = "installed refs fill task tool slots" if status == "pass" else "installed refs do not fill task tool slots"
    return CheckResult(
        "task_slots_filled",
        status,
        summary,
        {"missing_slots": missing, "required_slots": sorted(required_slots), "installed_slots": sorted(installed_slots)},
    )


@register_check("section_catalog_links")
def check_section_catalog_links(root: Path, section_dir: Path | None) -> CheckResult:
    if section_dir is None:
        return CheckResult("section_catalog_links", "fail", "section_dir is required", {})
    section = load_section(section_dir)
    packs = discover_packs(root)
    pack_refs = section.data.get("pack_refs", [])
    task_refs = section.data.get("task_refs", [])
    stage_by_id = stage_skills(root, pack_refs)
    skills_by_id = skill_refs(root, pack_refs)
    packages_by_id = package_refs(root, pack_refs, section_dir=section_dir)
    tools_by_id = tool_refs(root, pack_refs, section_dir=section_dir)
    installed = active_manifest(section_dir) or {}
    installed_packages = list(installed.get("package_refs") or [])
    installed_tools = list(installed.get("tool_refs") or [])
    missing_packs = [pack for pack in pack_refs if pack not in packs]
    resolved_tasks = task_templates_for_section(root, pack_refs, task_refs)
    missing_tasks = [task for task in task_refs if task not in resolved_tasks]
    pack_checks = sorted({check for pack_id in pack_refs for check in (packs.get(pack_id).checks() if packs.get(pack_id) else [])})
    task_checks = sorted({check for task in resolved_tasks.values() for check in task.get("checks", [])})
    missing_skills = [skill for skill in section.data.get("skill_refs", []) if skill not in skills_by_id]
    missing_packages = [package for package in section.data.get("package_refs", []) if package not in packages_by_id]
    missing_tools = [tool for tool in section.data.get("tool_refs", []) if tool not in tools_by_id]
    undeclared_installed_packages = [package for package in installed_packages if package not in section.data.get("package_refs", [])]
    undeclared_installed_tools = [tool for tool in installed_tools if tool not in section.data.get("tool_refs", [])]
    missing_checks = [check for check in section.data.get("check_refs", []) if check not in pack_checks]
    undeclared_task_checks = [check for check in task_checks if check not in section.data.get("check_refs", [])]
    stage_ids = section.data.get("stage_ids", [])
    missing_stage_dirs = [
        stage for stage in stage_ids if not any(entry.path.parent.name == stage for entry in stage_by_id.values())
    ]
    workflow_ref = section.data.get("workflow_ref")
    workflow_resolved = False
    for pack_ref in pack_refs:
        pack = packs.get(pack_ref)
        if pack and workflow_ref in pack.workflows():
            workflow_resolved = True
            break
    errors = []
    if missing_packs:
        errors.append(f"missing pack refs: {missing_packs}")
    if workflow_ref and not workflow_resolved:
        errors.append(f"workflow_ref not found in declared packs: {workflow_ref}")
    if missing_tasks:
        errors.append(f"missing task refs: {missing_tasks}")
    if missing_skills:
        errors.append(f"missing skill refs: {missing_skills}")
    if missing_packages:
        errors.append(f"missing package refs: {missing_packages}")
    if missing_tools:
        errors.append(f"missing tool refs: {missing_tools}")
    if undeclared_installed_packages:
        errors.append(f"installed package refs not declared by section: {undeclared_installed_packages}")
    if undeclared_installed_tools:
        errors.append(f"installed tool refs not declared by section: {undeclared_installed_tools}")
    if missing_checks:
        errors.append(f"check refs not exposed by declared packs: {missing_checks}")
    if undeclared_task_checks:
        errors.append(f"task check refs not declared by section: {undeclared_task_checks}")
    if missing_stage_dirs:
        errors.append(f"missing stage ids: {missing_stage_dirs}")
    status = "pass" if not errors else "fail"
    summary = "section catalog links resolve" if not errors else "section catalog links have unresolved refs"
    return CheckResult(
        "section_catalog_links",
        status,
        summary,
        {
            "errors": errors,
            "pack_refs": pack_refs,
            "workflow_ref": workflow_ref,
            "task_refs": task_refs,
            "task_checks": task_checks,
            "installed_packages": installed_packages,
            "installed_tools": installed_tools,
            "stage_ids": stage_ids,
        },
    )


@register_check("wrapper_binding")
def check_wrapper_binding(root: Path, section_dir: Path | None) -> CheckResult:
    if section_dir is None:
        return CheckResult("wrapper_binding", "fail", "section_dir is required", {})
    section = load_section(section_dir)
    wrapper = section.wrapper_path
    exists = bool(wrapper and (root / wrapper).exists())
    status = "pass" if exists else "fail"
    summary = "wrapper binding exists" if exists else "wrapper binding is missing"
    return CheckResult("wrapper_binding", status, summary, {"wrapper": wrapper})


@register_check("adapter_binding")
def check_adapter_binding(root: Path, section_dir: Path | None) -> CheckResult:
    if section_dir is None:
        return CheckResult("adapter_binding", "fail", "section_dir is required", {})
    section = load_section(section_dir)
    adapter = section.adapter_path
    exists = bool(adapter and (root / adapter).exists())
    status = "pass" if exists else "fail"
    summary = "adapter binding exists" if exists else "adapter binding is missing"
    return CheckResult("adapter_binding", status, summary, {"adapter": adapter})


@register_check("anndata_contract")
def check_anndata_contract(root: Path, _section_dir: Path | None = None) -> CheckResult:
    contract = root / "contracts/anndata_scrna_state_v0.yml"
    required = [
        "layers:",
        "counts:",
        "log1p_norm:",
        "sample_id:",
        "batch:",
        "X_pca:",
        "X_umap:",
        "bioinfo_skills:",
    ]
    text = contract.read_text(encoding="utf-8")
    missing = [token for token in required if token not in text]
    status = "pass" if not missing else "fail"
    summary = "AnnData contract contains required conventions" if not missing else "AnnData contract is missing tokens"
    return CheckResult("anndata_contract", status, summary, {"missing": missing})


@register_check("backend_neutral")
def check_backend_neutral(root: Path, _section_dir: Path | None = None) -> CheckResult:
    patterns = [
        r"^\s*rule\s+\w+",
        r"\bSnakefile\b",
        r"\bwildcards\b",
        r"\bsnakemake\.",
        r"^\s*process\s+\w+",
    ]
    offenders: list[str] = []
    for path in (root / "skills/scrna/scverse/workflow").glob("*/SKILL.md"):
        text = path.read_text(encoding="utf-8")
        for pattern in patterns:
            if re.search(pattern, text, flags=re.MULTILINE):
                offenders.append(f"{path}: {pattern}")
    status = "pass" if not offenders else "fail"
    summary = "workflow skills are backend-neutral" if not offenders else "workflow skills contain backend syntax"
    return CheckResult("backend_neutral", status, summary, {"offenders": offenders})


@register_check("snakemake_policy")
def check_snakemake_policy(root: Path, _section_dir: Path | None = None) -> CheckResult:
    workflow_dir = root / "workflow"
    if not workflow_dir.exists():
        return CheckResult("snakemake_policy", "pass", "no workflow directory found", {"files": 0})
    disallowed_patterns = [
        r"\bimport\s+scanpy\b",
        r"\bimport\s+anndata\b",
        r"\bscanpy\.",
        r"\bsc\.(pp|tl|pl|get)\.",
        r"\banndata\.",
        r"\bread_h5ad\(",
        r"\brank_genes_groups\(",
        r"\bnormalize_total\(",
        r"\blog1p\(",
        r"\bhighly_variable_genes\(",
        r"\bneighbors\(",
        r"\bumap\(",
        r"\bleiden\(",
    ]
    allowed_wrapper_hints = ["wrappers/python/", "wrappers/r/"]
    files = sorted([*workflow_dir.glob("Snakefile"), *workflow_dir.glob("rules/*.smk")])
    errors: list[str] = []
    for path in files:
        text = path.read_text(encoding="utf-8")
        for pattern in disallowed_patterns:
            if re.search(pattern, text):
                errors.append(f"{path}: embeds analysis logic matching {pattern}")
        if path.suffix == ".smk" and "rule " in text and not any(hint in text for hint in allowed_wrapper_hints):
            errors.append(f"{path}: rule file should call a wrapper under wrappers/")
    status = "pass" if not errors else "fail"
    summary = f"Snakemake policy check passed for {len(files)} files" if not errors else "Snakemake policy check failed"
    return CheckResult("snakemake_policy", status, summary, {"errors": errors, "files": len(files)})


@register_check("runtime_report")
def check_runtime_report(root: Path, _section_dir: Path | None = None) -> CheckResult:
    report_path = root / "reports/runtime/scverse_runtime_status.json"
    try:
        report = json.loads(report_path.read_text(encoding="utf-8"))
    except Exception as exc:
        return CheckResult("runtime_report", "fail", "runtime report is unreadable", {"error": str(exc)})
    reported = {row.get("package") for row in report.get("packages", [])}
    refs = {ref.stem for ref in market_package_ref_paths(root)}
    errors: list[str] = []
    for key in ["schema_version", "generated_at", "packages"]:
        if key not in report:
            errors.append(f"missing key: {key}")
    if reported != refs:
        errors.append("runtime report packages do not match package refs")
    status = "pass" if not errors else "fail"
    summary = "runtime report is schema-shaped and matches market package refs" if not errors else "runtime report has errors"
    return CheckResult("runtime_report", status, summary, {"errors": errors})


@register_check("skill_tree")
def check_skill_tree(root: Path, _section_dir: Path | None = None) -> CheckResult:
    errors: list[str] = []
    for path in sorted((root / "schemas").glob("*.schema.json")):
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"{path}: invalid JSON schema: {exc}")

    required_files = [
        "SPEC/README.md",
        "SPEC/skill_system_core_workflow.md",
        "SPEC/scrna_scverse_skill_system_v0.md",
        "schemas/skill_manifest.schema.json",
        "contracts/anndata_scrna_state_v0.yml",
        "skills/entry/SKILL.md",
        "skills/scrna/SKILL.md",
        "skills/scrna/scverse/SKILL.md",
        "execution/adapters/snakemake/python_rule_template.smk",
        "execution/adapters/snakemake/rscript_rule_template.smk",
        "reports/runtime/README.md",
    ]
    for rel in required_files:
        if not (root / rel).exists():
            errors.append(f"missing required file: {rel}")

    stages = [
        "00_state_inspection",
        "01_data_ingest",
        "02_qc_metrics_filtering",
        "03_doublet_detection",
        "04_normalization_transform",
        "05_feature_selection",
        "06_dimensionality_reduction",
        "07_batch_integration",
        "08_neighbor_graph",
        "09_embedding_visualization",
        "10_clustering",
        "11_marker_ranking",
        "12_annotation_support",
        "13_signature_scoring",
        "14_aggregation_pseudobulk_de",
        "15_trajectory_fate_velocity",
        "16_specialized_ecosystem",
    ]
    backend_syntax = [
        r"^\s*rule\s+\w+",
        r"\bSnakefile\b",
        r"\bwildcards\b",
        r"\bsnakemake\.",
        r"^\s*process\s+\w+",
        r"\bchannel\b",
        r"<<\s*[A-Z]+",
    ]
    filled_stage_sections = [
        "## Purpose",
        "## When Required",
        "## When Optional",
        "## When Forbidden",
        "## Required Input State",
        "## Produced Output State",
        "## User Decision Points",
        "## Registered Package Refs",
        "## Registered Tool Refs",
        "## Expected Artifacts",
        "## Validation Checks",
        "## Failure Modes",
        "## Allowed Claims",
        "## Forbidden Claims",
        "## Next Stage Routing",
    ]
    distilled_package_sections = [
        "## Role In Scverse Workflow",
        "## Supported Stages",
        "## Required Object State",
        "## Produced Object State",
        "## Major API Families",
        "## Runtime Availability",
        "## Failure Modes",
        "## Scientific Caveats",
        "## When To Avoid",
        "## Sources Used",
    ]
    distilled_tool_sections = [
        "## API Entry Point",
        "## Method Family",
        "## Required Object State",
        "## Output State",
        "## Important Parameters",
        "## Minimal Use",
        "## Validation Checks",
        "## Failure Modes",
        "## Statistical Caveats",
        "## Adapter Notes",
        "## Sources Used",
    ]
    distilled_statuses = {"distilled", "verified"}
    package_ids = set(package_refs(root))

    for stage in stages:
        skill = root / f"skills/scrna/scverse/workflow/{stage}/SKILL.md"
        if not skill.exists():
            errors.append(f"missing stage skill: {stage}")
            continue
        try:
            meta = _frontmatter(skill)
        except ValueError as exc:
            errors.append(str(exc))
            continue
        for key in ["id", "schema_version", "kind", "domain", "stage", "status"]:
            if key not in meta:
                errors.append(f"{skill}: missing frontmatter key {key}")
        body = skill.read_text(encoding="utf-8")
        for pattern in backend_syntax:
            if re.search(pattern, body, flags=re.MULTILINE):
                errors.append(f"{skill}: contains backend syntax matching {pattern}")
        if meta.get("status") == "filled":
            _require_sections(skill, body, filled_stage_sections, errors)
            _reject_placeholder_phrases(skill, body, errors)
            refs = _inline_list(meta.get("registered_refs"))
            if not refs:
                errors.append(f"{skill}: filled stage must declare registered_refs")

    for ref in market_package_ref_paths(root):
        try:
            meta = _frontmatter(ref)
        except ValueError as exc:
            errors.append(str(exc))
            continue
        for key in ["id", "kind", "package", "language", "ecosystem", "runtime_status"]:
            if key not in meta:
                errors.append(f"{ref}: missing frontmatter key {key}")
        if meta.get("distillation_status") in distilled_statuses:
            for key in ["source_urls", "source_version", "source_accessed_at", "distillation_status"]:
                if key not in meta:
                    errors.append(f"{ref}: distilled package ref missing frontmatter key {key}")
            body = ref.read_text(encoding="utf-8")
            _require_sections(ref, body, distilled_package_sections, errors)
            _reject_placeholder_phrases(ref, body, errors)

    for ref in market_tool_ref_paths(root):
        try:
            meta = _frontmatter(ref)
        except ValueError as exc:
            errors.append(str(exc))
            continue
        for key in ["id", "kind", "package_ref", "api_entrypoint", "method_family"]:
            if key not in meta:
                errors.append(f"{ref}: missing frontmatter key {key}")
        if meta.get("package_ref") and meta["package_ref"] not in package_ids:
            errors.append(f"{ref}: package_ref not found: {meta['package_ref']}")
        if meta.get("distillation_status") in distilled_statuses:
            for key in ["source_urls", "source_version", "source_accessed_at", "distillation_status"]:
                if key not in meta:
                    errors.append(f"{ref}: distilled tool ref missing frontmatter key {key}")
            body = ref.read_text(encoding="utf-8")
            _require_sections(ref, body, distilled_tool_sections, errors)
            _reject_placeholder_phrases(ref, body, errors)

    status = "pass" if not errors else "fail"
    summary = "skill tree validation passed" if not errors else "skill tree validation failed"
    return CheckResult("skill_tree", status, summary, {"errors": errors})
