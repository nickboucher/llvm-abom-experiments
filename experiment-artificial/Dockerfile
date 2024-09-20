FROM ubuntu:24.04
WORKDIR /usr/src/app
ARG low_memory=0
RUN if [ "${low_memory}" = "0" ]; then export LOW_MEMORY=""; else export LOW_MEMORY="-DLLVM_PARALLEL_TABLEGEN_JOBS=1 -DLLVM_PARALLEL_LINK_JOBS=1"; fi
COPY llvm-abom llvm-abom
# Build llvm-abom
WORKDIR /usr/src/app/llvm-abom/build
RUN apt update && apt install -y clang lld cmake git ninja-build libssl-dev python3 python3-tqdm && \
    cmake -DLLVM_ENABLE_PROJECTS="clang;lld" -DLLVM_ENABLE_RUNTIMES="libcxx;libcxxabi;libunwind" -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=/usr/src/app/llvm-abom/build/bin -DCMAKE_C_COMPILER=clang -DCMAKE_CXX_COMPILER=clang++ -DLLVM_USE_LINKER=lld $LOW_MEMORY -G "Ninja" ../llvm && \
    ninja install && \
    apt remove -y clang lld libssl-dev && \
    apt -y autoremove && \
    apt clean && \
    mv /usr/src/app/llvm-abom/build/bin /usr/src/app && \
    rm -rf /usr/src/app/llvm-abom && \
    mkdir -p /usr/src/app/llvm-abom/build && \
    mv /usr/src/app/bin /usr/src/app/llvm-abom/build && \
    mkdir -p /usr/src/app/experiment
# Run experiment
WORKDIR /usr/src/app
COPY artificial.py artificial.py
ENTRYPOINT [ "./artificial.py", "/usr/src/app/experiment/" ]