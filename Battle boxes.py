import pygame
import random
import math

pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Minimalist RPG")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (200, 200, 200)
PLAYER_COLOR = (0, 128, 255)
ENEMY_COLOR = (255, 0, 0)
WEAPON_COLOR = (0, 255, 0)

# Multiplier colors
COLOR_3X = (255, 0, 0)    # Red
COLOR_6X = (0, 0, 255)    # Blue
COLOR_9X = (0, 200, 0)    # Green
COLOR_12X = (255, 0, 255) # Magenta

# Define initial values as constants
INITIAL_PLAYER_POS = [WIDTH // 2, HEIGHT // 2]
INITIAL_PLAYER_SIZE = 20
INITIAL_PLAYER_SPEED = 1.5
INITIAL_WEAPON_SIZE = [30, 10]
INITIAL_WEAPON_DAMAGE = 5
INITIAL_ENEMY_SIZE = 20
INITIAL_ENEMY_SPEED = 0.5
INITIAL_ENEMY_HEALTH = 10
INITIAL_ENEMY_COUNT = 3
INITIAL_ENEMY_LUCK = 0
INITIAL_PLAYER_LUCK = 0
INITIAL_ENEMY_PROGRESS = {"size": 0, "speed": 0, "health": 0, "count": 0, "luck": 0}
INITIAL_PLAYER_PROGRESS = {"weapon size": 0, "weapon damage": 0, "speed": 0, "luck": 0}
INITIAL_ROUND_NUMBER = 1

# Difficulty increases per round
DIFFICULTY_INCREASES = {
    "speed": 0.1,
    "size": 3,
    "health": 7,
    "count": 1,
    "luck": 10
}

# Player upgrades
UPGRADE_OPTIONS = {
    "weapon size": 5,
    "weapon damage": 2,
    "character speed": 0.1,
    "luck": 10
}

safe_distance = 150  # Minimum distance enemies must spawn from the player

def spawn_enemies(count):
    """Spawn a specific number of enemies ensuring they are far from the player."""
    enemies = []
    for _ in range(count):
        while True:
            x = random.randint(0, WIDTH - enemy_size)
            y = random.randint(0, HEIGHT - enemy_size)
            distance = math.sqrt((x - player_pos[0])**2 + (y - player_pos[1])**2)
            if distance > safe_distance:
                enemies.append({
                    "pos": [x, y],
                    "size": enemy_size,
                    "speed": enemy_speed,
                    "health": enemy_health
                })
                break
    return enemies

def reset_variables():
    global player_pos, player_size, player_speed, weapon_size, weapon_damage
    global weapon_active, weapon_cooldown, enemy_size, enemy_speed, enemy_health, enemy_count, enemy_luck
    global enemy_progress, player_progress, round_number, enemies, player_luck

    player_pos = INITIAL_PLAYER_POS[:]
    player_size = INITIAL_PLAYER_SIZE
    player_speed = INITIAL_PLAYER_SPEED
    weapon_size = INITIAL_WEAPON_SIZE[:]
    weapon_damage = INITIAL_WEAPON_DAMAGE
    weapon_active = False
    weapon_cooldown = 0

    enemy_size = INITIAL_ENEMY_SIZE
    enemy_speed = INITIAL_ENEMY_SPEED
    enemy_health = INITIAL_ENEMY_HEALTH
    enemy_count = INITIAL_ENEMY_COUNT
    enemy_luck = INITIAL_ENEMY_LUCK
    player_luck = INITIAL_PLAYER_LUCK

    enemy_progress = INITIAL_ENEMY_PROGRESS.copy()
    player_progress = INITIAL_PLAYER_PROGRESS.copy()

    round_number = INITIAL_ROUND_NUMBER
    enemies = spawn_enemies(enemy_count)

reset_variables()
clock = pygame.time.Clock()

def draw_stats_box():
    """Draw the stats for player and enemies in a box in the top-right corner."""
    font = pygame.font.Font(None, 24)
    bold_font = pygame.font.Font(None, 26)
    box_width, box_height = 250, 350
    box_x, box_y = WIDTH - box_width - 10, 10
    bar_max_width = box_width - 20

    # Draw the box
    pygame.draw.rect(screen, GREY, (box_x, box_y, box_width, box_height))
    pygame.draw.rect(screen, BLACK, (box_x, box_y, box_width, box_height), 2)

    # Round Number
    screen.blit(bold_font.render(f"Round: {round_number}", True, BLACK), (box_x + 10, box_y + 10))

    # Enemy Stats
    screen.blit(bold_font.render("Enemy Stats:", True, BLACK), (box_x + 10, box_y + 40))
    y_offset = 60

    # Enemy Size
    screen.blit(font.render(f"  Size: {enemy_size}", True, BLACK), (box_x + 10, box_y + y_offset))
    bar_width = int((enemy_progress["size"] / 20) * bar_max_width)
    pygame.draw.rect(screen, (200, 0, 0), (box_x + 10, box_y + y_offset + 15, bar_width, 5))
    y_offset += 25

    # Enemy Speed
    screen.blit(font.render(f"  Speed: {enemy_speed:.1f}", True, BLACK), (box_x + 10, box_y + y_offset))
    bar_width = int((enemy_progress["speed"] / 20) * bar_max_width)
    pygame.draw.rect(screen, (200, 0, 0), (box_x + 10, box_y + y_offset + 15, bar_width, 5))
    y_offset += 25

    # Enemy Health
    screen.blit(font.render(f"  Health: {enemy_health}", True, BLACK), (box_x + 10, box_y + y_offset))
    bar_width = int((enemy_progress["health"] / 20) * bar_max_width)
    pygame.draw.rect(screen, (200, 0, 0), (box_x + 10, box_y + y_offset + 15, bar_width, 5))
    y_offset += 25

    # Enemy Count
    screen.blit(font.render(f"  Count: {enemy_count}", True, BLACK), (box_x + 10, box_y + y_offset))
    bar_width = int((enemy_progress["count"] / 20) * bar_max_width)
    pygame.draw.rect(screen, (200, 0, 0), (box_x + 10, box_y + y_offset + 15, bar_width, 5))
    y_offset += 25

    # Enemy Luck
    screen.blit(font.render(f"  Luck: {enemy_luck}", True, BLACK), (box_x + 10, box_y + y_offset))
    bar_width = int((enemy_progress["luck"] / 20) * bar_max_width)
    pygame.draw.rect(screen, (200, 0, 0), (box_x + 10, box_y + y_offset + 15, bar_width, 5))
    y_offset += 35

    # Player Stats
    screen.blit(bold_font.render("Player Stats:", True, BLACK), (box_x + 10, box_y + y_offset))
    y_offset += 30

    # Player Weapon Size
    screen.blit(font.render(f"  Weapon Size: {weapon_size[0]}", True, BLACK), (box_x + 10, box_y + y_offset))
    bar_width = int((player_progress["weapon size"] / 20) * bar_max_width)
    pygame.draw.rect(screen, (0, 200, 0), (box_x + 10, box_y + y_offset + 15, bar_width, 5))
    y_offset += 30

    # Player Weapon Damage
    screen.blit(font.render(f"  Weapon Damage: {weapon_damage}", True, BLACK), (box_x + 10, box_y + y_offset))
    bar_width = int((player_progress["weapon damage"] / 20) * bar_max_width)
    pygame.draw.rect(screen, (0, 200, 0), (box_x + 10, box_y + y_offset + 15, bar_width, 5))
    y_offset += 30

    # Player Speed (rounded)
    screen.blit(font.render(f"  Speed: {player_speed:.1f}", True, BLACK), (box_x + 10, box_y + y_offset))
    bar_width = int((player_progress["speed"] / 20) * bar_max_width)
    pygame.draw.rect(screen, (0, 200, 0), (box_x + 10, box_y + y_offset + 15, bar_width, 5))
    y_offset += 30

    # Player Luck
    screen.blit(font.render(f"  Luck: {player_luck}", True, BLACK), (box_x + 10, box_y + y_offset))
    bar_width = int((player_progress["luck"] / 20) * bar_max_width)
    pygame.draw.rect(screen, (0, 200, 0), (box_x + 10, box_y + y_offset + 15, bar_width, 5))
    y_offset += 30

def multiplier_chance(luck, base_start, base_chance=20):
    """General helper:
    3x starts at 20% at 0 luck, +10% per 10 luck until 100% at 80 luck
    For others (6x at 90 luck start, 9x at 190, 12x at 290), start at that luck with 10% and +10% per additional 10 luck.

    If base_start = 0, we start at 20% base and go up by 10% per 10 luck until 80 luck =100%.
    If base_start > 0, start at base_start luck with 10% and go up similarly.
    """
    if base_start == 0:
        # This is for 3x
        # 0 luck = 20%, each 10 luck +10%, max 100% at 80 luck
        increments = luck // 10
        chance = base_chance + increments*10
        return min(chance, 100)
    else:
        # For 6x, 9x, 12x etc., at base_start luck =10%, each +10 luck =+10%, max 100%
        if luck < base_start:
            return 0
        diff = luck - base_start
        increments = diff // 10
        chance = 10 + increments*10
        return min(chance, 100)

def roll_player_multipliers(luck):
    """Roll for each multiplier (3x,6x,9x,12x) independently.
    Returns a list of (factor, color, label) for each won multiplier.
    The order we assign them is based on the order we roll them: 3x first, then 6x, then 9x, then 12x.
    """
    # 3x chance:
    chance_3x = multiplier_chance(luck, 0)
    got_3x = (random.random() < (chance_3x/100.0)) if chance_3x > 0 else False

    # 6x chance (starts at 90 luck)
    chance_6x = multiplier_chance(luck, 90)
    got_6x = (random.random() < (chance_6x/100.0)) if chance_6x > 0 else False

    # 9x chance (starts at 190 luck)
    chance_9x = multiplier_chance(luck, 190)
    got_9x = (random.random() < (chance_9x/100.0)) if chance_9x > 0 else False

    # 12x chance (starts at 290 luck)
    chance_12x = multiplier_chance(luck, 290)
    got_12x = (random.random() < (chance_12x/100.0)) if chance_12x > 0 else False

    multipliers = []
    if got_3x:
        multipliers.append((3, COLOR_3X, "3x"))
    if got_6x:
        multipliers.append((6, COLOR_6X, "6x"))
    if got_9x:
        multipliers.append((9, COLOR_9X, "9x"))
    if got_12x:
        multipliers.append((12, COLOR_12X, "12x"))

    return multipliers

def assign_multipliers_to_stats(multipliers):
    """Given a list of multipliers, assign them to distinct stats randomly.
    Stats: 0:"weapon size",1:"weapon damage",2:"character speed",3:"luck"
    Returns a list of tuples: (stat_name, increment, multiplier_factor, color)
    For stats without multiplier, multiplier_factor=1,color=BLACK.
    """
    stats = ["weapon size", "weapon damage", "character speed", "luck"]
    random.shuffle(stats) # To add randomness from scratch.
    # Actually, we need to carefully assign so that each multiplier is on a different stat.
    # We'll pick random distinct stats for each multiplier.

    # Another approach: just pick distinct stats for each multiplier in the order the multipliers were won.
    # We'll shuffle stats first, then assign multipliers one by one to a random remaining stat.
    # Wait, the user didn't specify how to pick the stat for each multiplier exactly, just "randomly".
    # We'll do this: For each multiplier, pick a random stat from the currently available stats (those with no multiplier).
    assigned = [None, None, None, None] # will store (factor, color, label)
    available_indices = [0,1,2,3]

    for (factor, color, label) in multipliers:
        # pick a random available stat
        chosen_index = random.choice(available_indices)
        assigned[chosen_index] = (factor, color, label)
        available_indices.remove(chosen_index)

    # For stats without multipliers:
    for i in range(4):
        if assigned[i] is None:
            assigned[i] = (1, BLACK, "")

    # Combine with increments:
    w_size_inc = UPGRADE_OPTIONS["weapon size"]
    w_dmg_inc = UPGRADE_OPTIONS["weapon damage"]
    c_spd_inc = UPGRADE_OPTIONS["character speed"]
    luck_inc = UPGRADE_OPTIONS["luck"]

    increments = [w_size_inc, w_dmg_inc, c_spd_inc, luck_inc]

    # Now build final structure for display:
    result = []
    for i, stat in enumerate(["weapon size","weapon damage","character speed","luck"]):
        factor, color, label = assigned[i]
        base_inc = increments[i]
        result.append({"stat":stat, "inc":base_inc, "factor":factor, "color":color, "label":label})
    return result

def display_upgrade_options_with_multipliers(assigned_stats):
    """Display the four stats lines with their assigned multipliers.
    assigned_stats: list of dicts: {"stat":..., "inc":..., "factor":..., "color":..., "label":...}
    Player chooses one line to upgrade.
    """
    global weapon_size, weapon_damage, player_speed, player_luck, player_progress

    screen.fill(WHITE)
    font = pygame.font.Font(None, 36)

    lines = []
    # Build text lines
    # Example: "1: Increase Weapon Size (+5)" if no multiplier
    # If multiplier: "1: Increase Weapon Size (+5) x3"
    for i, info in enumerate(assigned_stats):
        base_inc = info["inc"]
        factor = info["factor"]
        color = info["color"]
        label = info["label"]  # "3x","6x","9x","12x" or ""
        stat_name = info["stat"]

        # Format increment line:
        # character speed increments show one decimal
        display_inc = base_inc if stat_name != "character speed" else f"{base_inc:.1f}"
        line_text = f"{i+1}: Increase {stat_name.title()} (+" + str(display_inc) + ")"
        if factor > 1:
            line_text += f" x{factor}"  # ex: x3

        line_render = font.render(line_text, True, color)
        lines.append(line_render)

    # Position lines
    start_y = HEIGHT//2 - 80
    for i, line_render in enumerate(lines):
        screen.blit(line_render, (WIDTH//2 - line_render.get_width()//2, start_y + i*50))

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                choice_map = {pygame.K_1:0, pygame.K_2:1, pygame.K_3:2, pygame.K_4:3}
                if event.key in choice_map:
                    chosen_index = choice_map[event.key]
                    info = assigned_stats[chosen_index]
                    stat = info["stat"]
                    factor = info["factor"]
                    inc = info["inc"]

                    # Apply increment:
                    if stat == "weapon size":
                        weapon_size[0] += inc * factor
                        player_progress["weapon size"] += factor if factor>1 else 1
                    elif stat == "weapon damage":
                        weapon_damage += inc * factor
                        player_progress["weapon damage"] += factor if factor>1 else 1
                    elif stat == "character speed":
                        player_speed += inc * factor
                        player_progress["speed"] += factor if factor>1 else 1
                    elif stat == "luck":
                        # luck increments are integers
                        player_luck += int(inc * factor)
                        player_progress["luck"] += factor if factor>1 else 1

                    waiting = False

def calculate_enemy_multiplier_factor(luck):
    """Determine enemy multiplier factor similarly:
    Enemy uses same roll logic but only applies highest successful multiplier."""
    # Roll multipliers as player:
    # Actually, enemy chooses one stat at random and apply a single multiplier factor (highest available).
    # We'll roll all multipliers, if multiple succeed, choose the highest factor.

    # 3x chance
    chance_3x = multiplier_chance(luck,0)
    got_3x = (random.random()<chance_3x/100.0) if chance_3x>0 else False
    # 6x chance
    chance_6x = multiplier_chance(luck,90)
    got_6x = (random.random()<chance_6x/100.0) if chance_6x>0 else False
    # 9x chance
    chance_9x = multiplier_chance(luck,190)
    got_9x = (random.random()<chance_9x/100.0) if chance_9x>0 else False
    #12x chance
    chance_12x = multiplier_chance(luck,290)
    got_12x = (random.random()<chance_12x/100.0) if chance_12x>0 else False

    factors = []
    if got_3x: factors.append(3)
    if got_6x: factors.append(6)
    if got_9x: factors.append(9)
    if got_12x: factors.append(12)

    if not factors:
        return 1
    else:
        return max(factors)

game_active = True
while game_active:
    running = True
    while running:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_pos[0] > 0:
            player_pos[0] -= player_speed
        if keys[pygame.K_RIGHT] and player_pos[0] < WIDTH - player_size:
            player_pos[0] += player_speed
        if keys[pygame.K_UP] and player_pos[1] > 0:
            player_pos[1] -= player_speed
        if keys[pygame.K_DOWN] and player_pos[1] < HEIGHT - player_size:
            player_pos[1] += player_speed

        # Weapon logic
        if keys[pygame.K_SPACE] and weapon_cooldown == 0:
            weapon_active = True
            weapon_cooldown = 15
        if weapon_cooldown > 0:
            weapon_cooldown -= 1

        # Calculate weapon position relative to the player
        if weapon_active:
            weapon_pos = [player_pos[0] + player_size, player_pos[1] + (player_size // 2 - weapon_size[1] // 2)]
        else:
            weapon_pos = [-100, -100]

        # Enemy movement
        for enemy in enemies:
            if enemy["pos"][0] < player_pos[0]:
                enemy["pos"][0] += enemy["speed"]
            elif enemy["pos"][0] > player_pos[0]:
                enemy["pos"][0] -= enemy["speed"]
            if enemy["pos"][1] < player_pos[1]:
                enemy["pos"][1] += enemy["speed"]
            elif enemy["pos"][1] > player_pos[1]:
                enemy["pos"][1] -= enemy["speed"]

        # Collision detection: player vs enemies
        player_rect = pygame.Rect(*player_pos, player_size, player_size)
        for enemy in enemies:
            enemy_rect = pygame.Rect(*enemy["pos"], enemy["size"], enemy["size"])
            if player_rect.colliderect(enemy_rect):
                running = False

        # Collision detection: weapon vs enemies
        if weapon_active:
            weapon_rect = pygame.Rect(*weapon_pos, *weapon_size)
            for enemy in enemies[:]:
                enemy_rect = pygame.Rect(*enemy["pos"], enemy["size"], enemy["size"])
                if weapon_rect.colliderect(enemy_rect):
                    enemy["health"] -= weapon_damage
                    if enemy["health"] <= 0:
                        enemies.remove(enemy)
            weapon_active = False

        # Check for new round
        if not enemies:
            round_number += 1

            # Roll player multipliers
            player_multipliers = roll_player_multipliers(player_luck)
            # Assign them to stats:
            assigned_stats = assign_multipliers_to_stats(player_multipliers)
            # Display options and let player pick a stat:
            display_upgrade_options_with_multipliers(assigned_stats)

            # Enemy factor:
            enemy_factor = calculate_enemy_multiplier_factor(enemy_luck)
            choice = random.choice(["size", "speed", "health", "count", "luck"])
            enemy_progress[choice] += 1

            increment = DIFFICULTY_INCREASES[choice] * enemy_factor
            if choice == "size":
                enemy_size += increment
            elif choice == "speed":
                enemy_speed += increment
            elif choice == "health":
                enemy_health += increment
            elif choice == "count":
                enemy_count += increment
            elif choice == "luck":
                enemy_luck += increment

            enemies = spawn_enemies(enemy_count)

        # Drawing
        screen.fill(WHITE)
        draw_stats_box()
        pygame.draw.rect(screen, WEAPON_COLOR, (*weapon_pos, *weapon_size))

        # Draw enemies with health bars
        for enemy in enemies:
            pygame.draw.rect(screen, ENEMY_COLOR, (*enemy["pos"], enemy["size"], enemy["size"]))

            health_bar_width = enemy["size"]
            health_bar_height = 5
            health_ratio = max(enemy["health"], 0) / enemy_health
            current_health_width = health_bar_width * health_ratio

            health_bar_x = enemy["pos"][0]
            health_bar_y = enemy["pos"][1] - health_bar_height - 2

            pygame.draw.rect(screen, (150, 150, 150), (health_bar_x, health_bar_y, health_bar_width, health_bar_height))
            pygame.draw.rect(screen, (0, 200, 0), (health_bar_x, health_bar_y, current_health_width, health_bar_height))

        pygame.draw.rect(screen, PLAYER_COLOR, (*player_pos, player_size, player_size))

        pygame.display.flip()

    if not running:
        font = pygame.font.Font(None, 72)
        game_over_text = font.render("GAME OVER", True, BLACK)
        restart_text = pygame.font.Font(None, 36).render("Press R to restart or Q to quit", True, BLACK)

        screen.fill(WHITE)
        screen.blit(game_over_text, (WIDTH//2 - game_over_text.get_width()//2, HEIGHT//2 - 50))
        screen.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2, HEIGHT//2 + 10))
        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    game_active = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        reset_variables()
                        running = True
                        waiting = False
                    elif event.key == pygame.K_q:
                        waiting = False
                        game_active = False

        if running:
            continue
        else:
            break

pygame.quit()