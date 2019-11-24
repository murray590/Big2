import pygame
import time
from enum import Enum

from core.card_list import CardList
from core.printer import Printer


class Colour(Enum):
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    PURPLE = (255, 0, 255)
    GREY = (180, 180, 180)


class Graphics(Printer):
    def __init__(self, width, height):
        pygame.init()
        pygame.display.set_caption("Big2")
        self.width = width
        self.height = height
        self.card_width = self.width / 16
        self.card_height = self.height / 8
        self.screen = pygame.display.set_mode((self.width, self.height))

    def choose_cards(self, hand):
        selected_cards = []
        while True:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP:
                    position = pygame.mouse.get_pos()
                    if self.play_button.collidepoint(position):
                        return selected_cards
                    elif any(card.image.collidepoint(position) for card in hand):
                        clicked_card = next(
                            (y for y in hand if y.image.collidepoint(position)), None
                        )
                        self.handle_card_click(clicked_card, selected_cards)
                elif event.type == pygame.QUIT:
                    pygame.quit()

    def handle_card_click(self, clicked_card, selected_cards):
        if clicked_card in selected_cards:
            selected_cards.remove(clicked_card)
            self.move_card_vertically(clicked_card, self.card_height / 2)
        else:
            selected_cards.append(clicked_card)
            self.move_card_vertically(clicked_card, -self.card_height / 2)

    def move_card_vertically(self, card, distance):
        pygame.draw.rect(
            self.screen,
            Colour.WHITE.value,
            (card.left, card.top, self.card_width, self.card_height),
            0,
        )
        self.display_single_card(card, card.left, card.top + distance)
        pygame.display.update()

    def display_single_card(self, card, left, top):
        card.left = left
        card.top = top
        card.image = pygame.draw.rect(
            self.screen, card.colour, (left, top, self.card_width, self.card_height), 0
        )
        self.display_text(
            str(card.pp_value), 60, Colour.GREY.value, card.colour, (left, top)
        )

    def display_text(self, text, size, colour, background, location):
        basic_font = pygame.font.SysFont(None, size)
        words = basic_font.render(text, True, colour, background)
        self.screen.blit(words, location)

    def repaint(self, player, cards):
        self.screen.fill(Colour.WHITE.value)
        pygame.draw.ellipse(
            self.screen,
            Colour.GREY.value,
            (self.width / 6, self.height / 4, 2 * self.width / 3, self.height / 2),
            0,
        )
        self.play_button = pygame.draw.rect(
            self.screen,
            Colour.GREY.value,
            (
                6 * self.width / 7,
                3 * self.height / 4,
                2.1 * self.card_width,
                0.5 * self.card_height,
            ),
            0,
        )
        self.display_text(
            "Play/pass",
            30,
            Colour.PURPLE.value,
            Colour.GREY.value,
            (6 * self.width / 7, 3 * self.height / 4),
        )
        self.display_text(
            f"Player {player.name}:",
            30,
            Colour.PURPLE.value,
            Colour.WHITE.value,
            (0, 3 * self.height / 4),
        )
        self.display_cards(
            cards,
            self.width / 2 - 2.5 * self.card_width,
            self.height / 2 - 0.5 * self.card_height,
        )

    def display_cards(self, cards, left, top):
        for i in range(0, len(cards)):
            self.display_single_card(cards[i], left + i * self.card_width, top)
        pygame.display.update()

    def message(self, message):
        self.display_text(
            message,
            30,
            Colour.PURPLE.value,
            Colour.GREY.value,
            (self.width / 10, self.height / 3),
        )
        pygame.display.update()
        time.sleep(5)

    def error(self, message):
        pass
        # self.display_text(message, 30, Colour.PURPLE.value, Colour.GREY.value, (self.width/10, self.height/3))
        # pygame.display.update()
        # time.sleep(5)
