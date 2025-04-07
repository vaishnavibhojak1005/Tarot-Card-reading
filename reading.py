import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import sys
import random
import subprocess
from mysql.connector import connect


class ReadingApp:
    def __init__(self, root, question):
        self.root = root
        self.question = question
        self.cards = [
            "The Fool", "The Magician", "The High Priestess", "The Empress", "The Emperor",
            "The Hierophant", "The Lovers", "The Chariot", "Strength", "The Hermit", "Wheel of Fortune",
            "Justice", "The Hanged Man", "Death", "Temperance", "The Devil", "The Tower", "The Star",
            "The Moon", "The Sun", "Judgement", "The World"
        ]
        self.drawn_cards = []
        self.user_data = self.get_user_data()

        try:
            self.bg_image = Image.open("tarot.png")
            self.card_image = Image.open("card.png").resize((220, 330))  # Increased card size
        except Exception as e:
            messagebox.showerror("Image Load Error", f"Error loading images:\n{e}")
            sys.exit(1)

        self.build_ui()

    def get_user_data(self):
        try:
            conn = connect(
                host="localhost",
                user="root",
                password="1005",
                database="tarot_app"
            )
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                "SELECT * FROM user_info WHERE question = %s ORDER BY created_at DESC LIMIT 1",
                (self.question,)
            )
            result = cursor.fetchone()
            cursor.close()
            conn.close()
            return result
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to fetch user info:\n{e}")
            return None

    def build_ui(self):
        self.root.title("Tarot Reading")
        self.root.attributes("-fullscreen", True)
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()

        self.canvas = tk.Canvas(self.root, width=self.screen_width, height=self.screen_height)
        self.canvas.pack(fill="both", expand=True)

        # Background
        self.bg_resized = ImageTk.PhotoImage(self.bg_image.resize((self.screen_width, self.screen_height)))
        self.canvas.create_image(0, 0, image=self.bg_resized, anchor="nw")

        # Question
        self.canvas.create_text(self.screen_width // 2, 60, text="Your Question:",
                                font=("Georgia", 24, "bold"), fill="white")
        self.canvas.create_text(self.screen_width // 2, 110, text=self.question,
                                font=("Georgia", 18), fill="white", width=self.screen_width - 100)

        # Cards Frame (adjusted position)
        self.cards_frame = tk.Frame(self.root, bg="black")
        self.canvas.create_window(self.screen_width // 2, self.screen_height // 2 - 20, window=self.cards_frame)

        # Draw Button
        self.draw_button = tk.Button(self.root, text="🔮 Draw 3 Cards", command=self.draw_cards,
                                     font=("Arial", 14, "bold"), bg="#333", fg="white", padx=20, pady=8)
        self.canvas.create_window(self.screen_width // 2, self.screen_height - 140, window=self.draw_button)

        # Result Button
        self.result_button = tk.Button(self.root, text="✨ View Result", command=self.show_answers,
                                       font=("Arial", 13), bg="#555", fg="white", padx=20, pady=7, state="disabled")
        self.canvas.create_window(self.screen_width // 2, self.screen_height - 80, window=self.result_button)

        self.root.bind("<Escape>", lambda e: self.root.destroy())

    def draw_cards(self):
        try:
            self.drawn_cards = random.sample(self.cards, 3)
            for widget in self.cards_frame.winfo_children():
                widget.destroy()

            card_img = ImageTk.PhotoImage(self.card_image)
            for card in self.drawn_cards:
                card_frame = tk.Frame(self.cards_frame, bg="black", padx=5, pady=5)
                tk.Label(card_frame, image=card_img, bg="black").pack()
                tk.Label(card_frame, text=card, font=("Arial", 14, "italic"), bg="black", fg="white").pack(pady=4)
                card_frame.pack(side="left", padx=10)  # Reduced padding to make frame tighter

            self.result_button.config(state="normal")
            self.cards_frame.image = card_img

        except Exception as e:
            messagebox.showerror("Card Drawing Error", f"Something went wrong:\n{e}")

    def show_answers(self):
        try:
            if not self.drawn_cards:
                messagebox.showinfo("No Cards", "Please draw your 3 cards first.")
                return
            subprocess.Popen([sys.executable, "answer.py"] + self.drawn_cards)
        except Exception as e:
            messagebox.showerror("View Result Error", f"Could not open results:\n{e}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python reading.py 'your question'")
        sys.exit(1)

    question_text = " ".join(sys.argv[1:])
    root = tk.Tk()
    app = ReadingApp(root, question_text)
    root.mainloop()
