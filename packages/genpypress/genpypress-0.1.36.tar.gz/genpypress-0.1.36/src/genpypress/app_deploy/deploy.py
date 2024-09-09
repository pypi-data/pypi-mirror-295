#!/usr/bin/env python3

import pathlib
import shutil
import os
import re
from textwrap import dedent
import argparse

DEPLOYDIR = "_deployment"

HOME_DIR = pathlib.Path.home()

BTEQ_HEADER = f"""
-----------------------------------------------------------
.SET SESSION CHARSET 'UTF8'
.SET WIDTH 65531
.SET ERRORLEVEL UNKNOWN SEVERITY 8;
.SET ERROROUT STDOUT;
.SET MAXERROR 1
-----------------------------------------------------------
.RUN FILE='{str(HOME_DIR)}/Vaults/o2/logon_prod.sql  -- collect stats - pro neex. stat - projde
--.SET ERRORLEVEL 3803 SEVERITY 0;          -- projde create tabulky ktera existuje
--.SET ERRORLEVEL 3807 SEVERITY 0;          -- projde drop tabulky ktera neexistuje

"""


def _get_bash_cmd(p: pathlib.Path) -> str:
    rv = dedent(
        f"""
    echo "running {p.stem}"
    bteq < {p.name}.bteq &>>../../log/{p.stem}.log
    retval=$?
    if [ $retval -ne 0 ]; then
        echo "===============ERROR================="
        echo "====================================="
        exit $retval
    fi
    """
    )
    return rv


def _make_executable(path: pathlib.Path):
    mode = os.stat(path).st_mode
    mode |= (mode & 0o444) >> 2  # copy R bits to X
    os.chmod(path, mode)


def _attempts(name: str) -> list[str]:
    return [name.upper(), name.lower(), name.title()]


def _get_dir(path: pathlib.Path) -> pathlib.Path:
    parent = path.parent
    name = path.name
    for attempt in _attempts(name):
        d = parent / attempt
        if d.is_dir():
            return d
    raise ValueError(f"dir does not exist: {path}")


def _scandir(p: pathlib.Path, to_prod: bool):
    pack_dir = _get_dir(p / "db")
    tera_dir = _get_dir(pack_dir / "teradata")
    deploy_dir = pack_dir / DEPLOYDIR
    log_dir = p / "log"
    step_directories = [
        i for i in tera_dir.iterdir() if i.is_dir() and i.name != DEPLOYDIR
    ]
    step_directories = sorted(step_directories, key=lambda x: x.name)

    deploy_dir.mkdir(parents=True, exist_ok=True)
    shutil.rmtree(log_dir, ignore_errors=True)
    log_dir.mkdir(parents=True, exist_ok=True)

    # produkce nebo dev?
    replacements = {}
    if not to_prod:
        replacements = {
            "^ap_(.*)": r"ad0_\1",
            "^ep_(.*)": r"ed0_\1",
        }

    commands = []
    for step in step_directories:
        _make_step(pack_dir, step, replacements)
        commands.append(_get_bash_cmd(step))

    shc = "#!/bin/bash\n" + "\n\n".join(commands)
    sh = deploy_dir / "runme.sh"
    sh.write_text(shc, encoding="utf-8")
    _make_executable(sh)


def _make_step(
    pack_dir: pathlib.Path, step_dir: pathlib.Path, replacements: dict[str, str]
):
    """
    _make_step: vrací seznam BTEQ příkazů, které spustí nasazení.
    Mimo jiné řeší problematiku převodu prod databází na dev databáze, podkel konfigurace.
    """

    def replace_database(d: str) -> str:
        for k, v in replacements.items():
            d = re.sub(k, v, d, flags=re.IGNORECASE)
        return d

    databases = [d.name for d in step_dir.iterdir() if d.is_dir()]
    databases = sorted(databases)

    # TODO: doplnit standardní BTEQ header, podle konfigurace (optional, klidně hard code)
    commands = []

    files = sorted(
        [f for f in step_dir.glob("*.*") if f.suffix.lower() in (".sql", ".bteq")]
    )
    for f in files:
        rp = f.relative_to(step_dir)
        commands.append(f".run file='../{step_dir.name}/{str(rp)}'")

    for db in databases:
        dbdir = step_dir / db
        commands.append("")

        commands.append(f"database {replace_database(db)};")
        files = [f for f in dbdir.rglob("*.*") if f.suffix.lower() in (".sql", ".bteq")]
        for f in files:
            rp = f.relative_to(step_dir)
            commands.append(f".run file='../teradata/{step_dir.name}/{str(rp)}'")

    commands.insert(0, BTEQ_HEADER)
    bteq_content = "\n".join(commands)

    fbtq = pack_dir / DEPLOYDIR / f"{step_dir.name}.bteq"
    fbtq.write_text(bteq_content, encoding="utf-8")


def deploy():
    ap = argparse.ArgumentParser(
        prog="bi",
        description="bihelp deploy",
    )
    ap.add_argument("--prod", default=False, action="store_true")
    args = ap.parse_args()
    _scandir(pathlib.Path.cwd(), to_prod=args.prod)
