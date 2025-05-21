import matplotlib
matplotlib.use('Agg')
import numpy as np
from collections import Counter
import tools
import os
import argparse
from copy import deepcopy
import random



def getArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p1', '--seeds_RFClabel_file_path', type=str, default="6forest1/dataset/test_dataset/seeds_1e5_RFClabel.txt")
    parser.add_argument('-p2', '--seeds_file_path', type=str, default="6forest1/dataset/test_dataset/seeds_1e5.txt")
    parser.add_argument('-p3', '--ipv6_pred_save_path', type=str, default="6forest1/result/IPv6_Hitlist/pred.txt")
    parser.add_argument('-p4', '--budget', type=str, default="1000")
    parser.add_argument('-p5', '--budget_testing_ratio', type=str, default="0.01")
    return parser.parse_args()


def main():
    np.random.seed(0)
    random.seed(0)
    args = getArgs()
    print(matplotlib.pyplot.get_backend())


    # TODO: 2.1 two-level DHC: step 1.
    file_path = args.seeds_RFClabel_file_path
    ip_patterns = [] # every ip's generation patterns
    with open(file_path) as f:
        for ip_type in f.read().splitlines():
            ip_patterns.append(ip_type.split("=")[3])
    print(Counter(ip_patterns))

    file_path = args.seeds_file_path
    ips = []
    with open(file_path) as f:
        for ip in f.read().splitlines():
            ips.append(ip)
    
    # Preset some commonly used keys. 
    group1 = {'ieee-derived': [], 'randomized': [], 'low-byte': [], 'embedded-ipv4': [], 'embedded-port': [], 'pattern-bytes': [], 'isatap': []} 
    # When there are too many patterns and adding them manually is too cumbersome, the alternative solutions are as follows
    # group1_ip = {}
    # for p in ip_patterns:
    #     if p not in group1_ip:
    #         group1_ip[p] = []

    for i in range(0,len(ips)):
        temp = tools.ip2list(ips[i]) # change ip to numpy array
        group1[ip_patterns[i]].append(temp)    
    
    
    # TODO: 2.2 + 3 two-level DHC: step 2, with outlier detection.
    group2 = {}
    count_seed_0 = 0 # the number of unique addresses
    for key in group1:
        data = tools.deduplicate(group1[key])  # Deduplication operation, otherwise the DHC algorithm will fall into an infinite loop
        if len(data) == 0:
            continue
        data = np.array(data)
        print('pattern: ', key, ',    the number of seed:', data.shape[0])
        count_seed_0 += data.shape[0]
        reserved_patterns, _ = tools.coveringBasedDHC(data)
        group2[key] = reserved_patterns
    print("the number of unique addresses:", count_seed_0)
    
    
    # TODO: 1 pattern filter
    patterns = [] # A two-dimensional list, each element is a set of seeds, belonging to a final address space.
    noKeys = ['randomized', 'ieee-derived'] # abandoned patterns
    for key in group2:
        if key in noKeys:
            print("abandon pattern:", key)
            continue
        patterns += group2[key]
    
    
    # TODO: 4 generate potential addresses (numpy arrays)
    count = 0
    for arrs in patterns:
        count += arrs.shape[0]
    print("useful seed number:", count)
    print("removal rate:", 1-count/len(ips))
    budget = int(float(args.budget) * float(args.budget_testing_ratio))
    arrs_num = [arrs.shape[0] for arrs in patterns]
    arrs_sum = sum(arrs_num)
    arrs_budgets = [max(1, budget * num // arrs_sum) for num in arrs_num]
    
    arrs_pred_all = []
    patterns = np.array(patterns,dtype=object)
    for i in range(patterns.shape[0]):
        arrs_pred_all.append(tools.randomGeneration(arrs=patterns[i], budget=arrs_budgets[i]))
    
    # change arrays to IP
    ips_pred_all = []
    for i in range(len(arrs_pred_all)):
        temp = []
        for j in range(arrs_pred_all[i].shape[0]):
            temp.append(tools.numpyArr2ip(arrs_pred_all[i][j]))
        ips_pred_all.append(deepcopy(temp))

    # save ips to file
    file_path = args.ipv6_pred_save_path
    with open(file_path, 'w') as f:
        for ips_pred in ips_pred_all:
            for ip in ips_pred:
                f.write(f"{ip}\n")

    # hit rate can be calculated by Zmap test!

if __name__ == "__main__":
    main()