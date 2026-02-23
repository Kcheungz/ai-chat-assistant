import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import simpledialog
from assistant.utils.credentials import get_api_key, set_api_key
from assistant.config import get_settings
from assistant.openai_client import OpenAIClient
from assistant.models import ExplainRequest, QuizRequest
from assistant.services.explain_service import ExplainService
from assistant.services.quiz_service import QuizService
from assistant.utils.errors import ConfigError, AssistantError


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.withdraw()  # Hide window until key setup complete
        self.title("Study Assistant")
        self.geometry("950x650")

        settings = get_settings()

        # 1) Try env first
        api_key = (settings.api_key or "").strip()

        # 2) Try OS keyring
        if not api_key:
            api_key = (get_api_key() or "").strip()

        # 3) Prompt if missing
        if not api_key:
            api_key = simpledialog.askstring(
                "OpenAI API Key Required",
                "Enter your OpenAI API key.\n\n"
                "It will be securely stored on this computer.",
                show="*",
            ) or ""

            api_key = api_key.strip()

            if not api_key:
                messagebox.showerror(
                    "API Key Required",
                    "An OpenAI API key is required to use this application."
                )
                self.destroy()
                return

            set_api_key(api_key)

        # Initialize client + services
        client = OpenAIClient(api_key=api_key, model=settings.model)
        self.explain_service = ExplainService(client)
        self.quiz_service = QuizService(client)

        self._build_ui()

        self._build_menu()


        self.deiconify()  # Show window after setup


    def _build_ui(self):
        # Top input panel
        top = ttk.Frame(self, padding=10)
        top.pack(fill="x")

        ttk.Label(top, text="Topic / Prompt:").pack(anchor="w")
        self.topic = tk.Text(top, height=4, wrap="word")
        self.topic.pack(fill="x", pady=(5, 0))

        # Controls
        controls = ttk.Frame(self, padding=10)
        controls.pack(fill="x")

        ttk.Label(controls, text="Questions:").pack(side="left")
        self.num_q = tk.StringVar(value="5")
        ttk.Entry(controls, width=6, textvariable=self.num_q).pack(side="left", padx=(6, 16))

        ttk.Label(controls, text="Difficulty:").pack(side="left")
        self.diff = tk.StringVar(value="medium")
        ttk.Combobox(
            controls,
            width=10,
            textvariable=self.diff,
            values=["easy", "medium", "hard"],
            state="readonly",
        ).pack(side="left", padx=(6, 16))

        ttk.Button(controls, text="Explain", command=self.on_explain).pack(side="left", padx=(0, 8))
        ttk.Button(controls, text="Generate Quiz", command=self.on_quiz).pack(side="left")

        # Output
        out = ttk.Frame(self, padding=10)
        out.pack(fill="both", expand=True)

        ttk.Label(out, text="Output:").pack(anchor="w")
        self.output = tk.Text(out, wrap="word")
        self.output.pack(fill="both", expand=True, pady=(5, 0))

    def on_explain(self):
        try:
            topic = self.topic.get("1.0", "end").strip()
            if not topic:
                messagebox.showwarning("Missing topic", "Enter a topic first.")
                return

            resp = self.explain_service.explain(ExplainRequest(topic=topic))

            self.output.delete("1.0", "end")
            self.output.insert("1.0", resp.explanation)

        except AssistantError as e:
            messagebox.showerror("Error", str(e))

    def on_quiz(self):
        try:
            topic = self.topic.get("1.0", "end").strip()
            if not topic:
                messagebox.showwarning("Missing topic", "Enter a topic first.")
                return

            n = int(self.num_q.get())
            difficulty = self.diff.get()

            resp = self.quiz_service.quiz(QuizRequest(topic=topic, n=n, difficulty=difficulty))

            lines = [f"Topic: {resp.topic} (difficulty: {resp.difficulty})", ""]
            for i, q in enumerate(resp.questions, 1):
                lines.append(f"{i}. {q.question}")
                for c in q.choices:
                    lines.append(f"   {c.label}) {c.text}")
                lines.append(f"   Answer: {q.correct_label}")
                lines.append(f"   Rationale: {q.rationale}")
                lines.append("")
            text = "\n".join(lines)

            self.output.delete("1.0", "end")
            self.output.insert("1.0", text)

        except ValueError:
            messagebox.showerror("Invalid input", "Questions must be a number.")
        except AssistantError as e:
            messagebox.showerror("Error", str(e))


    def _build_menu(self):
        menubar = tk.Menu(self)

        settings_menu = tk.Menu(menubar, tearoff=0)
        settings_menu.add_command(label="Change API Key", command=self._change_api_key)
        settings_menu.add_command(label="Clear API Key", command=self._clear_api_key)
        menubar.add_cascade(label="Settings", menu=settings_menu)

        self.config(menu=menubar)

    def _change_api_key(self):
        from assistant.utils.credentials import set_api_key
        from tkinter import simpledialog

        new_key = simpledialog.askstring(
            "Change API Key",
            "Enter new OpenAI API key:",
            show="*",
        )

        if new_key:
            set_api_key(new_key.strip())
            messagebox.showinfo("Success", "API key updated.")

    def _clear_api_key(self):
        from assistant.utils.credentials import clear_api_key
        clear_api_key()
        messagebox.showinfo("Cleared", "API key removed. Restart app to re-enter.")



if __name__ == "__main__":
    try:
        App().mainloop()
    except ConfigError as e:
        # If tkinter is up, show popup. Otherwise print.
        try:
            messagebox.showerror("Configuration Error", str(e))
        except Exception:
            print(f"[config error] {e}")