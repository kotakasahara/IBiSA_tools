#!/bin/tcsh
#$ -S /bin/tcsh
#$ -cwd

## 
set ISACMD=~/dev/gromacs_tools/isac-md
## Specify the title of your run
set TITLE = "120mv_150mm"

## 1.
## Analyzing MD trajectories produced by Gromacs.
## The Cartesian coordinates of focused atoms are
##  converted into the pore axis coordinates 

#echo "trachan"
#$ISACMD/bin/trachan --fn-cfg config.txt

## 2. 
## Deciding boundaries among binding sites,
## by checking pore_axis.txt

R --vanilla --slave < $ISACMD/r/pore_axis_density.R > pore_axis_density.log

## 3.
## Discretize trajectory based on ion-binding sites
echo "site_occupancy"
$ISACMD/bin/site_occupancy.py \
  --i-pore-crd-h pore_axis.txt \
  --i-pore-crd-r pore_axis_r.txt \
  --o-site-occ   site_occ.txt \
  -b 15.13 -b 12.93 -b 9.32 -b 6.25 -b 3.00 -b 0.44 -b -2.21 -b -6.08  -b -20 \
  -n '-1'  -n 0     -n 1    -n 2    -n 3    -n 4    -n 5     -n 6

## 4.
## Generating ion-binding state graphs

echo "analyze_site_state.py"
$ISACMD/bin/analyze_site_state.py \
  --i-site-occ site_occ.txt \
  --o-states   state_traj.txt \
  --o-graph    state_graph.gml \
  --o-table       state_table.txt \
  --o-table-trans state_trans_table.txt \
  --atomname   K \
  -i '-1' -i 7

## from this result, checking what state was the most major state.
## It will be defined as the "home state".

## 5.
## The .gml file can be visualized by using Cytoscape software
## 

## 6.
## Analyzing trajectories in each ion

echo "analyze_ion_path"
$ISACMD/bin/analyze_ion_path.py \
  --i-site-occ        site_occ.txt \
  --o-all-path        site_path.txt \
  --o-count-full      site_path_count_full.txt \
  --o-count-head-tail site_path_count_ht.txt

## 7.
## Extracting cyclic parts from the state trajectory

echo "extract_cycles.py"
$ISACMD/bin/extract_cycles.py \
  --i-state  state_traj.txt \
  --o-cycles state_traj_cycles.txt \
  --o-state-dict state_dict_pre.txt \
  --title    ${TITLE}

## 8.
## Converting states into characters.
## A cyclic parts transformed into a sequence.
echo "cycle_to_sequence"
$ISACMD/bin/cycle_to_sequence.py \
  --i-cycles     state_traj_cycles.txt \
  --i-state-dict state_dict_pre.txt \
  --o-state-dict state_dict.txt \
  --o-sequence   sequences.fsa \

## 9.
## Generating score matrix of states
echo "make_score_matrix"
$ISACMD/bin/make_score_matrix.py \
   --i-state-dict  state_dict.txt \
   --o-score       score_matrix.txt

## 10.
## Performing sequence alignments 
echo "dp_align"
$ISACMD/bin/dp_align.py \
   --i-score-matrix score_matrix.txt \
   --i-sequence     sequences.fsa \
   --o-align        align.txt -a\
   --min-len   4 \
   -g 1.0 \
   -m 1.0 \
   --ignore *

## 11
echo "align_similarity"
$ISACMD/bin/align_similarity.py \
  --i-align     align.txt \
  --i-sequence  sequences.fsa \
  --o-sim       align_sim.txt \
  -g 1 -m 1

grep '>' sequences.fsa > sequences_header.txt

## Clustering aligned sequences
echo "R clustering sequences"
R --vanilla --slave < $ISACMD/r/clustering_seq.R > clustering_seq.log
