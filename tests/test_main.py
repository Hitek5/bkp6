"""Tests for app.main."""

import unittest

from app.main import app


class AppTests(unittest.TestCase):
    def test_title_is_available(self) -> None:
        self.assertEqual(app.title, "bkp6 API")

    def test_health(self) -> None:
        self.assertEqual(
            app.health(),
            {"status": "ok", "service": "bkp6 API", "version": "0.1.0"},
        )

    def test_add(self) -> None:
        self.assertEqual(app.add(2, 3), 5)


if __name__ == "__main__":
    unittest.main()
