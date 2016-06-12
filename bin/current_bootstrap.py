#!/usr/bin/env python2.6
#$ -S /usr/bin/python2.6
#$ -cwd

from optparse import OptionParser
import random
import numpy as np

def get_options():
    p = OptionParser()
    p.add_option('--i-permeation-event', dest='fn_permeation_event',
                 help="input file name for site occupation trajectory")
    p.add_option('--iteration', dest='iteration',
                 type="int",
                 help="The number of iteration for bootstrapping")
    #p.add_option('--block-size', dest='block_size',
    #type="int",
    #help="The block size (the number of frames for each block)")
    p.add_option('--block-num', dest='block_num',
                 type="int",
                 help="The block number")
    p.add_option('--atomname', dest='atomnames',
                 help="Atom names")
    p.add_option('--begin', dest='f_begin',
                 type="int",
                 help="frame to begin")
    p.add_option('--end', dest='f_end',
                 type="int",
                 help="frame to end")
    opts, args = p.parse_args()
    return opts, args

def read_perm_event(fn, atomname):
    f = open(fn)
    pass_frames = set()
    for line in f:
        terms = line.strip().split()
        if terms[1] != atomname: continue
        outward = False
        if terms[2] == "-" and terms[3] == "+":            
            outward = True
        elif terms[2] == "+" and terms[3] == "-":
            outward = False
        else:
            continue
        pass_frames.add(int(terms[5]))
    f.close()
    return pass_frames

def sampling(pass_frames, f_begin, f_end, block_num):
    frame_range = f_end - f_begin
    block_size = frame_range / block_num
    #print "block_size : " + str(block_size)
    max_frame = frame_range - block_size
    pass_num = 0
    for i in range(block_num):
        #rnd_frame = random.randrange(0, max_frame)
        rnd = random.randrange(0, block_num)
        rnd_frame = rnd*block_size
        #print rnd_frame
        for pf in pass_frames:
            if pf >= rnd_frame and pf < rnd_frame+block_size:
                pass_num+=1
                #print "*"
    return pass_num

def _main():
    opts, args = get_options()
    pass_frames = read_perm_event(opts.fn_permeation_event, opts.atomnames)
    random.seed()
    
    pass_num = np.zeros(opts.iteration, np.int32)
    for i in xrange(opts.iteration):
        pass_num[i] = sampling(pass_frames, opts.f_begin, opts.f_end, opts.block_num)

    print "average : " + str(np.average(pass_num))
    print "sd      : " + str(np.std(pass_num))
        
    return 
    
if __name__ == '__main__':
    _main()
    
