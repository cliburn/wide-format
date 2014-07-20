import os
import sys
from pandas import DataFrame
import pandas as pd
import numpy as np

filename = sys.argv[1]
current_sample = sys.argv[2]

h5f = filename.replace('txt', 'h5')
f = os.path.join(basedir, filename)

try:
    # Part 3 - working with wide format 
    df = pd.read_hdf(h5f, 'wide_format')
    df.to_csv('wide_format.csv', index=False)
except:

    # Part 1 - chunking by sample
    samples = []
    rows = []

    i = 0
    for i, line in enumerate(open(f)):
        if i < 10:
            continue
        snp, sample, g1, g2 = line.split('\t')[:4]
        genotype = ''.join([g1, g2])
        if sample == current_sample:
            rows.append((snp, genotype))
        else:
            print current_sample, i
            samples.append(current_sample)
            df = DataFrame(rows, columns=['SNP', current_sample])
            df.to_hdf(h5f, current_sample)
            rows = [(snp, genotype)]
            current_sample = sample

    # Part 2 - assemble wide format
    print 'Assembling wide format'
    df = pd.read_hdf(h5f, samples[0])
    for sample in samples[1:]:
        print sample
        df1 = pd.read_hdf(filename.replace('txt', 'h5'),sample)
        df = df.merge(df1, on='SNP')

    df.to_hdf(h5f, 'wide_format')
    print 'Wide format assembled'

