import customtkinter as tk # type:ignore

def center_ctk(WINDOW: tk.CTk) -> None:
    """
    Centers the window on the screen.
    
    :param WINDOW: Window to center.
    """
    WINDOW.update_idletasks()
    width = WINDOW.winfo_width()
    height = WINDOW.winfo_height()

    screen_width = WINDOW.winfo_screenwidth()
    screen_height = WINDOW.winfo_screenheight()

    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)

    WINDOW.geometry(f"{width}x{height}+{x}+{y}")