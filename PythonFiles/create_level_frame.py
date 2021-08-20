from settings import *


def add_zeros(file, blockwidth, blockheight):
    with open(file, "w") as file:
        for _ in range(blockheight):
            for _ in range(blockwidth - 1):
                file.write("t0,")
            file.write("t0\n")
    file.close()


#add_zeros("../LevelTileMaps/empty_level",  120, 80)
data = read_level_data("../LevelTileMaps/empty_level")
print(data)
print(len(data))
print(len(data[1]))


