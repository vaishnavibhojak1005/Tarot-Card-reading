import tkinter as tk
from PIL import Image, ImageTk
import sys
import os

# Detailed tarot card meanings
descriptions = {
    "The Fool": "A fresh start is on the horizon. If you're wondering when something new will happen — like love, success, or opportunity — it will begin when you take a leap of faith. Trust your instincts. The timing is soon, but only once you're ready to step into the unknown.",

    "The Magician": "You already have what it takes. Manifestation is the key here. Whatever you're asking about — love, career, exams — success will come when you align your actions with your intent. Expect progress in the near term, especially if you stay focused.",

    "The High Priestess": "Now is a time for inner reflection. Answers will come from within, not from external action. Be patient — timing is uncertain, but you’ll intuitively feel when the right moment arrives.",

    "The Empress": "Abundance is coming. If your question is about relationships, pregnancy, or creativity, this card brings a big YES. Things are already in motion. Nurture what you’ve started, and expect blossoming results within months.",

    "The Emperor": "Structure and stability will bring the outcome you seek. Whether it’s career, marriage, or goals — commit to a plan, and the results will follow. Timing depends on discipline, but you’re on the right path.",

    "The Lovers": "In matters of love or choice, a meaningful connection is forming. A relationship will deepen or a major decision will guide your path. If asking about marriage — this card often predicts it within the year.",

    "The Chariot": "Victory is close. If you’re asking about success or progress, this card says YES — but only if you take control. Momentum is on your side. Expect movement within weeks to a few months.",

    "The Hermit": "Pause and look inward. This card suggests time is needed for self-discovery. If asking when, the answer is: not yet. Focus on understanding yourself first — the outcome will come naturally later.",

    "Justice": "The outcome will be fair. If you're facing a decision, exam, or relationship question — balance and honesty will prevail. Things will resolve once all truths are known — likely during a legal, academic, or karmic shift.",

    "Death": "Let go of the old. A transformation is happening. If asking when change will come — it will arrive after something ends. Embrace it. What you seek may come suddenly after a major shift.",

    "The Tower": "Expect the unexpected. A sudden event will shake things up. It might feel chaotic, but it's clearing space for growth. If you’re waiting for change — it’s coming fast and might not look how you expect.",

    "The Moon": "Confusion surrounds this issue. If you’re asking about outcomes, timing is unclear. Dreams, illusions, or fears may be clouding your path. Wait for clarity before taking action.",

    "The Sun": "YES! Joy and success are guaranteed. Whether it's about love, career, or life purpose — things will turn out beautifully. The timing is soon — this is a bright omen of happiness and achievement.",

    "Temperance": "Patience will bring balance. Things will happen gradually, in divine timing. If you're wondering when, this card says: not right away — but in perfect harmony when it’s meant to.",

    "The Devil": "You're being held back by fear, addiction, or toxic patterns. If asking why something isn’t happening — this is your answer. Free yourself, and the path will clear. Timing depends on you.",

    "The Star": "Hope is your compass. Healing is taking place, and what you desire is aligning for your future. If you asked about timing — expect a positive turn within the next few months. Keep believing.",

    "The World": "Completion is near. A cycle is finishing, and fulfillment awaits. If asking when something will happen — the answer is: at the end of your current phase. You’re almost there. Celebrate the progress!"
}


class AnswerApp:
    def __init__(self, root, cards):
        self.root = root
        self.cards = cards
        self.root.title("🔮 Your Tarot Reading 🔮")
        self.root.state("zoomed")  # Fullscreen

        self.set_background("tarot.png")

        self.overlay = tk.Frame(self.root, bg="#000000", bd=2)
        self.overlay.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.85, relheight=0.9)

        title = tk.Label(
            self.overlay, text="🃏 Your Tarot Reading 🃏",
            font=("Georgia", 26, "bold"),
            fg="#FFD700", bg="#000000"
        )
        title.pack(pady=20)

        self.display_cards()

    def set_background(self, image_path):
        try:
            if os.path.exists(image_path):
                screen_width = self.root.winfo_screenwidth()
                screen_height = self.root.winfo_screenheight()
                image = Image.open(image_path)
                image = image.resize((screen_width, screen_height), Image.LANCZOS)
                self.bg_image = ImageTk.PhotoImage(image)

                bg_label = tk.Label(self.root, image=self.bg_image)
                bg_label.place(x=0, y=0, relwidth=1, relheight=1)
            else:
                self.root.configure(bg="#1a1a2e")
        except Exception as e:
            print("Failed to set background:", e)
            self.root.configure(bg="#1a1a2e")

    def display_cards(self):
        card_frame = tk.Frame(self.overlay, bg="#111111")
        card_frame.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

        for card in self.cards:
            desc = descriptions.get(card, "This card holds mysterious power yet to be revealed...")
            frame = tk.Frame(card_frame, bg="#111111", pady=15, padx=15, bd=1, relief=tk.RIDGE)
            frame.pack(fill=tk.X, pady=10)

            label_title = tk.Label(frame, text=card, font=("Georgia", 18, "bold"),
                                   fg="#FF69B4", bg="#111111")
            label_title.pack(anchor="w")

            label_desc = tk.Label(frame, text=desc, font=("Arial", 12),
                                  fg="white", bg="#111111", wraplength=1000, justify="left")
            label_desc.pack(anchor="w", pady=(5, 0))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python answer.py 'The Fool' 'The Magician' 'The Sun'")
        sys.exit(1)

    root = tk.Tk()
    app = AnswerApp(root, sys.argv[1:])
    root.mainloop()
