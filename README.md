# llvm-abom Experiments

This repo contains a set of experiments to test the build performance of the ABOM llvm fork, via docker.

## Cloning

This repo uses submodules. To clone the repo, use the following command:

```bash
git clone --recurse-submodules -j8 --shallow-submodules https://github.com/nickboucher/llvm-abom-experiments.git
```

## Usage

To run these experiments, build the docker image and run the container. The container will output the results to the console. Experiments are run during the build process.

```bash
docker build --no-cache -t llvm-abom-experiments .
docker run llvm-abom-experiments
```

These experiments were initially run on an Ubuntu 24.04 VM with 4 vCores and 32GB of RAM (Azure E4as_v5 SKU).