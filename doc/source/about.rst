=====================================
About
=====================================

-------------------------------------
Authors
-------------------------------------

IBiSA_tools version 1.00 (12 Jul. 2016)

* Kota Kasahara, Ritsumeikan University, Japan
* Kengo Kinoshita, Tohoku University, Japan

-------------------------------------
Citation
-------------------------------------

* Kasahara K and Kinoshita K, (Under review) IBiSA_tools: A Computational Toolkit for the Ion Binding State Analysis on Molecular Dynamics Trajectories of Ion Channels.
* Kasahara K, Shirota M, and Kinoshita K (2016) Ion Concentration- and Voltage-Dependent Push and Pull Mechanisms of Potassium Channel Ion Conduction. PLoS ONE, 11, e0150716.
* Kasahara K, Shirota M, and Kinoshita K (2013) Ion Concentration-Dependent Ion Conduction Mechanism of a Voltage-Sensitive Potassium Channel. PLoS ONE, 8, e56342.

-------------------------------------
Requirements
-------------------------------------

* The current version of IBiSA_tools can be applied only for GROMACS trajectory file (.trr). If your trajectories are written in another format, you have to convert it into .trr, by using some tools, e.g., VMD plugin and MDAnalysis (see Appendix).
* IBiSA_tools is consisting of a C++ program and Python (2.6 or 2.7) scripts.
* The attached tutorial files use R software (www.r-project.org) to draw plots.
* Network drawing software, e.g., Cytoscape, is required to visualize ion-binding state graph.

-------------------------------------
Download
-------------------------------------

https://github.com/kotakasahara/IBiSA_tools

-------------------------------------
Installation
-------------------------------------

Only a C++ program, trachan, must be compiled as follows::

  cd src/trachan
  ./configure
  make

In this document, we assume the binary and python scripts are included in the directory indicated as ${IBISA}.
