#!/usr/bin/env python2.6
#$ -S /usr/bin/python2.6
#$ -cwd

from optparse import OptionParser
import sys
import re
import collections
import os
sys.path.append(os.path.join(os.environ.get("ISACMD"),"bin"))
from dp_align import read_sequences

def read_dict(fn_dict):
    f_dict = open(fn_dict)
    dict = {}
    for line in f_dict:
        terms = re.compile("\s+").split(line.strip())
        dict[terms[1]] = terms[2]
    f_dict.close()
    return dict

def _main():
    p = OptionParser()
    p.add_option('--i-sequence', dest='fn_sequences',
                 help="input output file name for sequeces in .fsa format")
    p.add_option('--i-state-dict', dest='fn_state_dict_in',
                 help="input file name for .fsa sequence file.")
    p.add_option('--o-sequence', dest='fn_sequences_out',
                 help="output file name for converted .fsa sequence file")
    p.add_option('--o-sequence-table', dest='fn_sequences_table_out',
                 help="output file name for converted .fsa sequence file")
    p.add_option('--o-sequence-count', dest='fn_sequences_count',
                 help="output file name for counts.")
    opts, args = p.parse_args()    

    dict = read_dict(opts.fn_state_dict_in)
    sequences = read_sequences(opts.fn_sequences, 0, [])

    seq_count = collections.defaultdict(int)
    f_out = None
    f_tbl_out = None
    if opts.fn_sequences_out:
        f_out = open(opts.fn_sequences_out,"w")
    if opts.fn_sequences_table_out:
        f_tbl_out = open(opts.fn_sequences_table_out,"w")
    for head, seq in sequences.items():
        new_seq = ""
        for c in seq:
            if len(new_seq) == 0 or new_seq[-1] != dict[c]:
                new_seq += dict[c]
        if len(head) > 0 and len(new_seq) > 0:
            if f_out:
                f_out.write(head+"\n")
                f_out.write(new_seq+"\n")
            if f_tbl_out:
                f_tbl_out.write(head[1:]+"\t"+new_seq+"\n")
            seq_count[new_seq] += 1
    if f_out:     f_out.close()
    if f_tbl_out: f_tbl_out.close()

    seq_count = sorted(seq_count.items(), key=lambda x:x[1], reverse=True)
    
    if opts.fn_sequences_count:
        f_cnt = open(opts.fn_sequences_count, 'w')
        for seq_cnt in seq_count:
            f_cnt.write(seq_cnt[0] + '\t' + str(seq_cnt[1]) + '\n')
        f_cnt.close()

if __name__ == '__main__':
    _main()

    
