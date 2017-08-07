from __future__ import (
    absolute_import, division, print_function, unicode_literals)

import argparse
import collections
import csv
import os
import re
import sys

try:
    range = xrange
except NameError:
    pass


def readable_dir(dir_path):
    if not os.path.isdir(dir_path):
        raise argparse.ArgumentTypeError("{} is not a valid path"
                                         .format(dir_path))
    if os.access(dir_path, os.R_OK):
        return dir_path
    else:
        raise argparse.ArgumentTypeError("{} is not readable"
                                         .format(dir_path))


def read_fasta(infile, include_other_letters=False):
    sequences = []

    currseq = []
    for line in infile:
        line = line.strip()
        if type(line) is bytes and type(line) is not str:
            line = line.decode()
        if not line or line[0] == '>':
            if currseq:
                sequences.append(''.join(currseq))
                currseq = []
        else:
            if not include_other_letters:
                line = re.sub('[^ACGT]', '', line)
            currseq.append(line)
    if currseq:
        sequences.append(''.join(currseq))

    return sequences


args_parser = argparse.ArgumentParser(
    description='Search for microarray probe sequences in a genome.'
)
args_parser.add_argument('probe_length', type=int,
                         help='the length of the probe sequences to search '
                              'for')
args_parser.add_argument('probe_sequence_file', type=argparse.FileType('r'),
                         help='the TSV file of probe sequences')
args_parser.add_argument('genome_directory', type=readable_dir,
                         help='the directory containing the genome in FASTA '
                              'files')
args_parser.add_argument('--probe-sequence-header', default='PROBE_SEQUENCE',
                         help='the name of the column of probe_sequence_file '
                              'containing probe sequences')
args_parser.add_argument('--probe-id-header', default='PROBESET_ID',
                         help='the name of the column of probe_sequence_file '
                              'containing probe IDs')
args = args_parser.parse_args()


probe_file_reader = csv.DictReader(args.probe_sequence_file,
                                   delimiter=str('\t'))

# check for required columns
if args.probe_sequence_header not in probe_file_reader.fieldnames:
    print("couldn't find column {} in probe file"
          .format(args.probe_sequence_header))
    sys.exit(1)
if args.probe_id_header not in probe_file_reader.fieldnames:
    print("couldn't find column {} in probe file"
          .format(args.probe_id_header))
    sys.exit(1)

# read the probe sequences
print('loading probe sequences... ', end='')
sys.stdout.flush()

probe_seqs = {}
for probe in probe_file_reader:
    probe_seq = probe[args.probe_sequence_header]
    probe_id = probe[args.probe_id_header]
    if len(probe_seq) == args.probe_length:
        probe_seqs[probe_seq] = probe_id

print('got {} unique probes.\n'.format(len(probe_seqs)))

# search for probes within each genome sequence
all_matches = collections.defaultdict(list)
total_match_count = 0
for filename in os.listdir(args.genome_directory):
    filepath = os.path.join(args.genome_directory, filename)
    if not os.path.isfile(filepath):
        continue

    # read sequence
    print('reading file {}... '.format(filename), end='')
    sys.stdout.flush()

    with open(filepath, 'r') as seq_file:
        sequence = read_fasta(seq_file, include_other_letters=True)[0]

    print('done; searching... ', end='')
    sys.stdout.flush()

    # search for matches
    curr_match_count = 0
    for i in range(len(sequence) - args.probe_length + 1):
        if sequence[i:i+args.probe_length] in probe_seqs:
            probe_seq = sequence[i:i+args.probe_length]
            probe_id = probe_seqs[probe_seq]
            all_matches[(probe_seq, probe_id)].append('{}:{}'
                                                      .format(filename, i))
            curr_match_count += 1
    total_match_count += curr_match_count
    print('found {} matches.'.format(curr_match_count))
print('\nfound {} matches in total.'.format(total_match_count))

# write a CSV with the match locations
results_filename = args.probe_sequence_file.name + '-matches.csv'
print('writing match locations to {}... '.format(results_filename), end='')
sys.stdout.flush()

with open(results_filename, 'w') as results_file:
    fieldnames = ['probe id', 'probe sequence', 'match count',
                  'match locations']
    # otherwise this fails on Windows
    csv.register_dialect('proper-excel', lineterminator='\n')
    results_writer = csv.DictWriter(results_file, fieldnames,
                                    dialect='proper-excel')
    results_writer.writeheader()

    for (probe_seq, probe_id) in sorted(all_matches.keys()):
        match_locations = all_matches[(probe_seq, probe_id)]
        results_writer.writerow({
            'probe id': probe_id,
            'probe sequence': probe_seq,
            'match count': len(match_locations),
            'match locations': ','.join(match_locations)
        })

print('done.')
