import sys
from os import walk, listdir
import json

def help():
    print("""
        Usage: python formatter.py <directory of Discord API json scraped files> <output file to write transcript>
        """)
    exit(0)

def main(argv):
    if len(argv) != 3:
        help()
    dirname = argv[1]
    files = []
    messages = []
    outpath = argv[2]
    print(f"Dirname: {dirname}")
    print(f"{listdir(dirname)}")
    for (dirpath, dirnames, filenames) in walk(dirname):
        print(f"Dirpath {dirpath}.\nDirnames {dirnames}.\nFilenames {filenames}.")
        files.extend(list(map(lambda x: dirpath+x, filenames)))
        # Earliest dates first
    files = sorted(files)
    print(f"Reading these files:\n{files} ")
    print(f"Writing to {outpath}.")
    with open(outpath, 'w') as outputfile:
        for f in files:
            if not f.endswith(".json"):
                continue
            print(f"Reading file {f}.")
            with open(f, 'r') as jsonfile:
                try:
                    data = json.load(jsonfile)
                except Exception:
                    print("Invalid JSON, continuing.")
                    continue
                for msg in data:
                    try:
                        username = msg["author"]["username"]
                    except KeyError:
                        username = "(unknown)"
                    content = msg["content"]
                    outputfile.write(f"{username}\t\t{content}\n")



if __name__ == "__main__":
    main(sys.argv)
