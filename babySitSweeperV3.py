import minescript
import math
import time
import sys
from dataclasses import dataclass

def exit():
    minescript.execute("/tellraw @s {\"text\":\"Please supply a name\",\"color\":\"green\"}")
    minescript.execute("/tellraw @a [\"Usage: \",{\"text\":\"babysitV2 \",\"color\":\"aqua\"},{\"text\":\"<name>\",\"color\":\"dark_green\"}]")
    minescript.execute("/tellraw @a [\"Example: \",{\"text\":\"babysitV2 \",\"color\":\"aqua\"},{\"text\":\"sweeper\",\"color\":\"dark_green\"}]")
    sys.exit(1)

# -------- INFO ----------
# The variable weStart should contain the start coordinate.
# So if your WorldEater is heading from north-south/south-north then set weStart to the coordinate most south
# If the WorldEater is heading east-west/west-east then set it to the most east
# If you find bugs feel free to report those. https://github.com/weirdge/minescript
# -------- CONFIG --------
renderDistance = 16
weStart = 2000
weLength = 4000
botName = str(sys.argv[1]) if len(sys.argv) > 1 else exit()
# ---------- ADVANCED CONFIG -------------
botHeight = 120
timeInBetweenSpawn = 0.3

#  utility vars
renderDistanceBlocks = renderDistance*16
position = minescript.player_position()
absoluteRotation = minescript.player_orientation()
relativeRotation = (absoluteRotation[0] + 180) % 360 - 180

@dataclass
class amount():
    direction: str
    amount: int
    positive: int
    position: int # 0 = Z | 1 = X
    angle1: int
    angle2: int

directions = [
amount("east",  abs(math.ceil((weStart-position[0])/(renderDistanceBlocks))),           1,  1, -45,  -135 ),
amount("south", abs(math.ceil((weStart-position[2])/(renderDistanceBlocks))),           1,  0,  45,   -45 ),
amount("west",  abs(math.ceil((weStart-weLength-position[0])/(renderDistanceBlocks))), -1,  1, 135,    45 ),
amount("north", abs(math.ceil((weStart-weLength-position[2])/(renderDistanceBlocks))), -1,  0, 180,  -180 ), # -135 135. This could be removed and replaced with an if/else
]


for i in range(len(directions)):
    if relativeRotation < directions[i].angle1 and relativeRotation > directions[i].angle2:
        print(f"heading: {directions[i].direction}")
        print(f"rotation: {relativeRotation}")
        looking = directions[i]
        c = 0
        for j in range(looking.amount):
            if j%2==1 or j == looking.amount-1:
                time.sleep(timeInBetweenSpawn)
                minescript.execute(f"/player {botName}{c} spawn at {position[0]+looking.positive*renderDistanceBlocks*j*looking.position} {botHeight} {position[2]+looking.positive*renderDistanceBlocks*j*int(not looking.position)}")
                c+=1
        break