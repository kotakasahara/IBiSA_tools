#!/usr/bin/python

from optparse import OptionParser
import sys
import re
import collections


def atom_path_full(site_path, separator):
    #str_path_full = atom_name + ":"
    str_path_full = separator.join(map(lambda x:str(x), site_path))
    return str_path_full

def atom_path_h_t(site_path, symbol_out, separator):
    #str_path_h_t = atom_name + ":"
    str_path_h_t = ""
    if len(site_path) <= 3:
        str_path_h_t = atom_path_full(site_path, separator)
    else:
        if site_path[0] == symbol_out:
            str_path_h_t += symbol_out + separator + str(site_path[1])
        else:
            str_path_h_t += str(site_path[0])
        if site_path[-1] == symbol_out:
            str_path_h_t += ':' + str(site_path[-2]) + separator + symbol_out
        else:
            str_path_h_t += ':' + str(site_path[-1])
    return str_path_h_t
                
def output_a_target_atom_path(atom_id, atom_id_name,
                              symbol_out, separator,
                              atom_path_site, atom_path_frame,
                              f_out,
                              count_path_full, count_path_h_t):
## output path of an ion
    str_path_full = atom_path_full(atom_path_site[atom_id], separator)
    str_path_h_t = atom_path_h_t(atom_path_site[atom_id], symbol_out, separator)
                
    st = str(atom_id) + "\t" + atom_id_name[atom_id] + "\t"
    st += str_path_h_t + "\t"
    st += str(atom_path_frame[atom_id][1]) + separator + str(atom_path_frame[atom_id][-1]) + '\t'
    st += str_path_full + '\t'
    st += separator.join([str(x) for x in atom_path_frame[atom_id][1:]])
    f_out.write(st + '\n')
    
    count_path_full[atom_id_name[atom_id] + separator + str_path_full] += 1
    count_path_h_t[atom_id_name[atom_id] + separator + str_path_h_t] += 1
    return count_path_full, count_path_h_t

def analyze_run(fn_site_occ, fn_all_path, fn_count_full, fn_count_h_t, symbol_out, separator):  
    try: f_in = open(fn_site_occ,'r')
    except IOError:
        sys.stderr.write("Error: File "+fn_site_occ+" could not be opened.\n")
        sys.exit()

    ## atom_name_id[aotm_name] = set(aotm_id, atom_id, ...)
    #### atom_name_id = collections.defaultdict(set)
    ## atom_id_name[aotm_id] = atom_name
    atom_id_name = {}

    ## atom_path_site[atom_id] = [site1, site2, ...]
    ## atom_path_frame[atom_id] = [frame1, frame2, ...]
    atom_path_site = collections.defaultdict(list)
    atom_path_frame = collections.defaultdict(list)

    ## counting path (full)
    ## count_path[path(described as a string, e.g., "1:2:3:4")] = int
    count_path_full = collections.defaultdict(int)

    ## counting path (first-last)
    ## count_path_h_t[path(described as a string, e.g., "1:4")] = int    
    count_path_h_t = collections.defaultdict(int)
    
    try: f_out = open(fn_all_path, 'w')
    except IOError:
        sys.stderr.write("Error: File "+fn_all_path+" could not be opened.\n")
        sys.exit()

    for line in f_in:  ## for each frame
        atom_info = re.compile("\s+").split(line.strip())
        frame = int(atom_info[0])
        atoms_in_sites = set()  ## atom id which was in sites at this frame

        for info in atom_info[1:]:         ## for each atom
            site_id, atom_id, atom_name = re.compile(":").split(info);
            atom_id = int(atom_id)
            atoms_in_sites.add(atom_id)
            atom_id_name[atom_id] = atom_name
            
            ## if there is no information about this atom,
            ## i.e. it is the first frame,
            ## the current site position was added into a path
            if len(atom_path_site[atom_id]) == 0:
                atom_path_site[atom_id] = [symbol_out]
                atom_path_frame[atom_id] = [frame]
                atom_path_site[atom_id].append(site_id)
                atom_path_frame[atom_id].append(frame)
            elif atom_path_site[atom_id][-1] != site_id:
                atom_path_site[atom_id].append(site_id)
                atom_path_frame[atom_id].append(frame)
                
        ## checking atoms disappeared from sites at this frame
        for atom_id, path in atom_path_site.items():
            if (not atom_id in atoms_in_sites) and path[-1] != symbol_out:
                atom_path_site[atom_id].append(symbol_out)
                atom_path_frame[atom_id].append(frame)

                count_path_full, count_path_h_t = output_a_target_atom_path(atom_id, atom_id_name,
                                                                            symbol_out, separator,
                                                                            atom_path_site, atom_path_frame,
                                                                            f_out,
                                                                            count_path_full, count_path_h_t)
                atom_path_site[atom_id] = [symbol_out]
                atom_path_frame[atom_id] = [frame]

    ## output residuel paths at the end of trajectory
    for atom_id, path in atom_path_site.items():
        if path != [symbol_out]:
            count_path_full, count_path_h_t = output_a_target_atom_path(atom_id, atom_id_name,
                                                                        symbol_out, separator,
                                                                        atom_path_site, atom_path_frame,
                                                                        f_out,
                                                                        count_path_full, count_path_h_t)
            atom_path_site[atom_id] = [symbol_out]
            atom_path_frame[atom_id] = [frame]
            
            
    #for atom_id, path in atom_path_site.items():
    #    if len(path) > 1:
    #        str_path_full = atom_path_full(atom_path_site[atom_id], separator)
    #        str_path_h_t = atom_path_h_t(atom_path_site[atom_id], symbol_out, separator)

    #        st = str(atom_id) + "\t" + atom_id_name[atom_id] + "\t"
    #        st += str_path_full + "\t" + str_path_h_t + "\t"
    #        for i, site in enumerate(atom_path_site[atom_id]):
    #            st += "\t" + str(atom_path_frame[atom_id][i])
    #        f_out.write(st + '\n')

    f_out.close()
    f_in.close()

    try: f_out = open(fn_count_full, 'w')
    except IOError:
        sys.stderr.write("Error: File "+fn_count_full+" could not be opened.\n")
        sys.exit()
    for path, count in count_path_full.items():
        f_out.write(path + '\t' + str(count) + '\n')
    f_out.close()

    try: f_out = open(fn_count_h_t, 'w')
    except IOError:
        sys.stderr.write("Error: File "+fn_count_h_t+" could not be opened.\n")
        sys.exit()
    for path, count in count_path_h_t.items():
        f_out.write(path + '\t' + str(count) + '\n')
    f_out.close()

def _main():
    p = OptionParser()
    p.add_option('--i-site-occ', dest='fn_site_occ',
                 help="input file name for site occupation trajectory")
    p.add_option('--o-all-path', dest='fn_all_paths',
                 default="site_path.txt",
                 help="output file name paths of all target atoms.")
    p.add_option('--o-count-full', dest='fn_count_full',
                 default="site_path_count_full.txt",
                 help="output file name for counts of each path (full trajectory).")
    p.add_option('--o-count-head-tail', dest='fn_count_h_t',
                 default="site_path_count_ht.txt",
                 help="output file name for counts of each paths (considering only the first and last site).")
    p.add_option('--symbol-out', dest='symbol_out',
                 default="*",
                 help="the symbol meaning out of sites")
    p.add_option('--separator', dest='separator',
                  default=":",
                 help="separator symbols between sites in paths")
    opts, args = p.parse_args()

    flg_fail = False
    if not opts.fn_site_occ:
        sys.stderr.write("Error: Option '--i-site-occ' is required.\n")
        flg_fail=True
    if flg_fail:
        exit(1)


    analyze_run(opts.fn_site_occ, opts.fn_all_paths, opts.fn_count_full, opts.fn_count_h_t,
                opts.symbol_out, opts.separator)
        
if __name__ == '__main__':
    _main()
