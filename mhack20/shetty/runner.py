#!/usr/bin/env python3

import os
import sys
import base64
import string
import secrets
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP


TOKEN_LEN = 16

SUPPORT_PUBKEY = """-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAwVkzaTDBDkV+9HNkFkUF
kSBdzGQRs/PtuoaUY5f5oDoBBEn39SaAfPYbICF9HZV5O1Dku1muUQ5VXECZILlR
3Z+OQfnchBeVCiPEvJlPLoWHDwoiVW/Efbg7MO4FDpyhTfC+kIxntfQQjB/fq3Zu
A0sgA96IFd1tRH0aHDmfq3s59k8w2U18cRuDkBEvWAde74fBh3GX/FT2feuCyv2m
QmHImFYeDIRtYfMGK8D/K1xJ2KneU22VTHGC8Ho+T7p7n2HUS+4N8lGkSAq2npUP
POVlMPMUs7eBqMT+IKmlKZw91kksTLRTUflJpZshNXQ0WDATH/c2uNsBW6fPzYvx
4QIDAQAB
-----END PUBLIC KEY-----"""

SWITCH_MAGIC = '$'


def check_username(s):
    allowed = string.ascii_letters + string.digits
    return len(s) > 0 and all(c in allowed for c in s)


def ensure_dirs(root):
    os.makedirs(os.path.join(root, 'auth'), 0o770, exist_ok=True)
    os.makedirs(os.path.join(root, 'users'), 0o770, exist_ok=True)


def create_user(root, username, password):
    auth_path = os.path.join(root, 'auth', username)
    # TODO: is there a TOCTTOU here?
    if os.path.exists(auth_path):
        return False
    with open(auth_path, 'w') as f:
        f.write(password)
    os.mkdir(os.path.join(root, 'users', username), 0o770)
    return True


def login(root, username, password):
    try:
        with open(os.path.join(root, 'auth', username), 'r') as f:
            return f.read() == password
    except:
        return False


def authenticate(root):
    print('\n--- Authentication ---')
    print('[1] Create a new user')
    print('[2] Log in')
    print('> ', end='')

    action = input()
    if action != '1' and action != '2':
        print('Wrong choice!')
        return None

    print('Username: ', end='')
    username = input()
    if not check_username(username):
        print('Invalid username!')
        return None

    print('Password: ', end='')
    password = input()
    if not password:
        print('Invalid password!')
        return None

    if action == '1':
        if not create_user(root, username, password):
            print('User already exists!')
            return None
    elif action == '2':
        if not login(root, username, password):
            print('Invalid credentials!')
            return None

    return username


def spawn(root, username, binpath, token):
    print(SWITCH_MAGIC, end='')
    user_root = os.path.join(root, 'users', username)
    os.execve(binpath, [binpath, user_root, token], os.environ)


def make_token():
    token = secrets.token_bytes(TOKEN_LEN)
    pubkey = RSA.importKey(SUPPORT_PUBKEY)
    cipher = PKCS1_OAEP.new(pubkey)
    token_enc = cipher.encrypt(token)
    print('Please attach the following to support tickets:')
    print(base64.b64encode(token_enc).decode())
    return token.hex()


def main():
    if len(sys.argv) != 3:
        print(f'Usage: {sys.argv[0]} <storage root> <binary path>', file=sys.stderr)
        exit(1)

    root = sys.argv[1]
    binpath = sys.argv[2]

    ensure_dirs(root)

    token = make_token()

    username = authenticate(root)
    if username:
        spawn(root, username, binpath, token)


if __name__ == '__main__':
    main()
