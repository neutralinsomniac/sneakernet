#!/usr/bin/env python3

import math
import sys
import argparse
from bitstring import BitArray, BitStream, ConstBitStream

parser = argparse.ArgumentParser()
parser.add_argument("-d", "--decode", help="file to decode into", nargs='?')
parser.add_argument("dictionary")
parser.add_argument("file_to_encode_or_decode")

args = parser.parse_args()

with open(args.dictionary, "r") as f:
    words = f.read()

dictionary = {}
index = 0
for word in words.split():
    dictionary[index] = word
    dictionary[word] = index
    index += 1

num_encoded_bits_per_word = int(math.log2(len(dictionary)/2))

if not args.decode:
    s = ConstBitStream(filename=args.file_to_encode_or_decode)

    num_bits_to_read = num_encoded_bits_per_word
    sys.stderr.write("able to encode {} bits per word\n".format(num_encoded_bits_per_word))

    counter = 0

    while (len(s) - s.pos) > 0:
        if (len(s) - s.pos) <= num_encoded_bits_per_word:
            num_bits_to_read = len(s) - s.pos
        index = s.read(num_bits_to_read).uint
        print(dictionary[index] + " ", end='')
        if (counter % 5) == 4:
            print("")
        counter += 1

    print("{}".format(num_bits_to_read))
    sys.stderr.write("encoded {} bytes to {} words\n".format(int(len(s) / 8), counter))
else:
    with open(args.file_to_encode_or_decode, "r") as f:
        words_to_decode = f.read()

    s = BitArray()
    words = words_to_decode.split()[0:-2]
    for word in words:
        index = dictionary[word]
        s.append(BitArray('uint:{}={}'.format(num_encoded_bits_per_word, index)))

    word = words_to_decode.split()[-2]
    index = dictionary[word]
    num_bits_to_encode = int(words_to_decode.split()[-1])
    s.append(BitArray('uint:{}={}'.format(num_bits_to_encode, index)))
    with open(args.decode, "wb") as f:
        f.write(s.tobytes())
