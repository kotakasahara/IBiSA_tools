#!/usr/bin/env python2.6
#$ -S /usr/bin/python2.6
#$ -cwd
from optparse import OptionParser
import sys
import re
import collections
from types import *

def output_cycles(fn_cycles, cycles, cal_title):
    try: f_cycles = open(fn_cycles,"w")
    except IOError:
        sys.stderr.write("Error: File "+fn_cycles+" could not be opend.\n")
        sys.exit()
    for i,cycle in enumerate(cycles):
        f_cycles.write('>\t' + str(i) + '\t'
                       + str(cycle[0][0]) + '\t' + str(cycle[-1][0]) + '\t'
                       + cal_title + '\n')
        for state in cycle:
            f_cycles.write('\t'.join(state)+'\n')

    f_cycles.close()
    return

def decide_home(fn_state, fn_dict, home_chara):
    count = collections.defaultdict(int)
    try: f_state = open(fn_state,"r")
    except IOError:
        sys.stderr.write("Error: File "+fn_state+" could not be opend.\n")
        sys.exit()

    ## counting all satets in trajectory
    for line in f_state:
        terms = re.compile("\s+").split(line.strip())
        count[terms[1]] += 1
    f_state.close()
    
    home = ""
    max_cnt = 0
    for state,cnt in count.items():
        if cnt > max_cnt:
            home = state
            max_cnt = cnt

    ## output dictionary containing only the home state
    try: f_dict = open(fn_dict,"w")
    except IOError:
        sys.stderr.write("Error: File "+fn_dict+" could not be opend.\n")
        sys.exit()
    f_dict.write(home+'\t'+home_chara+'\n')
    f_dict.close()


    return home

def analyze_state(fn_state, home_state):

    #cur_cycle = [line1, line2, ...]
    cur_cycle = []
    cycles = []

    try: f_state = open(fn_state,"r")
    except IOError:
        sys.stderr.write("Error: File "+fn_state+" could not be opend.\n")
        sys.exit()

    for line in f_state:
        terms = re.compile("\s+").split(line.strip())
        # terms[0]: time
        # terms[1]: state
        # terms[2]: atoms
        frame = int(float(terms[0]))
        site_state = terms[1] + '\t' + terms[2]

        ## checking existance of same state with same atoms in the cur_cycle
        flg_exist = False
        for i,prev_state in enumerate(cur_cycle):
            if prev_state[1:] == terms[1:]:
                cur_cycle = cur_cycle[:i]
                flg_exit = True
                break
        if not flg_exist:
            cur_cycle.append(terms)
            if terms[1] == home_state and len(cur_cycle)>2:
                cycles.append(cur_cycle)
                cur_cycle = [terms]

    f_state.close()

    return cycles            
    
def _main():
    p = OptionParser()
    p.add_option('--i-state', dest='fn_state',
                 type="str",
                 help="filename for state transition.")
    p.add_option('--o-cycles', dest='fn_cycles',
                 default="state_traj_cycles.txt",
                 help="filename for output.")
    p.add_option('--o-state-dict', dest='fn_dict',
                 default="state_dict_pre.txt",
                 help="filename for output.")
    p.add_option('--home', dest='home_state',
                 help="string of the home state, e.g., K:0:2:4")
    p.add_option('--home-chara', dest='home_chara',
                 default = '*',
                 help="character of the home state") 
    p.add_option('-t', '--title', dest='cal_title',
                 default='-',
                 help="title of this calculation. this information will be added to the output.")
    #p.add_option('-c', '--cycle', dest='flg_cycle',
    #             action="store_true",
    #             help="removing path in cycle")
    opts, args = p.parse_args()

    flg_fail = False
    if not opts.fn_state:
        sys.stderr.write("Error: Option '--i-state' is required.\n")
        flg_fail = True
        #if not opts.home_state:
        #sys.stderr.write("Error: Option '--home' is required.\n")
        #flg_fail = True
    if flg_fail:
        sys.exit()
        
    home = ""
    if opts.home_state:
        home = opts.home_state
    else:
        home = decide_home(opts.fn_state, opts.fn_dict, opts.home_chara)
        print "Home state : " + home
        
    cycles = analyze_state(opts.fn_state, home)
    output_cycles(opts.fn_cycles, cycles, opts.cal_title)

if __name__ == '__main__':
    _main()
