import tkinter as tk
import random
from PIL import Image, ImageTk

CARD_WIDTH = 60
CARD_HEIGHT = 90
CARD_VALUES = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
CARD_POINTS = {str(i): i for i in range(2, 11)}
CARD_POINTS.update({'J': 10, 'Q': 10, 'K': 10, 'A': 11})

class BlackjackGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Blackjack")
        
        self.canvas = tk.Canvas(master, width=400, height=300)
        self.canvas.pack(side=tk.LEFT)

        self.summary_frame = tk.Frame(master)
        self.summary_frame.pack(side=tk.RIGHT)

        self.start_button = tk.Button(self.summary_frame, text="Start Game", command=self.start_game)
        self.start_button.pack()

        self.hit_button = tk.Button(self.summary_frame, text="Hit", command=self.hit, state=tk.DISABLED)
        self.hit_button.pack()

        self.stand_button = tk.Button(self.summary_frame, text="Stand", command=self.stand, state=tk.DISABLED)
        self.stand_button.pack()

        self.summary_label = tk.Label(self.summary_frame, text="Total: 0")
        self.summary_label.pack()

        self.result_label = tk.Label(self.summary_frame, text="")
        self.result_label.pack()

        self.wins = 0
        self.losses = 0
        self.ties = 0

        self.statistics_label = tk.Label(self.summary_frame, text=f"Wins: {self.wins}, Losses: {self.losses}, Ties: {self.ties}\n")
        self.statistics_label.pack()

        self.deck = [f"{value}{symbol}" for value in CARD_VALUES for symbol in ['H', 'D', 'C', 'S']]
        self.player_cards = []
        self.dealer_cards = []
        self.player_total = 0
        self.dealer_total = 0
        self.game_over = False

        self.card_images = self.load_spritesheet("assets/cards.png", 71, 96)
        self.map_cards()

    def load_spritesheet(self, spritesheet_path, card_width, card_height):
        try:
            spritesheet = Image.open(spritesheet_path)
            cards = []
            for row in range(7):  # Es gibt 7 Reihen
                for col in range(8):  # Es gibt 8 Karten pro Reihe
                    x = col * card_width
                    y = row * card_height
                    card = spritesheet.crop((x, y, x + card_width, y + card_height))
                    cards.append(ImageTk.PhotoImage(card))
            return cards
        except Exception as e:
            print(f"Fehler beim Laden des Spritesheets: {e}")
            return []
        
    def map_cards(self):
        card_order = [
            'AH', 'AC', 'AD', 'AS', 'KH', 'KC', 'KD', 'KS',
            '2H', '2C', '2D', '2S', 'QH', 'QC', 'QD', 'QS',
            '3H', '3C', '3D', '3S', 'JH', 'JC', 'JD', 'JS',
            '4H', '4C', '4D', '4S', '10H', '10C', '10D', '10S',
            '5H', '5C', '5D', '5S', '9H', '9C', '9D', '9S',
            '6H', '6C', '6D', '6S', '8H', '8C', '8D', '8S',
            '7H', '7C', '7D', '7S', 'JOKER1', 'JOKER2', 'BACK', 'PATTERN'
        ]
        self.card_map = {card: self.card_images[i] for i, card in enumerate(card_order)}

    def load_card_image(self, card):
        try:
            # Übersetze Kartenwerte und Symbole ins Deutsche
            translations = {
                '2': 'Zwei', '3': 'Drei', '4': 'Vier', '5': 'Fünf', '6': 'Sechs', '7': 'Sieben', 
                '8': 'Acht', '9': 'Neun', '10': 'Zehn', 'J': 'Bube', 'Q': 'Dame', 'K': 'König', 'A': 'Ass',
                'hearts': 'Herz', 'diamonds': 'Karo', 'clubs': 'Kreuz', 'spades': 'Piek'
            }
            value, symbol = card[:-1], card[-1]
            symbol_translation = {'H': 'hearts', 'D': 'diamonds', 'C': 'clubs', 'S': 'spades'}
            translated_value = translations[value]
            translated_symbol = translations[symbol_translation[symbol]]

        # Lade das Bild
            image_path = f"assets/{translated_value}_{translated_symbol}.png"
            image = Image.open(image_path)
            return ImageTk.PhotoImage(image)
        except Exception as e:
            print(f"Fehler beim Laden des Bildes für {card}: {e}")
            return None


    def start_game(self):
        self.deck = [f"{value}{symbol}" for value in CARD_VALUES for symbol in ['H', 'D', 'C', 'S']]
        random.shuffle(self.deck)
        random.shuffle(self.deck)
        self.player_cards = [self.draw_card(), self.draw_card()]
        self.dealer_cards = [self.draw_card()]
        self.update_canvas()
        self.calculate_totals()
        
        if self.player_total == 21:
            self.result_label.config(text="Blackjack! You win!")
            self.wins += 1
            self.game_over = True
            self.end_game()
        else:
            self.hit_button.config(state=tk.NORMAL)
            self.stand_button.config(state=tk.NORMAL)
            self.start_button.config(state=tk.DISABLED)
            self.result_label.config(text="")
            self.game_over = False

    def draw_card(self):
        if self.deck:
            return self.deck.pop()  # Ziehe die oberste Karte aus dem Deck
        else:
            print("Das Deck ist leer!")
            return None

    def update_canvas(self):
        self.canvas.delete("all")
        self.draw_cards(self.player_cards, 50)
        self.draw_cards(self.dealer_cards, 150, hide_second_card=not self.game_over)

    def draw_cards(self, cards, y, hide_second_card=False):
        for i, card in enumerate(cards):
            x = 20 + i * (71 + 10)  # 71 ist die Breite der Karte
            if hide_second_card and i == 1:
                self.canvas.create_rectangle(x, y, x + 71, y + 96, fill="white")
                self.canvas.create_text(x + 35, y + 48, text="?", font=("Arial", 24))
            else:
                card_image = self.card_map.get(card)
                if card_image:
                    self.canvas.create_image(x, y, anchor=tk.NW, image=card_image)
                else:
                    # Fallback: Rechteck mit Kartenname anzeigen
                    self.canvas.create_rectangle(x, y, x + 71, y + 96, fill="white")
                    self.canvas.create_text(x + 35, y + 48, text=card, font=("Arial", 12))

    def calculate_totals(self):
        self.player_total = self.calculate_hand_total(self.player_cards)
        self.dealer_total = self.calculate_hand_total(self.dealer_cards)
        self.summary_label.config(text=f"Total: {self.player_total}")

    def calculate_hand_total(self, cards):
        total = sum(CARD_POINTS[card] for card in cards)
        aces = cards.count('A')
        while total > 21 and aces:
            total -= 10
            aces -= 1
        return total

    def hit(self):
        if not self.game_over:
            self.player_cards.append(self.draw_card())
            self.update_canvas()
            self.calculate_totals()
            if self.player_total > 21:
                self.result_label.config(text="You bust! Dealer wins.")
                self.losses += 1
                self.game_over = True
                self.end_game()


    def stand(self):
        self.game_over = True
        self.dealer_turn()
        self.end_game()

    def dealer_turn(self):
        while self.dealer_total < self.player_total and self.player_total < 21:
            self.dealer_cards.append(self.draw_card())
            self.dealer_total = self.calculate_hand_total(self.dealer_cards)

    def end_game(self):
        self.update_canvas()
        self.determine_winner()

    def determine_winner(self):
        if self.player_total > 21:
            self.result_label.config(text="You busts! Dealer wins.")
            self.losses += 1
        elif self.dealer_total > 21:
            self.result_label.config(text="Dealer bust! You win!")
            self.wins += 1
        elif self.player_total > self.dealer_total:
            self.result_label.config(text="You win!")
            self.wins += 1
        elif self.player_total < self.dealer_total:
            self.result_label.config(text="Dealer wins.")
            self.losses += 1
        else:
            self.result_label.config(text="It's a tie.")
            self.ties += 1

        self.statistics_label.config(text=f"Wins: {self.wins}, Losses: {self.losses}, Ties: {self.ties}\n")

        self.hit_button.config(state=tk.DISABLED)
        self.stand_button.config(state=tk.DISABLED)
        self.start_button.config(state=tk.NORMAL)

if __name__ == "__main__":
    root = tk.Tk()
    game = BlackjackGame(root)
    root.mainloop()