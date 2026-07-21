"""Setup script — installs dependencies and prepares development environment.

Usage:
    python scripts/setup.py
"""

import subprocess
import sys
from pathlib import Path


def run_command(cmd: list[str], description: str) -> None:
    """Run a shell command with feedback."""
    print(f"\n  ⏳ {description}...")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"  ❌ Failed: {result.stderr.strip()}")
        sys.exit(1)
    print(f"  ✅ Done")


def main() -> None:
    """Run the complete setup process."""
    root = Path(__file__).resolve().parent.parent

    print("=" * 60)
    print("  Barbershop SaaS — Development Setup")
    print("=" * 60)

    # 1. Check Python version
    print(f"\n  🐍 Python {sys.version.split()[0]}")

    # 2. Install uv (fast package manager)
    run_command(
        ["pip", "install", "uv"],
        "Installing uv package manager",
    )

    # 3. Install dependencies
    run_command(
        ["uv", "sync", "--dev"],
        "Installing project dependencies",
    )

    # 4. Setup pre-commit hooks
    run_command(
        ["uv", "run", "pre-commit", "install"],
        "Installing pre-commit hooks",
    )

    # 5. Copy .env if not exists
    env_file = root / ".env"
    env_example = root / ".env.example"
    if not env_file.exists():
        env_file.write_text(env_example.read_text())
        print("\n  ⏳ Creating .env from .env.example...")
        print("  ✅ Created .env — please review and update secrets")

    print("\n" + "=" * 60)
    print("  ✅ Setup complete!")
    print("=" * 60)
    print(f"""
  Next steps:
    1. Review and update .env with your settings
    2. Start Docker services: docker compose up -d
    3. Run database migrations: uv run alembic upgrade head
    4. Start dev server: uv run uvicorn src.presentation.api.app:create_app --factory --reload
    5. Open http://localhost:8000/docs for API documentation
    """)


if __name__ == "__main__":
    main()
