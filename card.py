import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import os
from mysql.connector import connect, Error
import subprocess
import sys
from datetime import datetime


def get_zodiac_from_dob(dob_str):
    try:
        dob = datetime.strptime(dob_str, "%Y-%m-%d")
        month, day = dob.month, dob.day
        zodiac_signs = [
            ("Capricorn", (1, 19)), ("Aquarius", (2, 18)), ("Pisces", (3, 20)),
            ("Aries", (4, 19)), ("Taurus", (5, 20)), ("Gemini", (6, 20)),
            ("Cancer", (7, 22)), ("Leo", (8, 22)), ("Virgo", (9, 22)),
            ("Libra", (10, 22)), ("Scorpio", (11, 21)), ("Sagittarius", (12, 21)),
            ("Capricorn", (12, 31))
        ]
        for sign, (m, d) in zodiac_signs:
            if (month, day) <= (m, d):
                return sign
        return "Capricorn"
    except:
        return ""


class TarotForm:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Tarot Reading Info")
        self.root.state("zoomed")

        self.set_background()

        self.main_frame = tk.Frame(self.root, bg="black", bd=2, relief=tk.RIDGE)
        self.main_frame.place(relx=0.5, rely=0.5, anchor="center", width=600, height=750)

        title = tk.Label(
            self.main_frame,
            text="🔮 Tarot Reading Form 🔮",
            font=("Georgia", 24, "bold"),
            fg="#9B30FF",
            bg="black",
            pady=20
        )
        title.pack()

        self.create_form()
        self.root.mainloop()

    def set_background(self):
        try:
            bg_image_path = "tarot.png"
            if os.path.exists(bg_image_path):
                screen_width = self.root.winfo_screenwidth()
                screen_height = self.root.winfo_screenheight()
                bg_image = Image.open(bg_image_path)
                bg_image = bg_image.resize((screen_width, screen_height), Image.LANCZOS)
                self.bg_photo = ImageTk.PhotoImage(bg_image)

                bg_label = tk.Label(self.root, image=self.bg_photo)
                bg_label.place(x=0, y=0, relwidth=1, relheight=1)
            else:
                self.root.configure(bg="#1a1a2e")
        except Exception as e:
            self.root.configure(bg="#1a1a2e")
            print(f"Background error: {e}")

    def create_form(self):
        form_frame = tk.Frame(self.main_frame, bg="black")
        form_frame.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)

        label_style = {"font": ("Arial", 12), "fg": "white", "bg": "black", "anchor": "w"}
        entry_style = {"font": ("Arial", 11), "bg": "#2d2d2d", "fg": "white", "insertbackground": "white"}

        # Name
        tk.Label(form_frame, text="Full Name:", **label_style).pack(pady=(5, 0))
        self.name_entry = tk.Entry(form_frame, **entry_style)
        self.name_entry.pack(fill=tk.X, pady=(0, 10), ipady=4)

        # Age
        tk.Label(form_frame, text="Age:", **label_style).pack(pady=(5, 0))
        self.age_entry = tk.Entry(form_frame, **entry_style)
        self.age_entry.pack(fill=tk.X, pady=(0, 10), ipady=4)

        # Date of Birth
        tk.Label(form_frame, text="Date of Birth (YYYY-MM-DD):", **label_style).pack(pady=(5, 0))
        self.dob_entry = tk.Entry(form_frame, **entry_style)
        self.dob_entry.pack(fill=tk.X, pady=(0, 10), ipady=4)
        self.dob_entry.bind("<FocusOut>", self.update_zodiac_from_dob)

        # Zodiac (read-only)
        tk.Label(form_frame, text="Zodiac Sign :", **label_style).pack(pady=(5, 0))
        self.zodiac_label = tk.Label(form_frame, text="", font=("Arial", 12, "bold"),
                                     bg="black", fg="#FFD700", anchor="w")
        self.zodiac_label.pack(fill=tk.X, pady=(0, 10))

        # Gender
        tk.Label(form_frame, text="Gender:", **label_style).pack(pady=(5, 0))
        self.gender_var = tk.StringVar()
        gender_combo = ttk.Combobox(form_frame, textvariable=self.gender_var,
                                    values=["Male", "Female", "Non-binary", "Other"],
                                    state="readonly")
        gender_combo.pack(fill=tk.X, pady=(0, 10), ipady=4)

        # Reading Type
        tk.Label(form_frame, text="Reading Type:", **label_style).pack(pady=(5, 0))
        self.reading_type_var = tk.StringVar()
        reading_combo = ttk.Combobox(form_frame, textvariable=self.reading_type_var,
                                     values=["Love & Relationships", "Career & Finances", "Life Path / Purpose",
                                             "Spiritual Growth", "Health & Wellness", "General Guidance"],
                                     state="readonly")
        reading_combo.pack(fill=tk.X, pady=(0, 10), ipady=4)

        # Question
        tk.Label(form_frame, text="Your Question:", **label_style).pack(pady=(5, 0))
        self.question_text = tk.Text(form_frame, height=5, wrap=tk.WORD,
                                     bg="#2d2d2d", fg="white", insertbackground="white",
                                     font=("Arial", 11))
        self.question_text.pack(fill=tk.X, pady=(0, 10))

        # Submit button
        submit_btn = tk.Button(form_frame, text="🔮 Submit Reading Request",
                               command=self.submit_form,
                               bg="#9B30FF", fg="white",
                               activebackground="#7D26CD", activeforeground="white",
                               font=("Arial", 12, "bold"),
                               padx=20, pady=10,
                               bd=0, relief=tk.FLAT, cursor="hand2")
        submit_btn.pack(pady=(30, 10), ipadx=20)


    def update_zodiac_from_dob(self, event=None):
        dob = self.dob_entry.get().strip()
        zodiac = get_zodiac_from_dob(dob)
        self.zodiac_label.config(text=zodiac)

    def submit_form(self):
        name = self.name_entry.get().strip()
        age = self.age_entry.get().strip()
        dob = self.dob_entry.get().strip()
        gender = self.gender_var.get()
        zodiac = self.zodiac_label.cget("text")
        reading_type = self.reading_type_var.get()
        question = self.question_text.get("1.0", tk.END).strip()

        if not all([name, age, dob, gender, zodiac, reading_type, question]):
            messagebox.showwarning("Missing Information", "Please fill in all fields.")
            return

        try:
            age = int(age)
        except ValueError:
            messagebox.showerror("Invalid Age", "Please enter a valid age.")
            return

        if insert_user_info(name, age, dob, gender, zodiac, reading_type, question):
            messagebox.showinfo("Success", "Reading submitted!")
            self.root.destroy()
            subprocess.Popen([sys.executable, "reading.py", question])


def insert_user_info(name, age, dob, gender, zodiac, reading_type, question):
    try:
        conn = connect(
            host="localhost",
            user="root",
            password="1005",
            database="tarot_app"
        )
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO user_info (name, age, dob, gender, zodiac, reading_type, question)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (name, age, dob, gender, zodiac, reading_type, question))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Error as e:
        messagebox.showerror("Database Error", str(e))
        return False


if __name__ == "__main__":
    TarotForm()
