#!/usr/bin/env python2.6
#$ -S /usr/bin/python2.6
#$ -cwd

from optparse import OptionParser
import sys
import re
import collections
import math
from types import *

def cal_sum_of_site_id(state):
    sp = re.compile(":").split(state)
    return sum([int(x) for x in sp[1:]])

def n_ions(state):
    sp = re.compile(":").split(state)
    return len(sp)-1

def n_chara_in_state(state,chara):
    i = 0
    for c in state:
        if c == chara:
            i+=1
    return i

def diff_list(lh, rh):
    ## lh-rh
    new_list = []
    for term in lh:
        if not term in rh:
            new_list.append(term)
            new_rh = []
            for i,t in enumerate(rh):
                if t != term:
                    new_rh.append(t)
                elif i != len(rh)-1:
                    new_rh += rh[i+1:]
                    break
            rh = new_rh
    return new_list
    
def output_state_similarity_score(fn_out, states, trans, trans_all):
    if not fn_out:
        return
    dic_sim = {}
    for s_t, cnt in trans.items():
        pair_id = s_t
        if s_t[1] < s_t[0]: pair_id = (s_t[1], s_t[0])
        if pair_id in dic_sim: continue
        print pair_id
        print "states[" + pair_id[0] + "] " +str(states[pair_id[0]])
        print "states[" + pair_id[1] + "] " +str(states[pair_id[1]])
        prob_0 = float(states[pair_id[0]]) / float(states[pair_id[0]]+states[pair_id[1]])
        prob_1 = float(states[pair_id[1]]) / float(states[pair_id[0]]+states[pair_id[1]])
        prob_0_1 = 0.0
        prob_1_0 = 0.0

        if pair_id in trans:
            prob_0_1 = float(trans[pair_id])/float(trans_all[pair_id[0]])
        if (pair_id[1],pair_id[0]) in trans:
            prob_1_0 = float(trans[(pair_id[1],pair_id[0])])/float(trans_all[pair_id[1]])

        print pair_id[0] + ":" + pair_id[1] + " " + str(prob_0) + ":" +str(prob_1) + ":"+str(prob_0_1)+":"+str(prob_1_0)

        dic_sim[pair_id] = math.log(prob_0*prob_0_1 + prob_1*prob_1_0)

    try: f_out = open(fn_out,"w")
    except IOError:
        sys.stderr.write("File"+ fn_out +" could not be opend.\n")
        sys.exit()
        
    for pair, sim in dic_sim.items():
        f_out.write(pair[0] + "\t" + pair[1] + "\t" + str(sim) + "\n")
        
    f_out.close()

def output_gml(fn_out, fn_table, fn_table_trans, states, trans, trans_all, count_wait):

    try: f_out = open(fn_out,"w")
    except IOError:
        sys.stderr.write("File"+ fn_out +" could not be opend.\n")
        sys.exit()

    f_table = None
    f_table_trans = None

    if fn_table:
        try: f_table = open(fn_table,"w")
        except IOError:
            sys.stderr.write("File"+ fn_table +" could not be opend.\n")
        f_table = open(fn_table,"w")
        f_table.write("node.id\tstate\tlifetime\twait\tcrd\n")
    state_id = {}
    id_state = {}
    i = 0
    f_out.write('graph [\n')
    f_out.write('  directed 1\n') 
    sum_cnt = 0.0
    for state,cnt in states.items():
        sum_cnt += cnt
    for state,cnt in states.items():
        flg_star = "0"
        if '*' in state:
            flg_star = "1"
        f_out.write('  node [\n')
        f_out.write('    id ' + str(i) + '\n')
        f_out.write('    state "' + state + '"\n')
        f_out.write('    count ' + str(cnt) + '\n')
        f_out.write('    count_rel ' + str(float(cnt)/sum_cnt) + '\n')
        f_out.write('    logcount ' + str(math.log10(float(cnt)/sum_cnt)) + '\n')
        f_out.write('    wait ' + str(count_wait[state]) + '\n')
        f_out.write('    crd ' + str(n_ions(state)) + '\n')
        #f_out.write('    star ' + flg_star + '\n')
        f_out.write('  ]\n')
        state_id[state] = i
        id_state[i] = state

        if f_table:
            line = str(i)+'\t'+state+'\t'+str(cnt)+'\t'
            line += str(count_wait[state])+'\t'+str(n_ions(state))+'\n'
            f_table.write(line)

        i += 1

    if f_table:
        f_table.close()

    if fn_table:
        try: f_table_trans = open(fn_table_trans,"w")
        except IOError:
            sys.stderr.write("File"+ fn_table_trans +" could not be opend.\n")
        f_table_trans.write("source\ttarget\tcnt\tdiff\tratio\tdiff_ions\n")

    sum_cnt = 0.0
    for s_t, cnt in trans.items():
        sum_cnt += cnt
    for s_t, cnt in trans.items():
        #diff_site_num = cal_sum_of_site_id(s_t[1]) - cal_sum_of_site_id(s_t[0])
        diff_crd = n_ions(s_t[1])-n_ions(s_t[0])
        diff_crd_nonstar = (n_ions(s_t[1]) - n_chara_in_state(s_t[1],'*')) \
                           - (n_ions(s_t[0]) - n_chara_in_state(s_t[0],'*'))
        ions_source = re.compile(":").split(s_t[0])[1:]
        ions_target = re.compile(":").split(s_t[1])[1:]
        ions_added = "".join(["+"+x for x in diff_list(ions_target, ions_source)])
        ions_popped = "".join(["-"+x for x in diff_list(ions_source, ions_target)])

        f_out.write('  edge [\n')
        f_out.write('    source ' + str(state_id[s_t[0]]) + '\n')
        f_out.write('    target ' + str(state_id[s_t[1]]) + '\n')
        f_out.write('    count ' + str(cnt) + '\n')
        f_out.write('    count_rel ' + str(float(cnt)/sum_cnt) + '\n')
        f_out.write('    logcount ' + str(math.log10(float(cnt)/sum_cnt)) + '\n')
        f_out.write('    diff ' + str(diff_crd) + '\n')
        #f_out.write('    diff_ns ' + str(diff_crd_nonstar) + '\n')
        f_out.write('    ratio %8.3f'%(float(cnt)/float(trans_all[s_t[0]])) + '\n')
        f_out.write('    diff_ions "' + ions_added+ions_popped + '"\n')        
        f_out.write('  ]\n')
        if f_table_trans:
            line = s_t[0] + '\t' + s_t[1] + '\t'
            line += str(cnt) + '\t' + str(diff_crd) + '\t'
            line += str(float(cnt)/float(trans_all[s_t[0]])) + '\t'
            line += str(ions_added+ions_popped) + '\n'
            f_table_trans.write(line)
    f_out.write(']\n')

    if f_table_trans:
        f_table_trans.close()

    f_out.close()

def read_pass_through_ion_frames(fn_path, through_path, atom_names,
                                 flg_first_end, through_path_begin):
    #through_ion_frames = [(atom_id, first, last)]
    through_ion_frames = []

    #entering_ion_frames[frame]=atom_id
    #exiting_ion_frames[frame]=atom_id
    entering_ion_frames = {}
    exiting_ion_frames = {}

    if fn_path == "":
        return [],[],[]

    try: f_path = open(fn_path, "r")
    except IOError:
        sys.stderr.write("File"+ fn_path +" could not be opend.\n")
        sys.exit()

    for line in f_path:
        terms = re.compile("\s+").split(line.strip())
        if not terms[2] in atom_names:
            continue
        p = re.compile(":").split(terms[3])

        flg_bound_at_begin = False
        if terms[3] in through_path_begin:
            flg_bound_at_begin = True
        flg_bound_at_end = False
        if p[-1] != "0":
            flg_bound_at_end = True

        if terms[3] == through_path:
            through_ion_frames.append((terms[1], int(terms[6]), int(terms[7])))
            entering_ion_frames[int(terms[6])] = terms[1]
            exiting_ion_frames[int(terms[7])] = terms[1]
        elif flg_first_end and flg_bound_at_begin:
            through_ion_frames.append((terms[1], int(terms[6]), int(terms[7])))
            exiting_ion_frames[int(terms[7])] = terms[1]
        elif flg_first_end and flg_bound_at_end:
            through_ion_frames.append((terms[1], int(terms[6]), int(terms[7])))
            entering_ion_frames[int(terms[6])] = terms[1]
    f_path.close()
    
    return through_ion_frames, entering_ion_frames, exiting_ion_frames

def is_ion_pass_through(atom_id, frame, through_ion_frames):
    flg = False
    for c_atom_id, first, last in through_ion_frames:
        if atom_id == c_atom_id and frame >= first and frame < last:
            return True
    
def analyze_run_vote(fn_in, fn_path, fn_out, fn_out_count,
                     fn_out_sim, fn_out_table, fn_out_table_trans,
                     atomnames, vote_steps, invalid_sites,
                     repl_site_label, through_path, only_through,
                     flg_through_first_end, through_path_begin,
                     separator_site, separator_atom,
                     t_begin, t_end):
    # take states by voting of before and after N steps
    through_ion_frames, entering_ion_frames, exiting_ion_frames = \
                        read_pass_through_ion_frames(fn_path, through_path, atomnames,
                                                     flg_through_first_end, through_path_begin)

    try: f_in = open(fn_in, "r")
    except IOError:
        sys.stderr.write("File"+ fn_in +" could not be opend.\n")
        sys.exit()
    try: f_out = open(fn_out, "w")
    except IOError:
        sys.stderr.write("File"+ fn_out +" could not be opend.\n")
        sys.exit()

    count_state = collections.defaultdict(int)
    count_trans = collections.defaultdict(int)
    count_trans_all = collections.defaultdict(int)
    count_wait = collections.defaultdict(int)

    prev_state = ''

    state_hist = []
    vote_size = vote_steps*2 + 1
    for line in f_in:  ## for each frame
        atom_info = re.compile("\s+").split(line.strip())
        frame = atom_info[0]
        if t_begin >= 0 and int(frame) < t_begin: continue
        if t_end >= 0 and int(frame) >= t_end:  break
        #site_state ... list of tuple(2 elements) [(site_id, atom_id)]
        site_state = collections.defaultdict(list)

        for info in atom_info[1:]:         ## for each atom
            site_id, atom_id, atom_name = re.compile(":").split(info);
            if atom_name in atomnames and not atom_name in invalid_sites or not site_id in invalid_sites[atom_name]:
                if site_id in repl_site_label:
                    site_id = repl_site_label[site_id]

                if through_ion_frames != [] and not is_ion_pass_through(atom_id, int(frame), through_ion_frames):
                    if not only_through:
                        site_state[atom_name].append((site_id+'*', atom_id))
                else:
                    site_state[atom_name].append((site_id, atom_id))
                    

        state_ = []
        state_atom = []
        for atom in atomnames:
            sites_ordered = sorted(site_state[atom], key=lambda x:x[0])
            state_.append(atom + separator_site + separator_site.join([x[0] for x in sites_ordered]))
            state_atom.append(atom + separator_site + separator_site.join([x[1] for x in sites_ordered]))
        state_str = separator_atom.join(state_)
        state_atom_str = separator_atom.join(state_atom)

        state_hist.append(state_str)
        
        if int(frame) in entering_ion_frames:
            f_out.write(frame + '\t@ENTERING\t' + entering_ion_frames[int(frame)] + '\n')
        if int(frame) in exiting_ion_frames:
            f_out.write(frame + '\t@EXITING\t' + exiting_ion_frames[int(frame)] + '\n')
        f_out.write(frame + '\t' + state_str + '\t' + state_atom_str + '\n')        

        if len(state_hist) == vote_size:
            voting = collections.defaultdict(int)
            for state in state_hist:
                voting[state]+=1
            state_repr = ""
            state_repr_cnt = 0
            for state, count in voting.items():
                if state_repr_cnt <= count:
                    state_repr = state
                    state_repr_cnt = count

            count_state[state_repr] += 1

            if prev_state != '':
                if prev_state != state_repr:
                    count_trans[(prev_state,state_repr)] += 1
                    count_trans_all[prev_state] += 1
                ##f_out.write(str(int(frame)-vote_steps) + '\t' + state_repr + '\n')
                else:
                    count_wait[state_repr] += 1
            prev_state = state_repr
            state_hist.pop(0)
        
            
    f_out.close()
    f_in.close()

    output_gml(fn_out_count, fn_out_table, fn_out_table_trans, count_state, count_trans, count_trans_all, count_wait)
    if fn_out_sim != "":
        output_state_similarity_score(fn_out_sim, count_state, count_trans, count_trans_all)

def _main():
    p = OptionParser()
    p.add_option('--i-site-occ', dest='fn_site_occ',
                 help="input file describing occupation in sites.")
    p.add_option('--i-path', dest='fn_path',
                 default = "",
                 help="input file for site path time generated by site_path_sort_by_passage_time.py")
    p.add_option('--o-states', dest='fn_states',
                 default="state_traj.txt",
                 help="output file for log of state transitions")
    p.add_option('--o-graph', dest='fn_graph',
                 help="output file for the graph in GML format")
    p.add_option('--o-table', dest='fn_table',
                 help="output file for the state table")
    p.add_option('--o-table-trans', dest='fn_table_trans',
                 help="output file for the state transition table.")
    p.add_option('--o-sim', dest='fn_sim',
                 help="output file for state similarities (TEST).")
    p.add_option('-a','--atomname', dest='atomnames',
                 action="append",
                 help="atom name to be considered")
    p.add_option('-i', dest='invalid_sites',
                 action="append", type="string",
                 help="Labels of binding sites to be ignroed")
    p.add_option('--averaging-steps', dest='ave_steps',
                 type="int",
                 default = 0,
                 help="number of steps for averaging coordinates")
    p.add_option('--rb', dest='repl_bef',
                 action="append",  type="str",
                 help="site label to be replaced")
    p.add_option('--ra', dest='repl_aft',
                 action="append",  type="str",
                 help="Labels of binding sites to be replaced into other labels specified by --rb option")
    p.add_option('--through-path', dest="through_path",
                 default="0:9:1:0",
                 help="Definition the path in site labels, that indicates through the entire pore, e.g. 0:9:1:0")
    p.add_option('--through-path-begin', dest="through_path_begin",
                 action="append",
                 help="Path definition for ions retained in the SF at the initial structure, e.g., 0:6:1:0, 0:4:1:0")
    p.add_option('--only-through', dest="only_through",
                 action="store_true", default=False,
                 help="A flag for considering only pass through ions")
    p.add_option('--without-first-end', dest="flg_through_first_end",
                 action="store_false", default=True,
                 help="Remove ions bound at the first and last frame from pass through paths")
    p.add_option('--separator-atom', dest="separator_atom",
                 default="/",
                 help="separator charactor for state string, spliting target atoms");
    p.add_option('--separator-site', dest="separator_site",
                 default=":",
                 help="separator charactor for state string, spliting binding sites")
    p.add_option('--begin', dest="begin",
                 type="int", default=-1,
                 help="frame to begin to consider")
    p.add_option('--end', dest="end",
                 type="int", default=-1,
                 help="frame to end to consider")
    opts, args = p.parse_args()
    flg_fail=False
    if not opts.fn_site_occ:
        sys.stderr.write("Option '--i-site-occ' is required.")
        flg_fail=True
    if not opts.fn_site_occ:
        sys.stderr.write("Option '--i-site-occ' is required.")
        flg_fail=True
    if not opts.atomnames:
        sys.stderr.write("At least one '--atomname' is required.")
        flg_fail=True
    if flg_fail:
        sys.exit()
    
    if not opts.through_path_begin:
        opts.through_path_begin = []
        
    repl_site_label = {}
    if opts.repl_bef and opts.repl_aft:
        if opts.repl_bef and opts.repl_aft and len(opts.repl_bef) != len(opts.repl_aft):
            print "ERROR: options for replacing site labels"
            sys.exit()
        for i,repl in enumerate(opts.repl_bef):
            repl_site_label[repl] = opts.repl_aft[i]

    invalid_sites = collections.defaultdict(set)
    if opts.invalid_sites:
        for invs in opts.invalid_sites:
            if re.compile(":").search(invs):
                atom, site = re.compile(":").split(invs)
                invalid_sites[atom].add(site)
            else:
                for atom in opts.atomnames:
                    invalid_sites[atom].add(invs)
    analyze_run_vote(opts.fn_site_occ, opts.fn_path,
                     opts.fn_states,   opts.fn_graph,
                     opts.fn_sim,      opts.fn_table,  opts.fn_table_trans,
                     opts.atomnames,
                     opts.ave_steps,   invalid_sites,
                     repl_site_label,  opts.through_path, opts.only_through,
                     opts.flg_through_first_end,  opts.through_path_begin,
                     opts.separator_site, opts.separator_atom,
                     opts.begin, opts.end)


if __name__ == '__main__':
    _main()
