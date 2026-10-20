import json
from pathlib import Path
import subprocess
import sys
import unittest


RUNNER = Path(__file__).with_name("run.py")


class RuntimeTests(unittest.TestCase):
    def run_tool(self, *args):
        return subprocess.run(
            [sys.executable, "-B", str(RUNNER), *args],
            capture_output=True, text=True, encoding="utf-8", timeout=30,
        )

    def test_python_environment_stays_on_d(self):
        code = (
            "import json, os, pathlib, tempfile; "
            "from agent_reach.config import Config; "
            "print(json.dumps({'home': str(pathlib.Path.home()), "
            "'config': str(Config.CONFIG_FILE), 'temp': tempfile.gettempdir(), "
            "'cache': os.environ['npm_config_cache']}))"
        )
        result = self.run_tool("python", "-c", code)
        self.assertEqual(result.returncode, 0, result.stderr)
        paths = json.loads(result.stdout)
        for value in paths.values():
            self.assertTrue(value.lower().startswith("d:"), value)
        self.assertFalse(Path(paths["temp"]).exists())

    def test_child_exit_code_is_preserved(self):
        result = self.run_tool("python", "-c", "raise SystemExit(7)")
        self.assertEqual(result.returncode, 7, result.stderr)

    def test_doctor_can_find_local_opencli(self):
        result = self.run_tool("python", "-c", "import shutil; print(shutil.which('opencli'))")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("node_modules", result.stdout)
        self.assertIn("opencli", result.stdout)

    def test_unknown_tool_is_rejected(self):
        result = self.run_tool("not-an-installed-tool")
        self.assertEqual(result.returncode, 2, result.stderr)
        self.assertIn("invalid choice", result.stderr)


if __name__ == "__main__":
    unittest.main()
