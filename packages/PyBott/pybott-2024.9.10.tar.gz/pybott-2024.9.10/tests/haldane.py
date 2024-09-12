#!/usr/bin/env python

# Haldane model from Phys. Rev. Lett. 61, 2015 (1988)
# Solves model and draws one of its edge states.

# Copyright under GNU General Public License 2010, 2012, 2016
# by Sinisa Coh and David Vanderbilt (see gpl-pythtb.txt)

from __future__ import print_function
from pythtb import * # import TB model class
import numpy as np

import bott

def haldane_model(n_side=6, t1=1, t2=0.2j, delta=0, pbc=True):
    t2c = t2.conjugate()

    lat=[[1.0,0.0],[0.5,np.sqrt(3.0)/2.0]]
    orb=[[1./3.,1./3.],[2./3.,2./3.]]

    my_model=tb_model(2,2,lat,orb)

    my_model.set_onsite([-delta,delta])

    my_model.set_hop(t1, 0, 1, [ 0, 0])
    my_model.set_hop(t1, 1, 0, [ 1, 0])
    my_model.set_hop(t1, 1, 0, [ 0, 1])

    my_model.set_hop(t2 , 0, 0, [ 1, 0])
    my_model.set_hop(t2 , 1, 1, [ 1,-1])
    my_model.set_hop(t2 , 1, 1, [ 0, 1])
    my_model.set_hop(t2c, 1, 1, [ 1, 0])
    my_model.set_hop(t2c, 0, 0, [ 1,-1])
    my_model.set_hop(t2c, 0, 0, [ 0, 1])

    # # print tight-binding model details
    # my_model.display()


    # cutout finite model first along direction x
    tmp_model=my_model.cut_piece(n_side,0,glue_edgs=pbc)
    # cutout also along y direction 
    fin_model=tmp_model.cut_piece(n_side,1,glue_edgs=pbc)


    (evals,evecs)=fin_model.solve_all(eig_vectors=True)

    # pick index of state in the middle of the gap
    ed=fin_model.get_num_orbitals()//2

    # draw one of the edge states in both cases
    # (fig,ax)=fin_model.visualize(0,1,eig_dr=evecs[ed,:],draw_hoppings=False)
    # ax.set_title("Edge state for finite model without periodic direction")
    # ax.set_xlabel("x coordinate")
    # ax.set_ylabel("y coordinate")
    # fig.tight_layout()
    # fig.savefig("edge_state.pdf")

    # print('Done.\n')

    # print("Coordonnées des vecteurs du réseau (lattice vectors) :")
    # for i, vector in enumerate(tmp_model._lat):
    #     print(f"Vecteur {i}: {vector}")

    return fin_model._orb, evals, evecs.T




