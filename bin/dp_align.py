#!/usr/bin/env python2.6

from optparse import OptionParser
import sys
import re
import collections
from types import *

##debug = True
debug = False

def order_normalize_pair(pair):
    if pair[0] > pair[1]:
        return (pair[1],pair[0])
    return pair

def align_pair(s1, s2, score_matrix, gap_score, match_score):
    ## dpmatrix[(i1,i2)] 
    ## i1 ... index of array s1  (rows)
    ## i2 ... index of array s2  (cols)
    dpmatrix = {}
    
    if debug: print s1
    if debug: print s2

    ## matrix
    for i1 in range(0,len(s1)+1):
        dpmatrix[(i1,0)] = float(i1)*-gap_score
    for i2 in range(0,len(s2)+1):
        dpmatrix[(0,i2)] = float(i2)*-gap_score
    for i1, c1 in enumerate(s1):
        i1 += 1
        for i2, c2 in enumerate(s2):
            i2 += 1
            char_pair = order_normalize_pair((c1,c2))
            score = -gap_score
            if char_pair[0] == char_pair[1]:
                score = match_score
            elif char_pair in score_matrix:
                score = score_matrix[(char_pair)]
            ue_kara = dpmatrix[(i1-1,i2)] - gap_score
            hidari_kara = dpmatrix[(i1,i2-1)] - gap_score
            naname_kara = dpmatrix[(i1-1,i2-1)]+score
            dpmatrix[(i1,i2)] = max([ue_kara, hidari_kara, naname_kara])
    
    if debug:
        for i1 in range(0,len(s1)+1):
            line = ""
            for i2 in range(0,len(s2)+1):
                line += ' %8.3f'%dpmatrix[(i1,i2)]
            print line

    ## trace back
    k=0
    i1 = len(s1)-1
    i2 = len(s2)-1
    align1 = ''
    align2 = ''
    while i1 >= 0 or i2 >= 0:
        if debug: print str(i1) + ' ' + str(i2)
        if i1 == -1 or (i2>0 and dpmatrix[(i1+1,i2+1)] == dpmatrix[(i1+1,i2)] - gap_score):
            align1 += '-'
            align2 += s2[i2]
            i2 -= 1
        elif i2 == -1 or dpmatrix[(i1+1,i2+1)] == dpmatrix[(i1,i2+1)] - gap_score:
            align1 += s1[i1]
            align2 += '-'
            i1 -= 1
        else:
            align1 += s1[i1]
            align2 += s2[i2]
            i1 -= 1
            i2 -= 1
    if debug:
        print align1[::-1]
        print align2[::-1]
        print dpmatrix[(len(s1)-1,len(s2)-1)]
    return align1[::-1],align2[::-1],dpmatrix[(len(s1)-1,len(s2)-1)]

def read_score_matrix(fn_score):
    score = {}
    try: f_sc = open(fn_score,"r")
    except IOError: 
        sys.stderr.write("Error: File "+fn_score+" could not be opend.\n")
        sys.exit()
    for line in f_sc:
        terms=re.compile("\s+").split(line.strip())
        score[order_normalize_pair((terms[0],terms[1]))] = float(terms[2])
    f_sc.close()
    return score


def read_sequences(fn_seq, min_len, ignore):
    seq = {}
    try: f_seq = open(fn_seq,"r")
    except IOError: 
        sys.stderr.write("Error: File "+fn_seq+" could not be opend.\n")
        sys.exit()
    c_header = ""
    c_seq = ""
    for line in f_seq:
        if line[0] == ">":
            if len(c_seq) >= min_len:
                seq[c_header] = c_seq
            c_header = line.strip()
            c_seq = ""
        else:
            tmp_seq = line.strip()
            for ig in ignore:
                tmp_seq = tmp_seq.replace(ig,'')
            c_seq += tmp_seq

    if len(c_seq) >= min_len:
        seq[c_header] = c_seq

    f_seq.close()
    return seq

def all_against_all(sequences, score_matrix, gap_score, match_score, fn_out, flg_out_align):
    f_out = open(fn_out,"w")

    for t1,s1 in sequences.items():
        t1id = int(re.compile("\s+").split(t1)[1])
        t1 = t1.replace(">","").strip()
        for t2,s2 in sequences.items():
            t2id = int(re.compile("\s+").split(t2)[1])
            t2 = t2.replace(">","").strip()
            if t1==t2: break
            align_str1, align_str2, score = align_pair(s1, s2, score_matrix, gap_score, match_score)
            line = "> " + str(t1id) + '\t' + str(t2id) + '\t'
            line += str(score) + '\t' + t1 + "\t" + t2 + "\n"
            if flg_out_align:
                line += str(align_str1) +'\n'
                line += str(align_str2) +'\n'
            f_out.write(line)
    f_out.close()
    return

def _main():
    p = OptionParser()
    p.add_option('--i-score-matrix', dest='fn_score',
                 help="filename for score matrix")
    p.add_option('--i-sequence', dest='fn_sequences',
                 help="filename for sequences")
    p.add_option('-o', '--o-align',dest='fn_out',
                 default="align.txt",
                 help="filename for output")
    p.add_option('-a', '--align-details',  dest='flg_out_align',
                 action="store_true",
                 help="output alignment details")
    p.add_option('-l', '--min-len', dest='min_len',
                 default="3",
                 type="int",
                 help="minimum length of each sequence")
    p.add_option('-g', dest='gap_score',
                 default="1.0",
                 type="float",
                 help="gap score for alignment")
    p.add_option('-m', dest='match_score',
                 default="1.0",
                 type="float",
                 help="match score for alignment")
    p.add_option('-i','--ignore', dest='ignore_chara',
                 action="append",
                 help="remove character of home state in sequences")
    opts, args = p.parse_args()
    
    flg_fail = False
    if not opts.fn_score:
        sys.stderr.write("Error: Option '--i-score-matrix' is required.\n")
        flg_fail=True
    if not opts.fn_sequences:
        sys.stderr.write("Error: Option '--i-sequence' is required.\n")
        flg_fail = True
    if flg_fail:
        sys.exit()
    
    if not opts.ignore_chara:
        opts.ignore_chara = ['*']
        
    score_matrix = read_score_matrix(opts.fn_score)
    sequences = read_sequences(opts.fn_sequences, opts.min_len, opts.ignore_chara)
    all_against_all(sequences, score_matrix,
                    opts.gap_score, opts.match_score,
                    opts.fn_out, opts.flg_out_align)

if __name__ == '__main__':
    _main()
