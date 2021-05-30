import json
from collections import defaultdict
from os.path import join
from pprint import pprint

import jsonlines


def print_tuples_statistics(tuples_file, pids_file):
    num_sets = 0
    num_qids = 0
    num_qids_w_pids = 0
    num_pids = 0
    counts_per_pid = defaultdict(lambda: defaultdict(int))

    good_pids = json.load(open(pids_file))

    for d in jsonlines.open(tuples_file):
        num_sets += 1
        for qid in d['qids']:
            num_qids += 1
            pids = d['qids'][qid]['pids']
            if len(pids) > 0:
                num_qids_w_pids += 1
                num_pids += len(pids)

            # Keep track of the PID counts
            entity_types = d['qids'][qid]['entity_types']
            for pid in pids:
                for et in entity_types:
                    if et in good_pids:
                        counts_per_pid[et][pid] += 1

    print('# of AmbER sets:', num_sets)
    print('Avg. # QIDs per set:', round(num_qids/num_sets, 2))
    print('Avg. # QIDs with PIDs per set', round(num_qids_w_pids/num_sets, 2))
    print('Avg. # PIDs per set:', round(num_pids/num_sets, 2))

    percent_per_pid = {
        et: {
            pid: round(100*count/num_pids, 2)
            for pid, count in counts_per_pid[et].items()
        }
        for et in counts_per_pid
    }
    print(json.dumps(percent_per_pid, indent=4))


def print_instances_statistics(instances_file, task):
    num_instances = 0
    for amber_set in jsonlines.open(instances_file):
        for qid in amber_set['qids']:
            num_instances += len(amber_set['qids'][qid]['queries'])

    print('Number of', task, 'instances:', num_instances)


def print_statistics(amber_subset):
    print('\nAmbER-' + amber_subset[0].upper(), '\n-------')
    tuples_file = join('amber_sets', amber_subset, 'amber_set_tuples.jsonl')
    pids_file = join('amber_sets', amber_subset, 'good_pids.json')
    print_tuples_statistics(tuples_file, pids_file)

    fc_file = join('amber_sets', amber_subset, 'fc/amber_sets.jsonl')
    print_instances_statistics(fc_file, 'FC')
    sf_file = join('amber_sets', amber_subset, 'sf/amber_sets.jsonl')
    print_instances_statistics(sf_file, 'SF')
    qa_file = join('amber_sets', amber_subset, 'qa/amber_sets.jsonl')
    print_instances_statistics(qa_file, 'QA')

if __name__ == '__main__':
    print_statistics('human')
    print_statistics('nonhuman')