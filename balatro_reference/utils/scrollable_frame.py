import tkinter as tk


class ScrollableFrame(tk.Frame):
    """
    A frame that can scroll vertically. Put your widgets inside `self.inner`
    instead of putting them directly in this frame.

    Useful when there's more content than fits on screen (like a long list
    of tarot cards).
    """

    def __init__(self, parent, bg="#1f1f2e"):
        super().__init__(parent, bg=bg)

        canvas = tk.Canvas(self, bg=bg, highlightthickness=0)
        scrollbar = tk.Scrollbar(self, orient="vertical", command=canvas.yview)

        self.inner = tk.Frame(canvas, bg=bg)

        self.inner.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all")),
        )

        canvas.create_window((0, 0), window=self.inner, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Let the mouse wheel scroll this canvas, but only while the mouse
        # is actually hovering over it.
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        def _bind_mousewheel(event):
            canvas.bind_all("<MouseWheel>", _on_mousewheel)

        def _unbind_mousewheel(event):
            canvas.unbind_all("<MouseWheel>")

        canvas.bind("<Enter>", _bind_mousewheel)
        canvas.bind("<Leave>", _unbind_mousewheel)