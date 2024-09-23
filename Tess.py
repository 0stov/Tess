#!/usr/bin/env python3
import sys
import numpy as np
import logging

"""
This program will calulate all possible combinations to try and figure out the maximum 2d arrays (bricks)will fit in a larger 2d array (area).

Have you ever wanted to know how many 3x3 crop plots fit around a scarecrow in stardew vally?
Ever wondered how many hydroponic troughs fit around a sun lamp in rimword?


"""
logging.basicConfig(filename="Debout.Tess.txt",
                    format='%(asctime)s %(message)s',
                    filemode='w')

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
"""
global variables for testing only. these should be overritten in __main__()
"""
#keeps count of the number of blocks that fit in an area
block_count = 0


block =         [[1, 1, 1],
                [1, 0, 0],
                [1, 0, 0]]

block =         [[1, 1],
                [0, 0]]


area = [[1, 1, 1, 1, 1, 1, 1, 1, 1],
       [1, 0, 1, 1, 1, 1, 1, 1, 1],
       [1, 1, 0, 1, 1, 1, 1, 1, 1],
       [1, 1, 1, 0, 1, 1, 1, 1, 1],
       [1, 1, 1, 1, 0, 1, 1, 1, 1],
       [1, 1, 1, 1, 1, 0, 1, 1, 1]]

area =          [[1, 1, 1],
                [1, 1, 1],
                [1, 1 , 1]]

# array([[  0,   1,   2,   3,   4],
#        [-99,   6, -99,   8, -99],
#        [-99,  11, -99,  13, -99]])

def rotate(to_rotate):
    #this function rotates a 2d array 90^ clockwise and outputs the transformed array
    return np.rot90(to_rotate, k=1, axes=(1, 0)).tolist()

def tess(block, area, block_count):
    #This function returns the most blocks that fit in a an area.
    for y_index, y in enumerate(area):
        for x_index, x in enumerate(y):
            logging.debug(area)
            logging.debug(f"Looking at ({x_index},{y_index})")

            if canFit(block, area, (y_index, x_index)):
                logging.debug(f"CanFit at ({x_index},{y_index})")
                fit(block, area, (y_index, x_index))

                block_count += 1
                logging.debug(f"Fit at ({x_index},{y_index}); block_count: {block_count}")
                tess(block, area, block_count)

                logging.debug(f"backtrack at ({x_index},{y_index})")
                fit(block, area, (y_index, x_index), reverse=True)
                block_count -= 1
                logging.debug(f"Reverse Fit at ({x_index},{y_index}); block_count: {block_count}")

            # if canFit(rotate(block), area, (y_index, x_index)):
            #     fit(rotate(block), area, (y_index, x_index))
            #     tess(rotate(block), area)
            #     fit(rotate(block), area, (y_index, x_index), reverse=True)
            # if canFit(rotate(rotate(block)), area, (y_index, x_index)):
            #     fit(rotate(rotate(block)), area, (y_index, x_index))
            #     tess(rotate(rotate(block)), area)
            #     fit(rotate(rotate(block)), area, (y_index, x_index), reverse=True)
            # if canFit(rotate(rotate(rotate(block))), area, (y_index, x_index)):
            #     fit(rotate(rotate(rotate(block))), area, (y_index, x_index))
            #     tess(rotate(rotate(rotate(block))), area)
            #     fit(rotate(rotate(rotate(block))), area, (y_index, x_index), reverse=True)
    return

    
def canFit(block, area, coordinates=(0, 0)):
    logger.debug(f"canFit: running canFit at {coordinates}")
    #this array returns True when the 2d block array can fit into the 2d sub_area array.
    #returns false if block cannot fit into sub_area

    # Extract a subarray from rows 1 to 2 (inclusive) and columns 0 to 1 (inclusive)
    #sub_array = arr[1:3, 0:2]
    if type(coordinates) is not tuple:
        logger.debug("canFit: Coordinates no a Tuple. Raising Exception")
        raise Exception("canFit: Coordinates variable needs to be Tuple format. (x, y)")

    #check if we have enough room along the y axis
    if len(area) < (coordinates[0] + len(block)):
        logger.debug(f"canFit: Not enough room along the y axis (only {len(area)} long), return False")
        return False

    #check if we have enough room along the x axis
    if len(area[0]) < (coordinates[1] + len(block[0])):
        logger.debug(f"canFit: Not enough room along the x axis (only {len(area[1])} long), return False")
        return False

    # lets cut the whole area down to only as big as we need
    sub_area = area
    sub_area = np.array(area)[coordinates[1]:3, coordinates[0]:3].tolist()
    logger.debug(f"canFit: sub_area: \n{sub_area}")
    for block_row, sub_area_row in zip(block, sub_area):
        for block_item, sub_area_item in zip(block_row, sub_area_row):
            #print(f"Comparing : {block_item} and {sub_area_item}")

            if block_item == 0: continue #if the block is a 0 square, it doesn't matter if it fits.
            if block_item != sub_area_item:
                logger.debug(f"canFit: {block_item} != {sub_area_item}; returning false")
                return False #if block isn't a 0 it must therefore be 1+; if it doesn't match the area square it must not fit.
    logger.debug("canFit: returning True")
    return True


def fit(block, area, coordinates=(0, 0), block_count=0, reverse=False):
    #places the block into the area starting at the parameter coordinates (tuple)
    # DOES NOT INCREMENT block_count!
    # DOES NOT CHECK IF BLOCK CAN FIT
    #reverse removes the block from the area

    if type(coordinates) is not tuple: raise Exception("Coordinates variable needs to be Tuple format. (x, y)")


    for y_index, y in enumerate(block):
        # print(f"y_index: {y_index}, y = {y}")
        for x_index, x in enumerate(block):
            # print(f"x_index: {x_index}, x = {x}")
            if block[x_index][y_index] == 0: continue
            if not reverse:
                area[x_index + coordinates[1]][y_index + coordinates[0]] += (block_count + 1)
            else:
                area[x_index + coordinates[1]][y_index + coordinates[0]] -= (block_count + 1)


def getXSize(in_array):
    #this function takes in a 2d array and outputs the longest x axis
    longest = 0
    for y in in_array:
        if len(y) > longest: longest = len(y)
    return longest

def main(argv):
    #keeps count of the number of blocks that fit in an area
    block_count = 0
    block = [[1, 1],
            [0, 0]]

    area =  [[1, 1, 1],
            [1, 1, 1],
            [1, 1 , 1]]

    tess(block, area, block_count)
    print("Done.")

if __name__ == "__main__":
    main(sys.argv)
