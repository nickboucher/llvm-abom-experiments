# llvm-abom Experiments

This repo contains a set of experiments to test the build performance of the ABOM llvm fork, via docker.

## Cloning

This repo uses submodules. To clone the repo, use the following command:

```bash
git clone --recurse-submodules -j8 --shallow-submodules https://github.com/nickboucher/llvm-abom-experiments.git
```

## Usage

This repository contains 2 experiments: `real` and `artificial`. The real experiment builds a collection of real-world applications with ABOMs to measure build performance, while the artificial experiment builds a collection of generated artifical programs designed to validate the correctness and errors rates of ABOMs.

### Real Experiment

To run these experiments, build the docker image and run the container. The container will output the results to the console. Experiments are run during the build process.

```bash
docker build --no-cache -t llvm-abom-experiment-real experiment-real/
docker run llvm-abom-experiment-real
```

These experiments were initially run on an Ubuntu 24.04 VM with 4 vCores and 32GB of RAM (Azure E4as_v5 SKU).

### Artificial Experiment

To run these experiments, build the docker image and run the container. The container will output the results to the console. Experiments are run during container runtime.

```bash
docker build --no-cache -t llvm-abom-experiment-artificial experiment-artificial/
docker run llvm-abom-experiment-artificial
```

These experiments were initially run on an Ubuntu 24.04 VM with 4 vCores and 32GB of RAM (Azure E4as_v5 SKU).