"""Project entry point with a tiny app object and business logic."""

from dataclasses import dataclass


@dataclass(frozen=True)
class App:
    """Minimal application object with metadata and useful methods."""

    title: str = "bkp6 API"
    version: str = "0.1.0"

    def health(self) -> dict[str, str]:
        """Return service health information."""
        return {"status": "ok", "service": self.title, "version": self.version}

    def add(self, left: int, right: int) -> int:
        """Add two integers."""
        return left + right


app = App()


if __name__ == "__main__":
    print(app.health())
