
def add_zeros(file, blockwidth, blockheight):
    with open(file, "w") as file:
        for _ in range(blockheight):
            for _ in range(blockwidth - 1):
                file.write("0,")
            file.write("0\n")
    file.close()


add_zeros("../LevelTileMaps/empty_level",  120, 40)
