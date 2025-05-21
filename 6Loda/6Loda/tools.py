import numpy as np
from IPy import IP
from SpacePartition import *
import random
from copy import deepcopy
from pyod.models.loda import LODA

# TODO: something to note
# 1. All addresses are in the default list format. The ipv6 abbreviation format needs to be converted to the corresponding list format using <ip2list> before processing.

def seed_distance(a, b):
    return len(np.argwhere(a != b))

def ip2list(ip):
    """
    input ipv6 (compact format), convert to corresponding list form
    """
    return [int(x, 16) for x in IP(ip).strFullsize().replace(":", "")]

def numpyArr2ip(arr):
    """
    Input a numpy IP array and return the corresponding hexadecimal IP.
    """
    arr = "".join([format(x, "x") for x in arr])
    return (":".join([arr[i:i+4] for i in range(0, len(arr), 4)]))



def deduplicate(array):
    """
    Remove duplicates from the list, with no guarantee of relative order.
    """
    unique_tuples = set(map(tuple, array))
    unique_list = list(map(list, unique_tuples))
    return unique_list
    """
    Remove duplicates from the list while keeping the relative order fixed
    """
    # seen = set()
    # unique_list = []
    # for sublist in array:
    #     tuple_sublist = tuple(sublist)
    #     if tuple_sublist not in seen:
    #         seen.add(tuple_sublist)
    #         unique_list.append(sublist)
    # return unique_list

def outlierDetect_null(arrs):
    """
    No outlier removal algorithm, only for comparison
    """
    return [arrs], []

def outlierDetect(arrs):  #  LODA-based
    """ 
    Detecting abnormal IPv6 addresses based on the Loda algorithm
    Input address clustering in numpy two-dimensional form, 
    and return the filtered clustering result list and the corresponding abnormal address list.
    """
    if len(arrs) == 1:
        return [], [arrs]
    if len(arrs) == 2:
        if seed_distance(arrs[0], arrs[1]) > 12: # If there are more than 12 nibbles, two addresses are considered to be abnormal addresses.
            return [], [arrs]
        else:
            return [arrs], []
    loda = LODA(contamination=0.1)
    loda.fit(arrs)
    outlier_scores = loda.labels_  # 0 means normal, 1 means abnormal
    return [arrs[outlier_scores == 0]], [arrs[outlier_scores == 1]]

def coveringBasedDHC(data):
    """
    Input a group of addresses, return the covering-based DHC results(reserved addresses and outliers).
    """
    outliers = []
    patterns = []
    results = DHC(data)
    for r in results:
        p, o = outlierDetect(r)
        patterns += p
        outliers += o
    # Calculate the number of outliers
    count_o = 0
    for o in outliers:
        count_o += o.shape[0]
    print("the number of outliers:", count_o)
    return patterns, outliers



def randomGeneration(arrs, budget):
    """
    Generate addresses randomly, based on the input address space and budget.
    """
    random.seed(0)
    if budget == 0:
        return np.array([])
    # find variable nibble
    address_space = []
    Tarrs = arrs.T
    indexes = []
    for i in range(32):
        splits = np.bincount(Tarrs[i], minlength=16)
        if len(splits[splits > 0]) == 1:
            address_space.append(format(np.argwhere(splits > 0)[0][0], "x"))
        else:
            address_space.append("*")
            indexes.append(i)
    # generate random addresses in variable nibble
    arrs = arrs.tolist()
    new_arrs = []
    count = 0
    max_count = 16 * len(indexes) - len(arrs) # change one nibble
    while (count < budget) and (count < max_count):
        arr = random.choice(arrs).copy()
        index = random.choice(indexes)
        arr[index] = random.randint(0, 15)
        if (arr not in arrs) and (arr not in new_arrs):
            new_arrs.append(arr)
            count += 1
    return np.array(new_arrs)


if __name__ == '__main__':
    ss = ["2a0e1bc0009700000000000000000001",
          "2a0e2400053f00000000000000000001",
          "2a0e04090c820000021132fffee5b604",
          "2a0e04090c8200000000000000000001",
          "2a0e8f02212f00000000000000000001"]
    arrs = np.array([[int(i, 16)for i in s] for s in ss]).astype("int")
    