#   Project:     VEXcode EXP UNO - Complete Game Loop (Version 2.3)
#   Author:      VEX
#   Description: Version 2.3 Updates:
#                - Removed unnecessary "START DISCARD" prompt
#                - Startup sequence fixed: Hand -> Incoming Attack Check -> Opponent Played Card
#                - Printed full shuffled deck & starting hand to console
#                - Enforces UNO forced draw (+2 / +4) turn-skip rule
#                - Phase 4 Effects: SoundType.SIREN2 + "UNO!" on second-to-last card
#                - Victory Celebration: SoundType.ALARM2 + "WINNER!" + victory_dance()
        brain.screen.set_fill_color(Color.RED)
        brain.screen.set_pen_color(Color.RED)
        for i in range(40):
            brain.screen.draw_circle(60+i, 42+(i/2), 30)
        brain.screen.set_pen_color(Color.YELLOW)
        for i in range(5):
            brain.screen.draw_line(75, 50+i-5, 85, 50+i-5)
            brain.screen.draw_line(75, 50+i+5, 85, 50+i+5)
            brain.screen.draw_line(75, 50+i+5, 85, 50+i-5)

            brain.screen.draw_line(75, 50+i-15, 85, 50+i-15)
            brain.screen.draw_line(75+(i/2), 50-15, 75+(i/2), 50-25)
            brain.screen.draw_line(83+(i/2), 50-15, 83+(i/2), 50-25)
            brain.screen.draw_line(75, 50+i-25, 85, 50+i-25)

            brain.screen.draw_line(75, 50+i+15, 85, 50+i+15)
            brain.screen.draw_line(83+(i/2), 50+15, 83+(i/2), 50+25)
            brain.screen.draw_line(75, 50+i+25, 85, 50+i+25)

    # Always reset screen colors back to standard default
    brain.screen.set_fill_color(Color.BLACK)
    brain.screen.set_pen_color(Color.WHITE)


def card_to_gfx_args(card_name):
    """
    Translates card text string into (card_str, color_code) tuple
    for draw_card_full_screen().
    """
    parts = card_name.split(" ")
    color_char = parts[0][0] if len(parts) > 1 and parts[0] in ["Red", "Green", "Blue", "Yellow"] else 'N'

    if "Wild" in card_name and "+4" not in card_name:
        return ("W", color_char)
    elif "+4" in card_name:
        return ("D4", color_char)
    
    val = parts[1] if len(parts) > 1 else ""

    if val == "Skip": val = "S"
    elif val == "Reverse": val = "Rv"
    elif val == "+2": val = "D2"

    return (color_char + val, color_char)


def flash_uno_card_back(count=1):
    """
    Flashes the UNO Card Back full-screen 'count' times when drawing cards.
    """
    for _ in range(count):
        draw_card_full_screen("BACK", "N")
        wait(600, MSEC)
        brain.screen.set_fill_color(Color.BLACK)
        brain.screen.clear_screen()
        wait(200, MSEC)

# ==========================================
# PHASE 1: ROBOT MOVEMENT & DANCE FUNCTIONS
# ==========================================

def robot_drive_forward_2():
    """
    Drives forward 2 units to reach center table.
    """
    for _ in range(2):
        FWD.broadcast()
        wait(800, MSEC)


def robot_turn_90_right():
    """
    Executes 90-degree right turn using RT event broadcast.
    """
    RT.broadcast()
    wait(600, MSEC)


def robot_turn_180():
    """
    Executes 180-degree turn around (two 90-degree turns).
    """
    robot_turn_90_right()
    robot_turn_90_right()


def robot_deliver_card(msg="ROBOT DELIVERING"):
    """
    Hides hand, drives 2 units forward to deliver card face-up,
    spins 180 degrees, and returns to player.
    """
    brain.screen.set_fill_color(Color.BLACK)
    brain.screen.set_pen_color(Color.WHITE)
    brain.screen.clear_screen()
    brain.screen.set_cursor(3, 1)
    brain.screen.print(msg[:16])
    robot_drive_forward_2()
    robot_turn_180()
    robot_drive_forward_2()
    robot_turn_180()


def robot_fetch_card():
    """
    Hides hand, drives 2 units forward to draw pile at center,
    spins 180 degrees, and returns to deliver drawn card.
    """
    brain.screen.set_fill_color(Color.BLACK)
    brain.screen.set_pen_color(Color.WHITE)
    brain.screen.clear_screen()
    brain.screen.set_cursor(3, 1)
    brain.screen.print("ROBOT FETCHING"[:16])
    robot_drive_forward_2()
    robot_turn_180()
    robot_drive_forward_2()
    robot_turn_180()


def victory_dance():
    """
    VICTORY CELEBRATION FUNCTION: Plays SoundType.ALARM2, displays "WINNER!",
    and uses motion broadcasts (RT, LT, FWD) to perform a victory dance.
    """
    brain.play_sound(SoundType.ALARM2)
    brain.screen.set_fill_color(Color.BLACK)
    brain.screen.set_pen_color(Color.WHITE)
    brain.screen.clear_screen()
    brain.screen.set_cursor(2, 1)
    brain.screen.print("WINNER!"[:16])
    
    # Motion broadcasts victory dance sequence
    RT.broadcast()
    wait(400, MSEC)
    LT.broadcast()
    wait(400, MSEC)
    LT.broadcast()
    wait(400, MSEC)
    RT.broadcast()
    wait(400, MSEC)
    FWD.broadcast()
    wait(500, MSEC)

# ==========================================
    Checks if player's hand is empty.
    If empty, triggers victory_dance() and returns True to end game loop.
    """
    if len(hand) == 0:
        victory_dance()
        return True
    return False

# ==========================================
# PHASE 4: MENU & SCREEN INTERACTION SYSTEM
# ==========================================

def select_menu_option(header_title, options):
    """
    Standard menu renderer for 5-row x 16-col VEX EXP Screen.
    Controls: buttonLeft, buttonRight, buttonCheck.
    """
    selected_index = 0
    
    while True:
        brain.screen.set_fill_color(Color.BLACK)
        brain.screen.set_pen_color(Color.WHITE)
        brain.screen.set_fill_color(Color.BLACK)
        brain.screen.set_pen_color(Color.WHITE)
def input_discard_pile(prompt_label="OPPONENT PLAYED:"):
    """
    Function to record initial discard or opponent played card.
    Displays graphical card face-up after entry.
    """
    categories = ["Red", "Yellow", "Green", "Blue", "Wild", "+4"]
    chosen_cat = select_menu_option(prompt_label, categories)
    
    if chosen_cat == "Wild":
        chosen_color = select_menu_option("WILD COLOR:", ["Red", "Yellow", "Green", "Blue"])
        card_res = chosen_color + " Wild"
    elif chosen_cat == "+4":
        chosen_color = select_menu_option("+4 COLOR:", ["Red", "Yellow", "Green", "Blue"])
        card_res = chosen_color + " +4"
    else:
        values = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "Skip", "Reverse", "+2"]
        chosen_val = select_menu_option(chosen_cat + " VAL:", values)
        card_res = chosen_cat + " " + chosen_val

    # Render card graphically face-up
    gfx_args = card_to_gfx_args(card_res)
    draw_card_full_screen(gfx_args[0], gfx_args[1])
    wait(1200, MSEC)

    return card_res


def process_player_turn(discard_card, hand, deck):
    """
    Handles turn choices for 'My Turn'.
    - Detects second-to-last card play (1 card remaining): plays SoundType.SIREN2 & displays "UNO!".
    - Detects last card play (0 cards remaining): displays "WINNING CARD!" before victory celebration.
    """
    while True:
        turn_menu_title = "YOUR MOVE:"
        options = ["View Hand", "Play Card", "Draw 1 Card"]

        choice = select_menu_option(turn_menu_title, options)

        # 1. View Hand option
        if choice == "View Hand":
            view_full_hand(hand, discard_card)
            continue

        # 2. Draw 1 Card option
        elif choice == "Draw 1 Card":
            wait(1000, MSEC)

            # PHASE 4 EFFECT & VICTORY CHECKS
            if len(hand) == 1:
                # Second-to-last card play (leaves 1 card in hand)
                brain.play_sound(SoundType.SIREN2)
                robot_deliver_card(msg="UNO!")
            elif len(hand) == 0:
                # Last card played
                robot_deliver_card(msg="FINAL CARD!")
            else:
                robot_deliver_card()

            return played_card


# ==========================================
# MAIN GAME EXECUTION (VERSION 2.3)
# ==========================================

# 1. Initialize deck, shuffle deck, and PRINT SHUFFLED DECK TO CONSOLE
uno_deck = build_uno_deck()
shuffle_deck(uno_deck)
print("=== SHUFFLED DECK ===")
print(uno_deck)

# 2. Deal starting hand and PRINT STARTING HAND TO CONSOLE IMMEDIATELY
player_hand = deal_hand(uno_deck, 7)
print("\n=== STARTING HAND (7 CARDS) ===")
print(player_hand)

print("\n==================================")
print("=== NEW UNO GAME STARTED (v2.3) ===")

# 3. EXACT STARTUP FLOW:
# 3A. Display Starting Hand on Screen
view_full_hand(player_hand, "STARTING HAND")

# 3B. Incoming Attack Check
attack_choice = select_menu_option("INCOMING ATTACK?", ["None", "+2", "+4"])
if attack_choice in ["+2", "+4"]:
    penalty = 2 if attack_choice == "+2" else 4
    flash_uno_card_back(penalty)
    robot_fetch_card()
    for _ in range(penalty):
        drawn = draw_card(uno_deck)
        if drawn:
            player_hand.append(drawn)
    view_full_hand(player_hand, "AFTER ATTACK")

# 3C. Prompt for Opponent's First Played Card (Initial Discard)
discard_top = input_discard_pile("OPPONENT PLAYED:")
print(">>> OPPONENT PLAYED: " + str(discard_top))

# Check if opponent played +2 or +4
if "+2" in discard_top or "+4" in discard_top:
    penalty = 2 if "+2" in discard_top else 4
    select_menu_option("ATTACK! DRAW " + str(penalty), ["Draw " + str(penalty) + " Cards"])
    flash_uno_card_back(penalty)
    robot_fetch_card()
    for _ in range(penalty):
        drawn = draw_card(uno_deck)
        if drawn:
            player_hand.append(drawn)
    discard_top = discard_top.replace("+2", "2").replace("+4", "Wild")
    view_full_hand(player_hand, discard_top)

# 4. Continuous Turn Loop
while True:
    if check_game_over(player_hand):
        break

    # 4A. Player Turn ("My Turn")
    discard_top = process_player_turn(discard_top, player_hand, uno_deck)

    if check_game_over(player_hand):
        break

    # 4B. View remaining hand after robot delivers and returns to player
    view_full_hand(player_hand, discard_top)

    # 4C. Opponent Turn Entry
    print_hand_to_console(player_hand, uno_deck, discard_top)
    discard_top = input_discard_pile("OPPONENT PLAYED:")
    print(">>> OPPONENT PLAYED: " + str(discard_top))

    # 4D. Check if opponent played +2 or +4 against player
    if "+2" in discard_top or "+4" in discard_top:
        penalty = 2 if "+2" in discard_top else 4
        select_menu_option("ATTACK! DRAW " + str(penalty), ["Draw " + str(penalty) + " Cards"])
        flash_uno_card_back(penalty)
        robot_fetch_card()
        for _ in range(penalty):
            drawn = draw_card(uno_deck)
            if drawn:
                player_hand.append(drawn)
        discard_top = discard_top.replace("+2", "2").replace("+4", "Wild")
        view_full_hand(player_hand, discard_top)

print("\nGAME OVER - All cards played!")