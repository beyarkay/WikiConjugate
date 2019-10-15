READ = "_data/europarl_v7_es.txt"
WRITE = "_data/europarl_small_es_"
MAX_LINES = 50_000

count = 0
if input(f"Warning: This will create a lot of files based on {READ}. \n\nContinue? y/[n]: ") == "y":
    with open(READ, "r") as readfile:
        while next(readfile):
            with open(WRITE + str(count) + ".txt", "w") as writefile:
                for j, line in enumerate(readfile):
                    if j < MAX_LINES:
                        writefile.write(line)
                    else:
                        break
            count += 1
