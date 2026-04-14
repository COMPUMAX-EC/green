#!/usr/bin/env python3
"""
Actualiza el registro de actividad solo en 5 días elegidos al azar por semana ISO (UTC).
No hace commits; solo modifica archivos en el working tree para que el workflow los confirme.
"""

from __future__ import annotations

import json
import os
import random
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEDULE_DIR = ROOT / "data" / "schedules"
LOG_PATH = ROOT / "data" / "activity-log.md"


def iso_week_key(now: datetime) -> str:
    y, w, _ = now.isocalendar()
    return f"{y}-W{w:02d}"


def load_or_create_schedule(week_key: str) -> dict:
    SCHEDULE_DIR.mkdir(parents=True, exist_ok=True)
    path = SCHEDULE_DIR / f"{week_key}.json"
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    # 1 = lunes … 7 = domingo (isocalendar)
    active = sorted(random.sample(range(1, 8), 5))
    data = {
        "week": week_key,
        "active_days": active,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
    }
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return data


def ensure_log_header() -> None:
    if LOG_PATH.exists() and LOG_PATH.stat().st_size > 0:
        return
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    LOG_PATH.write_text(
        "# Registro de ejecuciones\n\n"
        "Cada fila enlaza con una ejecución real de GitHub Actions.\n\n"
        "| Marca temporal (UTC) | Ejecución | Semana | Día ISO (1=lun) |\n"
        "| --- | --- | --- | --- |\n",
        encoding="utf-8",
    )


def main() -> int:
    now = datetime.now(timezone.utc)
    week_key = iso_week_key(now)
    _, _, today_dow = now.isocalendar()
    schedule = load_or_create_schedule(week_key)

    if today_dow not in schedule["active_days"]:
        print(
            f"Hoy (día ISO {today_dow}, semana {week_key}) no está en "
            f"{schedule['active_days']}; no se modifica el log."
        )
        return 0

    ensure_log_header()
    run_id = os.environ.get("GITHUB_RUN_ID", "local")
    server_url = os.environ.get("GITHUB_SERVER_URL", "https://github.com")
    repo = os.environ.get("GITHUB_REPOSITORY", "")
    if repo:
        run_url = f"{server_url}/{repo}/actions/runs/{run_id}"
        run_cell = f"[{run_id}]({run_url})"
    else:
        run_cell = f"`{run_id}`"

    line = (
        f"| {now.isoformat(timespec='seconds')} | {run_cell} | `{week_key}` | {today_dow} |\n"
    )
    with LOG_PATH.open("a", encoding="utf-8") as f:
        f.write(line)

    print(f"Añadida entrada al log para semana {week_key}, día {today_dow}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
