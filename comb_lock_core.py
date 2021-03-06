#!/usr/bin/env python
# -*- coding: utf-8 -*-

'Core functions of Comb Lock, encrypt & save in a text file, read from a text file & decrypt.'

__author__ = 'Nero Song'

from Crypto.Cipher import AES
from Crypto.Hash import MD5
from binascii import b2a_hex, a2b_hex
from Crypto import Random
import os

# padding
BS = AES.block_size
pad = lambda s: s + (BS - len(s) % BS) * chr(0).encode('utf-8')


def md5(text):
    hash = MD5.new()
    hash.update(text.encode('utf-8'))
    return hash.hexdigest()


class Core(object):
    def __init__(self, key):
        # AES-256 needs 32 bytes key length
        self.key = md5(key).encode('utf-8')
        self.mode = AES.MODE_CBC

    def encrypt(self, plaint_text):
        iv = Random.new().read(BS)
        cryptor = AES.new(self.key, self.mode, iv)
        plaint_text = b2a_hex(bytes(plaint_text.encode('utf-8')))
        clipher_text = cryptor.encrypt(pad(plaint_text))
        encrypted_text = b2a_hex(iv + clipher_text)
        return encrypted_text.decode("utf-8")

    def decrypt(self, encrypted_text):
        clipher_text = a2b_hex(encrypted_text)
        iv = clipher_text[0:BS]
        clipher_text = clipher_text[BS:len(clipher_text)]
        cryptor = AES.new(self.key, self.mode, iv)
        plaint_text = cryptor.decrypt(clipher_text)
        plaint_text = plaint_text.rstrip(chr(0).encode('utf-8'))
        plaint_text = a2b_hex(plaint_text)
        return plaint_text.decode("utf-8")

    def add_record(self, secret, note, loctation='./Lock'):
        if (os.path.isfile(loctation) and os.access(loctation, os.R_OK)
                and os.access(loctation, os.W_OK)):
            with open(loctation, 'r+') as f:
                lines = f.readlines()
                last_line = lines[-1].strip()
                if self.decrypt(last_line) != 'success':
                    return 'The root password is wrong!'
                lines.pop()
                lines.append(self.encrypt(secret) + ',' + self.encrypt(note))
                lines.append(last_line)
                f.seek(0)
                f.truncate()
                # print(lines)
                for i in lines:
                    i = i.strip()
                    f.write(i + '\n')

            return 'The new record has been add successfully!'
        else:
            return 'The Lock file is unavailable. Please check the path and permission to read & write.'

    def read_records(self, loctation='./Lock'):
        if (os.path.isfile(loctation) and os.access(loctation, os.R_OK)):
            with open(loctation, 'r') as f:
                lines = f.readlines()
                last_line = lines[-1]
                if self.decrypt(last_line.strip()) != 'success':
                    return 'The root password is wrong!'
                lines.pop()
                records = []
                for i in lines:
                    p = i.find(',')
                    temp_secret = self.decrypt(i[0:p])
                    temp_note = self.decrypt(
                        i[p + 1:len(i) -
                          1])  # There's a line break at the end, so minus 1
                    records.append([temp_secret, temp_note])
                return records
        else:
            return 'The Lock file is unavailable. Please check the path and permission to read.'

    def add_new_document(self, loctation):
        if (not os.path.isfile(loctation)):
            with open(loctation, 'w+') as f:
                f.write(self.encrypt('success'))
            return 'The new encrypted file has been created successfully!'
        else:
            return 'This Lock file has already existed. Please rename it.'


# bash test
if __name__ == "__main__":
    import sys
    core = Core(sys.argv[1])
    if sys.argv[2] == 'add':
        if (len(sys.argv) == 5):
            ans = core.add_record(sys.argv[3], sys.argv[4])
        else:
            ans = core.add_record(sys.argv[3], sys.argv[4], sys.argv[5])
        print(ans)
    if sys.argv[2] == 'read':
        if (len(sys.argv) == 3):
            ans = core.read_records()
        else:
            ans = core.read_records(sys.argv[3])
        print(ans)
    if sys.argv[2] == 'new':
        ans = core.add_new_document(sys.argv[3])
        print(ans)