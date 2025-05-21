# 6Loda

This repository provides a demo for **6Loda**, a Target Generation Algorithm (TGA) designed to discover potential active IPv6 addresses based on known active seeds. The design and methodology of 6Loda are detailed in our INFOCOM 2025 paper
"**6Loda: Pattern Filtering and Ensemble Learning for IPv6 Target Generation and Scanning**".

> ⚠️ **Note**: This repository includes only the core components of the 6Loda pipeline.


## Project Structure
```
ipv6-6loda/
├── README.md
├── ipv6toolkit/        # IPv6 toolkit (install separately)
├── zmap/               # zmap-v6 scanner tool (install separately)
└── 6Loda/
    ├── dataset/        # Folder for datasets
    ├── result/         # Folder for saving hit IPv6 results
    ├── convert.py      # Convert IPs into numpy arrays
    ├── main.py         # Core implementation of 6Loda pipeline
    ├── main.sh         # Script entry point for running 6Loda
    ├── SpacePartition.py  # Covering-based DHC algorithm 
    └── tools.py        # Utility functions
```


## Prerequisites

### 1. Recommended Environment
    - python 3.8.0 or higher version
    - numpy 1.21.1 or higher version
    - pyod 2.0.1 or higher version
    - ipy 1.01 or higher version

You can install these dependencies using pip:
```bash
pip install numpy>=1.21.1 pyod>=2.0.1 ipy>=1.01
```
### 2. Install External Tools
- **ipv6toolkit**: Toolkit for IPv6 experimentation. The tool folder replaces the original "ipv6toolkit" folder. Github: [ipv6toolkit](https://github.com/fgont/)
- **zmap-v6**: Required for IPv6 scanning. The tool folder replaces the original "zmap" folder. Github: [zmap-v6](https://github.com/tumi8/zmap)

## How to run?
The core data processing logic of 6Loda—including filtering, classification, outlier removal, and prediction—is implemented in `main.py`. The script `main.sh` serves as the main entry point, wrapping the entire workflow. You can modify it according to your dataset and configuration needs.

To start the 6Loda process with a custom dataset and budget upper limit, run:
```bash
sh 6Loda/main.sh
```
We recommend the IPv6 Hitlist dataset from Gasser et al. as the seed source: [IPv6 Hitlist](https://ipv6hitlist.github.io/).

## Acknowledgements
We sincerely thank the [6Forest](https://github.com/Lab-ANT/6Forest) team for their contributions to IPv6 measurement and for open-sourcing parts of their project. Some of their code is referenced in 6Loda.

If you find our work useful in your research, please consider citing our paper:
```bibtex
@inproceedings{sun20256loda,
  title={6Loda: Pattern Filtering and Ensemble Learning for IPv6 Target Generation and Scanning},
  author={Sun, Xikai and Dang, Fan and Yang, Zihao and Jin, Xinqi and Li, Junhao and Liu, Yunhao},
  booktitle={IEEE INFOCOM 2025},
  year={2025}
}
```