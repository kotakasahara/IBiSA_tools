#!/usr/bin/env python2.6
#$ -S /usr/bin/python2.6
#$ -cwd

from optparse import OptionParser
import sys
import re
import collections
from types import *

out_of_state = '-'

def read_cycles(fn_cycle):
    """ """
    try: f_cycles = open(fn_cycle,"r")
    except IOError:
        sys.stderr.write("Error: File "+fn_cycle+" could not be opened.\n")
        sys.exit()

    set_states = set()
    ## cycle_dict[cycle description] = [ ([state1,state2,....], [frame1, frame2, .... ]), ....  ]
    cycle_dict = {}
    cur_title = ""
    for line in f_cycles:
        terms = re.compile("\s+").split(line.strip())
        if terms[0] == '>':
            cur_title = '\t'.join(terms[1:])
            cycle_dict[cur_title] = ([],[]) ## ([state..], [frame...])
        else:
            frame = int(float(terms[0]))
            state = terms[1]
            atoms = terms[2]
            cycle_dict[cur_title][0].append(state)
            cycle_dict[cur_title][1].append(frame)
            set_states.add(state)
    f_cycles.close()
    return cycle_dict, set_states
    
def parse_state(state_str, separator_atom, separator_site):
    state = {}
    atom_types = state_str.split(separator_atom)
    for atom_type in atom_types:
        sites = atom_type.split(separator_site)
        state[sites[0]] = sites[1:]
    return state

def get_char(n_char, i):
    char = '-' 
    if n_char == 1:
        if i < 26:
            char = chr(ord('A')+i)
        elif i < 52:
            char = chr(ord('a')+i-26)
        elif i < 62:
            char = chr(ord('0')+i-52)
    elif n_char == 2:
        char = chr(ord('A') + i/26)
        char += chr(ord('a') + i%26)
    return char

def state_to_chara(fn_state_dict_in,
                   set_state, separator_atom, separator_site):

    state_dict = {}
    used_chara = set()
    ## read preliminary defined state-characters
    if fn_state_dict_in:
        try: f_dict = open(fn_state_dict_in,"r")
        except IOError:
            sys.stderr.write("Error: File "+fn_dict+" could not be opened.\n")
            sys.exit()

        for line in f_dict:
            terms = re.compile("\s+").split(line.strip())
            state_dict[terms[0]] = terms[1:]
            used_chara.add(terms[1])
        f_dict.close()
    
    #state_ionnum[num of ions] = [(state, sum of site id), (state, .), ...]
    state_ionnum = collections.defaultdict(list)
    
    for state_str in set_state:
        state = parse_state(state_str, separator_atom, separator_site)
        n_ions = [len(x) for x in state.values()]
        state_ionnum[tuple(n_ions)].append(state_str)

    n_atom_types = len(state_ionnum.keys()[0])
    s_ionnum = state_ionnum.keys()
    for i in range(n_atom_types-1, -1, -1):
        s_ionnum = sorted(s_ionnum, key=lambda x:x[i])

    #print s_ionnum

    ## 0-9: 48-57  : 10
    ## A-Z: 65-90  : 26
    ## a-z: 97-122 : 26

    print len(set_state)
    n_char = 0
    if len(set_state) < 62:
        n_char = 1
    elif len(set_state) < 676: #26*26
        n_cahr = 2
    else:
        sys.stderr.write("ERROR: the number of states is too large. " + str(len(set_state)) + "\n");
        sys.exit()
        
    i_state = 0
    skip_state = 0
    for ionnum in s_ionnum:
        for state_str in sorted(state_ionnum[ionnum]):
            if not state_str in state_dict:
                chara = get_char(n_char, i_state)
                while chara in used_chara:
                    i_state += 1
                    chara = get_char(n_char, i_state)
                state_dict[state_str] = [chara]
                i_state += 1
    return state_dict

def convert_path_string(state_dict, path):
    converted = ""
    for s in path:
        if s in state_dict:
            converted += state_dict[s][0]
        else:
            converted += out_of_state
    return converted

def output_state_dict(fn_state_dict, state_dict):
    try: f_out = open(fn_state_dict,"w")
    except IOError:
        sys.stderr.write("Error: File "+fn_dict+" could not be opened.\n")
        sys.exit()
    
    for state, chara in sorted(state_dict.items(), key=lambda x:x[1]):
        f_out.write(state + "\t" + '\t'.join(chara) + "\n")
    f_out.close()
    return

def output_sequences(fn_sequences, fn_sequences_header, sequences):
    try:
        f_out = open(fn_sequences,"w")
    except IOError:
        sys.stderr.write("Error: File "+fn_sequences+" could not be opened.\n")
        sys.exit()
    try:
        f_out_h = open(fn_sequences_header,"w")
    except IOError:
        sys.stderr.write("Error: File "+fn_sequences_header+" could not be opened.\n")
        sys.exit()

    seq_id = 0
    for file_id, sequence_dic in sequences.items():
        #print "file_id : " + str(file_id)
        for title, seq in sequence_dic.items():
            sequence = seq[0]
            frames = seq[1]
            line = "> "
            line += str(seq_id) + '\t'
            line += str(file_id) + '\t'
            line += sequence + '\t'
            line += title + '\n'
            f_out.write(line)
            f_out_h.write(line)
            f_out.write(sequence + '\n')
            seq_id += 1
    f_out_h.close()
    f_out.close()
    return 

def _main():
    p = OptionParser()
    p.add_option('--i-cycles', dest='fn_cycles',
                 action="append",
                 help="input file name for state cycles.")
    p.add_option('--i-state-dict', dest='fn_state_dict_in',
                 help="input file name for dictionary of states")
    p.add_option('--o-state-dict', dest='fn_state_dict',
                 help="output file name for dictionary of states")
    p.add_option('--o-sequence', dest='fn_sequences',
                 default = "sequences.fsa",
                 help="output file name for sequeces in .fsa format")
    p.add_option('--o-sequence-head', dest='fn_sequences_head',
                 default = "sequences_header.txt",
                 help="filename for headers of the sequences")
    p.add_option('--separator-atom', dest="separator_atom",
                 default="/",
                 help="separator charactor for state string, spliting target atoms")
    p.add_option('--separator-site', dest="separator_site",
                 default=":",
                 help="separator charactor for state string, spliting binding sites")
    opts, args = p.parse_args()
    flg_fail = False
    if not opts.fn_cycles:
        sys.stderr.write("Error: At least one '--i-cycles' is required.\n")
        flg_fail=True
    if flg_fail:
        sys.exit()

    set_state = set()

    ## cycle_dict_agg[integer id of path files] = {([state1,state2,....], [frame1,frame2,...]), (), (),... }
    cycle_dict_agg = {}

    for i,fn_cycle in enumerate(opts.fn_cycles):
        #print "path " + str(i) + " " + fn_cycle
        cycle_dict, cur_set_states = read_cycles(fn_cycle)
        cycle_dict_agg[i] = cycle_dict
        set_state = set_state.union(cur_set_states)

    state_dict = state_to_chara(opts.fn_state_dict_in,
                                set_state, opts.separator_atom, opts.separator_site)

    ### path_str_dic 
    sequences = {}

    for file_id, cycle_dict in cycle_dict_agg.items():
        sequences[file_id] = {}
        for title, cyc in cycle_dict.items():
            states = cyc[0]
            frames = cyc[1]
            sequence = convert_path_string(state_dict, states)
            sequences[file_id][title] = (sequence, frames)
            
    if opts.fn_state_dict:
        output_state_dict(opts.fn_state_dict, state_dict)
    if opts.fn_sequences:
        output_sequences(opts.fn_sequences, opts.fn_sequences_head, sequences)

if __name__ == '__main__':
    _main()
