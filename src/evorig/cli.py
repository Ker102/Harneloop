from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .candidate import create_candidate
from .diagnostics import run_doctor
from .errors import EvoRigError
from .evidence import add_evidence
from .packaging import package_unit
from .runs import add_artifact, finish_run, start_run
from .state import mark_active, mark_stopped, mark_waiting, read_state
from .unit import init_unit
from .validation import validate_unit
from .versioning import promote_candidate, rollback_unit


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="evorig", description="EvoRig harness-unit lifecycle engine")
    subparsers = parser.add_subparsers(dest="command", required=True)

    init_parser = subparsers.add_parser("init-unit", help="Create a new harness unit")
    init_parser.add_argument("path", type=Path)
    init_parser.add_argument("--id", required=True)
    init_parser.add_argument("--name", required=True)

    candidate_parser = subparsers.add_parser("candidate", help="Manage candidates")
    candidate_subparsers = candidate_parser.add_subparsers(dest="candidate_command", required=True)
    candidate_create = candidate_subparsers.add_parser("create", help="Create a candidate patch workspace")
    candidate_create.add_argument("unit", type=Path)
    candidate_create.add_argument("--summary", required=True)
    candidate_create.add_argument("--kind", default="mixed")
    candidate_evidence = candidate_subparsers.add_parser("evidence", help="Manage candidate evidence")
    candidate_evidence_subparsers = candidate_evidence.add_subparsers(dest="evidence_command", required=True)
    candidate_evidence_add = candidate_evidence_subparsers.add_parser("add", help="Add evidence to a candidate")
    candidate_evidence_add.add_argument("unit", type=Path)
    candidate_evidence_add.add_argument("candidate_id")
    candidate_evidence_add.add_argument("--kind", required=True)
    candidate_evidence_add.add_argument("--summary", required=True)
    candidate_evidence_add.add_argument("--outcome", default="supports")
    candidate_evidence_add.add_argument("--run-id")
    candidate_evidence_add.add_argument("--artifact-id")
    candidate_evidence_add.add_argument("--path", type=Path)

    promote_parser = subparsers.add_parser("promote", help="Promote a candidate into a version snapshot")
    promote_parser.add_argument("unit", type=Path)
    promote_parser.add_argument("candidate_id")
    promote_parser.add_argument("--version", required=True)
    promote_parser.add_argument("--summary")
    promote_parser.add_argument("--allow-missing-evidence", action="store_true")

    rollback_parser = subparsers.add_parser("rollback", help="Restore a promoted version snapshot")
    rollback_parser.add_argument("unit", type=Path)
    rollback_parser.add_argument("--to", required=True, dest="version")

    package_parser = subparsers.add_parser("package", help="Create a portable package from a promoted version")
    package_parser.add_argument("unit", type=Path)
    package_parser.add_argument("--output", type=Path, required=True)
    package_parser.add_argument("--profile", default="thin")
    package_parser.add_argument("--version")

    validate_parser = subparsers.add_parser("validate", help="Validate a harness unit")
    validate_parser.add_argument("unit", type=Path)

    status_parser = subparsers.add_parser("status", help="Print unit lifecycle state")
    status_parser.add_argument("unit", type=Path)

    doctor_parser = subparsers.add_parser("doctor", help="Check local EvoRig runtime prerequisites")
    doctor_parser.add_argument("--json", action="store_true", dest="json_output")
    doctor_parser.add_argument("--cwd", type=Path, default=Path.cwd())

    run_parser = subparsers.add_parser("run", help="Manage runtime run records")
    run_subparsers = run_parser.add_subparsers(dest="run_command", required=True)

    run_start = run_subparsers.add_parser("start", help="Start a run record")
    run_start.add_argument("unit", type=Path)
    run_start.add_argument("--task", required=True)
    run_start.add_argument("--candidate-id")

    run_finish = run_subparsers.add_parser("finish", help="Finish a run record")
    run_finish.add_argument("unit", type=Path)
    run_finish.add_argument("run_id")
    run_finish.add_argument("--status", required=True, choices=["succeeded", "failed", "stopped"])
    run_finish.add_argument("--summary")

    artifact_parser = subparsers.add_parser("artifact", help="Manage run artifacts")
    artifact_subparsers = artifact_parser.add_subparsers(dest="artifact_command", required=True)
    artifact_add = artifact_subparsers.add_parser("add", help="Attach an artifact to a run")
    artifact_add.add_argument("unit", type=Path)
    artifact_add.add_argument("run_id")
    artifact_add.add_argument("source", type=Path)
    artifact_add.add_argument("--kind", required=True)
    artifact_add.add_argument("--description", default="")
    artifact_add.add_argument("--name")

    state_parser = subparsers.add_parser("state", help="Manage wait, stop, and resume states")
    state_subparsers = state_parser.add_subparsers(dest="state_command", required=True)

    wait_parser = state_subparsers.add_parser("wait", help="Mark a unit as waiting")
    wait_parser.add_argument("unit", type=Path)
    wait_parser.add_argument("--reason", required=True)
    wait_parser.add_argument("--next-action", required=True)
    wait_parser.add_argument("--resume-after")
    wait_parser.add_argument("--resume-condition")

    stop_parser = state_subparsers.add_parser("stop", help="Mark a unit as stopped")
    stop_parser.add_argument("unit", type=Path)
    stop_parser.add_argument("--reason", required=True)
    stop_parser.add_argument("--next-action")

    resume_parser = state_subparsers.add_parser("resume", help="Return a unit to active state")
    resume_parser.add_argument("unit", type=Path)
    resume_parser.add_argument("--reason", default="manual_resume")
    resume_parser.add_argument("--next-action")

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        if args.command == "init-unit":
            path = init_unit(args.path, args.id, args.name)
            print(f"Created unit: {path}")
            return 0

        if args.command == "candidate" and args.candidate_command == "create":
            path = create_candidate(args.unit, args.summary, args.kind)
            print(f"Created candidate: {path.name}")
            return 0

        if args.command == "candidate" and args.candidate_command == "evidence":
            if args.evidence_command == "add":
                record = add_evidence(
                    args.unit,
                    args.candidate_id,
                    kind=args.kind,
                    summary=args.summary,
                    outcome=args.outcome,
                    run_id=args.run_id,
                    artifact_id=args.artifact_id,
                    path=args.path,
                )
                print(json.dumps(record, indent=2))
                return 0

        if args.command == "promote":
            path = promote_candidate(
                args.unit,
                args.candidate_id,
                args.version,
                args.summary,
                require_evidence=not args.allow_missing_evidence,
            )
            print(f"Promoted {args.candidate_id} to {path.name}")
            return 0

        if args.command == "rollback":
            path = rollback_unit(args.unit, args.version)
            print(f"Rolled back to {path.name}")
            return 0

        if args.command == "package":
            output = package_unit(args.unit, args.output, args.profile, args.version)
            print(f"Created package: {output}")
            return 0

        if args.command == "validate":
            issues = validate_unit(args.unit)
            if issues:
                for issue in issues:
                    print(f"{issue.path}: {issue.message}", file=sys.stderr)
                return 1
            print("Unit is valid")
            return 0

        if args.command == "status":
            print(json.dumps(read_state(args.unit), indent=2))
            return 0

        if args.command == "doctor":
            checks = run_doctor(args.cwd)
            if args.json_output:
                print(json.dumps([check.to_dict() for check in checks], indent=2))
            else:
                for check in checks:
                    label = "OK" if check.ok else "FAIL"
                    print(f"{label} {check.name}: {check.detail}")
            return 0 if all(check.ok for check in checks) else 1

        if args.command == "run":
            if args.run_command == "start":
                path = start_run(args.unit, args.task, args.candidate_id)
                print(f"Started run: {path.name}")
                return 0
            if args.run_command == "finish":
                record = finish_run(args.unit, args.run_id, args.status, args.summary)
                print(json.dumps(record, indent=2))
                return 0

        if args.command == "artifact" and args.artifact_command == "add":
            record = add_artifact(
                args.unit,
                args.run_id,
                args.source,
                kind=args.kind,
                description=args.description,
                name=args.name,
            )
            print(json.dumps(record, indent=2))
            return 0

        if args.command == "state":
            if args.state_command == "wait":
                state = mark_waiting(
                    args.unit,
                    args.reason,
                    args.next_action,
                    resume_after=args.resume_after,
                    resume_condition=args.resume_condition,
                )
            elif args.state_command == "stop":
                state = mark_stopped(args.unit, args.reason, args.next_action)
            elif args.state_command == "resume":
                state = mark_active(args.unit, args.reason, args.next_action)
            else:
                parser.error("Unknown state command")
            print(json.dumps(state, indent=2))
            return 0

    except EvoRigError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    parser.error("Unhandled command")
    return 2
