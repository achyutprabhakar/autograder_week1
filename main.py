import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def load_rules(rules_path):
    with open(rules_path, "r", encoding="utf-8") as f:
        rules = json.load(f)

    if rules.get("time_limit_s", 1) <= 0:
        raise ValueError("time_limit_s must be greater than zero")
    if rules.get("memory_limit_mb", 256) <= 0:
        raise ValueError("memory_limit_mb must be greater than zero")
    return rules


def compile_c(source_path, executable_path, compile_flags):
    command = ["gcc", str(source_path), "-o", str(executable_path), *compile_flags]
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=20,
            check=False,
        )
        return {
            "success": result.returncode == 0,
            "command": command,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode,
        }
    except FileNotFoundError:
        return {
            "success": False,
            "command": command,
            "stdout": "",
            "stderr": "GCC was not found. Install GCC and ensure 'gcc' is on PATH.",
            "returncode": None,
        }
    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "command": command,
            "stdout": "",
            "stderr": "Compilation exceeded the 20-second compilation timeout.",
            "returncode": None,
        }


def run_one(executable_path, test_case, time_limit_s):
    input_text = test_case.get("input", "")
    expected = test_case.get("expected", "")
    started = time.perf_counter()

    try:
        result = subprocess.run(
            [str(executable_path)],
            input=input_text,
            capture_output=True,
            text=True,
            timeout=time_limit_s,
            check=False,
        )
        elapsed = time.perf_counter() - started
        actual = result.stdout
        passed = result.returncode == 0 and actual.strip() == expected.strip()
        return {
            "name": test_case.get("name", "unnamed"),
            "input": input_text,
            "expected": expected,
            "actual": actual,
            "passed": passed,
            "returncode": result.returncode,
            "elapsed_seconds": round(elapsed, 6),
            "stderr": result.stderr,
            "error": None if result.returncode == 0 else f"Program exited with code {result.returncode}",
        }
    except subprocess.TimeoutExpired:
        elapsed = time.perf_counter() - started
        return {
            "name": test_case.get("name", "unnamed"),
            "input": input_text,
            "expected": expected,
            "actual": "",
            "passed": False,
            "returncode": None,
            "elapsed_seconds": round(elapsed, 6),
            "stderr": "",
            "error": f"Timed out after {time_limit_s} seconds",
        }


def load_tests(test_file):
    with open(test_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, list):
        raise ValueError("The tests file must contain a JSON list.")
    return data


def write_reports(report, report_dir, source_path):
    report_dir.mkdir(parents=True, exist_ok=True)
    stem = source_path.stem
    json_path = report_dir / f"{stem}_report.json"
    text_path = report_dir / f"{stem}_report.txt"

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    lines = [
        f"AutoGrader report: {report['submission']}",
        f"Status: {report['status']}",
        f"Grade: {report['grade']}/100",
        f"Tests passed: {report['tests_passed']}/{report['tests_total']}",
        "",
    ]

    if report.get("compile", {}).get("stderr"):
        lines.extend(["Compiler messages:", report["compile"]["stderr"], ""])

    for test in report.get("test_results", []):
        status = "PASS" if test["passed"] else "FAIL"
        lines.extend([
            f"[{status}] {test['name']}",
            f"  Input:    {test['input']!r}",
            f"  Expected: {test['expected']!r}",
            f"  Actual:   {test['actual']!r}",
        ])
        if test.get("error"):
            lines.append(f"  Error:    {test['error']}")
        if test.get("stderr"):
            lines.append(f"  stderr:   {test['stderr'].strip()}")
        lines.append("")

    lines.append("Note: this Week 1 prototype checks output and runtime only; it is not a secure sandbox.")
    with open(text_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    return json_path, text_path


def main():
    parser = argparse.ArgumentParser(
        description="Week 1 AutoGrader prototype: compile a C file and test it."
    )
    parser.add_argument("source", help="Path to the student's .c file")
    parser.add_argument("--rules", default=str(ROOT / "config" / "rules.json"))
    parser.add_argument("--tests", default=str(ROOT / "tests" / "tests.json"))
    parser.add_argument("--reports", default=str(ROOT / "reports"))
    parser.add_argument("--output", default=str(ROOT / "build" / "student_program"))
    args = parser.parse_args()

    source_path = Path(args.source).resolve()
    rules_path = Path(args.rules).resolve()
    tests_path = Path(args.tests).resolve()
    report_dir = Path(args.reports).resolve()
    executable_path = Path(args.output).resolve()

    report = {
        "submission": str(source_path),
        "status": "not_started",
        "grade": 0.0,
        "tests_passed": 0,
        "tests_total": 0,
        "compile": {},
        "test_results": [],
    }

    try:
        if not source_path.is_file():
            raise FileNotFoundError(f"C source file not found: {source_path}")
        if source_path.suffix.lower() != ".c":
            raise ValueError("Please provide a C source file with a .c extension.")

        rules = load_rules(rules_path)
        tests = load_tests(tests_path)

        executable_path.parent.mkdir(parents=True, exist_ok=True)
        compile_result = compile_c(
            source_path,
            executable_path,
            rules.get("compile_flags", ["-std=c11", "-Wall", "-Wextra"]),
        )
        report["compile"] = compile_result

        if not compile_result["success"]:
            report["status"] = "compilation_failed"
            report["compile_error"] = compile_result["stderr"]
        else:
            test_results = [
                run_one(executable_path, test, rules.get("time_limit_s", 1))
                for test in tests
            ]
            passed = sum(1 for result in test_results if result["passed"])
            total = len(test_results)
            report["test_results"] = test_results
            report["tests_passed"] = passed
            report["tests_total"] = total
            report["grade"] = round((passed / total) * 100, 2) if total else 0.0
            report["status"] = "completed"

    except (OSError, ValueError, json.JSONDecodeError) as exc:
        report["status"] = "error"
        report["error"] = str(exc)

    json_path, text_path = write_reports(report, report_dir, source_path)
    print(f"Status: {report['status']}")
    print(f"Grade: {report['grade']}/100")
    print(f"Tests passed: {report['tests_passed']}/{report['tests_total']}")
    print(f"JSON report: {json_path}")
    print(f"Text report: {text_path}")

    if report["status"] != "completed":
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
