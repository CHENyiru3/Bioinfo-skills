"""Command-line interface for the Bioinfo-skills SDD layer."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from .checks import CHECK_REGISTRY, run_check
from .installed_refs import install_tool_bundle, load_selection, replace_tool_bundle, uninstall_tool_bundle
from .market import bundles_for_task, discover_bundles, load_bundle
from .models import load_section
from .models import validate_section_file
from .packs import resolve_workflow
from .sections import resolve_section_dir, update_gate
from .templates import create_section_from_templates
from .workflow import WorkflowRunner


def repo_root(path: Path | None = None) -> Path:
    current = (path or Path.cwd()).resolve()
    for candidate in [current, *current.parents]:
        if (candidate / "SPEC").exists() and (candidate / "skills").exists():
            return candidate
    return current


def _print_json(payload: object) -> None:
    print(json.dumps(payload, indent=2, sort_keys=True))


def cmd_create_section(args: argparse.Namespace) -> int:
    root = repo_root(args.root)
    target = create_section_from_templates(
        args.section_id,
        root / "sdd" / "sections",
        root / "sdd" / "templates",
        force=args.force,
    )
    print(target.relative_to(root))
    return 0


def cmd_validate_section(args: argparse.Namespace) -> int:
    root = repo_root(args.root)
    section_dir = resolve_section_dir(root, args.section)
    errors = validate_section_file(section_dir)
    if errors:
        for error in errors:
            print(error)
        return 1
    print("section validation passed")
    return 0


def cmd_run_check(args: argparse.Namespace) -> int:
    root = repo_root(args.root)
    section_dir = resolve_section_dir(root, args.section) if args.section else None
    result = run_check(args.check_id, root, section_dir)
    _print_json(result.to_dict())
    return 0 if result.status in {"pass", "skip"} else 1


def cmd_run_workflow(args: argparse.Namespace) -> int:
    root = repo_root(args.root)
    section_dir = resolve_section_dir(root, args.section)
    section = load_section(section_dir)
    workflow_path = args.workflow or resolve_workflow(
        root,
        section.data.get("pack_refs", []),
        section.data.get("workflow_ref", "bioinfo.sdd.workflow.section_default.v0"),
    )
    state = WorkflowRunner(root, workflow_path, section_dir, args.run_id).run()
    _print_json(state)
    return 0 if state["status"] in {"completed", "paused"} else 1


def cmd_gate(args: argparse.Namespace) -> int:
    root = repo_root(args.root)
    section_dir = resolve_section_dir(root, args.section)
    update_gate(section_dir, args.gate, args.status, args.reason)
    print(f"{args.gate}: {args.status}")
    return 0


def cmd_market_list(args: argparse.Namespace) -> int:
    root = repo_root(args.root)
    bundles = bundles_for_task(root, args.task_ref) if args.task_ref else discover_bundles(root)
    payload = [
        {
            "bundle_id": bundle_id,
            "name": bundle.data.get("name"),
            "task_refs": bundle.data.get("task_refs", []),
            "stage_ids": bundle.data.get("stage_ids", []),
        }
        for bundle_id, bundle in sorted(bundles.items())
    ]
    _print_json(payload)
    return 0


def cmd_market_show(args: argparse.Namespace) -> int:
    root = repo_root(args.root)
    _print_json(load_bundle(root, args.bundle_id).data)
    return 0


def cmd_install_tool_bundle(args: argparse.Namespace) -> int:
    root = repo_root(args.root)
    section_dir = resolve_section_dir(root, args.section)
    manifest = install_tool_bundle(root, section_dir, args.bundle_id, append=True)
    _print_json({"installed": args.bundle_id, "revision_id": manifest["revision_id"]})
    return 0


def cmd_replace_tool_bundle(args: argparse.Namespace) -> int:
    root = repo_root(args.root)
    section_dir = resolve_section_dir(root, args.section)
    manifest = replace_tool_bundle(root, section_dir, args.bundle_id)
    _print_json({"replaced_with": args.bundle_id, "revision_id": manifest["revision_id"]})
    return 0


def cmd_uninstall_tool_bundle(args: argparse.Namespace) -> int:
    root = repo_root(args.root)
    section_dir = resolve_section_dir(root, args.section)
    selection = uninstall_tool_bundle(root, section_dir, args.bundle_id)
    _print_json(selection)
    return 0


def cmd_installed_refs(args: argparse.Namespace) -> int:
    root = repo_root(args.root)
    section_dir = resolve_section_dir(root, args.section)
    _print_json(load_selection(section_dir))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="bioinfo-sdd")
    parser.add_argument("--root", type=Path, help="Repository root; defaults to auto-detection")
    subparsers = parser.add_subparsers(dest="command", required=True)

    create = subparsers.add_parser("create-section", help="Create a section from SDD templates")
    create.add_argument("section_id")
    create.add_argument("--force", action="store_true")
    create.set_defaults(func=cmd_create_section)

    validate = subparsers.add_parser("validate-section", help="Validate section.yml")
    validate.add_argument("section")
    validate.set_defaults(func=cmd_validate_section)

    checks = subparsers.add_parser("list-checks", help="List registered deterministic checks")
    checks.set_defaults(func=lambda _args: (print("\n".join(sorted(CHECK_REGISTRY))) or 0))

    run = subparsers.add_parser("run-check", help="Run one registered check")
    run.add_argument("check_id")
    run.add_argument("--section")
    run.set_defaults(func=cmd_run_check)

    workflow = subparsers.add_parser("run-workflow", help="Run or resume the section SDD workflow")
    workflow.add_argument("section")
    workflow.add_argument("--run-id", required=True)
    workflow.add_argument("--workflow", type=Path)
    workflow.set_defaults(func=cmd_run_workflow)

    gate = subparsers.add_parser("set-gate", help="Update a section review gate")
    gate.add_argument("section")
    gate.add_argument("gate")
    gate.add_argument("status", choices=["pending", "approved", "rejected"])
    gate.add_argument("--reason")
    gate.set_defaults(func=cmd_gate)

    market_list = subparsers.add_parser("market-list", help="List installable tool bundles")
    market_list.add_argument("--task-ref")
    market_list.set_defaults(func=cmd_market_list)

    market_show = subparsers.add_parser("market-show", help="Show one tool bundle manifest")
    market_show.add_argument("bundle_id")
    market_show.set_defaults(func=cmd_market_show)

    install = subparsers.add_parser("install-tool-bundle", help="Install a tool bundle into a section")
    install.add_argument("section")
    install.add_argument("bundle_id")
    install.set_defaults(func=cmd_install_tool_bundle)

    replace = subparsers.add_parser("replace-tool-bundle", help="Replace the active section tool bundle revision")
    replace.add_argument("section")
    replace.add_argument("bundle_id")
    replace.set_defaults(func=cmd_replace_tool_bundle)

    uninstall = subparsers.add_parser("uninstall-tool-bundle", help="Deactivate a tool bundle from a section")
    uninstall.add_argument("section")
    uninstall.add_argument("bundle_id")
    uninstall.set_defaults(func=cmd_uninstall_tool_bundle)

    installed = subparsers.add_parser("installed-refs", help="Show section installed-ref selection")
    installed.add_argument("section")
    installed.set_defaults(func=cmd_installed_refs)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)
