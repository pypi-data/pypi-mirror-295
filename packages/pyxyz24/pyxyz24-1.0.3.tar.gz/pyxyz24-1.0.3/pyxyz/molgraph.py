import networkx as nx
import numpy as np
from copy import deepcopy
from typing import Tuple, List

from .base_load import base


class Molecule:

    def __init__(self, start_obj: base.MolProxy) -> None:
        if not isinstance(start_obj, base.MolProxy):
            raise RuntimeError("Molecule should be initialized from MolProxy")

        self.G = nx.Graph(start_obj.molgraph)
        xyz = start_obj.xyz
        for i in self.G.nodes:
            self.G.nodes[i]['xyz'] = xyz[i, :]
        self.G = nx.convert_node_labels_to_integers(self.G)

    def set_orientation(self, U: np.ndarray, new_center: np.ndarray) -> None:
        n_atoms = self.G.number_of_nodes()
        my_center = np.zeros(3)
        for node in self.G.nodes:
            my_center += self.G.nodes[node]['xyz']
        my_center /= n_atoms
        for node in self.G.nodes:
            self.G.nodes[node]['xyz'] -= my_center
            self.G.nodes[node]['xyz'] = self.G.nodes[node]['xyz'] @ U
            self.G.nodes[node]['xyz'] += new_center

    def __add__(self, other: 'Molecule') -> 'Molecule':
        res = deepcopy(other)
        n_reserve = self.G.number_of_nodes()
        mapping = {node: n_reserve + node for node in res.G.nodes}
        res.G = nx.relabel_nodes(res.G, mapping)
        res.G = nx.compose(res.G, self.G)
        return res

    def save_sdf(self, fname: str) -> None:
        lines = ["", "", ""]
        lines.append("%3d%3d  0  0  0  0  0  0  0  0999 V2000" %
                     (self.G.number_of_nodes(), self.G.number_of_edges()))
        for i in range(self.G.number_of_nodes()):
            lines.append(
                "%10.4f%10.4f%10.4f%3s  0  0  0  0  0  0  0  0  0  0  0  0" %
                (self.G.nodes[i]['xyz'][0], self.G.nodes[i]['xyz'][1],
                 self.G.nodes[i]['xyz'][2], self.G.nodes[i]['symbol']))

        for edge in self.G.edges:
            lines.append("%3s%3s%3s  0" % (edge[0] + 1, edge[1] + 1, 1))
        lines.append("M  END\n")

        with open(fname, "w") as f:
            f.write("\n".join(lines))

    def as_xyz(self) -> Tuple[List[np.ndarray], List[str]]:
        xyzs = []
        syms = []
        for atom in range(self.G.number_of_nodes()):
            xyzs.append(self.G.nodes[atom]['xyz'])
            syms.append(self.G.nodes[atom]['symbol'])
        return xyzs, syms
