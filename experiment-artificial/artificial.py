#!/usr/bin/env python3
from subprocess import run
from random import randint
from hashlib import shake_128
from sys import argv, exit
from random import choices
from string import ascii_lowercase
from os import makedirs
from os.path import join

llvm = '/usr/src/app/llvm-abom/build/bin'

def abom_hash(data) -> str:
    return shake_128(data).hexdigest(5)[:9]

def random_abom_hash() -> str:
    return abom_hash(randint(0, 2**36).to_bytes(5, 'little'))

def main(directory: str, dependency_count: int, collision_attempts: int):
    print(f'Generating C solution in {directory} with {dependency_count} dependencies...', end=' ')
    # Generate artificial C solution
    try:
        makedirs(join(directory, 'src'))
        makedirs(join(directory, 'include'))
        makedirs(join(directory, 'bin'))
    except FileExistsError:
        print('Directory already exists')
        exit(1)
    deps = set()
    for i in range(dependency_count):
        while True:
            name = ''.join(choices(ascii_lowercase, k=8))
            if name not in deps:
                deps.add(name)
                break
        with open(join(directory, f'src/{name}.c'), 'w') as f:
            f.write(f'void {name}() {{}}')
        with open(join(directory, f'include/{name}.h'), 'w') as f:
            f.write(f'#ifndef {name.upper()}_H\n#define {name.upper()}_H\nvoid {name}();\n#endif')
    with open(join(directory, f'src/abom{dependency_count}.c'), 'w') as f:
        for dep in deps:
            f.write(f'#include "{dep}.h"\n')
        f.write('\nint main() {\n   return 0;\n}\n')
    print('Done')
    # Compile artificial C solution
    print(f'Compiling generated C solution with ABOM...', end=' ')
    binary = f'{directory}/bin/abom{dependency_count}'
    run(f"{llvm}/clang "
        f"-fabom "
        f"-fuse-ld={llvm}/lld "
        f"-I {directory}/include "
        f"-o {binary} "
        f"{directory}/src/abom{dependency_count}.c "
        f"{' '.join([f'{directory}/src/{dep}.c' for dep in deps])}",
        shell=True)
    print('Done')
    print('Generated ABOM details:')
    result = run(f'{llvm}/llvm-readobj --abom {binary}', capture_output=True, shell=True)
    # Calculate true set of hahes
    print('Checking ABOM for true set of hashes...', end=' ')
    true_hashes = set()
    for dep in deps:
        c_hash = abom_hash(open(f'{directory}/src/{dep}.c', 'rb').read())
        h_hash = abom_hash(open(f'{directory}/include/{dep}.h', 'rb').read())
        true_hashes.add(hash)
    # Validate ABOM contains true hashes
    true_present = 0
    true_absent = 0
    for hash in true_hashes:
        result = run(f'{llvm}/llvm-abom-check {binary} {hash}',
                      capture_output=True, shell=True)
        if result.stdout.startswith(b'Present'):
            true_present += 1
        elif result.stdout.startswith(b'Absent'):
            true_absent += 1
        else:
            print(f'Error: {hash}')
            exit(1)
    print('Done')
    print(f'===\nTrue Hashes Present: {true_present}\n'
          f'True Hahes Absent: {true_absent}\n'
          f'True Hashes Success Rate: {true_present / len(true_hashes):.0%}\n===')
    # Test for false positives
    print(f'Generating {collision_attempts} random hashes to test for false positives...', end=' ')
    false_hashes = set()
    false_present = 0
    false_absent = 0
    for i in range(collision_attempts):
        while True:
            hash = random_abom_hash()
            if hash not in true_hashes and hash not in false_hashes:
                false_hashes.add(hash)
                break
        result = run(f'{llvm}/llvm-abom-check {binary} {hash}',
                     capture_output=True, shell=True)
        if result.stdout.startswith(b'Present'):
            false_present += 1
        elif result.stdout.startswith(b'Absent'):
            false_absent += 1
        else:
            print(f'Error: {hash}')
            exit(1)
    print('Done')
    print(f'===\nFalse Hashes Present: {false_present}\n'
          f'False Hashes Absent: {false_absent}\n'
          f'False Hashes Success Rate: {false_absent / len(false_hashes):.0%}\n===')
    print('Experiment Complete.')

if __name__ == '__main__':
    if len(argv) != 4:
        print(f'Usage: {argv[0]} <directory> <dependency_count> <collision_attempts>')
        exit(1)
    else:
        main(argv[1], int(argv[2]), int(argv[3]))