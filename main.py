#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
main.py

Unified controller for prompt-library conversions.

Capabilities
- Scan default folders and let user select a source to convert
  - If you select an Excel file (.xlsx), it will convert Excel → Docs
  - If you select a prompt docs folder, it will convert Docs → Excel
- Fully non-interactive CLI flags are also supported (automation-friendly)

Conventions (relative to repository root = this file's parent)
- Excel sources under: ./prompt_excel/
- Docs sources under:  ./prompt_docs/
- Outputs:
  - Excel→Docs: ./prompt_docs/prompt_docs_YYYY_MMDD_HHMMSS/{prompts,docs}
  - Docs→Excel: ./prompt_excel/prompt_excel_YYYY_MMDD_HHMMSS/rebuilt.xlsx

Examples
  # Interactive selection
  python3 main.py

  # Non-interactive: choose one Excel file
  python3 main.py --select "prompt_excel/prompt (3).xlsx"

  # Non-interactive: choose one docs set directory
  python3 main.py --select "prompt_docs/prompt_docs_2025_0903_055708"

Notes
- This script is a thin orchestrator that delegates actual work to
  scripts/start_convert.py to ensure a single source of truth.
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Sequence, Tuple

# Optional Rich UI imports (fallback to plain if unavailable)
try:
    from rich.console import Console
    from rich.layout import Layout
    from rich.panel import Panel
    from rich.table import Table
    from rich.text import Text
    from rich import box
    from rich.prompt import IntPrompt
    _RICH_AVAILABLE = True
except Exception:  # pragma: no cover
    _RICH_AVAILABLE = False

# Optional InquirerPy for arrow-key selection
try:
    from InquirerPy import inquirer as _inq
    _INQUIRER_AVAILABLE = True
except Exception:  # pragma: no cover
    _INQUIRER_AVAILABLE = False


@dataclass
class Candidate:
    index: int
    kind: str  # "excel" | "docs"
    path: Path
    label: str


def get_repo_root() -> Path:
    return Path(__file__).resolve().parent


def list_excel_files(excel_dir: Path) -> List[Path]:
    if not excel_dir.exists():
        return []
    return sorted([p for p in excel_dir.iterdir() if p.is_file() and p.suffix.lower() == ".xlsx"], key=lambda p: p.stat().st_mtime)


def has_prompt_files(directory: Path) -> bool:
    if not directory.exists():
        return False
    # Detect files like "(r,c)_*.md" anywhere under the directory
    for file_path in directory.rglob("*.md"):
        name = file_path.name
        if name.startswith("(") and ")_" in name:
            return True
    return False


def list_doc_sets(docs_dir: Path) -> List[Path]:
    results: List[Path] = []
    if not docs_dir.exists():
        return results
    # If the docs_dir itself looks like a set, include it
    if has_prompt_files(docs_dir):
        results.append(docs_dir)
    # Also include any immediate children that look like a docs set
    for child in sorted(docs_dir.iterdir()):
        if child.is_dir() and has_prompt_files(child):
            results.append(child)
    return results


def run_start_convert(start_convert: Path, mode: str, project_root: Path, select_path: Optional[Path] = None, excel_dir: Optional[Path] = None, docs_dir: Optional[Path] = None) -> int:
    """Delegate to scripts/start_convert.py with appropriate flags."""
    python_exe = sys.executable
    cmd: List[str] = [python_exe, str(start_convert), "--mode", mode]
    if select_path is not None:
        # Always pass as repo-root-relative or absolute string
        cmd.extend(["--select", str(select_path)])
    if excel_dir is not None:
        cmd.extend(["--excel-dir", str(excel_dir)])
    if docs_dir is not None:
        cmd.extend(["--docs-dir", str(docs_dir)])

    # Execute in repo root to ensure relative defaults resolve correctly
    proc = subprocess.run(cmd, cwd=str(project_root))
    return proc.returncode


def build_candidates(project_root: Path, excel_dir: Path, docs_dir: Path) -> List[Candidate]:
    candidates: List[Candidate] = []
    idx = 1
    for path in list_excel_files(excel_dir):
        label = f"[Excel] {path.name}"
        candidates.append(Candidate(index=idx, kind="excel", path=path, label=label))
        idx += 1
    for path in list_doc_sets(docs_dir):
        display = path.relative_to(project_root) if path.is_absolute() else path
        label = f"[Docs] {display}"
        candidates.append(Candidate(index=idx, kind="docs", path=path, label=label))
        idx += 1
    return candidates


def select_interactively(candidates: Sequence[Candidate]) -> Optional[Candidate]:
    if not candidates:
        print("没有可用的 Excel 或 Docs 源。请将 .xlsx 放到 prompt_excel/ 或将文档放到 prompt_docs/ 下。")
        return None

    # Prefer arrow-key selection if available
    if _INQUIRER_AVAILABLE:
        try:
            choices = [
                {"name": f"{'[Excel]' if c.kind=='excel' else '[Docs]'} {c.label}", "value": c.index}
                for c in candidates
            ]
            selection = _inq.select(
                message="选择要转换的源（上下箭头，回车确认，Ctrl+C 取消）:",
                choices=choices,
                default=choices[0]["value"],
            ).execute()
            match = next((c for c in candidates if c.index == selection), None)
            return match
        except KeyboardInterrupt:
            return None

    if _RICH_AVAILABLE:
        console = Console()
        layout = Layout()
        layout.split_column(
            Layout(name="header", size=3),
            Layout(name="list"),
            Layout(name="footer", size=3),
        )
        header = Panel(Text("提示词库转换器", style="bold cyan"), subtitle="选择一个源开始转换", box=box.ROUNDED)

        table = Table(box=box.SIMPLE_HEAVY)
        table.add_column("编号", style="bold yellow", justify="right", width=4)
        table.add_column("类型", style="magenta", width=8)
        table.add_column("路径/名称", style="white")
        for c in candidates:
            table.add_row(str(c.index), "Excel" if c.kind == "excel" else "Docs", c.label)

        layout["header"].update(header)
        layout["list"].update(Panel(table, title="可选源", border_style="cyan"))
        layout["footer"].update(Panel(Text("输入编号并回车（0 退出）", style="bold"), box=box.ROUNDED))
        console.print(layout)

        while True:
            try:
                choice = IntPrompt.ask("编号", default=0)
            except Exception:
                return None
            if choice == 0:
                return None
            match = next((c for c in candidates if c.index == choice), None)
            if match is not None:
                return match
            console.print("[red]编号不存在，请重试[/red]")

    # Plain fallback
    print("请选择一个源进行转换：")
    for c in candidates:
        print(f"  {c.index:2d}. {c.label}")
    print("  0. 退出")
    while True:
        try:
            raw = input("输入编号后回车：").strip()
        except EOFError:
            return None
        if not raw:
            continue
        if raw == "0":
            return None
        if not raw.isdigit():
            print("请输入有效数字。")
            continue
        choice = int(raw)
        match = next((c for c in candidates if c.index == choice), None)
        if match is None:
            print("编号不存在，请重试。")
            continue
        return match


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="prompt-library conversion controller")
    p.add_argument("--excel-dir", type=str, default="prompt_excel", help="Excel sources directory (default: prompt_excel)")
    p.add_argument("--docs-dir", type=str, default="prompt_docs", help="Docs sources directory (default: prompt_docs)")
    p.add_argument("--select", type=str, default=None, help="Path to a specific .xlsx file or a docs folder")
    p.add_argument("--non-interactive", action="store_true", help="Do not prompt; require --select or exit")
    return p.parse_args()


def main() -> int:
    repo_root = get_repo_root()
    start_convert = repo_root / "scripts" / "start_convert.py"
    if not start_convert.exists():
        print("找不到 scripts/start_convert.py。")
        return 1

    args = parse_args()

    excel_dir = (repo_root / args.excel_dir).resolve() if not Path(args.excel_dir).is_absolute() else Path(args.excel_dir).resolve()
    docs_dir = (repo_root / args.docs_dir).resolve() if not Path(args.docs_dir).is_absolute() else Path(args.docs_dir).resolve()

    # Non-interactive path with explicit selection
    if args.non_interactive or args.select:
        if not args.select:
            print("--non-interactive 需要配合 --select 使用。")
            return 2
        selected = Path(args.select)
        if not selected.is_absolute():
            selected = (repo_root / selected).resolve()
        if not selected.exists():
            print(f"选择的路径不存在: {selected}")
            return 2
        if selected.is_file() and selected.suffix.lower() == ".xlsx":
            return run_start_convert(start_convert, mode="excel2docs", project_root=repo_root, select_path=selected, excel_dir=excel_dir)
        if selected.is_dir():
            # Treat as docs set
            return run_start_convert(start_convert, mode="docs2excel", project_root=repo_root, select_path=selected, docs_dir=docs_dir)
        print("无法识别的选择类型（既不是 .xlsx 文件也不是目录）。")
        return 2

    # Interactive selection
    candidates = build_candidates(repo_root, excel_dir, docs_dir)
    chosen = select_interactively(candidates)
    if chosen is None:
        return 0
    if chosen.kind == "excel":
        return run_start_convert(start_convert, mode="excel2docs", project_root=repo_root, select_path=chosen.path, excel_dir=excel_dir)
    else:
        return run_start_convert(start_convert, mode="docs2excel", project_root=repo_root, select_path=chosen.path, docs_dir=docs_dir)


if __name__ == "__main__":
    sys.exit(main())
