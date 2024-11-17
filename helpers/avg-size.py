#!/usr/bin/env python3
from sys import argv, exit
from glob import glob
from collections import Counter
from math import ceil

binaries = [('openssl/bin/openssl', 'openssl-abom/bin/openssl'),
            ('curl/bin/curl', 'curl-abom/bin/curl'),
            ('llvm-abom/bin/clang-19', 'llvm-abom-abom/bin/clang-19'),
            ('llvm-abom/bin/lld', 'llvm-abom-abom/bin/lld'),
            ('coreutils/bin/install', 'coreutils-abom/bin/install'),
            ('coreutils/bin/chroot', 'coreutils-abom/bin/chroot'),
            ('coreutils/bin/hostid', 'coreutils-abom/bin/hostid'),
            ('coreutils/bin/timeout', 'coreutils-abom/bin/timeout'),
            ('coreutils/bin/nice', 'coreutils-abom/bin/nice'),
            ('coreutils/bin/who', 'coreutils-abom/bin/who'),
            ('coreutils/bin/users', 'coreutils-abom/bin/users'),
            ('coreutils/bin/pinky', 'coreutils-abom/bin/pinky'),
            ('coreutils/bin/stty', 'coreutils-abom/bin/stty'),
            ('coreutils/bin/df', 'coreutils-abom/bin/df'),
            ('coreutils/bin/stdbuf', 'coreutils-abom/bin/stdbuf'),
            ('coreutils/bin/[', 'coreutils-abom/bin/['),
            ('coreutils/bin/b2sum', 'coreutils-abom/bin/b2sum'),
            ('coreutils/bin/base64', 'coreutils-abom/bin/base64'),
            ('coreutils/bin/base32', 'coreutils-abom/bin/base32'),
            ('coreutils/bin/basenc', 'coreutils-abom/bin/basenc'),
            ('coreutils/bin/basename', 'coreutils-abom/bin/basename'),
            ('coreutils/bin/cat', 'coreutils-abom/bin/cat'),
            ('coreutils/bin/chcon', 'coreutils-abom/bin/chcon'),
            ('coreutils/bin/chgrp', 'coreutils-abom/bin/chgrp'),
            ('coreutils/bin/chmod', 'coreutils-abom/bin/chmod'),
            ('coreutils/bin/chown', 'coreutils-abom/bin/chown'),
            ('coreutils/bin/cksum', 'coreutils-abom/bin/cksum'),
            ('coreutils/bin/comm', 'coreutils-abom/bin/comm'),
            ('coreutils/bin/cp', 'coreutils-abom/bin/cp'),
            ('coreutils/bin/csplit', 'coreutils-abom/bin/csplit'),
            ('coreutils/bin/cut', 'coreutils-abom/bin/cut'),
            ('coreutils/bin/date', 'coreutils-abom/bin/date'),
            ('coreutils/bin/dd', 'coreutils-abom/bin/dd'),
            ('coreutils/bin/dir', 'coreutils-abom/bin/dir'),
            ('coreutils/bin/dircolors', 'coreutils-abom/bin/dircolors'),
            ('coreutils/bin/dirname', 'coreutils-abom/bin/dirname'),
            ('coreutils/bin/du', 'coreutils-abom/bin/du'),
            ('coreutils/bin/echo', 'coreutils-abom/bin/echo'),
            ('coreutils/bin/env', 'coreutils-abom/bin/env'),
            ('coreutils/bin/expand', 'coreutils-abom/bin/expand'),
            ('coreutils/bin/expr', 'coreutils-abom/bin/expr'),
            ('coreutils/bin/factor', 'coreutils-abom/bin/factor'),
            ('coreutils/bin/false', 'coreutils-abom/bin/false'),
            ('coreutils/bin/fmt', 'coreutils-abom/bin/fmt'),
            ('coreutils/bin/fold', 'coreutils-abom/bin/fold'),
            ('coreutils/bin/groups', 'coreutils-abom/bin/groups'),
            ('coreutils/bin/head', 'coreutils-abom/bin/head'),
            ('coreutils/bin/id', 'coreutils-abom/bin/id'),
            ('coreutils/bin/join', 'coreutils-abom/bin/join'),
            ('coreutils/bin/kill', 'coreutils-abom/bin/kill'),
            ('coreutils/bin/link', 'coreutils-abom/bin/link'),
            ('coreutils/bin/ln', 'coreutils-abom/bin/ln'),
            ('coreutils/bin/logname', 'coreutils-abom/bin/logname'),
            ('coreutils/bin/ls', 'coreutils-abom/bin/ls'),
            ('coreutils/bin/md5sum', 'coreutils-abom/bin/md5sum'),
            ('coreutils/bin/mkdir', 'coreutils-abom/bin/mkdir'),
            ('coreutils/bin/mkfifo', 'coreutils-abom/bin/mkfifo'),
            ('coreutils/bin/mknod', 'coreutils-abom/bin/mknod'),
            ('coreutils/bin/mktemp', 'coreutils-abom/bin/mktemp'),
            ('coreutils/bin/mv', 'coreutils-abom/bin/mv'),
            ('coreutils/bin/nl', 'coreutils-abom/bin/nl'),
            ('coreutils/bin/nproc', 'coreutils-abom/bin/nproc'),
            ('coreutils/bin/nohup', 'coreutils-abom/bin/nohup'),
            ('coreutils/bin/numfmt', 'coreutils-abom/bin/numfmt'),
            ('coreutils/bin/od', 'coreutils-abom/bin/od'),
            ('coreutils/bin/paste', 'coreutils-abom/bin/paste'),
            ('coreutils/bin/pathchk', 'coreutils-abom/bin/pathchk'),
            ('coreutils/bin/pr', 'coreutils-abom/bin/pr'),
            ('coreutils/bin/printenv', 'coreutils-abom/bin/printenv'),
            ('coreutils/bin/printf', 'coreutils-abom/bin/printf'),
            ('coreutils/bin/ptx', 'coreutils-abom/bin/ptx'),
            ('coreutils/bin/pwd', 'coreutils-abom/bin/pwd'),
            ('coreutils/bin/readlink', 'coreutils-abom/bin/readlink'),
            ('coreutils/bin/realpath', 'coreutils-abom/bin/realpath'),
            ('coreutils/bin/rm', 'coreutils-abom/bin/rm'),
            ('coreutils/bin/rmdir', 'coreutils-abom/bin/rmdir'),
            ('coreutils/bin/runcon', 'coreutils-abom/bin/runcon'),
            ('coreutils/bin/seq', 'coreutils-abom/bin/seq'),
            ('coreutils/bin/sha1sum', 'coreutils-abom/bin/sha1sum'),
            ('coreutils/bin/sha224sum', 'coreutils-abom/bin/sha224sum'),
            ('coreutils/bin/sha256sum', 'coreutils-abom/bin/sha256sum'),
            ('coreutils/bin/sha384sum', 'coreutils-abom/bin/sha384sum'),
            ('coreutils/bin/sha512sum', 'coreutils-abom/bin/sha512sum'),
            ('coreutils/bin/shred', 'coreutils-abom/bin/shred'),
            ('coreutils/bin/shuf', 'coreutils-abom/bin/shuf'),
            ('coreutils/bin/sleep', 'coreutils-abom/bin/sleep'),
            ('coreutils/bin/sort', 'coreutils-abom/bin/sort'),
            ('coreutils/bin/split', 'coreutils-abom/bin/split'),
            ('coreutils/bin/stat', 'coreutils-abom/bin/stat'),
            ('coreutils/bin/sum', 'coreutils-abom/bin/sum'),
            ('coreutils/bin/sync', 'coreutils-abom/bin/sync'),
            ('coreutils/bin/tac', 'coreutils-abom/bin/tac'),
            ('coreutils/bin/tail', 'coreutils-abom/bin/tail'),
            ('coreutils/bin/tee', 'coreutils-abom/bin/tee'),
            ('coreutils/bin/test', 'coreutils-abom/bin/test'),
            ('coreutils/bin/touch', 'coreutils-abom/bin/touch'),
            ('coreutils/bin/tr', 'coreutils-abom/bin/tr'),
            ('coreutils/bin/true', 'coreutils-abom/bin/true'),
            ('coreutils/bin/truncate', 'coreutils-abom/bin/truncate'),
            ('coreutils/bin/tsort', 'coreutils-abom/bin/tsort'),
            ('coreutils/bin/tty', 'coreutils-abom/bin/tty'),
            ('coreutils/bin/uname', 'coreutils-abom/bin/uname'),
            ('coreutils/bin/unexpand', 'coreutils-abom/bin/unexpand'),
            ('coreutils/bin/uniq', 'coreutils-abom/bin/uniq'),
            ('coreutils/bin/unlink', 'coreutils-abom/bin/unlink'),
            ('coreutils/bin/uptime', 'coreutils-abom/bin/uptime'),
            ('coreutils/bin/vdir', 'coreutils-abom/bin/vdir'),
            ('coreutils/bin/wc', 'coreutils-abom/bin/wc'),
            ('coreutils/bin/whoami', 'coreutils-abom/bin/whoami'),
            ('coreutils/bin/yes', 'coreutils-abom/bin/yes')]

def main(results_dir: str) -> None:
    totals = Counter()
    items = Counter()
    for file in glob(f"{results_dir}/*.txt"):
        with open(file, "r") as f:
            lines = f.readlines()
            for pair in binaries:
                for binary in pair:
                    for line in lines:
                        if line.startswith(binary + ' '):
                            totals[binary] += int(line.split()[-1])
                            items[binary] += 1
    print(f"{'Binary':<40}{'Samples':<15}{'Average Size':<20}Increase\n")
    for pair in binaries:
        size_0 = ceil(totals[pair[0]] / items[pair[0]])
        size_1 = ceil(totals[pair[1]] / items[pair[1]])
        print(f"{pair[0]:<40}{items[pair[0]]:<15}{size_0:<20}")
        print(f"{pair[1]:<40}{items[pair[1]]:<15}{size_1:<20}{size_1-size_0:<8}({size_1/size_0-1:.2%})\n")
            

if __name__ == "__main__":
    if (len(argv) != 2):
        print(f"Usage: {argv[0]} <results_dir>")
        exit(1)
    main(argv[1])