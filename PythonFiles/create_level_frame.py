from settings import *


def add_zeros(file, blockwidth, blockheight):
    with open(file, "w") as file:
        for _ in range(blockheight):
            for _ in range(blockwidth - 1):
                file.write("t0,")
            file.write("t0\n")
    file.close()


#add_zeros("../LevelTileMaps/level2",  200, 200)




