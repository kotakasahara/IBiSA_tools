#!/usr/bin/env python2.6

from optparse import OptionParser
import sys
import re
import collections
from types import *

def order_normalize_pair(pair):
    if pair[0] > pair[1]:
        return (pair[1],pair[0])
    return pair

def parse_state(state_str, separator_atom, separator_site):
    state = {}
    state_atoms = state_str.split(separator_atom)
    for state_atom in state_atoms:
        sites = state_atom.split(separator_site)
        state[sites[0]] = sites[1:]
    return state

def sim_n_atoms(state1, state2):
    if state1==state2: return 1.0
    for atom1, sites1 in state1.items():
        if not atom1 in state2 or len(sites1) != len(state2[atom1]):
            return 0.0
    return 0.5
            
def cal_sim(fn_out, state_dict, separator_atom, separator_site):
    try: f_out = open(fn_out,"w")
    except IOError:
        sys.stderr.write("Error: File "+fn_out+" could not be opend.\n")
        sys.exit()
    
    for state1_str, c1 in state_dict.items():
        state1 = parse_state(state1_str, separator_atom, separator_site)
        for state2_str, c2 in state_dict.items():
            if state1_str == state2_str: break
            state2 = parse_state(state2_str, separator_atom, separator_site)
            sim = sim_n_atoms(state1,state2)
            state_pair = order_normalize_pair((state1_str,state2_str))
            if sim != 0.0:
                f_out.write(state_pair[0]+'\t'+state_pair[1]+'\t'+str(sim)+'\n')
    f_out.close()
    
    
def read_states(fn_state_dict, separator_atom, separator_site):
    state_dict = {}
    try: f_state = open(fn_state_dict,'r')
    except IOError:
        sys.stderr.write("Error: File "+fn_state_dict+" could not be opend.\n")
        sys.exit()

    for line in f_state:
        terms = re.compile("\s+").split(line.strip())
        if len(terms) < 2: continue
        state = terms[0]
        chara = terms[1]
        state_dict[state] = chara
    return state_dict

def _main():
    p = OptionParser()
    p.add_option('--i-state-dict', dest='fn_state_dict',
                 help="input file name for state dictionary.")
    p.add_option('--o-score', dest='fn_score',
                 default="score_matrix.txt",
                 help="output file name for score matrix.")
    p.add_option('--separator-site', dest="separator_site",
                 default=":",
                 help="separator charactor for state string, spliting binding sites")
    p.add_option('--separator-atom', dest="separator_atom",
                 default="/",
                 help="separator charactor for state string, spliting atom species")
    opts, args = p.parse_args()
    
    flg_fail = False
    if not opts.fn_state_dict:
        sys.stderr.write("Error: Option '--i-state-dict' is required.\n")
        flg_fail=True
    if flg_fail:
        sys.exit()

    set_state = set()

    state_dict = read_states(opts.fn_state_dict, opts.separator_atom, opts.separator_site)
    cal_sim(opts.fn_score, state_dict, opts.separator_atom, opts.separator_site)

if __name__ == '__main__':
    _main()
