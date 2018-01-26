import numpy as np
import argparse
from argparse import RawTextHelpFormatter
import sys
from dockml import index

class TimeStamp :

    def __init__(self):
        pass

    def selectDataPoints(self, dataf, upbounds, lowbounds, dt=100, usecols=[0, 1]):

        df = np.loadtxt(dataf, comments="#", delimiter=" ", usecols=usecols)
        timestamp = np.arange(df.shape[0]) * dt

        df[:, df.shape[1]] = timestamp

        selected = df

        for i in range(df.shape[1]) :
            selected = selected[ selected[:, i] > upbounds[i] ]
            selected = selected[ selected[:, i] < lowbounds[i]]

        return selected

    def outputIndex(self, output, groupname, indexes):

        tofile = open(output, 'w')
        tofile.write("[ %s ] \n"%(groupname))
        i = 0
        for atom in indexes :
            i += 1
            tofile.write('%6d ' % atom)
            if i % 15 == 0:
                tofile.write('  \n')
        tofile.write(" \n")
        tofile.close()

        return 1

def arguments() :

    d = """
    
    """

    parser = argparse.ArgumentParser(description=d)
    parser.add_argument('-dat', type=str, help="Input data set")
    parser.add_argument('-dt', type=int, default=10,
                        help="Time step used in the dataset file. Default is 10. \n")
    parser.add_argument('-up', type=float, default=[0, 1], nargs="+",
                        help="Upbounds for selection of data points. \n")
    parser.add_argument('-low', type=float, default=[0, 1], nargs="+",
                        help="Lowbounds for selection of data points. \n")
    parser.add_argument('-cols', type=int, default=[0, 1], nargs="+",
                        help="Used cols for datapoint selections. Default is 0 and 1. \n")
    parser.add_argument('-out', type=str, default="index.ndx",
                        help="Output the index of the data points to GMX format file. \n")
    parser.add_argument('-gn', type=str, default="",
                        help="Output the index group name. Default is empty. \n")

    args = parser.parse_args()

    if len(sys.argv) < 2 :
        parser.print_help()

    return args

def main() :

    ts = TimeStamp()

    args = arguments()

    dp = ts.selectDataPoints(args.dat, args.up, args.low, dt=args.dt, usecols=args.cols)

    indexes = dp[:, 0]

    if len(args.gn) :
        groupname = args.gn
    else :
        groupname = "+".join([str(x) for x in args.up ]) + "_" + "+".join([str(x) for x in args.low ])

    ts.outputIndex(args.out, groupname, [int(x) for x in indexes])