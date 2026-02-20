from __future__ import annotations

import argparse


def main() -> None:
    parser = argparse.ArgumentParser(description="bkp6 MVP")
    parser.add_argument("--gui", action="store_true", help="Run GUI mode")
    args, _ = parser.parse_known_args()

    if args.gui:
        from src.bkp6_mvp import gui

        gui.main()
    else:
        from src.bkp6_mvp import cli

        cli.main()


if __name__ == "__main__":
    main()
