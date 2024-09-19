FROM ubuntu:24.04
WORKDIR /usr/src/app
COPY llvm-abom llvm-abom
# Build llvm-abom
WORKDIR /usr/src/app/llvm-abom/build
RUN apt update && apt install -y clang lld cmake ninja-build libssl-dev python3
RUN cmake -DLLVM_ENABLE_PROJECTS="clang;lld" -DLLVM_ENABLE_RUNTIMES="libcxx;libcxxabi;libunwind" -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=/usr/src/app/llvm-abom/build/bin -DCMAKE_C_COMPILER=clang -DCMAKE_CXX_COMPILER=clang++ -DLLVM_USE_LINKER=lld -G "Ninja" ../llvm
RUN ninja install
RUN apt remove -y clang lld libssl-dev && mv /usr/src/app/llvm-abom/build/bin /usr/src/app && rm -rf /usr/src/app/llvm-abom && mkdir /usr/src/app/llvm-abom/build && mv /usr/src/app/bin /usr/src/app/llvm-abom/build
# Run experiment
COPY artificial.py artificial.py
RUN mkdir experiment
ENTRYPOINT [ "./artificial.py", "experiment" ]