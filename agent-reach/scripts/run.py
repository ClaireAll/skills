"""Run the installed research tools with process-local storage on D:."""

import argparse
import os
from pathlib import Path
import subprocess
import tempfile


ROOT = Path(r"D:\Claire\tools\investment-research")
NODE = Path(r"D:\Claire\tools\node-v24.21.0-win-x64\node.exe")
SCRIPTS = ROOT / ".venv" / "Scripts"
TOOLS = {
    "agent-reach": [str(SCRIPTS / "agent-reach.exe")],
    "python": [str(SCRIPTS / "python.exe"), "-B"],
    "opencli": [str(NODE), str(ROOT / "node/node_modules/@jackwener/opencli/dist/src/main.js")],
}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("tool", choices=TOOLS)
    parser.add_argument("arguments", nargs=argparse.REMAINDER)
    args = parser.parse_args()
    home = ROOT / "home"
    home.mkdir(parents=True, exist_ok=True)
    temp_root = Path(r"D:\Claire\temp")
    temp_root.mkdir(parents=True, exist_ok=True)
    env = os.environ.copy()
    env.update({
        "HOME": str(home),
        "USERPROFILE": str(home),
        "APPDATA": str(home / "AppData/Roaming"),
        "LOCALAPPDATA": str(home / "AppData/Local"),
        "XDG_CONFIG_HOME": str(home / ".config"),
        "XDG_CACHE_HOME": str(home / ".cache"),
        "npm_config_cache": r"D:\Claire\cache\npm",
        "PIP_CACHE_DIR": r"D:\Claire\cache\pip",
        "NODE_COMPILE_CACHE": r"D:\Claire\cache\node-compile",
        "PYTHONDONTWRITEBYTECODE": "1",
        "PYTHONUTF8": "1",
        "PATH": os.pathsep.join([str(SCRIPTS), str(NODE.parent), str(ROOT / "node/node_modules/.bin"), env.get("PATH", "")]),
    })
    with tempfile.TemporaryDirectory(prefix="investment-research-", dir=temp_root) as scratch:
        env.update({"TEMP": scratch, "TMP": scratch})
        return subprocess.run([*TOOLS[args.tool], *args.arguments], env=env).returncode


if __name__ == "__main__":
    raise SystemExit(main())
