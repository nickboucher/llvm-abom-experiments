# llvm-abom Experiments

This repo contains a set of experiments to test the build performance of the ABOM llvm fork, via docker.

## Usage

To run these experiments, build the docker image and run the container. The container will output the results to the console. Experiments are run during the build process.

```bash
docker build --no-cache -t llvm-abom-experiments .
docker run llvm-abom-experiments
```

These experiments were initially run on an Ubuntu 24.04 VM with 4 vCores and 16GB of RAM (Azure B4as_v2 SKU).