import argparse
import string
import sys
import os
import unicodedata

def _normalize(s: str) -> str:
    return unicodedata.normalize('NFKC', s).strip()


def load_common(path):
    """Load common passwords file and return a set of normalized, lower-cased entries."""
    if not path or not os.path.exists(path):
        return set()
    with open(path, encoding='utf-8', errors='ignore') as f:
        return set(_normalize(line).lower() for line in f if line.strip())


def check_password(pwd, common_set, min_length=6):
    reasons = []
    if len(pwd) < min_length:
        reasons.append(f"too short (<{min_length})")
    if not any(c.islower() for c in pwd):
        reasons.append("missing lowercase")
    if not any(c.isupper() for c in pwd):
        reasons.append("missing uppercase")
    if not any(c.isdigit() for c in pwd):
        reasons.append("missing digit")
    if not any(c in string.punctuation for c in pwd):
        reasons.append("missing special char")

    pwd_norm = _normalize(pwd).lower()
    if pwd_norm in common_set:
        reasons.append("common password")
    return reasons


def main():
    p = argparse.ArgumentParser(description='Check password strength from a file (one password per line)')
    p.add_argument('input_file', help='Input file containing passwords (one per line)')
    p.add_argument('--common', '-c', help='Common passwords file to check against (default: common_passwords.txt)', default='common_passwords.txt')
    p.add_argument('--both-common', '-b', help='If set, merge the specified common file with bundled common_passwords.txt for comparison', action='store_true')
    p.add_argument('--min-length', '-m', help='Minimum password length (default: 6)', type=int, default=6)
    args = p.parse_args()

    if not os.path.exists(args.input_file):
        print('Input file not found:', args.input_file, file=sys.stderr)
        sys.exit(2)

    # load user-specified common list
    common = load_common(args.common)
    # if requested, merge with bundled default common file
    if args.both_common and args.common != 'common_passwords.txt':
        common |= load_common('common_passwords.txt')

    total = 0
    weak = 0
    with open(args.input_file, encoding='utf-8', errors='ignore') as f:
        for lineno, line in enumerate(f, start=1):
            pwd = line.rstrip('\n')
            if not pwd:
                continue
            total += 1
            reasons = check_password(pwd, common, min_length=args.min_length)
            if reasons:
                weak += 1
                print(f'[WEAK] line {lineno}: {pwd} -> {", ".join(reasons)}')
            else:
                print(f'[OK]   line {lineno}: {pwd}')

    print('\nSummary:')
    print(' Total checked:', total)
    print(' Weak found :', weak)
    if weak:
        sys.exit(1)


if __name__ == '__main__':
    main()
