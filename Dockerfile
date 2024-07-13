FROM ubuntu:24.04
WORKDIR /usr/src/app
COPY . .
RUN cp -r llvm-abom llvm-abom-src && cp -r llvm-abom llvm-abom-abom-src && mv openssl openssl-src && cp -r ./openssl-src ./openssl-abom-src && mv curl curl-src && cp -r curl-src curl-abom-src && mv coreutils coreutils-src && cp -r coreutils-src coreutils-abom-src
RUN mkdir clang-llvm openssl openssl-abom curl curl-abom coreutils coreutils-abom llvm-abom-abom
RUN apt update && apt install -y git time clang lld cmake ninja-build libssl-dev autoconf automake libtool autopoint bison gettext gperf texinfo wget xz-utils
# Build llvm-abom
WORKDIR /usr/src/app/llvm-abom/build
RUN cmake -DLLVM_ENABLE_PROJECTS="clang;lld" -DLLVM_ENABLE_RUNTIMES="libcxx;libcxxabi;libunwind" -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=/usr/src/app/clang-llvm -DCMAKE_C_COMPILER=clang -DCMAKE_CXX_COMPILER=clang++ -DLLVM_USE_LINKER=lld -G "Ninja" ../llvm
RUN time -o ../../clang.time ninja install
RUN apt remove -y clang lld libssl-dev && rm -rf /usr/src/app/llvm-abom && mkdir /usr/src/app/llvm-abom
ENV abomc=/usr/src/app/clang-llvm/bin
# Build openssl
WORKDIR /usr/src/app/openssl-src
RUN CC=${abomc}/clang CXX=${abomc}/clang++ LD=${abomc}/ld.lld CFLAGS="-fuse-ld=lld" CPPFLAGS="-fuse-ld=lld" ./Configure --prefix=/usr/src/app/openssl --openssldir=/usr/src/app/openssl/config
RUN time -o ../openssl.time make install
WORKDIR /usr/src/app/openssl-abom-src
RUN CC=${abomc}/clang CXX=${abomc}/clang++ LD=${abomc}/ld.lld CFLAGS="-fabom -fuse-ld=lld" CPPFLAGS="-fabom -fuse-ld=lld" ./Configure --prefix=/usr/src/app/openssl-abom --openssldir=/usr/src/app/openssl-abom/config
RUN time -o ../openssl-abom.time make install
# Build curl
WORKDIR /usr/src/app/curl-src
RUN autoreconf -fi
RUN CC=${abomc}/clang CXX=${abomc}/clang++ LDFLAGS="-L/usr/src/app/openssl/lib64" CFLAGS="-fuse-ld=${abomc}/ld.lld -fPIC" CPPFLAGS="-fuse-ld=${abomc}/ld.lld -fPIC -I/usr/src/app/openssl/include" ./configure --with-openssl --prefix=/usr/src/app/curl
RUN time -o ../curl.time make install
WORKDIR /usr/src/app/curl-abom-src
RUN autoreconf -fi
RUN CC=${abomc}/clang CXX=${abomc}/clang++ LDFLAGS="-L/usr/src/app/openssl-abom/lib64" CFLAGS="-fabom -fuse-ld=${abomc}/ld.lld -fPIC" CPPFLAGS="-fabom -fuse-ld=${abomc}/ld.lld -fPIC -I/usr/src/app/openssl-abom/include" ./configure --with-openssl --prefix=/usr/src/app/curl-abom
RUN time -o ../curl-abom.time make install
# Build coreutils
WORKDIR /usr/src/app/coreutils-src
RUN ./bootstrap
RUN CC=${abomc}/clang CXX=${abomc}/clang++ LD=${abomc}/ld.lld LDFLAGS="-L/usr/src/app/openssl/lib64" CFLAGS="-fuse-ld=${abomc}/ld.lld" CPPFLAGS="-fuse-ld=${abomc}/ld.lld -I/usr/src/app/openssl/include" FORCE_UNSAFE_CONFIGURE=1 ./configure --prefix=/usr/src/app/coreutils --with-openssl=yes
RUN time -o ../coreutils.time make install
WORKDIR /usr/src/app/coreutils-src
RUN ./bootstrap
RUN CC=${abomc}/clang CXX=${abomc}/clang++ LD=${abomc}/ld.lld LDFLAGS="-L/usr/src/app/openssl-abom/lib64" CFLAGS="-fabom -fuse-ld=${abomc}/ld.lld" CPPFLAGS="-fabom -fuse-ld=${abomc}/ld.lld -I/usr/src/app/openssl-abom/include" FORCE_UNSAFE_CONFIGURE=1 ./configure --prefix=/usr/src/app/coreutils-abom --with-openssl=yes
RUN time -o ../coreutils-abom.time make install
# Rebuild llvm-abom
WORKDIR /usr/src/app/llvm-abom-src/build
RUN OPENSSL_ROOT_DIR="/usr/src/app/openssl" cmake -DLLVM_ENABLE_PROJECTS="clang;lld" -DLLVM_ENABLE_RUNTIMES="libcxx;libcxxabi;libunwind" -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=/usr/src/app/llvm-abom -DCMAKE_C_COMPILER=${abomc}/clang -DCMAKE_CXX_COMPILER=${abomc}/clang++ -DCMAKE_C_FLAGS="-I/usr/src/app/openssl/include" -DCMAKE_CXX_FLAGS="-I/usr/src/app/openssl/include" -DLLVM_USE_LINKER=${abomc}/ld.lld -G "Ninja" ../llvm
RUN time -o ../llvm-abom.time ninja install
WORKDIR /usr/src/app/llvm-abom-abom-src/build
RUN mv /usr/bin/ld /usr/bin/ld.bak && ln -s /usr/src/app/clang-llvm/bin/ld.lld /usr/bin/ld
RUN OPENSSL_ROOT_DIR="/usr/src/app/openssl-abom" cmake -DLLVM_ENABLE_PROJECTS="clang;lld" -DLLVM_ENABLE_RUNTIMES="libcxx;libcxxabi;libunwind" -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=/usr/src/app/llvm-abom-abom -DCMAKE_C_COMPILER=${abomc}/clang -DCMAKE_CXX_COMPILER=${abomc}/clang++ -DCMAKE_C_FLAGS="-fabom -I/usr/src/app/openssl-abom/include" -DCMAKE_CXX_FLAGS="-fabom -I/usr/src/app/openssl-abom/include" -DLLVM_USE_LINKER=${abomc}/ld.lld -G "Ninja" ../llvm
RUN time -o ../llvm-abom-abom.time ninja install
RUN rm /usr/bin/ld && mv /usr/bin/ld.bak /usr/bin/ld
WORKDIR /usr/src/app
CMD ["bash", "-c", "'cd /usr/src/app; for x in *.time; do echo \"$x:\" && cat $x && echo; done'"]