file = "poi_names.txt"

def readtxt(file):
    f = open(file, 'r')
    for line in f:
        print line.readline()


if __name__ == '__main__':
    readtxt(file)