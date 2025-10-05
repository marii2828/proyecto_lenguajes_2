import json, subprocess, os, random

CLI_PATH = os.environ.get("SOPA_CLI_PATH", None)

def _call_cli(op: str, payload: dict):
    if CLI_PATH and os.path.exists(CLI_PATH):
        cmd = [CLI_PATH, op]
    else:
        root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        cli_proj = os.path.join(root, "backend", "Sopa.Cli", "Sopa.Cli.fsproj")
        cmd = ["dotnet", "run", "--project", cli_proj, "--", op]

    proc = subprocess.run(
        cmd, input=json.dumps(payload, ensure_ascii=False),
        text=True, capture_output=True
    )
    if proc.returncode != 0:
        raise RuntimeError(f"CLI error {proc.returncode}: {proc.stderr.strip()}")
    return json.loads(proc.stdout)

def generate(words, size=None, seed=random.randint(1, 100)):
    return _call_cli("generate", {"words": words, "size": size, "seed": seed})

def validate(grid, words_remaining, start, end):
    return _call_cli("validate", {
        "grid": grid,
        "wordsRemaining": words_remaining,
        "selection": {"start": start, "end": end}
    })

def solve(grid, words_remaining):
    return _call_cli("solve", {"grid": grid, "wordsRemaining": words_remaining})
