# Structural Entropy Community Detection

This repository contains the code for structural entropy community detection. The philosophy behind this method is to use the structural entropy of a network to detect communities. The structural entropy is a measure of the uncertainty of the network structure. The idea is that the higher the uncertainty, the more likely it is that the network is divided into communities.

## Installation

To install the package, run the following command:

```bash
pip install structural-entropy-community-detection
```

Or you can directly install the latest version from the GitHub repository:

```bash
pip install git+hhttps://github.com/c0mm4nd/structural-entropy-community-detection
```

## Usage

```python
from networkx import karate_club_graph
from se_community import community_detection

G = karate_club_graph()
communities = community_detection(G)

print(communities)
# {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 1, 9: 1, 10: 0, 11: 0, 12: 0, 13: 0, 14: 1, 15: 1, 16: 0, 17: 0, 18: 1, 19: 0, 20: 1, 21: 0, 22: 1, 23: 1, 24: 1, 25: 1, 26: 1, 27: 1, 28: 1, 29: 1, 30: 1, 31: 1, 32: 1, 33: 1}
```

## Contributing

The code is not perfect and there is always room for improvement. If you have any suggestions or ideas, feel free to open an issue or a pull request.
