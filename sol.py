import asyncio
import logging
import random
import argparse
from viam.robot.client import RobotClient
from viam.rpc.dial import Credentials, DialOptions
from viam.components.gantry import Gantry

async def connect():
    creds = Credentials(
        type='robot-location-secret',
        payload='yzl1w4e70v5c3pl44nuv9on4r7s6vaug56x3qnm32eqbqd5i')
    opts = RobotClient.Options(
        refresh_interval=0,
        dial_options=DialOptions(credentials=creds)
    )
    return await RobotClient.at_address('mbp-main.8fc0qlpm4c.viam.cloud', opts)

def getValue(minVal: float, maxVal: float) -> float:
    return float(minVal + (maxVal - minVal) * random.random())


def mm2inch(l):
    return l*0.0393701

async def draw_line(axidraw: Gantry, x1, y1, x2, y2):


    pos = await axidraw.get_position()
    #lift the pen
    await axidraw.move_to_position([pos[0], pos[1], 1], [])

    # go to initial point
    await axidraw.move_to_position([x1, y1, 1], [])

    #put down the pen
    await axidraw.move_to_position([x1, y1, 0], [])

    #draw the line
    await axidraw.move_to_position([x2, y2, 0], [])
    
    #lift the pen
    await axidraw.move_to_position([x2, y2, 1], [])





async def main():
    robot = await connect()
    logger = logging.getLogger("axidraw")

    axidraw = Gantry.from_robot(robot, "axidraw")

    n = 500  ##number of random lines
    X1 = []
    Y1 = []
    X2 = []
    Y2 = []
    maxX = 175 #in mm
    maxY = 120 # in mm 
    for _ in range(n):
        X1.append(random.randint(0, maxX))
        Y1.append(random.randint(0, maxY))
        X2.append(random.randint(0, maxX))
        Y2.append(random.randint(0, maxY))
    
    for i in range(n):
        await draw_line(axidraw, mm2inch(X1[i]), mm2inch(Y1[i]), mm2inch(X2[i]), mm2inch(Y2[i]))

    await robot.close()

if __name__ == "__main__":
    asyncio.run(main())