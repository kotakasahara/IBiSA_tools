#!/usr/bin/python2.6
#$ -S /usr/bin/python2.6
#$ -cwd

from optparse import OptionParser
import sys
import re
import collections

def analyze_run(fn_in, fn_out,  path_f_l):
    f_in = open(fn_in,'r')
    f_out = open(fn_out, 'w')

    for i,line in enumerate(f_in):
        ##print line
        terms = re.compile("\s+").split(line.strip())
        flg_valid = False
        path = terms[1]+':'+terms[2]
        for atom_path in path_f_l:
            if atom_path == path:
                sp = re.compile(":").split(terms[3])
                start = sp[0]
                end = sp[-1]
                f_out.write(terms[0] + '\t' + terms[1] + '\t' + start + '\t' + end + '\n')

    f_out.close()
    f_in.close()


def _main():
    p = OptionParser()
    p.add_option('--i-all-path', dest='fn_all_path',
                 help="file name for pore axis coordinates h generated by trachan.")
    p.add_option('--o-path-time', dest='fn_path_time',
                 help="output file name.")
    p.add_option('--path', dest='path_f_l',
                 action="append",
                 help="target site path")

    opts, args = p.parse_args()

    analyze_run(opts.fn_all_path,
                opts.fn_path_time,
                opts.path_f_l)
        
if __name__ == '__main__':
    _main()
