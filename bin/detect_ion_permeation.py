#!/usr/bin/env python2.6
#$ -S /usr/bin/python2.6
#$ -cwd

from optparse import OptionParser
import sys
import re
import collections
import json 

def convert_options(opts):
    cfg = {}
    cfg["files"] = {}
    cfg["files"]["pore-crd-h"] = opts.fn_pore_crd_h
    cfg["files"]["pore-crd-r"] = opts.fn_pore_crd_r
    cfg["files"]["permeation-event"] = opts.fn_permeation_event
    cfg["target-atoms"] = []
    cfg["boundary-r"] = opts.boundary_r
    cfg["boundary-h-nega-high"] = opts.boundary_h_nega_high
    cfg["boundary-h-posi-low"] = opts.boundary_h_posi_low
    for at in opts.target_atoms:
        at_config = {}
        at_config["name"] = at
        cfg["target-atoms"].append(at_config)
    cfg["time"] = {}
    cfg["time"]["begin"] = opts.begin
    cfg["time"]["end"] = opts.end
    if opts.fn_config:
        try: f_js = open(opts.fn_config,"r")
        except IOError:
            sys.stderr.write("File "+opts.fn_config+" could not be opend.")
        js = ""
        for line in f_js:
            if line[0] != "#" and line[0] != ";":
                js += line
        try:
            cfg = json.JSONDecoder().decode(js)
        except:
            sys.stderr.write("Fail to parse the JSON file: " + opts.fn_config)
            raise
        f_js.close()
    return cfg

def analyze_run(fn_in, fn_in_r, fn_out,
                target_atoms_conf,
                boundary_r,
                boundary_h_nega_high,
                boundary_h_posi_low,
                t_begin, t_end):  
    target_atoms = []
    for conf in target_atoms_conf:
        target_atoms.append(conf["name"])

    try: f_in = open(fn_in,'r')
    except IOError:
        sys.stderr.write("Could not open "+fn_in)
    try: f_in_r = open(fn_in_r,'r')
    except IOError:
        sys.stderr.write("Could not open "+fn_in_r)
    try: f_out = open(fn_out, 'w')
    except IOError:
        sys.stderr.write("Could not open "+fn_out)

    atom_id_list = []

    ## atom_id_name[aotm_id] = atom_name
    atom_id_name = {}

    ## ion_states[int(ATOM-ID)] = (FIRST_TIME, SIGN_COORD_H,  LAST_TIME, SIGN_COORD_H)
    ion_states = collections.defaultdict(list)

    atom_def = re.compile("\s+").split(f_in.readline().strip())
    f_in_r.readline().strip()
    for atom in atom_def:
        atom_id, atom_name = re.compile(":").split(atom)
        atom_id = int(atom_id)
        atom_id_name[atom_id] = atom_name
        atom_id_list.append(atom_id)
        ion_states[atom_id] = [-1,"0",-1,"0"]
        
    first_frame = -1
    frame = -1
    coords = None
    for line in f_in:  ## for each frame
        line_r = f_in_r.readline()
    
        coords = re.compile("\s+").split(line.strip())
        coords_r = re.compile("\s+").split(line_r.strip())[1:]
        frame = int(float(coords[0]))

        if t_begin >= 0 and frame < t_begin: continue
        if t_end >= 0 and frame >= t_end:  break

        if first_frame == -1: first_frame=frame
        if frame%1000==0: print frame

        coords = coords[1:]
        for i, crd in enumerate(coords):
            atom_id = atom_id_list[i]
            atom_name = atom_id_name[atom_id]
            if not atom_name in target_atoms: continue

            flg_out = False
            if crd == "-": flg_out = True
            if coords_r[i] == "-": flg_out = True
            crd_r = 0.0
            if not flg_out:
                crd = float(crd)
                crd_r = float(coords_r[i])
                if boundary_r > 0 and crd_r > boundary_r: flg_out = True

            ##check history
            if flg_out:
                if ion_states[atom_id][2] >= 0 and \
                       ion_states[atom_id][1] != ion_states[atom_id][3]:
                    line = str(atom_id) + '\t'
                    line += str(atom_name) + '\t'
                    line += str(ion_states[atom_id][1]) + '\t'
                    line += str(ion_states[atom_id][3]) + '\t'
                    line += str(ion_states[atom_id][0]) + '\t'
                    line += str(ion_states[atom_id][2]) + '\n'
                    f_out.write(line)
                ion_states[atom_id] = [-1,"0",-1,"0"]
            else:
                field_a = 0
                if ion_states[atom_id][0] >= 0: field_a += 2
                if crd < boundary_h_nega_high: ## or (frame==first_frame and crd<0.0):
                    ion_states[atom_id][field_a] = frame
                    ion_states[atom_id][field_a+1] = "-"
                elif crd > boundary_h_posi_low: ## or (frame==first_frame and crd>=0.0):
                    ion_states[atom_id][field_a] = frame
                    ion_states[atom_id][field_a+1] = "+"
                #print ion_state[atom_id]
    f_out.close()
    f_in_r.close()
    f_in.close()

    ##for i, crd in enumerate(coords):
    ##    atom_id = atom_id_list[i]
    ##    if ion_states[atom_id][0] >= 0:
    ##        line = str(atom_id) + '\t'
    ##        line += str(atom_name) + '\t'
    ##        line += str(ion_states[atom_id][1]) + '\t'
    ##        line += '*\t'
    ##        line += str(ion_states[atom_id][0]) + '\t'
    ##        line += str(frame) + '\n'
    ##        f_out.write(line)
            

def _main():
    p = OptionParser()
    p.add_option('--i-pore-crd-h', dest='fn_pore_crd_h',
                 help="file name for pore axis coordinates h generated by trachan.")
    p.add_option('--i-pore-crd-r', dest='fn_pore_crd_r',
                 help="file name for pore axis coordinates r generated by trachan.")
    p.add_option('--o-permeation-event', dest='fn_permeation_event',
                 default = "permeation_event.txt",
                 help="output file name.")
    p.add_option('--atom', dest='target_atoms',
                 action="append",
                 help="target atom name")
    p.add_option('--b-r', dest="boundary_r",
                 type="float", default = -1.0,
                 help="maximum r value to be considered")
    p.add_option('--b-h-posi-low', dest="boundary_h_posi_low",
                 type="float", default = -1.0,
                 help="lower boundaries in h axis for positive h")
    p.add_option('--b-h-nega-high', dest="boundary_h_nega_high",
                 type="float", default = -1.0,
                 help="higher boundaries in h axis for negative h")
    p.add_option('-c', dest="fn_config",
                 help="file name for settings in json")
    p.add_option('--begin', dest="begin",
                 type="int", default=-1,
                 help="frame to begin to consider")
    p.add_option('--end', dest="end",
                 type="int", default=-1,
                 help="frame to end to consider")
    opts, args = p.parse_args()
    
    cfg = convert_options(opts)

    print "//\n"
    analyze_run(cfg["files"]["pore-crd-h"],
                cfg["files"]["pore-crd-r"],
                cfg["files"]["permeation-event"],
                cfg["target-atoms"],
                cfg["boundary-r"],
                cfg["boundary-h-nega-high"],
                cfg["boundary-h-posi-low"],
                cfg["time"]["begin"], cfg["time"]["end"])
        
if __name__ == '__main__':
    _main()

