from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import random
import time

# GAME CONSTANTS
MAZE_SIZE     = 15
CELL_SIZE     = 40
WALL_HEIGHT   = 38
PLAYER_HEIGHT = 20

#ZONE DEFINITIONS
# Split that into 4 quadrants:
#   Zone 0 (top-left)     : cols 1-6,  rows 1-6
#   Zone 1 (top-right)    : cols 7-13, rows 1-6
#   Zone 2 (bottom-left)  : cols 1-6,  rows 7-13
#   Zone 3 (bottom-right) : cols 7-13, rows 7-13
# Enemy zone field (index 8):  0-3 = locked to that quadrant, -1 = free roam

ZONE_BOUNDS = {
    0: (1, 6,  1, 6),   # (col_min, col_max, row_min, row_max)
    1: (7, 13, 1, 6),
    2: (1, 6,  7, 13),
    3: (7, 13, 7, 13),
}

def in_zone(mx, mz, zone_id):
    """Return True if maze cell (mx, mz) is inside the given zone."""
    col_min, col_max, row_min, row_max = ZONE_BOUNDS[zone_id]
    return col_min <= mx <= col_max and row_min <= mz <= row_max

def clamp_to_zone(mx, mz, zone_id):
    """Return the nearest in-zone cell to (mx, mz)."""
    col_min, col_max, row_min, row_max = ZONE_BOUNDS[zone_id]
    return (max(col_min, min(col_max, mx)),
            max(row_min, min(row_max, mz)))

# THREE MAZES walls (1) and paths (0) only.
maze_level1 = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,1,0,0,0,0,0,1,0,0,0,1],
    [1,0,1,0,1,0,1,1,1,0,1,0,1,0,1],
    [1,0,1,0,0,0,1,0,0,0,0,0,1,0,1],
    [1,0,1,1,1,0,1,0,1,1,1,0,1,0,1],
    [1,0,0,0,0,0,1,0,0,0,1,0,0,0,1],
    [1,1,1,0,1,0,0,0,1,0,1,1,1,0,1],
    [1,0,0,0,1,0,1,0,1,0,0,0,0,0,1],
    [1,0,1,0,1,0,1,0,1,1,1,0,1,0,1],
    [1,0,1,0,0,0,1,0,0,0,0,0,1,0,1],
    [1,0,1,1,1,0,1,1,1,0,1,0,1,0,1],
    [1,0,0,0,0,0,0,0,0,0,1,0,0,0,1],
    [1,0,1,0,1,1,1,0,1,0,1,1,1,0,1],
    [1,0,1,0,0,0,0,0,1,0,0,0,0,0,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
]

maze_level2 = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,1,0,0,0,0,0,1,0,0,0,1],
    [1,0,1,0,1,0,1,1,1,0,1,0,1,0,1],
    [1,0,1,0,0,0,1,0,0,0,0,0,1,0,1],
    [1,0,1,1,1,0,1,0,1,1,1,0,1,0,1],
    [1,0,0,0,0,0,1,0,0,0,1,0,0,0,1],
    [1,1,1,0,1,0,0,0,1,0,1,1,1,0,1],
    [1,0,0,0,1,0,1,0,1,0,0,0,0,0,1],
    [1,0,1,0,1,0,1,0,1,1,1,0,1,0,1],
    [1,0,1,0,0,0,1,0,0,0,0,0,1,0,1],
    [1,0,1,1,1,0,1,1,1,0,1,0,1,0,1],
    [1,0,0,0,0,0,0,0,0,0,1,0,0,0,1],
    [1,0,1,0,1,1,1,0,1,0,1,1,1,0,1],
    [1,0,1,0,0,0,0,0,1,0,0,0,0,0,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
]

maze_level3 = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,1,0,0,0,0,0,1,0,0,0,1],
    [1,0,1,0,1,0,1,1,1,0,1,0,1,0,1],
    [1,0,1,0,0,0,1,0,0,0,0,0,1,0,1],
    [1,0,1,1,1,0,1,0,1,1,1,0,1,0,1],
    [1,0,0,0,0,0,1,0,0,0,1,0,0,0,1],
    [1,1,1,0,1,0,0,0,1,0,1,1,1,0,1],
    [1,0,0,0,1,0,1,0,1,0,0,0,0,0,1],
    [1,0,1,0,1,0,1,0,1,1,1,0,1,0,1],
    [1,0,1,0,0,0,1,0,0,0,0,0,1,0,1],
    [1,0,1,1,1,0,1,1,1,0,1,0,1,0,1],
    [1,0,0,0,0,0,0,0,0,0,1,0,0,0,1],
    [1,0,1,0,1,1,1,0,1,0,1,1,1,0,1],
    [1,0,1,0,0,0,0,0,1,0,0,0,0,0,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
]

mazes = [maze_level1, maze_level2, maze_level3]

# Level 1: 5 enemies, free-roam
# Level 2: 7 enemies, 1 in Zone 0, 2 each in other zones
# Level 3: 8 enemies, 2 per zone
LEVEL_CONFIG = {
    1: {"keys": 1, "enemies": 5,  "speed": 0.8},
    2: {"keys": 2, "enemies": 7,  "speed": 0.8},
    3: {"keys": 3, "enemies": 8,  "speed": 1.0},
}

# Level 1: all free roam (zone_id = -1)
# Level 2: zone 0 → 1 enemy, zones 1/2/3 → 2 enemies each  (total 7)
# Level 3: all zones → 2 enemies each                       (total 8)
ZONE_ENEMY_COUNT = {
    1: {0: 0, 1: 0, 2: 0, 3: 0},   # all free
    2: {0: 1, 1: 2, 2: 2, 3: 2},   # 1 + 2+2+2 = 7
    3: {0: 2, 1: 2, 2: 2, 3: 2},   # 2+2+2+2  = 8
}

# Active maze (rebuilt each level)
maze = [row[:] for row in maze_level1]

# GAME STATE
playerPosition = [1 * CELL_SIZE + CELL_SIZE // 2,
                  PLAYER_HEIGHT,
                  1 * CELL_SIZE + CELL_SIZE // 2]
playerAngle    = 0
movementSpeed  = 8

gameScore      = 0
gameWon        = False
gameOver       = False
keysCollected  = 0
totalKeys      = 1
coinsCollected = 0
totalCoins     = 5
playerHealth   = 100
maxHealth      = 100
hasShield      = False
gameLevel      = 1
maxLevel       = 3
gameStartTime  = time.time()
enemySpeed     = LEVEL_CONFIG[1]["speed"]

EYE_HEIGHT  = 35
firstPerson = True

animationTime = 0.0
playerBob     = 0.0
flashlightFlicker  = 1.0

# Cheat mode state
enemiesFrozen   = False
freezeStartTime = 0.0
cheatUsed       = False

# Object lists
coins         = []
healthPotions = []
flashlights       = []
treasures     = []
enemies       = []
shields       = []
key_positions = []
exit_position = None

# MAZE HELPERS
def isFree(mx, mz):
    if mx < 0 or mx >= MAZE_SIZE or mz < 0 or mz >= MAZE_SIZE:
        return False
    return maze[mz][mx] != 1

def getNeighbours(mx, mz):
    result = []
    for dx, dz in [(1,0),(-1,0),(0,1),(0,-1)]:
        if isFree(mx+dx, mz+dz):
            result.append((mx+dx, mz+dz))
    return result

def getNeighboursInZone(mx, mz, zone_id):
    """Like getNeighbours but only returns cells inside the given zone."""
    result = []
    for dx, dz in [(1,0),(-1,0),(0,1),(0,-1)]:
        nx, nz = mx+dx, mz+dz
        if isFree(nx, nz) and in_zone(nx, nz, zone_id):
            result.append((nx, nz))
    return result

def isIntersection(mx, mz):
    return len(getNeighbours(mx, mz)) >= 3

# ENEMY DATA LAYOUT
# index: 0=world_x, 1=world_y, 2=world_z, 3=alive,
#        4=rot_angle, 5=dir_x, 6=dir_z, 7=step_count,
#        8=zone_id (-1 = free roam, 0-3 = locked zone)

#INITIALIZE
def initializeGame():
    global coins, healthPotions, flashlights, treasures, enemies, shields
    global key_positions, exit_position, gameStartTime, animationTime, maze
    global totalKeys, keysCollected, enemySpeed

    coins=[]; healthPotions=[]; flashlights=[]
    treasures=[]; enemies=[]; shields=[]
    key_positions = []
    exit_position = None
    gameStartTime = time.time()
    animationTime = 0.0

    cfg           = LEVEL_CONFIG[gameLevel]
    totalKeys     = cfg["keys"]
    keysCollected = 0
    enemySpeed    = cfg["speed"]

    src  = mazes[gameLevel - 1]
    maze = [row[:] for row in src]

    def world(cx, cz):
        return (cx * CELL_SIZE + CELL_SIZE // 2,
                cz * CELL_SIZE + CELL_SIZE // 2)

    # Exit portal is fixed at bottom-right cell (13,13)
    wx, wz = world(13, 13)
    exit_position = [wx, PLAYER_HEIGHT, wz]

    # Hardcoded flashlights
    flashlight_cells = [(3,1), (11,4), (3,8), (9,11)]
    for (tx, tz) in flashlight_cells:
        if maze[tz][tx] == 0:
            wx2, wz2 = world(tx, tz)
            flashlights.append([wx2, WALL_HEIGHT - 10, wz2])

    # Build available cell pools
    reserved = {(13, 13)} | {(tx, tz) for tx, tz in flashlight_cells}
    all_empty = [
        (j, i) for i in range(MAZE_SIZE)
                for j in range(MAZE_SIZE)
                if maze[i][j] == 0 and (j, i) not in reserved
    ]

    def too_close(cx, cz, min_dist=4):
        return abs(cx - 1) + abs(cz - 1) < min_dist

    safe_far = [c for c in all_empty if not too_close(c[0], c[1])]
    safe_any = list(all_empty)
    random.shuffle(safe_far)
    random.shuffle(safe_any)

    used = set(reserved)

    #SPAWN ENEMIES
    # Level 1 : all 5 enemies free-roam (zone_id = -1)
    # Level 2 : 1 enemy locked to Zone 0,
    #           2 enemies locked to each of zones
    # Level 3 : 2 enemies locked to every zone

    def spawn_enemy(cx, cz, zone_id):
        wx2, wz2 = world(cx, cz)
        enemies.append([
            wx2, PLAYER_HEIGHT, wz2,   # 0,1,2  position
            True,                       # 3      alive
            0,                          # 4      rotation angle
            random.choice([-1, 1]),     # 5      dir_x
            random.choice([-1, 1]),     # 6      dir_z
            0,                          # 7      step count
            zone_id,                    # 8      zone (-1 = free)
        ])
        used.add((cx, cz))

    def spawn_zone_enemies(zone_id, count):
        """Spawn `count` enemies locked to zone_id; safe_far first, safe_any as fallback."""
        if count == 0:
            return
        col_min, col_max, row_min, row_max = ZONE_BOUNDS[zone_id]
        pool = [
            (cx, cz) for (cx, cz) in safe_far
            if col_min <= cx <= col_max and row_min <= cz <= row_max
            and (cx, cz) not in used
        ]
        random.shuffle(pool)
        spawned = 0
        for cx, cz in pool:
            if spawned >= count:
                return
            spawn_enemy(cx, cz, zone_id)
            spawned += 1
        if spawned < count:
            fallback = [
                (cx, cz) for (cx, cz) in safe_any
                if col_min <= cx <= col_max and row_min <= cz <= row_max
                and (cx, cz) not in used
            ]
            random.shuffle(fallback)
            for cx, cz in fallback:
                if spawned >= count:
                    return
                spawn_enemy(cx, cz, zone_id)
                spawned += 1

    zone_counts    = ZONE_ENEMY_COUNT[gameLevel]
    total_zoned    = sum(zone_counts.values())
    free_roam_need = cfg["enemies"] - total_zoned   # >0 only on Level 1

    # Spawn zoned enemies per zone
    for zone_id in range(4):
        spawn_zone_enemies(zone_id, zone_counts[zone_id])

    # Spawn free-roamers (Level 1 only)
    spawned_free = 0
    for cx, cz in safe_far:
        if spawned_free >= free_roam_need:
            break
        if (cx, cz) in used:
            continue
        spawn_enemy(cx, cz, -1)
        spawned_free += 1

    # Keys
    for cx, cz in safe_far:
        if len(key_positions) >= totalKeys:
            break
        if (cx, cz) in used:
            continue
        wx2, wz2 = world(cx, cz)
        key_positions.append([wx2, PLAYER_HEIGHT, wz2])
        used.add((cx, cz))

    # Coins (5)
    for cx, cz in safe_any:
        if len(coins) >= 5:
            break
        if (cx, cz) in used:
            continue
        wx2, wz2 = world(cx, cz)
        coins.append([wx2, PLAYER_HEIGHT, wz2, True])
        used.add((cx, cz))

    # Health potions (L1: 2, L2: 2, L3: 1)
    num_potions = 1 if gameLevel == 3 else 2
    for cx, cz in safe_any:
        if len(healthPotions) >= num_potions:
            break
        if (cx, cz) in used:
            continue
        wx2, wz2 = world(cx, cz)
        healthPotions.append([wx2, PLAYER_HEIGHT, wz2, True])
        used.add((cx, cz))

    # Treasure (1)
    for cx, cz in safe_any:
        if len(treasures) >= 1:
            break
        if (cx, cz) in used:
            continue
        wx2, wz2 = world(cx, cz)
        treasures.append([wx2, PLAYER_HEIGHT, wz2, True])
        used.add((cx, cz))

    # Shield (1)
    for cx, cz in safe_any:
        if len(shields) >= 1:
            break
        if (cx, cz) in used:
            continue
        wx2, wz2 = world(cx, cz)
        shields.append([wx2, PLAYER_HEIGHT, wz2, True])
        used.add((cx, cz))

# DRAW TEXT
def draw_text(x, y, text, font=GLUT_BITMAP_HELVETICA_18):
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, 1000, 0, 800)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(font, ord(ch))
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

# FLOOR
def drawFloor():
    for i in range(MAZE_SIZE):
        for j in range(MAZE_SIZE):
            if gameLevel == 1:
                base = 0.22
            elif gameLevel == 2:
                base = 0.16
            else:
                base = 0.12
            if (i + j) % 2 == 0:
                glColor3f(base + 0.05, base, base - 0.02)
            else:
                glColor3f(base - 0.04, base - 0.06, base - 0.08)
            x1 = j * CELL_SIZE;  x2 = x1 + CELL_SIZE
            z1 = i * CELL_SIZE;  z2 = z1 + CELL_SIZE
            glBegin(GL_QUADS)
            glVertex3f(x1, 0, z1)
            glVertex3f(x2, 0, z1)
            glVertex3f(x2, 0, z2)
            glVertex3f(x1, 0, z2)
            glEnd()

# WALL
def drawWall(x, z):
    glPushMatrix()
    glTranslatef(x + CELL_SIZE/2, WALL_HEIGHT/2, z + CELL_SIZE/2)
    if gameLevel == 1:
        glColor3f(0.40, 0.32, 0.25)
    elif gameLevel == 2:
        glColor3f(0.32, 0.18, 0.14)
    else:
        glColor3f(0.20, 0.12, 0.18)
    glScalef(CELL_SIZE, WALL_HEIGHT, CELL_SIZE)
    glutSolidCube(1)
    glPopMatrix()

def drawMaze():
    for i in range(MAZE_SIZE):
        for j in range(MAZE_SIZE):
            if maze[i][j] == 1:
                drawWall(j * CELL_SIZE, i * CELL_SIZE)

# Player
def drawPlayer():
    global playerBob
    playerBob = math.sin(animationTime * 8) * 2

    glPushMatrix()
    glTranslatef(playerPosition[0], playerPosition[1] + playerBob, playerPosition[2])
    glRotatef(playerAngle, 0, 1, 0)

    glPushMatrix()
    glColor3f(0.2, 0.5, 0.2)
    glScalef(1.0, 1.5, 1.0)
    glutSolidCube(15)
    glPopMatrix()

    glPushMatrix()
    glTranslatef(0, -5, 0)
    glColor3f(0.4, 0.2, 0.1)
    glScalef(1.2, 0.3, 1.2)
    glutSolidCube(15)
    glPopMatrix()

    glPushMatrix()
    glTranslatef(0, 20, 0)
    glColor3f(1.0, 0.8, 0.6)
    gluSphere(gluNewQuadric(), 8, 10, 10)
    glPopMatrix()

    glPushMatrix()
    glTranslatef(0, 27, 0)
    glColor3f(0.3, 0.15, 0.0)
    glScalef(1.8, 0.2, 1.8)
    glutSolidCube(10)
    glPopMatrix()

    glPushMatrix()
    glTranslatef(0, 33, 0)
    glColor3f(0.3, 0.15, 0.0)
    glScalef(1.0, 1.2, 1.0)
    glutSolidCube(10)
    glPopMatrix()

    glPushMatrix()
    glTranslatef(-12, 5, 0)
    glRotatef(math.sin(animationTime * 6) * 35, 1, 0, 0)
    glColor3f(1.0, 0.8, 0.6)
    gluCylinder(gluNewQuadric(), 3, 3, 15, 8, 8)
    glPopMatrix()

    glPushMatrix()
    glTranslatef(12, 5, 0)
    glRotatef(-math.sin(animationTime * 6) * 35, 1, 0, 0)
    glColor3f(1.0, 0.8, 0.6)
    gluCylinder(gluNewQuadric(), 3, 3, 15, 8, 8)
    glPopMatrix()

    glPushMatrix()
    glTranslatef(-5, -12, 0)
    glRotatef(-math.sin(animationTime * 6) * 35, 1, 0, 0)
    glColor3f(0.1, 0.1, 0.5)
    gluCylinder(gluNewQuadric(), 3, 3, 14, 8, 8)
    glPopMatrix()

    glPushMatrix()
    glTranslatef(5, -12, 0)
    glRotatef(math.sin(animationTime * 6) * 35, 1, 0, 0)
    glColor3f(0.1, 0.1, 0.5)
    gluCylinder(gluNewQuadric(), 3, 3, 14, 8, 8)
    glPopMatrix()

    glPopMatrix()

# KEYS
def drawKeys():
    for kp in key_positions:
        if kp[3] if len(kp) > 3 else True:
            glPushMatrix()
            glTranslatef(kp[0], kp[1] + 15, kp[2])
            glRotatef(animationTime * 60, 0, 1, 0)

            glColor3f(1.0, 0.8, 0.1)
            gluSphere(gluNewQuadric(), 6, 10, 10)

            glPushMatrix()
            glTranslatef(8, 0, 0)
            glRotatef(90, 0, 1, 0)
            glColor3f(0.9, 0.7, 0.1)
            gluCylinder(gluNewQuadric(), 2, 2, 16, 8, 8)
            glPopMatrix()

            glColor3f(0.8, 0.6, 0.1)
            for i in range(3):
                glPushMatrix()
                glTranslatef(12 + i * 4, -4, 0)
                glutSolidCube(4)
                glPopMatrix()

            glPopMatrix()

# COINS
def drawCoins():
    for coin in coins:
        if coin[3]:
            glPushMatrix()
            glTranslatef(coin[0], coin[1] + 10, coin[2])
            glRotatef(animationTime * 90, 0, 1, 0)
            glColor3f(1.0, 0.8, 0.2)
            glPushMatrix()
            glScalef(1.0, 0.2, 1.0)
            gluSphere(gluNewQuadric(), 7, 12, 12)
            glPopMatrix()
            glPopMatrix()

# hEALTH Potions
def drawHealthPotions():
    for potion in healthPotions:
        if potion[3]:
            bob = math.sin(animationTime * 3 + potion[0]) * 2
            glPushMatrix()
            glTranslatef(potion[0], potion[1] + 8 + bob, potion[2])
            glColor3f(0.8, 0.1, 0.1)
            gluCylinder(gluNewQuadric(), 4, 3, 12, 10, 8)
            glPushMatrix()
            glTranslatef(0, 0, 12)
            glColor3f(0.4, 0.2, 0.1)
            glutSolidCube(5)
            glPopMatrix()
            glColor3f(1.0, 0.3, 0.3)
            gluSphere(gluNewQuadric(), 6, 8, 8)
            glPopMatrix()

# Flashlights
def drawFlashlights():
    global flashlightFlicker
    flashlightFlicker = math.sin(animationTime * 15) * 0.25 + 0.75

    for flashlight in flashlights:
        glPushMatrix()
        glTranslatef(flashlight[0], flashlight[1], flashlight[2])

        glColor3f(0.4, 0.2, 0.1)
        glPushMatrix()
        glRotatef(180, 1, 0, 0)
        gluCylinder(gluNewQuadric(), 2, 2, 20, 8, 8)
        glPopMatrix()

        glPushMatrix()
        glTranslatef(0, 5, 0)
        glScalef(flashlightFlicker, flashlightFlicker * 1.4, flashlightFlicker)
        glColor3f(1.0, 0.7, 0.1)
        gluSphere(gluNewQuadric(), 5, 8, 8)
        glPopMatrix()

        glPopMatrix()

# Treasures
def drawTreasures():
    for treasure in treasures:
        if treasure[3]:
            glPushMatrix()
            glTranslatef(treasure[0], treasure[1] + 5, treasure[2])

            glColor3f(0.4, 0.22, 0.1)
            glPushMatrix()
            glScalef(1.2, 0.8, 1.0)
            glutSolidCube(14)
            glPopMatrix()

            glColor3f(1.0, 0.8, 0.2)
            glPushMatrix()
            glTranslatef(0, 0, 7.5)
            glScalef(1.3, 0.15, 0.1)
            glutSolidCube(14)
            glPopMatrix()

            glColor3f(0.6, 0.6, 0.3)
            glPushMatrix()
            glTranslatef(0, -2, 8)
            gluSphere(gluNewQuadric(), 2, 8, 8)
            glPopMatrix()

            glPopMatrix()

def drawEnemies():
    for enemy in enemies:
        if enemy[3]:
            glPushMatrix()
            glTranslatef(enemy[0], enemy[1] + 10, enemy[2])
            enemy[4] = (enemy[4] + 2) % 360
            glRotatef(enemy[4], 0, 1, 0)

            if enemiesFrozen:
                glColor3f(0.2, 0.6, 1.0)
            elif gameLevel == 1:
                glColor3f(0.8, 0.1, 0.1)
            elif gameLevel == 2:
                glColor3f(0.55, 0.04, 0.04)
            else:
                glColor3f(0.35, 0.02, 0.35)

            glPushMatrix()
            glScalef(1.2, 1.8, 1.2)
            glutSolidCube(12)
            glPopMatrix()

            glColor3f(0.45, 0.04, 0.04)
            for i in range(4):
                glPushMatrix()
                glRotatef(i * 90, 0, 1, 0)
                glTranslatef(10, 4, 0)
                glRotatef(90, 0, 1, 0)
                gluCylinder(gluNewQuadric(), 2, 0, 8, 6, 4)
                glPopMatrix()

            glColor3f(1.0, 0.9, 0.0)
            glPushMatrix()
            glTranslatef(-3, 8, 8)
            gluSphere(gluNewQuadric(), 2, 6, 6)
            glPopMatrix()
            glPushMatrix()
            glTranslatef(3, 8, 8)
            gluSphere(gluNewQuadric(), 2, 6, 6)
            glPopMatrix()

            glPopMatrix()

#Enemy movements
def updateEnemies():
    global enemiesFrozen

    if enemiesFrozen:
        if time.time() - freezeStartTime >= 7.0:
            enemiesFrozen = False
            print("Enemies unfrozen!")
        return

    for enemy in enemies:
        if not enemy[3]:
            continue

        ex      = enemy[0]
        ez      = enemy[2]
        dx      = enemy[5]
        dz      = enemy[6]
        step    = enemy[7]
        zone_id = enemy[8]    # -1 = free roam

        newX = ex + dx * enemySpeed
        newZ = ez + dz * enemySpeed

        margin = 10

        def enemyCollides(cx, cz):
            for ddx in [-margin, margin]:
                for ddz in [-margin, margin]:
                    mx = max(0, min(MAZE_SIZE - 1, int((cx + ddx) / CELL_SIZE)))
                    mz = max(0, min(MAZE_SIZE - 1, int((cz + ddz) / CELL_SIZE)))
                    if maze[mz][mx] == 1:
                        return True
            return False

        def outOfZone(cx, cz):
            """True if the world position has left the assigned zone."""
            if zone_id == -1:
                return False
            mx = max(0, min(MAZE_SIZE - 1, int(cx / CELL_SIZE)))
            mz = max(0, min(MAZE_SIZE - 1, int(cz / CELL_SIZE)))
            return not in_zone(mx, mz, zone_id)

        # Try to move forward
        if not enemyCollides(newX, newZ) and not outOfZone(newX, newZ):
            enemy[0] = newX
            enemy[2] = newZ
            enemy[7] = step + 1

            cMX = max(0, min(MAZE_SIZE - 1, int(newX / CELL_SIZE)))
            cMZ = max(0, min(MAZE_SIZE - 1, int(newZ / CELL_SIZE)))

            threshold = int(CELL_SIZE / max(enemySpeed, 0.1))

            # At intersections or after enough steps, pick a new direction
            if step >= threshold and isIntersection(cMX, cMZ):
                if zone_id == -1:
                    neighbours = getNeighbours(cMX, cMZ)
                else:
                    neighbours = getNeighboursInZone(cMX, cMZ, zone_id)
                    # If no in-zone neighbours (e.g. narrow passage at border),
                    # fall back to any neighbour to avoid getting stuck
                    if not neighbours:
                        neighbours = getNeighbours(cMX, cMZ)
                if neighbours:
                    chosen   = random.choice(neighbours)
                    enemy[5] = chosen[0] - cMX
                    enemy[6] = chosen[1] - cMZ
                    enemy[7] = 0
        else:
            # Blocked by wall or zone boundary then pick a new valid direction
            curMX = max(0, min(MAZE_SIZE - 1, int(ex / CELL_SIZE)))
            curMZ = max(0, min(MAZE_SIZE - 1, int(ez / CELL_SIZE)))

            if zone_id == -1:
                neighbours = getNeighbours(curMX, curMZ)
            else:
                neighbours = getNeighboursInZone(curMX, curMZ, zone_id)
                if not neighbours:
                    neighbours = getNeighbours(curMX, curMZ)

            if neighbours:
                chosen   = random.choice(neighbours)
                enemy[5] = chosen[0] - curMX
                enemy[6] = chosen[1] - curMZ
            else:
                enemy[5] = -dx
                enemy[6] = -dz
            enemy[7] = 0

# Shields
def drawShields():
    for shield in shields:
        if shield[3]:
            glPushMatrix()
            glTranslatef(shield[0], shield[1] + 10, shield[2])
            glRotatef(animationTime * 45, 0, 1, 0)

            glColor3f(0.7, 0.7, 0.85)
            glPushMatrix()
            glScalef(1.0, 1.3, 0.2)
            gluSphere(gluNewQuadric(), 10, 12, 8)
            glPopMatrix()

            glColor3f(1.0, 0.8, 0.2)
            glPushMatrix()
            glTranslatef(0, 0, 2)
            gluSphere(gluNewQuadric(), 3, 8, 8)
            glPopMatrix()

            glPopMatrix()

# EXIT
def drawExit():
    if exit_position:
        allKeysCollected = (keysCollected >= totalKeys)

        glPushMatrix()
        glTranslatef(exit_position[0], WALL_HEIGHT/2, exit_position[2])

        glColor3f(0.3, 0.1, 0.5)
        glPushMatrix()
        glScalef(CELL_SIZE - 4, WALL_HEIGHT, 6)
        glutSolidCube(1)
        glPopMatrix()

        if allKeysCollected:
            glColor3f(0.2, 0.8, 1.0)
            for i in range(5):
                angle = math.radians(animationTime * 60 + i * 72)
                glPushMatrix()
                glTranslatef(math.cos(angle) * 10, math.sin(angle) * 10, 4)
                gluSphere(gluNewQuadric(), 3, 8, 8)
                glPopMatrix()
            glColor3f(0.8, 1.0, 1.0)
            gluSphere(gluNewQuadric(), CELL_SIZE/4, 14, 14)
        else:
            glColor3f(0.7, 0.1, 0.1)
            gluSphere(gluNewQuadric(), CELL_SIZE/5, 10, 10)

        glColor3f(0.6, 0.3, 0.8)
        for i in range(8):
            angle = math.radians(i * 45 + animationTime * 30)
            glPushMatrix()
            glTranslatef(math.cos(angle) * (CELL_SIZE/2),
                         math.sin(angle) * (CELL_SIZE/2), 3)
            glutSolidCube(4)
            glPopMatrix()

        glPopMatrix()

# Camera
def setupCamera():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    angle_rad = math.radians(playerAngle)

    if firstPerson:
        gluPerspective(75, 1.25, 1.0, 2000)
        eye_x = playerPosition[0]
        eye_y = playerPosition[1] + EYE_HEIGHT
        eye_z = playerPosition[2]
        look_x = eye_x + math.sin(angle_rad)
        look_y = eye_y
        look_z = eye_z + math.cos(angle_rad)
        gluLookAt(eye_x, eye_y, eye_z,
                  look_x, look_y, look_z,
                  0, 1, 0)
    else:
        gluPerspective(60, 1.25, 0.1, 2000)
        cam_x = playerPosition[0]
        cam_y = playerPosition[1] + 520
        cam_z = playerPosition[2] + 350
        gluLookAt(cam_x, cam_y, cam_z,
                  playerPosition[0], playerPosition[1], playerPosition[2],
                  0, 1, 0)

# Collision
def checkCollision(newX, newZ):
    margin = 15
    for ddx in [-margin, margin]:
        for ddz in [-margin, margin]:
            mx = int((newX + ddx) / CELL_SIZE)
            mz = int((newZ + ddz) / CELL_SIZE)
            if mx < 0 or mx >= MAZE_SIZE or mz < 0 or mz >= MAZE_SIZE:
                return True
            if maze[mz][mx] == 1:
                return True
    return False

# Collectibles and interactions
def checkCollectibles():
    global keysCollected, coinsCollected, gameScore, playerHealth, hasShield, gameOver

    px, pz = playerPosition[0], playerPosition[2]

    # Keys
    for kp in key_positions:
        active = kp[3] if len(kp) > 3 else True
        if active:
            dist = math.sqrt((px - kp[0])**2 + (pz - kp[2])**2)
            if dist < 25:
                if len(kp) <= 3:
                    kp.append(False)
                else:
                    kp[3] = False
                keysCollected += 1
                gameScore += 50
                print(f"Key collected! ({keysCollected}/{totalKeys})")

    # Coins
    for coin in coins:
        if coin[3]:
            dist = math.sqrt((px - coin[0])**2 + (pz - coin[2])**2)
            if dist < 20:
                coin[3] = False
                coinsCollected += 1
                gameScore += 15
                print(f"Gold coin! Total: {coinsCollected}")

    # Health potions
    for potion in healthPotions:
        if potion[3]:
            dist = math.sqrt((px - potion[0])**2 + (pz - potion[2])**2)
            if dist < 20:
                potion[3] = False
                gameScore += 20
                playerHealth = min(maxHealth, playerHealth + 30)
                print(f"Health restored! HP: {playerHealth}")

    # Treasures
    for treasure in treasures:
        if treasure[3]:
            dist = math.sqrt((px - treasure[0])**2 + (pz - treasure[2])**2)
            if dist < 22:
                treasure[3] = False
                gameScore += 100
                print("Treasure! +100 points!")

    # Shields
    for shield in shields:
        if shield[3]:
            dist = math.sqrt((px - shield[0])**2 + (pz - shield[2])**2)
            if dist < 20:
                shield[3] = False
                hasShield = True
                gameScore += 50
                print("Magical shield acquired!")

    # Enemies
    for enemy in enemies:
        if enemy[3]:
            dist = math.sqrt((px - enemy[0])**2 + (pz - enemy[2])**2)
            if dist < 25:
                if hasShield:
                    enemy[3] = False
                    hasShield = False
                    gameScore += 50
                    print("Enemy defeated with shield!")
                else:
                    playerHealth -= 25
                    gameScore = max(0, gameScore - 20)
                    print(f"Enemy hit! HP: {playerHealth}")
                    if playerHealth <= 0:
                        gameOver = True

# Win condition, level up
def checkWinCondition():
    global gameWon, gameOver, gameScore, gameLevel, enemySpeed
    global keysCollected, coinsCollected, playerHealth, hasShield
    global playerPosition, playerAngle, animationTime
    global enemiesFrozen, freezeStartTime, cheatUsed

    if exit_position and keysCollected >= totalKeys:
        dist = math.sqrt((playerPosition[0] - exit_position[0])**2 +
                         (playerPosition[2] - exit_position[2])**2)
        if dist < 30:
            elapsed      = time.time() - gameStartTime
            time_bonus   = max(0, 300 - int(elapsed))
            health_bonus = playerHealth * 2
            gameScore   += time_bonus + health_bonus + coinsCollected * 15

            if gameLevel < maxLevel:
                gameLevel += 1
                print(f"LEVEL UP! Now on Level {gameLevel}!")

                savedScore  = gameScore
                savedHealth = playerHealth

                keysCollected  = 0
                coinsCollected = 0
                hasShield      = False
                enemiesFrozen  = False
                cheatUsed      = False
                playerPosition = [1 * CELL_SIZE + CELL_SIZE // 2,
                                  PLAYER_HEIGHT,
                                  1 * CELL_SIZE + CELL_SIZE // 2]
                playerAngle    = 0
                animationTime  = 0.0

                initializeGame()
                gameScore    = savedScore
                playerHealth = savedHealth

            else:
                gameWon  = True
                gameOver = True
                print("VICTORY! You escaped the dungeon across all 3 levels!")

# INPUT
def keyboardListener(key, x, y):
    global playerPosition, playerAngle, animationTime, gameOver

    if gameOver:
        if key == b'r' or key == b'R':
            resetGame()
        return

    angle_rad = math.radians(playerAngle)
    newX  = playerPosition[0]
    newZ  = playerPosition[2]
    moved = False

    if key == b'w' or key == b'W':
        newX += math.sin(angle_rad) * movementSpeed
        newZ += math.cos(angle_rad) * movementSpeed
        moved = True
    elif key == b's' or key == b'S':
        newX -= math.sin(angle_rad) * movementSpeed
        newZ -= math.cos(angle_rad) * movementSpeed
        moved = True
    elif key == b'a' or key == b'A':
        newX -= math.cos(angle_rad) * movementSpeed
        newZ += math.sin(angle_rad) * movementSpeed
        moved = True
    elif key == b'd' or key == b'D':
        newX += math.cos(angle_rad) * movementSpeed
        newZ -= math.sin(angle_rad) * movementSpeed
        moved = True
    elif key == b'v' or key == b'V':
        global firstPerson
        firstPerson = not firstPerson
        print("View:", "First-Person" if firstPerson else "Third-Person")

    if moved:
        animationTime += 0.3

    if not checkCollision(newX, playerPosition[2]):
        playerPosition[0] = newX
    if not checkCollision(playerPosition[0], newZ):
        playerPosition[2] = newZ

    checkCollectibles()
    checkWinCondition()
    glutPostRedisplay()

def specialKeyListener(key, x, y):
    global playerAngle

    if gameOver:
        return

    if key == GLUT_KEY_LEFT:
        playerAngle -= 5
    elif key == GLUT_KEY_RIGHT:
        playerAngle += 5

    glutPostRedisplay()


def mouseListener(button, state, x, y):
    global enemiesFrozen, freezeStartTime, cheatUsed

    if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        if gameLevel == 3 and not cheatUsed and not gameOver:
            enemiesFrozen   = True
            freezeStartTime = time.time()
            cheatUsed       = True
            print("CHEAT: Enemies frozen for 7 seconds!")

    glutPostRedisplay()

# RESET
def resetGame():
    global playerPosition, playerAngle, gameScore, gameWon, gameOver
    global keysCollected, coinsCollected, playerHealth, hasShield
    global animationTime, gameLevel, enemySpeed, firstPerson
    global enemiesFrozen, freezeStartTime, cheatUsed

    playerPosition  = [1 * CELL_SIZE + CELL_SIZE // 2,
                       PLAYER_HEIGHT,
                       1 * CELL_SIZE + CELL_SIZE // 2]
    playerAngle     = 0
    gameScore       = 0
    gameWon         = False
    gameOver        = False
    keysCollected   = 0
    coinsCollected  = 0
    playerHealth    = 100
    hasShield       = False
    firstPerson     = True
    animationTime   = 0.0
    gameLevel       = 1
    enemySpeed      = LEVEL_CONFIG[1]["speed"]
    enemiesFrozen   = False
    freezeStartTime = 0.0
    cheatUsed       = False
    initializeGame()
    print("Game restarted from Level 1!")

# DISPLAY
def showScreen():
    global animationTime

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glViewport(0, 0, 1000, 800)

    setupCamera()
    updateEnemies()

    drawFloor()
    if not firstPerson:
        drawPlayer()
    drawMaze()
    drawKeys()
    drawCoins()
    drawHealthPotions()
    drawFlashlights()
    drawTreasures()
    drawEnemies()
    drawShields()
    drawExit()

    # HUD
    elapsed = int(time.time() - gameStartTime)

    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, 1000, 0, 800)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    glColor3f(0.2, 0.2, 0.2)
    glBegin(GL_QUADS)
    glVertex3f(20, 775, 0); glVertex3f(170, 775, 0)
    glVertex3f(170, 790, 0); glVertex3f(20, 790, 0)
    glEnd()
    bar_w = int(150 * max(playerHealth, 0) / 100)
    if playerHealth < 30:
        glColor3f(1, 0, 0)
    elif playerHealth < 60:
        glColor3f(1, 1, 0)
    else:
        glColor3f(0, 1, 0)
    glBegin(GL_QUADS)
    glVertex3f(20, 775, 0); glVertex3f(20 + bar_w, 775, 0)
    glVertex3f(20 + bar_w, 790, 0); glVertex3f(20, 790, 0)
    glEnd()
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

    if playerHealth < 30:
        glColor3f(1, 0, 0)
    elif playerHealth < 60:
        glColor3f(1, 1, 0)
    else:
        glColor3f(0, 1, 0)
    draw_text(20, 758, f"HP: {playerHealth}/100")

    glColor3f(1, 1, 1)
    draw_text(20, 733, f"Score: {gameScore}")
    draw_text(20, 708, f"Level: {gameLevel}/{maxLevel}")
    draw_text(20, 683, f"Time:  {elapsed}s")

    glColor3f(0.8, 0.8, 0.8)
    draw_text(20, 658, f"Keys: {keysCollected}/{totalKeys}")
    if keysCollected >= totalKeys:
        glColor3f(0, 1, 0)
        draw_text(110, 658, "ALL COLLECTED!")
    else:
        glColor3f(1, 0.4, 0.4)
        remaining = totalKeys - keysCollected
        draw_text(110, 658, f"{remaining} remaining")

    glColor3f(0.8, 0.8, 0.8)
    draw_text(20, 633, "Shield:")
    if hasShield:
        glColor3f(0, 0.8, 1)
        draw_text(90, 633, "Yes")
    else:
        glColor3f(0.5, 0.5, 0.5)
        draw_text(90, 633, "No")

    glColor3f(0.6, 0.6, 0.6)
    draw_text(20, 608, f"View: {'First-Person' if firstPerson else 'Third-Person'}  [V]")

    # Cheat mode is only shown on level 3
    if gameLevel == 3:
        if enemiesFrozen:
            remaining_freeze = max(0, 7 - int(time.time() - freezeStartTime))
            glColor3f(0, 1, 1)
            draw_text(20, 583, f"FREEZE: {remaining_freeze}s left")
        elif cheatUsed:
            glColor3f(0.5, 0.5, 0.5)
            draw_text(20, 583, "Cheat: Used")
        else:
            glColor3f(0.8, 0.6, 0.0)
            draw_text(20, 583, "Cheat: Right click to freeze enemies!")

    # Game over & win screen
    if gameWon:
        glColor3f(0, 1, 0)
        draw_text(320, 470, "CONGRATULATIONS!")
        draw_text(300, 440, "YOU ESCAPED ALL 3 LEVELS!")
        glColor3f(1, 1, 1)
        draw_text(330, 410, f"Final Score: {gameScore}")
        draw_text(290, 380, f"Time: {elapsed}s  |  Health: {playerHealth}")
        draw_text(300, 350, "Press R to play again")
    elif playerHealth <= 0:
        glColor3f(1, 0, 0)
        draw_text(380, 470, "GAME OVER")
        draw_text(340, 440, "You have fallen!")
        glColor3f(1, 1, 1)
        draw_text(350, 410, f"Score: {gameScore}")
        draw_text(310, 380, "Press R to try again")
    elif elapsed > 600:
        glColor3f(1, 0.5, 0)
        draw_text(360, 470, "TIME'S UP!")
        draw_text(280, 440, "The dungeon has claimed you!")
        glColor3f(1, 1, 1)
        draw_text(350, 410, f"Score: {gameScore}")
        draw_text(310, 380, "Press R to escape again")

    glutSwapBuffers()

# IDLE
def idle():
    global animationTime
    animationTime += 0.016
    glutPostRedisplay()

# MAIN
def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(1000, 800)
    glutInitWindowPosition(100, 100)
    glutCreateWindow(b"3D Dungeon Escape")

    glEnable(GL_DEPTH_TEST)
    initializeGame()

    glutDisplayFunc(showScreen)
    glutIdleFunc(idle)
    glutKeyboardFunc(keyboardListener)
    glutSpecialFunc(specialKeyListener)
    glutMouseFunc(mouseListener)

    print("3D DUNGEON ESCAPE")
    print("Collect ALL keys and reach the EXIT to advance!")
    print("WASD = Move, Arrow Keys = Turn, V = Camera Change, R = Restart")
    print("Level 3 Cheat: Right-click to freeze enemies for 7 seconds")
    glutMainLoop()

if __name__ == "__main__":
    main()