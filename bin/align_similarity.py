#!/usr/bin/env python2.6

from optparse import OptionParser
import sys
import re
import collections
from types import *

debug = True
#debug = False

def pair_normalize(pair):
    if pair[0] > pair[1]:
        return (pair[1],pair[0])
    return pair

def read_seq_len(fn_seq, ignore_char):
    seq = {}
    try: f_seq= open(fn_seq,"r")
    except IOError:
        sys.stderr.write("Error: File "+fn_seq+" could not be opend.\n")
        sys.exit()

    for line in f_seq:
        terms = re.compile("\s+").split(line.strip())
        if terms[0][0] == '>':
            cur_seq = terms[3]
            for ig in ignore_char:
                cur_seq = cur_seq.replace(ig,'')
            seq[int(terms[1])] = float(len(cur_seq))

    f_seq.close()
    return seq
        
def read_align(fn_align, seq_len, gap, match):
    try: f_align = open(fn_align,"r")
    except IOError:
        sys.stderr.write("Error: File "+fn_align+" could not be opend.\n")
        sys.exit()
    score_matrix = {}
    id_set = set()
    for line in f_align:
        if line[0] != '>': continue
        terms = re.compile("\s+").split(line.strip())
        seq1id = int(terms[1])
        seq2id = int(terms[2])
        score = float(terms[3])
        len_max = max([seq_len[seq1id],seq_len[seq2id]])
        len_sum = seq_len[seq1id] + seq_len[seq2id]
        sim = (gap + score/len_sum) / (gap + match)
        score_matrix[pair_normalize((seq1id,seq2id))] = sim
        id_set.add(seq1id)
        id_set.add(seq2id)
    f_align.close()
    return list(id_set), score_matrix

def write_score(fn_out, id_list, score_matrix):
    try: f_out = open(fn_out,"w")
    except IOError:
        sys.stderr.write("Error: File "+fn_out+" could not be opend.\n")
        sys.exit()

    line = '\t'.join([str(x) for x in id_list])
    f_out.write(line+'\n')
    for id1 in id_list:
        line = str(id1)
        for id2 in id_list:
            pair = pair_normalize((id1,id2))
            if id1 == id2:
                line += '\t1.0'
            elif pair in score_matrix:
                line += '\t' + str(score_matrix[pair])
            else:
                line += '\t0.0'
        f_out.write(line+'\n')

    f_out.close()
    
def _main():
    p = OptionParser()

    p.add_option('--i-align', dest='fn_align',
                 help="filename for input")
    p.add_option('--o-sim', dest='fn_out_sim',
                 default="align_sim.txt",
                 help="filename for output")
    p.add_option('--i-sequence', dest='fn_seq',
                 help="filename for sequences")
    p.add_option('-g', '--gap', dest='gap_score',
                 default=1.0,
                 type="float",
                 help="gap score")
    p.add_option('-m', '--match', dest='match_score',
                 default=1.0,
                 type="float",
                 help="match score")
    p.add_option('-i', '--ignore', dest='ignore_chara',
                 action="append",
                 help="remove character of home state in sequences")
    opts, args = p.parse_args()
    
    flg_fail = False
    if not opts.fn_align:
        sys.stderr.write("Error: Option '--i-align' is required.\n")
        flg_fail=True
    if not opts.fn_seq:
        sys.stderr.write("Error: Option '--i-sequence' is required.\n")
        flg_fail = True
    if flg_fail:
        print "exit"
        sys.exit()
        
    if not opts.ignore_chara:
        opts.ignore_chara = ['*']

    seq_len = read_seq_len(opts.fn_seq, opts.ignore_chara)
    id_list, score_matrix = read_align(opts.fn_align, seq_len,
                                       opts.gap_score, opts.match_score)
    write_score(opts.fn_out_sim, id_list, score_matrix)

if __name__ == '__main__':
    _main()
