import logging
import json

from flask import request, jsonify;

from codeitsuisse import app;
from wordsegment import load, segment
import wordninja

from random import randrange
import string
import math

logger = logging.getLogger(__name__)

class CaesarCipher(object):
    def __init__(self, message=None, encode=False, decode=False, offset=False,
                 crack=None, verbose=None, alphabet=None):

        self.message = message
        self.encode = encode
        self.decode = decode
        self.offset = offset
        self.verbose = verbose
        self.crack = crack
        self.alphabet = alphabet

        # http://en.wikipedia.org/wiki/Letter_frequency
        self.frequency = {
            'a': 0.08167,
            'b': 0.01492,
            'c': 0.02782,
            'd': 0.04253,
            'e': 0.130001,
            'f': 0.02228,
            'g': 0.02015,
            'h': 0.06094,
            'i': 0.06966,
            'j': 0.00153,
            'k': 0.00772,
            'l': 0.04025,
            'm': 0.02406,
            'n': 0.06749,
            'o': 0.07507,
            'p': 0.01929,
            'q': 0.00095,
            'r': 0.05987,
            's': 0.06327,
            't': 0.09056,
            'u': 0.02758,
            'v': 0.00978,
            'w': 0.02360,
            'x': 0.00150,
            'y': 0.01974,
            'z': 0.00074}

        
        if alphabet is None:
            self.alphabet = tuple(string.ascii_lowercase)

    def cipher(self):
        
        if self.offset is False:
            self.offset = randrange(5, 25)

        # Cipher
        ciphered_message_list = list(self.message)
        for i, letter in enumerate(ciphered_message_list):
            if letter.isalpha():

                if letter.isupper():
                    alphabet = [character.upper()
                                for character in self.alphabet]
                else:
                    alphabet = self.alphabet

                value = alphabet.index(letter)
                cipher_value = value + self.offset
                if cipher_value > 25 or cipher_value < 0:
                    cipher_value = cipher_value % 26
                ciphered_message_list[i] = alphabet[cipher_value]
        self.message = ''.join(ciphered_message_list)
        return self.message

    def calculate_entropy(self, entropy_string):
        total = 0
        for char in entropy_string:
            if char.isalpha():
                prob = self.frequency[char.lower()]
                total += - math.log(prob) / math.log(2)
        return total

    @property
    def cracked(self):
        entropy_values = {}
        attempt_cache = {}
        message = self.message
        for i in range(25):
            self.message = message
            self.offset = i * -1
            test_cipher = self.cipher()
            entropy_values[i] = self.calculate_entropy(test_cipher)
            attempt_cache[i] = test_cipher

        sorted_by_entropy = sorted(entropy_values, key=entropy_values.get)
        self.offset = sorted_by_entropy[0] * -1
        cracked_text = attempt_cache[sorted_by_entropy[0]]
        self.message = cracked_text


        return cracked_text

    @property
    def encoded(self):
        return self.cipher()

    @property
    def decoded(self):
        self.offset = self.offset * -1
        return self.cipher()

def solve(data):
    res = []
    load()
    for dic in data:
        ans = {}
        i,s = dic['id'],dic['encryptedText']
        ans['id']=i
        cip = CaesarCipher(s)
        ori = cip.cracked
        nn,cnt,l,ind = 0,0,0,0
        for x in range(len(s)-1):
            for y in range(x+1,len(s)):
                tmp=ori[x:y+1]
                cur=y-x+1
                if tmp==tmp[::-1]:
                    if cur>l:
                        ind,l=x,cur
                    nn+=1
        has=[]
        for c in ori[ind:ind+l]:
            has.append(ord(c))
        ans['encryptionCount'] = 0
        tar=ord(s[0])
        cnt=ord(ori[0])
        if l==0:
            for t in range(100):
                if cnt==tar:
                    ans['encryptionCount'] = t
                    break
                cnt+=cnt
                if cnt>122:
                    cnt=(cnt-123)%26+97
        else:
            for t in range(100):
                print(cnt,t)
                if cnt==tar:
                    ans['encryptionCount'] = t
                    break
                print(has,nn)
                tmp=sum(has)+nn
                for i in range(len(has)):
                    has[i]+=tmp
                    if has[i]>122:
                        has[i]=(has[i]-123)%26+97
                cnt+=tmp
                if cnt>122:
                    cnt=(cnt-123)%26+97
        s=' '.join(wordninja.split(ori))
        ans['originalText'] = s
        res.append(ans)
    return res

@app.route('/bored-scribe', methods=['POST'])
def bored_scribe():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    result=solve(data)
    logging.info("My result :{}".format(result))
    return jsonify(result)