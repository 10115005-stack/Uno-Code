#region VEXcode Generated Robot Configuration
from vex import *
import urandom
import math

# Brain should be defined by default
brain = Brain()

# Robot configuration code
brain_inertial = Inertial()
motor_1 = Motor(Ports.PORT1, False)
motor_5 = Motor(Ports.PORT5, True)

# Wait for sensor(s) to fully initialize
wait(100, MSEC)

# Generating and setting random seed
def initializeRandomSeed():
    wait(100, MSEC)
    xaxis = brain_inertial.acceleration(XAXIS) * 1000
    yaxis = brain_inertial.acceleration(YAXIS) * 1000
    zaxis = brain_inertial.acceleration(ZAXIS) * 1000
    systemTime = brain.timer.system() * 100
    urandom.seed(int(xaxis + yaxis + zaxis + systemTime)) 

# Initialize random seed 
initializeRandomSeed()

#endregion VEXcode Generated Robot Configuration
# ------------------------------------------
# 
#   Project:     VEXcode EXP UNO - Version 3.5
#   Author:      VEX
#   Description: - Reverted to Full Graphical UNO Framework.
#                - Calibrated Movement Engine:
#                  * Single Continuous Forward Drive (`FORWARD_DEGREES = 850`).
#                  * Tuned Turn Calibration (`TURN_90_DEGREES = 228`).
#                  * Repositioning Right Alignment (`ALIGN_RIGHT_DEGREES = 12`).
#                - Full House Rules, Attack Handling, Custom Menus & Graphics preserved.
# 
# ------------------------------------------

from vex import *

# ==========================================
# MOVEMENT CALIBRATION & SETUP
# ==========================================

DRIVE_SPEED = 40          # Straight driving percentage speed
TURN_SPEED = 30           # Precise turning percentage speed
FORWARD_DEGREES = 850     # Single continuous forward motion distance
TURN_90_DEGREES = 228     # Standard 90-degree turn calibration
ALIGN_RIGHT_DEGREES = 12  # Fine-tuned right adjustment during 180° turns/repositioning

def configure_motors():
    motor_1.set_stopping(HOLD)
    motor_5.set_stopping(HOLD)
    motor_1.set_velocity(DRIVE_SPEED, PERCENT)
    motor_5.set_velocity(DRIVE_SPEED, PERCENT)

configure_motors()

# ==========================================
# GLOBAL CUSTOM RULES CONFIGURATION
# ==========================================

custom_rules = {
    "stack_similar": False,        # Automatically play matching rank cards together
    "stack_draw2": False,          # Automatically stack +2 when attacked with a +2
    "draw_until_playable": False   # Stay at center drawing cards until finding a playable card
}


def setup_custom_rules_menu():
    """
    Rules Menu: Displays options in RED when OFF and GREEN when ON.
    Rule options: "Stack Similar", "Stack +2s", "Draw Till Play"
    """
    rule_keys = ["stack_similar", "stack_draw2", "draw_until_playable"]
    rule_names = ["Stack Similar", "Stack +2s", "Draw Till Play"]
    
    current_idx = 0
    
    while True:
        brain.screen.set_fill_color(Color.BLACK)
        brain.screen.clear_screen()
        
        brain.screen.set_cursor(1, 1)
        brain.screen.set_pen_color(Color.WHITE)
        brain.screen.print("CUSTOM RULES MENU"[:16])
        
        brain.screen.set_cursor(3, 1)
        
        if current_idx < len(rule_keys):
            key = rule_keys[current_idx]
            is_on = custom_rules[key]
            status = "ON" if is_on else "OFF"
            
            if is_on:
                brain.screen.set_pen_color(Color.GREEN)
            else:
                brain.screen.set_pen_color(Color.RED)
                
            opt_str = rule_names[current_idx] + ":" + status
            brain.screen.print(("< " + opt_str + " >")[:16])
            
            brain.screen.set_pen_color(Color.WHITE)
            brain.screen.set_cursor(5, 1)
            brain.screen.print("[L/R]Sel [v]Toggle"[:16])
        else:
            brain.screen.set_pen_color(Color.GREEN)
            brain.screen.print("< Done >"[:16])
            
            brain.screen.set_pen_color(Color.WHITE)
            brain.screen.set_cursor(5, 1)
            brain.screen.print("[L/R]Sel [v]Confirm"[:16])
            
        while not (brain.buttonLeft.pressing() or brain.buttonRight.pressing() or brain.buttonCheck.pressing()):
            wait(20, MSEC)
            
        if brain.buttonLeft.pressing():
            current_idx = (current_idx - 1) % (len(rule_keys) + 1)
            while brain.buttonLeft.pressing():
                wait(20, MSEC)
        elif brain.buttonRight.pressing():
            current_idx = (current_idx + 1) % (len(rule_keys) + 1)
            while brain.buttonRight.pressing():
                wait(20, MSEC)
        elif brain.buttonCheck.pressing():
            while brain.buttonCheck.pressing():
                wait(20, MSEC)
            if current_idx == len(rule_keys):
                break
            else:
                key = rule_keys[current_idx]
                custom_rules[key] = not custom_rules[key]


def start_main_menu():
    """
    Startup main menu allowing players to enter Rules or Play Game.
    """
    while True:
        choice = select_menu_option("UNO MAIN MENU", ["Play Game", "Rules"])
        if choice == "Rules":
            setup_custom_rules_menu()
        elif choice == "Play Game":
            break

# ==========================================
# COLOR HELPER & GRAPHICAL CARD RENDERER
# ==========================================

def set_color_by_card(card_name):
    if "Red" in card_name:
        brain.screen.set_pen_color(Color.RED)
    elif "Green" in card_name:
        brain.screen.set_pen_color(Color.GREEN)
    elif "Blue" in card_name:
        brain.screen.set_pen_color(Color.BLUE)
    elif "Yellow" in card_name:
        brain.screen.set_pen_color(Color.YELLOW)
    else:
        brain.screen.set_pen_color(Color.WHITE)


def draw_card_full_screen(card_str, color_code):
    brain.screen.clear_screen()
    if color_code == 'R': brain.screen.set_fill_color(Color.RED)
    elif color_code == 'G': brain.screen.set_fill_color(Color.GREEN)
    elif color_code == 'B': brain.screen.set_fill_color(Color.BLUE)
    elif color_code == 'Y': brain.screen.set_fill_color(Color.YELLOW)
    else: brain.screen.set_fill_color(Color.BLACK)
    brain.screen.set_pen_color(Color.WHITE)
    for i in range(5):
        brain.screen.draw_rectangle(0+i, 0+i, 159-(i*2), 107-(i*2))
   
    card = card_str[1:]
    if card == "0":
        for i in range(15):
            brain.screen.draw_rectangle(20+i, 20+i, 119-(i*2), 67-(i*2))
    elif card == "8":
        for i in range(15):
            brain.screen.draw_rectangle(20+i, 20+i, 119-(i*2), 67-(i*2))
        for i in range(15):
            brain.screen.draw_line(72+i, 20, 72+i, 85)
    elif card == "1":
        for i in range(15):
            brain.screen.draw_line(20, 47+i, 139, 47+i)
    elif card == "3":
        for i in range(15):
            brain.screen.draw_line(20, 20+i, 139, 20+i)
            brain.screen.draw_line(20+i, 20, 20+i, 87)
            brain.screen.draw_line(72+i, 20, 72+i, 87)
            brain.screen.draw_line(125+i, 20, 125+i, 87)
    elif card == "2":
        for i in range(15):
            brain.screen.draw_line(20+i, 20, 20+i, 87)
            brain.screen.draw_line(20, 20+i, 72, 20+i)
            brain.screen.draw_line(72+i, 20, 72+i, 87)
            brain.screen.draw_line(72, 73+i, 139, 73+i)
            brain.screen.draw_line(125+i, 20, 125+i, 87)
        for i in range(3):
            brain.screen.draw_line(145+i, 20, 145+i, 87)
    elif card == "5":
        for i in range(15):
            brain.screen.draw_line(20+i, 20, 20+i, 87)
            brain.screen.draw_line(20, 73+i, 72, 73+i)
            brain.screen.draw_line(72+i, 20, 72+i, 87)
            brain.screen.draw_line(72, 20+i, 139, 20+i)
            brain.screen.draw_line(125+i, 20, 125+i, 87)
        for i in range(3):
            brain.screen.draw_line(145+i, 20, 145+i, 87)
    elif card == "6":
        for i in range(15):
            brain.screen.draw_line(20+i, 20, 20+i, 87)
            brain.screen.draw_line(20, 73+i, 72, 73+i)
            brain.screen.draw_line(72+i, 20, 72+i, 87)
            brain.screen.draw_line(72, 20+i, 139, 20+i)
            brain.screen.draw_line(125+i, 20, 125+i, 87)
            brain.screen.draw_line(72, 73+i, 139, 73+i)
        for i in range(3):
            brain.screen.draw_line(145+i, 20, 145+i, 87)
    elif card == "9":
        for i in range(15):
            brain.screen.draw_line(20+i, 20, 20+i, 87)
            brain.screen.draw_line(20, 20+i, 72, 20+i)
            brain.screen.draw_line(20, 73+i, 72, 73+i)
            brain.screen.draw_line(72+i, 20, 72+i, 87)
            brain.screen.draw_line(72, 20+i, 139, 20+i)
            brain.screen.draw_line(125+i, 20, 125+i, 87)
        for i in range(3):
            brain.screen.draw_line(145+i, 20, 145+i, 87)
    elif card == "4" and "D" not in card_str:
        for i in range(15):
            brain.screen.draw_line(20, 20+i, 72, 20+i)
            brain.screen.draw_line(20, 73+i, 72, 73+i)
            brain.screen.draw_line(72+i, 20, 72+i, 87)
            brain.screen.draw_line(72, 20+i, 139, 20+i)
    elif card == "7":
        for i in range(15):
            brain.screen.draw_line(20, 20+i, 139, 20+i)
            brain.screen.draw_line(20+i, 20, 20+i, 87)
    elif card == "Rv":
        for i in range(15):
            brain.screen.draw_line(62+i, 30, 62+i, 87)
            brain.screen.draw_line(69, 20, 52+i, 40)
            brain.screen.draw_line(69, 20, 82-i, 40)
            brain.screen.draw_line(82+i, 20, 82+i, 77)
            brain.screen.draw_line(89, 87, 74+i, 67)
            brain.screen.draw_line(89, 87, 104-i, 67)
    elif card == "S":
        for i in range(15):
            brain.screen.draw_rectangle(40+i, 20+i, 82-(i*2), 67-(i*2))
        for i in range(15):
            brain.screen.draw_line(52+i, 20, 92+i, 80)
    elif card == "D2":
        brain.screen.set_fill_color(Color.WHITE)
        for i in range(40):
            brain.screen.draw_circle(60+i, 42+(i/2), 30)
        if color_code == 'R': brain.screen.set_fill_color(Color.RED)
        elif color_code == 'G': brain.screen.set_fill_color(Color.GREEN)
        elif color_code == 'B': brain.screen.set_fill_color(Color.BLUE)
        elif color_code == 'Y': brain.screen.set_fill_color(Color.YELLOW)
        brain.screen.draw_rectangle(47, 32, 40, 25)
        brain.screen.draw_rectangle(73, 52, 40, 25)
        for i in range(5):
            brain.screen.draw_line(18+i, 85, 18+i, 95)
            brain.screen.draw_line(14, 88+i, 26, 88+i)
            brain.screen.draw_line(10+i, 66, 10+i, 79)
            brain.screen.draw_line(10, 66+i, 20, 66+i)
            brain.screen.draw_line(18+i, 66, 18+i, 79)
            brain.screen.draw_line(20, 75+i, 30, 75+i)
            brain.screen.draw_line(26+i, 66, 26+i, 79)

            brain.screen.draw_line(159-18-i, 107-85, 159-18-i, 107-95)
            brain.screen.draw_line(159-14, 107-88-i, 159-26, 107-88-i)
            brain.screen.draw_line(159-10-i, 107-66, 159-10-i, 107-79)
            brain.screen.draw_line(159-10, 107-66-i, 159-20, 107-66-i)
            brain.screen.draw_line(159-18-i, 107-66, 159-18-i, 107-79)
            brain.screen.draw_line(159-20, 107-75-i, 159-30, 107-75-i)
            brain.screen.draw_line(159-26-i, 107-66, 159-26-i, 107-79)
    elif card_str == "W":
        brain.screen.set_fill_color(Color.BLUE)
        brain.screen.draw_rectangle(50, 20, 30, 32)
        brain.screen.set_fill_color(Color.RED)
        brain.screen.draw_rectangle(50, 52, 30, 32)
        brain.screen.set_fill_color(Color.GREEN)
        brain.screen.draw_rectangle(80, 20, 30, 32)
        brain.screen.set_fill_color(Color.YELLOW)
        brain.screen.draw_rectangle(80, 52, 30, 32)
        brain.screen.set_fill_color(Color.TRANSPARENT)
        brain.screen.set_pen_width(3)
        for i in range(15):
            brain.screen.draw_circle(80, 52, 30-(i/5))
        brain.screen.set_pen_color(Color.BLACK)
        for i in range(65):
            brain.screen.draw_circle(80, 52, 31+(i/5))
        brain.screen.set_pen_width(1)
    elif card_str == "D4":
        brain.screen.set_fill_color(Color.YELLOW)
        brain.screen.draw_rectangle(78, 42, 40, 25)
        brain.screen.set_fill_color(Color.GREEN)
        brain.screen.draw_rectangle(60, 28, 40, 25)
        brain.screen.set_fill_color(Color.BLUE)
        brain.screen.draw_rectangle(42, 42, 40, 25)
        brain.screen.set_fill_color(Color.RED)
        brain.screen.draw_rectangle(60, 56, 40, 25)
        for i in range(5):
            brain.screen.draw_line(18+i, 85, 18+i, 95)
            brain.screen.draw_line(14, 88+i, 26, 88+i)
            brain.screen.draw_line(10, 75+i, 20, 75+i)
            brain.screen.draw_line(16+i, 75, 16+i, 66)
            brain.screen.draw_line(10, 66+i, 30, 66+i)

            brain.screen.draw_line(159-18-i, 107-85, 159-18-i, 107-95)
            brain.screen.draw_line(159-14, 107-88-i, 159-26, 107-88-i)
            brain.screen.draw_line(159-10, 107-75-i, 159-20, 107-75-i)
            brain.screen.draw_line(159-16-i, 107-75, 159-16-i, 107-66)
            brain.screen.draw_line(159-10, 107-66-i, 159-30, 107-66-i)
    else:
        # UNO Card Back Display
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

    brain.screen.set_fill_color(Color.BLACK)
    brain.screen.set_pen_color(Color.WHITE)


def card_to_gfx_args(card_name):
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
    for _ in range(count):
        draw_card_full_screen("BACK", "N")
        wait(600, MSEC)
        brain.screen.set_fill_color(Color.BLACK)
        brain.screen.clear_screen()
        wait(200, MSEC)

# ==========================================
# HIGH-PRECISION ROBOT MOVEMENT FUNCTIONS
# ==========================================

def robot_drive_forward_2():
    """
    Drives forward in a single continuous smooth motion (850 degrees).
    """
    motor_1.set_velocity(DRIVE_SPEED, PERCENT)
    motor_5.set_velocity(DRIVE_SPEED, PERCENT)
    
    motor_1.spin_for(FORWARD, FORWARD_DEGREES, DEGREES, False)
    motor_5.spin_for(FORWARD, FORWARD_DEGREES, DEGREES, True)
    wait(150, MSEC)


def robot_turn_90_right():
    """
    Executes a right turn using calibrated rotation angles (228°).
    """
    motor_1.set_velocity(TURN_SPEED, PERCENT)
    motor_5.set_velocity(TURN_SPEED, PERCENT)
    
    motor_1.spin_for(FORWARD, TURN_90_DEGREES, DEGREES, False)
    motor_5.spin_for(REVERSE, TURN_90_DEGREES, DEGREES, True)
    wait(150, MSEC)
    
    motor_1.set_velocity(DRIVE_SPEED, PERCENT)
    motor_5.set_velocity(DRIVE_SPEED, PERCENT)


def robot_turn_180():
    """
    Executes a full 180° turn with a 12° micro-correction right adjustment.
    """
    robot_turn_90_right()
    wait(100, MSEC)
    robot_turn_90_right()
    wait(100, MSEC)
    
    if ALIGN_RIGHT_DEGREES > 0:
        motor_1.set_velocity(TURN_SPEED, PERCENT)
        motor_5.set_velocity(TURN_SPEED, PERCENT)
        motor_1.spin_for(FORWARD, ALIGN_RIGHT_DEGREES, DEGREES, False)
        motor_5.spin_for(REVERSE, ALIGN_RIGHT_DEGREES, DEGREES, True)
        wait(100, MSEC)
    
    motor_1.set_velocity(DRIVE_SPEED, PERCENT)
    motor_5.set_velocity(DRIVE_SPEED, PERCENT)


def robot_deliver_card(played_card, is_uno=False, is_final=False):
    gfx_args = card_to_gfx_args(played_card)
    draw_card_full_screen(gfx_args[0], gfx_args[1])

    if is_uno:
        brain.play_sound(SoundType.SIREN2)
        brain.screen.set_cursor(1, 1)
        brain.screen.set_pen_color(Color.WHITE)
        brain.screen.set_fill_color(Color.BLACK)
        brain.screen.print("     UNO!     ")
    elif is_final:
        brain.screen.set_cursor(1, 1)
        brain.screen.set_pen_color(Color.WHITE)
        brain.screen.set_fill_color(Color.BLACK)
        brain.screen.print("  FINAL CARD! ")

    robot_drive_forward_2()
    robot_turn_180()

    brain.screen.set_fill_color(Color.BLACK)
    brain.screen.clear_screen()

    robot_drive_forward_2()
    robot_turn_180()

    brain.screen.set_fill_color(Color.BLACK)
    brain.screen.set_pen_color(Color.WHITE)
    brain.screen.clear_screen()
    brain.screen.set_cursor(3, 1)
    brain.screen.print("  CARD PLAYED   ")
    wait(1000, MSEC)


def robot_fetch_card(count=1):
    brain.screen.set_fill_color(Color.BLACK)
    brain.screen.clear_screen()
    robot_drive_forward_2()

    flash_uno_card_back(count)

    robot_turn_180()

    brain.screen.set_fill_color(Color.BLACK)
    brain.screen.clear_screen()
    robot_drive_forward_2()
    robot_turn_180()

    brain.screen.set_fill_color(Color.BLACK)
    brain.screen.set_pen_color(Color.WHITE)
    brain.screen.clear_screen()
    brain.screen.set_cursor(3, 1)
    brain.screen.print("   CARD ADDED   ")
    wait(1000, MSEC)


def robot_fetch_until_playable(hand, deck, top_card):
    brain.screen.set_fill_color(Color.BLACK)
    brain.screen.clear_screen()
    robot_drive_forward_2()

    drawn_count = 0
    while True:
        drawn = draw_card(deck)
        if not drawn:
            break
        hand.append(drawn)
        drawn_count += 1
        flash_uno_card_back(1)
        print(">>> DRAW TILL PLAYABLE DREW: " + drawn)

        legal = get_legal_moves(hand, top_card)
        if legal:
            break

    robot_turn_180()

    brain.screen.set_fill_color(Color.BLACK)
    brain.screen.clear_screen()
    robot_drive_forward_2()
    robot_turn_180()

    brain.screen.set_fill_color(Color.BLACK)
    brain.screen.set_pen_color(Color.WHITE)
    brain.screen.clear_screen()
    brain.screen.set_cursor(3, 1)
    msg = str(drawn_count) + " CARDS DREW"
    brain.screen.print(msg[:16])
    wait(1200, MSEC)


def victory_dance():
    brain.play_sound(SoundType.ALARM2)
    brain.screen.set_fill_color(Color.BLACK)
    brain.screen.set_pen_color(Color.WHITE)
    brain.screen.clear_screen()
    brain.screen.set_cursor(2, 1)
    brain.screen.print("WINNER!"[:16])
    
    robot_turn_90_right()
    robot_turn_90_right()
    robot_drive_forward_2()

# ==========================================
# PHASE 2: DECK & HAND CORE
# ==========================================

def build_uno_deck():
    colors = ["Red", "Yellow", "Green", "Blue"]
    action_cards = ["Skip", "Reverse", "+2"]
    deck = []
    
    for color in colors:
        deck.append(color + " 0")
        for num in range(1, 10):
            deck.append(color + " " + str(num))
            deck.append(color + " " + str(num))
        for action in action_cards:
            deck.append(color + " " + action)
            deck.append(color + " " + action)
            
    for _ in range(4):
        deck.append("Wild")
        deck.append("+4")
        
    return deck

def shuffle_deck(deck):
    for i in range(len(deck) - 1, 0, -1):
        j = urandom.randint(0, i)
        deck[i], deck[j] = deck[j], deck[i]

def draw_card(deck):
    if len(deck) > 0:
        return deck.pop(0)
    return None

def deal_hand(deck, hand_size=7):
    hand = []
    for _ in range(hand_size):
        card = draw_card(deck)
        if card:
            hand.append(card)
    return hand

def abbreviate_card(card):
    if card == "Wild":
        return "WLD"
    if card == "+4":
        return "W+4"
    
    parts = card.split(" ")
    if len(parts) == 2:
        color_code = parts[0][0]
        value = parts[1]
        if value == "Skip":
            value = "SK"
        elif value == "Reverse":
            value = "RV"
        return color_code + value
    return card[:4]

def get_card_rank(card_str):
    parts = card_str.split(" ")
    if len(parts) > 1:
        return parts[1]
    return parts[0]

def print_hand_to_console(hand, deck, current_top):
    print("\n--------------------------------------------------")
    print("TOP CARD: " + str(current_top) + " | DECK REMAINING: " + str(len(deck)))
    formatted = " | ".join("[" + str(i + 1) + "] " + card for i, card in enumerate(hand))
    print("YOUR HAND (" + str(len(hand)) + "): " + formatted)
    print("--------------------------------------------------\n")

# ==========================================
# PHASE 3: GAME STATE & RULE FUNCTIONS
# ==========================================

def get_legal_moves(hand, top_card):
    legal_indices = []
    top_parts = top_card.split(" ")
    top_color = top_parts[0] if len(top_parts) > 0 else ""
    top_val = top_parts[1] if len(top_parts) > 1 else top_parts[0]

    for idx, card in enumerate(hand):
        if "Wild" in card or "+4" in card:
            legal_indices.append(idx)
        else:
            card_parts = card.split(" ")
            card_color = card_parts[0] if len(card_parts) > 0 else ""
            card_val = card_parts[1] if len(card_parts) > 1 else card_parts[0]

            if card_color == top_color or card_val == top_val:
                legal_indices.append(idx)

    return legal_indices


def check_game_over(hand):
    if len(hand) == 0:
        victory_dance()
        return True
    return False

# ==========================================
# PHASE 4: MENU & SCREEN INTERACTION SYSTEM
# ==========================================

def select_menu_option(header_title, options, option_color=Color.GREEN):
    selected_index = 0
    
    while True:
        brain.screen.set_fill_color(Color.BLACK)
        brain.screen.set_pen_color(Color.WHITE)
        brain.screen.clear_screen()
        
        brain.screen.set_cursor(1, 1)
        brain.screen.print(header_title[:16])
        
        brain.screen.set_cursor(3, 1)
        brain.screen.set_pen_color(option_color)
        opt_text = "< " + str(options[selected_index]) + " >"
        brain.screen.print(opt_text[:16])
        
        brain.screen.set_pen_color(Color.WHITE)
        brain.screen.set_cursor(5, 1)
        brain.screen.print("[L/R]Sel  [v]OK"[:16])
        
        while not (brain.buttonLeft.pressing() or brain.buttonRight.pressing() or brain.buttonCheck.pressing()):
            wait(20, MSEC)
            
        if brain.buttonLeft.pressing():
            selected_index = (selected_index - 1) % len(options)
            while brain.buttonLeft.pressing():
                wait(20, MSEC)
        elif brain.buttonRight.pressing():
            selected_index = (selected_index + 1) % len(options)
            while brain.buttonRight.pressing():
                wait(20, MSEC)
        elif brain.buttonCheck.pressing():
            while brain.buttonCheck.pressing():
                wait(20, MSEC)
            return options[selected_index]


def select_menu_option_indexed(header_title, options, option_color=Color.GREEN):
    selected_index = 0
    
    while True:
        brain.screen.set_fill_color(Color.BLACK)
        brain.screen.set_pen_color(Color.WHITE)
        brain.screen.clear_screen()
        
        brain.screen.set_cursor(1, 1)
        brain.screen.print(header_title[:16])
        
        brain.screen.set_cursor(3, 1)
        brain.screen.set_pen_color(option_color)
        opt_text = "< " + str(options[selected_index]) + " >"
        brain.screen.print(opt_text[:16])
        
        brain.screen.set_pen_color(Color.WHITE)
        brain.screen.set_cursor(5, 1)
        brain.screen.print("[L/R]Sel  [v]OK"[:16])
        
        while not (brain.buttonLeft.pressing() or brain.buttonRight.pressing() or brain.buttonCheck.pressing()):
            wait(20, MSEC)
            
        if brain.buttonLeft.pressing():
            selected_index = (selected_index - 1) % len(options)
            while brain.buttonLeft.pressing():
                wait(20, MSEC)
        elif brain.buttonRight.pressing():
            selected_index = (selected_index + 1) % len(options)
            while brain.buttonRight.pressing():
                wait(20, MSEC)
        elif brain.buttonCheck.pressing():
            while brain.buttonCheck.pressing():
                wait(20, MSEC)
            return (selected_index, options[selected_index])


def view_full_hand(hand):
    page = 0
    while True:
        max_page = (len(hand) - 1) // 8 if len(hand) > 0 else 0
        if page > max_page:
            page = max_page

        brain.screen.set_fill_color(Color.BLACK)
        brain.screen.clear_screen()
        
        slots = [[1, 1], [1, 9], [2, 1], [2, 9], [3, 1], [3, 9], [4, 1], [4, 9]]
        start_idx = page * 8
        end_idx = min(start_idx + 8, len(hand))
        
        if not hand:
            brain.screen.set_pen_color(Color.WHITE)
            brain.screen.set_cursor(3, 1)
            brain.screen.print("(HAND EMPTY)"[:16])
        else:
            for i in range(start_idx, end_idx):
                slot = slots[i - start_idx]
                card_item = hand[i]
                set_color_by_card(card_item)
                
                brain.screen.set_cursor(slot[0], slot[1])
                lbl = str(i + 1) + ":" + abbreviate_card(card_item)
                brain.screen.print(lbl[:7])
                
        brain.screen.set_pen_color(Color.WHITE)
        brain.screen.set_cursor(5, 1)
        if max_page > 0:
            brain.screen.print("[L/R]Pg  [v]OK"[:16])
        else:
            brain.screen.print("   [v] Continue"[:16])
            
        while not (brain.buttonLeft.pressing() or brain.buttonRight.pressing() or brain.buttonCheck.pressing()):
            wait(20, MSEC)
            
        if brain.buttonCheck.pressing():
            while brain.buttonCheck.pressing():
                wait(20, MSEC)
            break
        elif brain.buttonLeft.pressing() and max_page > 0:
            page = (page - 1) % (max_page + 1)
            while brain.buttonLeft.pressing():
                wait(20, MSEC)
        elif brain.buttonRight.pressing() and max_page > 0:
            page = (page + 1) % (max_page + 1)
            while brain.buttonRight.pressing():
                wait(20, MSEC)


def input_top_card():
    chosen_color = select_menu_option("TOP CARD COLOR:", ["Red", "Yellow", "Green", "Blue", "Wild"])
    
    if chosen_color == "Wild":
        wild_type = select_menu_option("WILD TYPE:", ["Wild", "+4"])
        if wild_type == "+4":
            eff_color = select_menu_option("EFFECT COLOR:", ["Red", "Yellow", "Green", "Blue"])
            card_res = eff_color + " +4"
        else:
            eff_color = select_menu_option("EFFECT COLOR:", ["Red", "Yellow", "Green", "Blue"])
            card_res = eff_color + " Wild"
    else:
        values = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "Skip", "Reverse", "+2"]
        chosen_val = select_menu_option("TOP CARD VALUE:", values)
        card_res = chosen_color + " " + chosen_val

    return card_res


def handle_draw_action(hand, deck, top_card):
    if custom_rules["draw_until_playable"]:
        robot_fetch_until_playable(hand, deck, top_card)
    else:
        robot_fetch_card(count=1)
        drawn = draw_card(deck)
        if drawn:
            hand.append(drawn)
            print(">>> YOU DREW: " + drawn)
        else:
            select_menu_option("DECK EMPTY!", ["No Cards Left"])


def process_player_turn(discard_card, hand, deck):
    while True:
        turn_menu_title = "YOUR MOVE:"
        options = ["Play Card", "Draw 1 Card", "View Hand"]

        choice = select_menu_option(turn_menu_title, options)

        if choice == "Play Card":
            legal_indices = get_legal_moves(hand, discard_card)

            if not legal_indices:
                select_menu_option("NO LEGAL MOVES!", ["Draw Cards"])
                handle_draw_action(hand, deck, discard_card)
                return discard_card

            hand_options = ["Back"]
            for idx in legal_indices:
                card = hand[idx]
                hand_options.append(abbreviate_card(card))

            select_header = "Select Move"
            sel_idx, selected_str = select_menu_option_indexed(select_header, hand_options)

            if selected_str == "Back" or sel_idx == 0:
                continue

            card_idx = legal_indices[sel_idx - 1]
            played_card = hand.pop(card_idx)

            if "Wild" in played_card or "+4" in played_card:
                chosen_color = select_menu_option("CHOOSE COLOR:", ["Red", "Yellow", "Green", "Blue"])
                if "+4" in played_card:
                    played_card = chosen_color + " +4"
                else:
                    played_card = chosen_color + " Wild"

            print(">>> YOU PLAYED: " + played_card)

            if custom_rules["stack_similar"]:
                played_rank = get_card_rank(played_card)
                matching_indices = [i for i, c in enumerate(hand) if get_card_rank(c) == played_rank]
                
                if matching_indices:
                    for m_idx in sorted(matching_indices, reverse=True):
                        stacked_card = hand.pop(m_idx)
                        print(">>> AUTO STACKED MATCH PLAYED: " + stacked_card)

            if len(hand) == 1:
                robot_deliver_card(played_card, is_uno=True)
            elif len(hand) == 0:
                robot_deliver_card(played_card, is_final=True)
            else:
                robot_deliver_card(played_card)

            return played_card

        elif choice == "Draw 1 Card":
            handle_draw_action(hand, deck, discard_card)
            return discard_card

        elif choice == "View Hand":
            view_full_hand(hand)
            continue


# ==========================================
# MAIN GAME EXECUTION (VERSION 3.5)
# ==========================================

uno_deck = build_uno_deck()
shuffle_deck(uno_deck)
print("=== SHUFFLED DECK ===")
print(uno_deck)

player_hand = deal_hand(uno_deck, 7)
print("\n=== STARTING HAND (7 CARDS) ===")
print(player_hand)

print("\n==================================")
print("=== NEW UNO GAME STARTED (v3.5) ===")

start_main_menu()

while True:
    if check_game_over(player_hand):
        break

    view_full_hand(player_hand)

    attack_choice = select_menu_option("INCOMING ATTACK?", ["None", "Draw 2", "Draw 4"])
    if attack_choice != "None":
        penalty = 2 if attack_choice == "Draw 2" else 4
        
        if attack_choice == "Draw 2" and custom_rules["stack_draw2"]:
            plus2_indices = [i for i, c in enumerate(player_hand) if "+2" in c]
            if plus2_indices:
                plus2_idx = plus2_indices[0]
                played_2 = player_hand.pop(plus2_idx)
                print(">>> AUTO STACKED +2 PLAYED: " + played_2)
                
                brain.screen.set_fill_color(Color.BLACK)
                brain.screen.set_pen_color(Color.GREEN)
                brain.screen.clear_screen()
                brain.screen.set_cursor(3, 1)
                brain.screen.print("   STACKED +2!   ")
                wait(1000, MSEC)
                
                robot_deliver_card(played_2)
                penalty = 0
            else:
                brain.screen.set_fill_color(Color.BLACK)
                brain.screen.set_pen_color(Color.RED)
                brain.screen.clear_screen()
                brain.screen.set_cursor(3, 1)
                brain.screen.print("   TOOK CARDS   ")
                wait(1000, MSEC)
                
        if penalty > 0:
            robot_fetch_card(count=penalty)
            for _ in range(penalty):
                drawn = draw_card(uno_deck)
                if drawn:
                    player_hand.append(drawn)
            view_full_hand(player_hand)

        continue

    discard_top = input_top_card()
    print_hand_to_console(player_hand, uno_deck, discard_top)

    discard_top = process_player_turn(discard_top, player_hand, uno_deck)

    if check_game_over(player_hand):
        break

print("\nGAME OVER - All cards played!")