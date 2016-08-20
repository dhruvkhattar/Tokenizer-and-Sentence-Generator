#! /usr/bin/env python
#######################################
#     Author : Dhruv Khattar         #
#####################################

import pdb
import re
import random

# Various Regex
EMOJI = r'([\:\;\=8B][\-oO\*\'\"]?[\/\)\]\(\[dDpP\\\}\{\@\#\|\]]{1,2}|\<3)'
URL = r'(http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+)'
BRACKETS = r'([\(\)\"\[\]\{\}])'
LCORNER = r'^([\'\*\:\$\%\-]*)([\'\*\:\$\%\-])'
RCORNER = r'([\'\*\:\%\$\-])([\'\*\:\%\$\-]*)$'
M = r'([^\=\&\+]*)([\=\&\+])([^\=\&\+]*)'
PUNCTUATION = r'([\,\!\.\?])+$'


def generateSentences(tokens, n):
    ''' Function for generating sentences by predicting the next word using the previous n-gram.'''
    
    sentence = ''
    # Unigram: Random Sentence
    if n == 1:
        for i in xrange(10):
            sentence = sentence + ' ' + random.choice(tokens)
        print '1-gram : ' +  sentence.encode('utf-8')
        return

    ngrams = []
    c = []
    for i in xrange(n-1):
        c.append('<s>')
    # Creating n-grams
    for token in tokens:
        if token != '':
            c.append(token)
            c.pop(0)
            string = ''
            for i in xrange(n-1):
                string = string + c[i] + ' '
            ngrams.append(string.strip())
    # Choosing random n-gram as starting n-gram
    phrase = random.choice(ngrams)
    c = phrase.split()[-1]
    sentence = sentence + phrase
    # Checking if the last token is the sentence-ending token
    limit = 0
    while c != '</s>' and limit <= 15:
        limit += 1
        flag = 0
        count = {}
        p = []
        for i in xrange(n-1):
            p.append('<s>')
        for token in tokens:
            p.append(token)
            p.pop(0)
            # Increasing count of token
            if flag == 1:
                if token not in count:
                    count[token] = 1
                else:
                    count[token] += 1
                flag = 0
            ngram = ''
            for i in xrange(n-1):
                ngram = ngram + p[i] + ' '
            ngram = ngram.strip()
            if ngram == phrase:
                flag = 1
            else:
                flag = 0
        # Predicting next token 
        v = list(count.values())
        k = list(count.keys())
        if not v:
            break
        c = k[v.index(max(v))]
        # Updating n-gram
        phrase = phrase + ' ' + c
        phrase = re.sub(r'^[^\ ]*\ ', '', phrase)
        if c != '</s>':
            sentence = sentence + ' ' + c
    print str(n) + '-gram : ' + sentence.encode('utf-8')


def tokenize():
    ''' Function for tokenizing the corpus '''

    # Opening file
    fi = open('TokenizedOutput', 'w')
    with open('tweets.en.txt') as f:
        # Iterating over lines
        total = []
        for line in f:
            # Tokenizing Glyphs
            line = re.sub(ur'([\U00016fe0-\U0001f64f])', ur' \1 ', line.decode('utf-8'))
            # Tokenizing URLs
            line = re.sub(URL, r' \1 ', line)
            line = '<s> ' + line + ' </s>'
            # Adding start and end characters
            line = re.sub(r'([^.]\.\ )', r'\1 </s> ',line)
            line = re.sub(r'(</s>)\ ', r'\1 <s> ',line)
            tokens = []
            # Splitting over whitespace
            for w in line.split():
                # Matching token with URL
                m = re.match(URL, w)
                # If it is a URL, go to next token
                # Else tokenize Emoticons
                if m:
                    tokens = tokens + [w]
                else:
                    # Tokenizing Emoticons
                    w = re.sub(EMOJI, r' \1 ', w)
                    for wo in w.split():
                        # If it is an emoticon, go to next token
                        # Else tokenize Brackets, Punctuation Marks and Special Characters
                        if re.match(EMOJI, wo):
                            tokens.append(wo)
                        else:
                            wo = re.sub(BRACKETS, r' \1 ', wo)
                            for word in wo.split():
                                word = re.sub(M, r' \1 \2 \3 ', word)
                                word = re.sub(LCORNER, r' \1 \2 ', word)
                                word = re.sub(RCORNER, r' \1 \2 ', word)
                                word = re.sub(PUNCTUATION, r' \1 ', word)
                                tokens = tokens + word.split()
            fi.write(str(tokens) + '\n')
            total = total + tokens
        for i in range(1, 7):
            for j in xrange(10):
               generateSentences(total, i)
    fi.close()

if __name__ == '__main__':
    tokenize()
