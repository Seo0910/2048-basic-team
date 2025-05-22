import pygame
import sys
import random

pygame.init()
WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Indian Game")
clock = pygame.time.Clock()
font = pygame.font.SysFont("AppleGothic", 28)
small_font = pygame.font.SysFont("AppleGothic", 22)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (34, 139, 34)
RED = (255, 80, 80)
BLUE = (80, 80, 255)
GRAY = (160, 160, 160)

player_money = 1000
computer_money = 1000
player_card = None
computer_card = None
player_prob = 0
computer_prob = 0
round_result = ""
betting_done = False
player_bets = False
explanation = ""

deck = [i for i in range(1, 6) for _ in range(4)]
random.shuffle(deck)

def draw_card(x, y, value=None):
    pygame.draw.rect(screen, WHITE, (x, y, 80, 120))
    pygame.draw.rect(screen, BLACK, (x, y, 80, 120), 2)
    text = font.render("?" if value is None else str(value), True, BLACK)
    screen.blit(text, (x + 25, y + 40))

def draw_button(text, x, y, w, h, color):
    pygame.draw.rect(screen, color, (x, y, w, h))
    label = small_font.render(text, True, BLACK)
    screen.blit(label, (x + 10, y + 10))
    return pygame.Rect(x, y, w, h)

def get_remaining_cards():
    full_deck = [i for i in range(1, 6) for _ in range(4)]
    used = [player_card, computer_card]
    for c in used:
        full_deck.remove(c)
    return full_deck

def calculate_player_win_prob(computer_card):
    remaining = get_remaining_cards()
    wins = sum(1 for c in remaining if c > computer_card)
    return int((wins / len(remaining)) * 100)

def calculate_computer_win_prob(player_card):
    remaining = get_remaining_cards()
    wins = sum(1 for c in remaining if c < player_card)
    return int((wins / len(remaining)) * 100)

def expected_reward(win_prob, max_amount=100):
    return int(max_amount * (1 - win_prob / 100))

def deal_cards():
    global player_card, computer_card, player_prob, computer_prob
    global round_result, betting_done, player_bets, explanation
    if len(deck) < 2:
        return
    player_card = deck.pop()
    computer_card = deck.pop()
    player_prob = calculate_player_win_prob(computer_card)
    computer_prob = calculate_computer_win_prob(player_card)
    round_result = ""
    betting_done = False
    player_bets = False
    explanation = ""

def resolve_round():
    global player_money, computer_money, round_result, betting_done, explanation
    player_expected = expected_reward(computer_prob)
    computer_expected = expected_reward(player_prob)

    if not player_bets:
        if player_card > computer_card:
            player_money -= computer_expected
            computer_money += computer_expected
            round_result = "No Betting"
            explanation = (
                f"Computer's Money Down: {computer_expected}Won\n"
                f"Computer Win!"
            )
        elif player_card < computer_card:
            loss = int(player_money / 3)
            player_money -= loss
            computer_money += loss
            round_result = "Lose! (not betting)"
            explanation = (
                f"lose money 1/3\n"
                f"lose money {loss}won"
            )
        else:
            round_result = "winlose"
            explanation = "same number"
    else:
        if player_card > computer_card:
            player_money += computer_expected
            computer_money -= computer_expected
            round_result = "Win!"
            explanation = (
                f"Computer's lose : {computer_expected}won\n"
                f"Compueter lose {player_prob}%"
            )
        elif player_card < computer_card:
            player_money -= player_expected
            computer_money += player_expected
            round_result = "Lose!"
            explanation = (
                f"My Money lsoe : {player_expected}won\n"
                f"I lose {computer_prob}%"
            )
        else:
            round_result = "Same"
            explanation = "Same"

    betting_done = True

def draw_ui():
    screen.fill(GREEN)
    screen.blit(font.render(f"Me: {player_money}", True, WHITE), (50, 30))
    screen.blit(font.render(f"Computer: {computer_money}", True, WHITE), (650, 30))

    rounds_left = len(deck) // 2
    screen.blit(small_font.render(f"Round: {rounds_left}", True, WHITE), (380, 30))

    draw_card(300, 250, None if not betting_done else player_card)
    draw_card(500, 250, computer_card)
    screen.blit(font.render("VS", True, WHITE), (430, 290))
    screen.blit(small_font.render(f"%: {player_prob}%", True, WHITE), (650, 200))
    screen.blit(font.render(round_result, True, WHITE), (300, 390))
    for i, line in enumerate(explanation.split("\n")):
        screen.blit(small_font.render(line, True, WHITE), (50, 460 + i * 20))
    if not betting_done:
        return draw_button("Betting", 250, 520, 140, 40, BLUE), draw_button("No Betting", 450, 520, 180, 40, RED)
    else:
        return draw_button("Next", 380, 520, 180, 40, GRAY), None

deal_cards()
running = True
while running:
    buttons = draw_ui()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if buttons:
                if buttons[0].collidepoint(event.pos):
                    if not betting_done:
                        player_bets = True
                        resolve_round()
                    else:
                        deal_cards()
                elif buttons[1] and buttons[1].collidepoint(event.pos):
                    player_bets = False
                    resolve_round()
    pygame.display.flip()
    clock.tick(30)

pygame.quit()
sys.exit()
