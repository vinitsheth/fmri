# -*- coding: utf-8 -*-
"""
Created on Fri Oct 19 14:07:01 2018

@author: 
"""
import argparse
#
if __name__ == "__main__":
    
    # Ignore matplotlib and numpy warnings
    import warnings
    warnings.filterwarnings("ignore")

    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('integers', metavar='N', type=int, nargs='+',
                        help='an integer for the accumulator')
    parser.add_argument('--sum', dest='accumulate', action='store_const',
                        const=sum, default=max,help='sum the integers (default: find the max)')

    args = parser.parse_args()
    print(args.accumulate(args.integers))