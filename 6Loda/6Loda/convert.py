# convert IPv6 str to numpy seeds.npy
# This section of code is adapted from the GitHub repository:
# https://github.com/Lab-ANT/6Forest
# Author: 6Forest Team (Yang, Tao and Cai, Zhiping and Hou, Bingnan and Zhou, Tongqing)
# Only used here for research purposes.

import numpy as np
from IPy import IP
import sys

filePath = '6forest/dataset/IPv6_Hitlist/IPv6_Hitlist_1e6.txt'
saveNpyPath = '6forest/dataset/IPv6_Hitlist/IPv6_Hitlist_1e6.npy'
num = 1e6 # number of IPs to convert

with open(filePath) as f:
    arrs = []
    for ip in f.read().splitlines()[:int(num)]:
        arrs.append([int(x, 16)
                    for x in IP(ip).strFullsize().replace(":", "")])
    np.save(saveNpyPath, np.array(arrs, dtype=np.uint8))


