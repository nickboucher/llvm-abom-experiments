#!/usr/bin/env python3
import matplotlib.pyplot as plt
from sys import argv, exit
from csv import DictReader

def main(results: str) -> None:
    print(f"Reading results from {results}... ", end="", flush=True)
    with open(results, "r") as f:
        reader = DictReader(f)
        results = list(reader)


    deps = [2 * int(row['deps']) for row in results]
    false_positive_rate = [float(row['false_positive_rate']) for row in results]

    plt.figure(figsize=(10, 6))
    plt.scatter(deps, false_positive_rate, color='b')  # Use scatter plot to remove lines between points
    plt.xscale('log')  # Set x-axis to log scale
    plt.yscale('log', base=2)  # Set y-axis to log_2 scale
    plt.xlabel('Source Code File Dependencies')
    plt.ylabel('False Positive Rate')
    plt.title('Experimental False Positive Rates\n')
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    if (len(argv) != 2):
        print(f"Usage: {argv[0]} artificial_results.csv")
        exit(1)
    main(argv[1])