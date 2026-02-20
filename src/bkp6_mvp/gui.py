from __future__ import annotations

import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox

from .cli import run_selection


class App(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("bkp6 MVP — Отбор комплектов")
        self.geometry("640x280")

        self.input_var = tk.StringVar()
        self.trigger_var = tk.StringVar()
        self.discipline_var = tk.StringVar()
        self.output_var = tk.StringVar(value="output/result.xlsx")
        self.db_var = tk.StringVar(value="output/rules.db")

        self._build()

    def _build(self) -> None:
        pad = {"padx": 8, "pady": 6}

        tk.Label(self, text="Входной Excel").grid(row=0, column=0, sticky="w", **pad)
        tk.Entry(self, textvariable=self.input_var, width=55).grid(row=0, column=1, **pad)
        tk.Button(self, text="...", command=self.pick_file).grid(row=0, column=2, **pad)

        tk.Label(self, text="Триггер").grid(row=1, column=0, sticky="w", **pad)
        tk.Entry(self, textvariable=self.trigger_var, width=30).grid(row=1, column=1, sticky="w", **pad)

        tk.Label(self, text="Спец").grid(row=2, column=0, sticky="w", **pad)
        tk.Entry(self, textvariable=self.discipline_var, width=30).grid(row=2, column=1, sticky="w", **pad)

        tk.Label(self, text="Выходной Excel").grid(row=3, column=0, sticky="w", **pad)
        tk.Entry(self, textvariable=self.output_var, width=55).grid(row=3, column=1, **pad)

        tk.Label(self, text="SQLite БД").grid(row=4, column=0, sticky="w", **pad)
        tk.Entry(self, textvariable=self.db_var, width=55).grid(row=4, column=1, **pad)

        tk.Button(self, text="Запустить", command=self.run).grid(row=5, column=1, sticky="e", **pad)

    def pick_file(self) -> None:
        path = filedialog.askopenfilename(filetypes=[("Excel", "*.xlsx")])
        if path:
            self.input_var.set(path)

    def run(self) -> None:
        try:
            out = run_selection(
                input_file=Path(self.input_var.get()),
                trigger=self.trigger_var.get(),
                discipline=self.discipline_var.get(),
                output_file=Path(self.output_var.get()),
                db_file=Path(self.db_var.get()),
            )
            messagebox.showinfo("Готово", f"Результат сохранен: {out}")
        except Exception as exc:
            messagebox.showerror("Ошибка", str(exc))


def main() -> None:
    app = App()
    app.mainloop()
