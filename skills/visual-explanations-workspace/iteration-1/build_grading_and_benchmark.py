#!/usr/bin/env python3
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
import statistics


ROOT = Path("/Users/yoda/forProgramming/DK/skills/visual-explanations-workspace/iteration-1")

RUNS = [
    ("vm-container-comparison", 1, "with_skill"),
    ("vm-container-comparison", 1, "without_skill"),
    ("oauth-login-flow", 2, "with_skill"),
    ("oauth-login-flow", 2, "without_skill"),
    ("kubernetes-hierarchy", 3, "with_skill"),
    ("kubernetes-hierarchy", 3, "without_skill"),
]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def has_markdown_table(text: str) -> bool:
    return "|---" in text or "| ---" in text


def check_expectation(text: str, expectation: str) -> tuple[bool, str]:
    if expectation == "Markdown に Mermaid コードブロックが含まれる":
        passed = "```mermaid" in text
        evidence = "Found ```mermaid block." if passed else "No Mermaid code block found."
        return passed, evidence

    if expectation == "本文に共通点と差分の両方への言及がある":
        has_common = "共通" in text
        has_diff = any(word in text for word in ["差分", "違い", "分かれ目"])
        passed = has_common and has_diff
        evidence = f"common={has_common}, difference={has_diff}"
        return passed, evidence

    if expectation == "図または補足で読み順（上から下 / 左から右など）が示されている":
        passed = any(word in text for word in ["上から下", "左から右", "読み方", "読み順"])
        evidence = "Found reading-order guidance." if passed else "No explicit reading-order guidance found."
        return passed, evidence

    if expectation == "認可コードとアクセストークンの両方が本文または図に現れる":
        has_code = "認可コード" in text
        has_token = "アクセストークン" in text
        passed = has_code and has_token
        evidence = f"auth_code={has_code}, access_token={has_token}"
        return passed, evidence

    if expectation == "ブラウザ・アプリ・認可サーバ・API サーバの4者が説明に含まれる":
        checks = {term: term in text for term in ["ブラウザ", "アプリ", "認可サーバ", "API サーバ"]}
        passed = all(checks.values())
        evidence = ", ".join(f"{k}={v}" for k, v in checks.items())
        return passed, evidence

    if expectation == "Markdown の表が含まれる":
        passed = has_markdown_table(text)
        evidence = "Found markdown table syntax." if passed else "No markdown table syntax found."
        return passed, evidence

    if expectation == "Deployment・ReplicaSet・Pod・Container の4語がすべて含まれる":
        checks = {term: term in text for term in ["Deployment", "ReplicaSet", "Pod", "Container"]}
        passed = all(checks.values())
        evidence = ", ".join(f"{k}={v}" for k, v in checks.items())
        return passed, evidence

    return False, "Unknown expectation."


def stats(values: list[float]) -> dict[str, float]:
    if not values:
        return {"mean": 0.0, "stddev": 0.0, "min": 0.0, "max": 0.0}
    if len(values) == 1:
        return {"mean": values[0], "stddev": 0.0, "min": values[0], "max": values[0]}
    return {
        "mean": round(statistics.mean(values), 4),
        "stddev": round(statistics.stdev(values), 4),
        "min": round(min(values), 4),
        "max": round(max(values), 4),
    }


def main() -> None:
    benchmark_runs = []

    for eval_name, eval_id, config in RUNS:
        run_dir = ROOT / eval_name / config
        outputs_dir = run_dir / "outputs"
        metadata = json.loads(read_text(ROOT / eval_name / "eval_metadata.json"))
        answer_path = outputs_dir / "answer.md"
        answer = read_text(answer_path)

        expectations = []
        for exp in metadata["assertions"]:
            passed, evidence = check_expectation(answer, exp)
            expectations.append({"text": exp, "passed": passed, "evidence": evidence})

        passed_count = sum(1 for item in expectations if item["passed"])
        total = len(expectations)
        failed = total - passed_count
        pass_rate = round(passed_count / total, 2) if total else 0.0
        output_chars = len(answer)

        grading = {
            "expectations": expectations,
            "summary": {
                "passed": passed_count,
                "failed": failed,
                "total": total,
                "pass_rate": pass_rate,
            },
            "execution_metrics": {
                "tool_calls": {},
                "total_tool_calls": 0,
                "total_steps": 0,
                "errors_encountered": 0,
                "output_chars": output_chars,
                "transcript_chars": 0,
            },
            "timing": {
                "executor_duration_seconds": 0.0,
                "grader_duration_seconds": 0.0,
                "total_duration_seconds": 0.0,
            },
            "claims": [],
            "user_notes_summary": {
                "uncertainties": [],
                "needs_review": [],
                "workarounds": [],
            },
            "eval_feedback": {
                "overall": "Timing/tokens were not recoverable from the background subagent transcripts in this run, so benchmark comparisons focus on pass-rate and qualitative output review."
            },
        }
        (run_dir / "grading.json").write_text(json.dumps(grading, ensure_ascii=False, indent=2), encoding="utf-8")

        benchmark_runs.append(
            {
                "eval_id": eval_id,
                "eval_name": eval_name,
                "configuration": config,
                "run_number": 1,
                "result": {
                    "pass_rate": pass_rate,
                    "passed": passed_count,
                    "failed": failed,
                    "total": total,
                    "time_seconds": 0.0,
                    "tokens": output_chars,
                    "tool_calls": 0,
                    "errors": 0,
                },
                "expectations": expectations,
                "notes": [],
            }
        )

    summaries = {}
    for config in ["with_skill", "without_skill"]:
        runs = [r for r in benchmark_runs if r["configuration"] == config]
        summaries[config] = {
            "pass_rate": stats([r["result"]["pass_rate"] for r in runs]),
            "time_seconds": stats([r["result"]["time_seconds"] for r in runs]),
            "tokens": stats([r["result"]["tokens"] for r in runs]),
        }

    delta_pass = summaries["with_skill"]["pass_rate"]["mean"] - summaries["without_skill"]["pass_rate"]["mean"]
    delta_time = summaries["with_skill"]["time_seconds"]["mean"] - summaries["without_skill"]["time_seconds"]["mean"]
    delta_tokens = summaries["with_skill"]["tokens"]["mean"] - summaries["without_skill"]["tokens"]["mean"]

    benchmark = {
        "metadata": {
            "skill_name": "visual-explanations",
            "skill_path": "/Users/yoda/forProgramming/DK/skills/visual-explanations",
            "executor_model": "fast-subagent",
            "analyzer_model": "inline",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "evals_run": [1, 2, 3],
            "runs_per_configuration": 1,
        },
        "runs": benchmark_runs,
        "run_summary": {
            "with_skill": summaries["with_skill"],
            "without_skill": summaries["without_skill"],
            "delta": {
                "pass_rate": f"{delta_pass:+.2f}",
                "time_seconds": f"{delta_time:+.1f}",
                "tokens": f"{delta_tokens:+.0f}",
            },
        },
        "notes": [
            "Pass-rate only checks presence/structure level assertions; human review should decide whether the diagrams are genuinely easier to understand.",
            "Timing and token counts were not recoverable from background subagent notifications in this run, so time_seconds is 0 and tokens uses output character count as a placeholder.",
        ],
    }

    (ROOT / "benchmark.json").write_text(json.dumps(benchmark, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
