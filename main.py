import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import subprocess
import sys
import os

def show_welcome_screen():
    def start_reading():
        welcome_root.destroy()
        # Launch card.py using same Python interpreter
        subprocess.run([sys.executable, "card.py"])

    welcome_root = tk.Tk()
    welcome_root.title("Welcome to the Tarot!")
    welcome_root.state("zoomed")  # Fullscreen

    # Get screen size for background image
    screen_width = welcome_root.winfo_screenwidth()
    screen_height = welcome_root.winfo_screenheight()

    # Load background image with error handling
    image_path = "C:/Users/bhoja/OneDrive/Pictures/tarot.png"
    if not os.path.exists(image_path):
        messagebox.showerror("Image Not Found", f"Could not find image at:\n{image_path}")
        return

    bg_image = Image.open(image_path)
    bg_image = bg_image.resize((screen_width, screen_height), Image.LANCZOS)
    bg_photo = ImageTk.PhotoImage(bg_image)

    # Set background
    bg_label = tk.Label(welcome_root, image=bg_photo)
    bg_label.image = bg_photo  # keep a reference
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    # Centered frame for text and button
    frame = tk.Frame(welcome_root, bg="#000000")
    frame.place(relx=0.5, rely=0.4, anchor="center")

    # Welcome text
    title = tk.Label(
        frame,
        text=(
            "🔮 Welcome to the Tarot 🔮\n\n"
            "Having trouble making a decision?\n"
            "Worried about the future?\n"
            "Concerned that secret forces are controlling your destiny?"
        ),
        font=("Segoe UI", 20, "bold"),
        fg="white",
        bg="#000000",
        justify="center",
        padx=40,
        pady=30
    )
    title.pack()

    # Start Reading button
    start_btn = tk.Button(
        frame,
        text="✨ Start Reading ✨",
        font=("Segoe UI", 14, "bold"),
        bg="#9B30FF",
        fg="white",
        activebackground="#BF40BF",
        activeforeground="white",
        padx=20,
        pady=10,
        command=start_reading
    )
    start_btn.pack(pady=20)

    welcome_root.mainloop()

if __name__ == "__main__":
    show_welcome_screen()
