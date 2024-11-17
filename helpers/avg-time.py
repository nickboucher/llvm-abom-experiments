#!/usr/bin/env python3
from sys import argv, exit
from glob import glob
from collections import Counter
from math import ceil
from re import search

builds = [('coreutils.time', 'coreutils-abom.time')]

def main(results_dir: str) -> None:
    totals = Counter()
    items = Counter()
    for file in glob(f"{results_dir}/*.txt"):
        with open(file, "r") as f:
            lines = f.readlines()
            for pair in builds:
                for build in pair:
                    for idx, line in enumerate(lines):
                        if line.startswith(build):
                            time = search(r"(\d*):?(\d+):([\d\.]+)elapsed", lines[idx+1])
                            hours = 0 if time.group(1) == "" else int(time.group(1))
                            seconds = hours * 60 * 60 + int(time.group(2)) * 60 + float(time.group(3))
                            totals[build] += seconds
                            items[build] += 1
    print(f"{'Build':<40}{'Samples':<15}{'Average Time (s)':<20}Increase\n")
    for pair in builds:
        size_0 = totals[pair[0]] / items[pair[0]]
        size_1 = totals[pair[1]] / items[pair[1]]
        print(f"{pair[0]:<40}{items[pair[0]]:<15}{size_0:<20.2f}")
        print(f"{pair[1]:<40}{items[pair[1]]:<15}{size_1:<20.2f}{size_1-size_0:<8.2f}({size_1/size_0-1:.2%})\n")
            

if __name__ == "__main__":
    if (len(argv) != 2):
        print(f"Usage: {argv[0]} <results_dir>")
        exit(1)
    main(argv[1])