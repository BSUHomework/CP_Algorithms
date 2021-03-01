#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@author: soliva
@Site: 
@file: submask.py
@time: 2021/2/9
@desc:
'''
from functools import reduce
import collections
words = ["aaaa", 'asas', 'able', 'ability', 'actt', 'acto', 'access']
puzzles = ['aboveyz', 'abrodyz', 'abslute', 'absoryz', 'actresz', 'gaswxyz']


def findNumOfValidWords(words, puzzles):
    scores = collections.Counter(
        reduce(lambda s, c: s | 1 << (ord(c) - ord('a')), w, 0) for w in words)
    ans = []
    print(scores)
    for p in puzzles:
        score = 0
        required_bit = 1 << (ord(p[0]) - ord('a'))

        mask = submask = reduce(lambda s, c: s | 1 <<
                                (ord(c) - ord('a')), p, 0)

        # enumerate all masks in descending order without repetion
        while submask:
            if submask & required_bit:
                score += scores[submask]

            submask = (submask - 1) & mask

        ans.append(score)
    return ans


findNumOfValidWords(words, puzzles)
