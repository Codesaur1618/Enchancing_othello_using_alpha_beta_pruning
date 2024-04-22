# PLAYERS
EMPTY_SPACE = 0
PLAYER = 1
CPU = 2

# COLORS 
PLAYER_COLOR = "#3D1600"
CPU_COLOR = "#F5F5DC"
BROWN_CELL = "#795231"
WHITE_CELL = "#D3AC8B"
CHIP_PRESSED = "#8c8c8c"

# BOARD
NUM_ROWS = 8
NUM_COLS = 8
INITIAL_STATE = [
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, PLAYER, CPU, 0, 0, 0],
            [0, 0, 0, CPU, PLAYER, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0]
        ]