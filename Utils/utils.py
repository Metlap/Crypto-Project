import secrets
import random
import hashlib
import numpy


class Utils:
    # static method to generate random hexadecimal numbers
    @staticmethod
    def rand_160():
        return random.getrandbits(160)

    def rand_320():
        return random.getrandbits(320)

    def concat_hash(part1, part2, isint=1):
        if isint:
            return int(
                hashlib.sha1(
                    (str(part1) + str(part2)).encode("utf8")).hexdigest(), 16
            )
        else:
            return 0

    def xor_two_str(a, b):
        return ''.join([hex(ord(a[i % len(a)]) ^ ord(b[i % (len(b))]))[2:] for i in range(max(len(a), len(b)))])
