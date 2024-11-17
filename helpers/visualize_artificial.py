#!/usr/bin/env python3
from sys import argv, exit
from glob import glob
from re import search
from csv import DictWriter

class ArtificialResult:
    def __init__(self, deps: int, attempts: int, iter: int, abom_filters: int, abom_bytes: int, true_present: int, true_absent: int, false_present: int, false_absent: int):
        self.deps = deps
        self.attempts = attempts
        self.iter = iter
        self.abom_filters = abom_filters
        self.abom_bytes = abom_bytes
        self.true_present = true_present
        self.true_absent = true_absent
        self.false_present = false_present
        self.false_absent = false_absent
        self.true_success_rate = true_present / (true_present + true_absent)
        self.false_positive_rate = false_present / (false_present + false_absent)

    def __str__(self):
        return f"deps: {self.deps}, attempts: {self.attempts}, iter: {self.iter}, abom_filters: {self.abom_filters}, abom_bytes: {self.abom_bytes}, true_present: {self.true_present}, true_absent: {self.true_absent}, true_success_rate: {self.true_success_rate}, false_present: {self.false_present}, false_absent: {self.false_absent}, false_positive_rate: {self.false_positive_rate}"

    def __repr__(self):
        return str(self)

def main(results_dir: str) -> None:
    print(f"Reading results from {results_dir}... ", end="", flush=True)
    results = []
    for txt in glob(f"{results_dir}/*-*-*.txt"):
        with open(txt, "r") as f:
            contents = f.read()
            if contents.rstrip(" \n").endswith("Experiment Complete."):
                deps, attempts, iter = [int(x) for x in txt.split("/")[-1].rstrip(".txt").split("-")]
                abom_filters = int(search(r"ABOM num filters: (\d+)", contents).group(1))
                abom_bytes = int(search(r"ABOM blob size: (\d+)", contents).group(1))
                true_present = int(search(r"True Hashes Present: (\d+)", contents).group(1))
                true_absent = int(search(r"True Hashes Absent: (\d+)", contents).group(1))
                false_present = int(search(r"False Hashes Present: (\d+)", contents).group(1))
                false_absent = int(search(r"False Hashes Absent: (\d+)", contents).group(1))
                result = ArtificialResult(deps=deps, attempts=attempts, iter=iter,
                                          abom_filters=abom_filters, abom_bytes=abom_bytes,
                                          true_present=true_present, true_absent=true_absent,
                                          false_present=false_present, false_absent=false_absent)
                results.append(result)
    print(f"Done\nLocated {len(results)} valid experiment results.", flush=True)
    out = f"{results_dir}/artificial_results.csv"
    print(f"Writing results to {out}... ", end="", flush=True)
    with open(out, "w") as f:
        writer = DictWriter(f, fieldnames=vars(results[0]).keys())
        writer.writeheader()
        for result in results:
            writer.writerow(vars(result))
    print("Done", flush=True)

if __name__ == "__main__":
    if (len(argv) != 2):
        print(f"Usage: {argv[0]} <results_dir>")
        exit(1)
    main(argv[1])