#!/usr/bin/env python

import mdanaly
import dockml.pdbIO as pio
import os, sys
from collections import defaultdict
import dockml.index as ndx
from datetime import datetime
from mpi4py import MPI
import math
import numpy as np

def calculateNbyN(pdbfile, dcutoff, res1, res2, ndxlist) :

    cutoff = dcutoff ** 2

    cmap = mdanaly.ContactMap(pdbfile)

    crd1 = pio.coordinatesPDB().getAtomCrdByNdx(pdbfile, ndxlist[ res1 ])
    crd2 = pio.coordinatesPDB().getAtomCrdByNdx(pdbfile, ndxlist[ res2 ])

    t = cmap.residueContacts(resCrd1=crd1,
                             resCrd2=crd2,
                             distcutoff=cutoff,
                             verbose=False,
                             rank=0,
                             NbyN=True
                             )
    #print(t)
    return t

def scatterFileList(ranksize, fileList) :
    load4each = int(math.ceil(float(len(fileList)) / float(ranksize)))
    filesList = []

    pdbFileList = []
    for i in range(ranksize - 1):
        filesList.append(pdbFileList[i * load4each: load4each * (i + 1)])
    filesList.append(pdbFileList[(ranksize - 1) * load4each:])

    return pdbFileList

if __name__ == "__main__" :

    startTime = datetime.now()

    comm = MPI.COMM_WORLD
    size = comm.Get_size()
    rank = comm.rank

    MAX = 2000

    fileList = [ "S_%d.pdb"%str(x) for x in range(MAX) ]

    if rank == 0 :
        pdbFileList = scatterFileList(size, fileList)
    else :
        pdbFileList = None

    filesList = comm.scatter(pdbFileList, root=0)

    results = []

    for fn in filesList :
        count = 0
        print("progress file name {}, number {} out of ".format(fn, count, len(filesList)))

        chain = ' '
        resindex = [ str(x) for x in range(1, 251) ]
        cutoff= 5.0
        atomtype = "side-chain-noH"

        ndxdict = defaultdict(list)
        for res in resindex :
            ndxdict[res] = ndx.PdbIndex().res_index(fn, chain,
                                                    residueNdx=[int(res)],
                                                    atomtype=atomtype,
                                                    atomList=[],
                                                    )

        print(ndxdict)

        nbyn = [ calculateNbyN(fn, cutoff, x, y, ndxdict) for x in resindex for y in resindex ]
        #pair = [ [x, y] for x in resindex for y in resindex ]

        results.append(nbyn)
        count += 1


    overallValuesList = comm.gather(results, root=0)
    if rank == 0:
        np.savetxt("res_sidechain_cmap_nbyn.csv", np.array(overallValuesList), delimiter=',', fmt="%5.3f")

    print("Total Time Usage: ")
    print(datetime.now() - startTime)