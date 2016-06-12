#!/usr/bin/env python2.6
#$ -S /usr/bin/python2.6
#$ -cwd

from optparse import OptionParser
import sys
import re
import collections
import os
import math
sys.path.append(os.path.join(os.environ.get("ISACMD"),"bin"))
from dp_align import read_sequences

def read_table(fn_table):
    f_table = open(fn_table)
    table = {}
    header = f_table.readline()
    for line in f_table:
        terms = re.compile("\s+").split(line.strip())
        ## lifetime, wait
        table[terms[1]] = (int(terms[2]), int(terms[3]))
    f_table.close()
    return table

def read_table_trans(fn_table_trans):
    f_trans = open(fn_table_trans)
    table = {}
    header = f_trans.readline()
    for line in f_trans:
        terms = re.compile("\s+").split(line.strip())
        table[(terms[0],terms[1])] = int(terms[2])
    f_trans.close()
    return table

def read_dict(fn_dict):
    f_dict = open(fn_dict)
    dict = {}
    for line in f_dict:
        terms = re.compile("\s+").split(line.strip())
        dict[terms[0]] = terms[2]
    f_dict.close()
    return dict

def group_table(table,dict):
    table_group = {}
    for state, val in table.items():
        grp = dict[state]
        if grp in table_group:
            table_group[grp] = (table_group[grp][0] + val[0],
                                table_group[grp][1] + val[1])
        else:
            table_group[grp] = (val[0], val[1])
    return table_group

def group_trans(table_group_pre, trans, dict):
    table_group = table_group_pre
    trans_group = {}
    for state_pair, val in trans.items():
        grp_s = dict[state_pair[0]]
        grp_t = dict[state_pair[1]]        
        if grp_s==grp_t:
            table_group[grp_s] = (table_group[grp_s][0],
                                  table_group[grp_s][1] + val)       
        elif (grp_s,grp_t) in trans_group:
            trans_group[(grp_s,grp_t)] = trans_group[(grp_s,grp_t)] + val
        else:
            trans_group[(grp_s,grp_t)] = val
    return table_group, trans_group

def output_gml(fn_graph_conv, table_group, trans_group):

    try: f_out = open(fn_graph_conv, 'w')
    except IOError:
        sys.stderr.write("File"+ fn_out +" could not be opend.\n")
        sys.exit()
        
    f_out.write('graph [\n')
    f_out.write('  directed 1\n') 

    sum_cnt = 0.0
    for state,val in table_group.items():
        sum_cnt += val[0]
    i = 0
    state_id = {}
    for state,val in table_group.items():
        f_out.write('  node [\n')
        f_out.write('    id ' + str(i) + '\n')
        f_out.write('    state "' + state + '"\n')
        f_out.write('    count ' + str(val[0]) + '\n')
        f_out.write('    count_rel ' + str(float(val[0])/sum_cnt) + '\n')
        f_out.write('    logcount ' + str(math.log10(float(val[0])/sum_cnt)) + '\n')
        f_out.write('    wait ' + str(val[1]) + '\n')
        f_out.write('  ]\n')
        state_id[state] = i
        i+=1
        
    sum_cnt_trans = 0.0
    for s_t, val in trans_group.items():
        sum_cnt += val
    for s_t, val in trans_group.items():
        f_out.write('  edge [\n')
        f_out.write('    source ' + str(state_id[s_t[0]]) + '\n')
        f_out.write('    target ' + str(state_id[s_t[1]]) + '\n')
        f_out.write('    count ' + str(val) + '\n')
        f_out.write('    count_rel ' + str(float(val)/sum_cnt) + '\n')
        f_out.write('    logcount ' + str(math.log10(float(val)/sum_cnt)) + '\n')
        f_out.write('  ]\n')

    f_out.close()

def _main():
    p = OptionParser()
    p.add_option('--i-table', dest='fn_table',
                 help="input file for state table")
    p.add_option('--i-table-trans', dest='fn_table_trans',
                 help="input file for state transition table")
    p.add_option('--i-state-dict', dest='fn_state_dict_in',
                 help="input file name for .fsa sequence file.")
    p.add_option('--o-graph-conv', dest='fn_graph_conv',
                 help="output file for the graph in GML format")

    opts, args = p.parse_args()    

    dict = read_dict(opts.fn_state_dict_in)
    table = read_table(opts.fn_table)
    table_trans = read_table_trans(opts.fn_table_trans)

    table_group_pre = group_table(table, dict)
    table_group, trans_group = group_trans(table_group_pre, table_trans, dict)
    output_gml(opts.fn_graph_conv, table_group, trans_group)

if __name__ == '__main__':
    _main()

    
