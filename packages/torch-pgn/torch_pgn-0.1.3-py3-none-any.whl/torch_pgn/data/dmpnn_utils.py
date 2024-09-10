"""
A lot of this code is repurposed from https://github.com/chemprop. This code is used in order to make the proximity
graph dataset compatible with using the D-MPNN with edge messages.
"""
import numpy as np
import torch
from tqdm import tqdm
import multiprocessing
from torch_geometric.data import DataLoader
import warnings


class ProxGraph():
    """
    A :class:`ProxGraph` represents the graph structure and featurization of a single molecule.
    A ProxGraph computes the following attributes:
    * :code:`n_atoms`: The number of atoms in the molecule.
    * :code:`n_bonds`: The number of bonds in the molecule.
    * :code:`f_atoms`: A mapping from an atom index to a list of atom features.
    * :code:`f_bonds`: A mapping from a bond index to a list of bond features.
    * :code:`a2b`: A mapping from an atom index to a list of incoming bond indices.
    * :code:`b2a`: A mapping from a bond index to the index of the atom the bond originates from.
    * :code:`b2revb`: A mapping from a bond index to the index of the reverse bond.
    """

    def __init__(self, mol, atom_descriptors: np.ndarray = None):
        """
        :param mol: A SMILES or an RDKit molecule.
        """
        # Convert SMILES to RDKit molecule if necessary
        x, edge_attr, edge_index = mol

        self.n_atoms = 0  # number of atoms
        self.n_bonds = 0  # number of bonds
        self.f_atoms = []  # mapping from atom index to atom features
        self.f_bonds = []  # mapping from bond index to concat(in_atom, bond) features
        self.a2b = []  # mapping from atom index to incoming bond indices
        self.b2a = []  # mapping from bond index to the index of the atom the bond is coming from
        self.b2revb = []  # mapping from bond index to the index of the reverse bond

        # Get atom features
        self.f_atoms = [list(x[i, :].reshape(x.shape[1])) for i in range(x.shape[0])]
        if atom_descriptors is not None:
            self.f_atoms = [f_atoms + descs.tolist() for f_atoms, descs in zip(self.f_atoms, atom_descriptors)]

        self.n_atoms = x.shape[0]

        # Initialize atom to bond mapping for each atom
        for _ in range(self.n_atoms):
            self.a2b.append([])

        # Get bond features
        for a1 in range(self.n_atoms):
            for a2 in range(a1 + 1, self.n_atoms):
                bond = _get_bond_attr(a1, a2, mol)

                if bond is None:
                    continue

                f_bond = bond
                self.f_bonds.append(self.f_atoms[a1] + f_bond)
                self.f_bonds.append(self.f_atoms[a2] + f_bond)

                # Update index mappings
                b1 = self.n_bonds
                b2 = b1 + 1
                self.a2b[a2].append(b1)  # b1 = a1 --> a2
                self.b2a.append(a1)
                self.a2b[a1].append(b2)  # b2 = a2 --> a1
                self.b2a.append(a2)
                self.b2revb.append(b2)
                self.b2revb.append(b1)
                self.n_bonds += 2

    def apply_dist_norm(self, dist_column, mean, std):
        for index in range(len(self.f_bonds)):
            self.f_bonds[index][dist_column] = (self.f_bonds[index][dist_column] - mean) / std

    def remove_dist_norm(self, dist_column, mean, std):
        for index in range(len(self.f_bonds)):
            self.f_bonds[index][dist_column] = (self.f_bonds[index][dist_column] * std) + mean


class BatchProxGraph():
    """
    A :class:`BatchMolGraph` represents the graph structure and featurization of a batch of molecules.
    A BatchMolGraph contains the attributes of a :class:`MolGraph` plus:
    * :code:`atom_fdim`: The dimensionality of the atom feature vector.
    * :code:`bond_fdim`: The dimensionality of the bond feature vector (technically the combined atom/bond features).
    * :code:`a_scope`: A list of tuples indicating the start and end atom indices for each molecule.
    * :code:`b_scope`: A list of tuples indicating the start and end bond indices for each molecule.
    * :code:`max_num_bonds`: The maximum number of bonds neighboring an atom in this batch.
    * :code:`b2b`: (Optional) A mapping from a bond index to incoming bond indices.
    * :code:`a2a`: (Optional): A mapping from an atom index to neighboring atom indices.
    """

    def __init__(self, mol_graphs, atom_fdim, bond_fdim):
        r"""
        :param mol_graphs: A list of :class:`MolGraph`\ s from which to construct the :class:`BatchMolGraph`.
        """
        self.atom_fdim = atom_fdim
        self.bond_fdim = bond_fdim

        # Start n_atoms and n_bonds at 1 b/c zero padding
        self.n_atoms = 1  # number of atoms (start at 1 b/c need index 0 as padding)
        self.n_bonds = 1  # number of bonds (start at 1 b/c need index 0 as padding)
        self.a_scope = []  # list of tuples indicating (start_atom_index, num_atoms) for each molecule
        self.b_scope = []  # list of tuples indicating (start_bond_index, num_bonds) for each molecule

        # All start with zero padding so that indexing with zero padding returns zeros
        f_atoms = [[0] * self.atom_fdim]  # atom features
        f_bonds = [[0] * self.bond_fdim]  # combined atom/bond features
        a2b = [[]]  # mapping from atom index to incoming bond indices
        b2a = [0]  # mapping from bond index to the index of the atom the bond is coming from
        b2revb = [0]  # mapping from bond index to the index of the reverse bond
        try:
            mol_graphs = [item for sublist in mol_graphs for item in sublist]
        except:
            pass
        for mol_graph in mol_graphs:
            f_atoms.extend(mol_graph.f_atoms)
            f_bonds.extend(mol_graph.f_bonds)

            for a in range(mol_graph.n_atoms):
                a2b.append([b + self.n_bonds for b in mol_graph.a2b[a]])

            for b in range(mol_graph.n_bonds):
                b2a.append(self.n_atoms + mol_graph.b2a[b])
                b2revb.append(self.n_bonds + mol_graph.b2revb[b])

            self.a_scope.append((self.n_atoms, mol_graph.n_atoms))
            self.b_scope.append((self.n_bonds, mol_graph.n_bonds))
            self.n_atoms += mol_graph.n_atoms
            self.n_bonds += mol_graph.n_bonds

        self.max_num_bonds = max(1, max(
            len(in_bonds) for in_bonds in a2b))  # max with 1 to fix a crash in rare case of all single-heavy-atom mols

        self.f_atoms = torch.FloatTensor(f_atoms)
        self.f_bonds = torch.FloatTensor(f_bonds)
        self.a2b = torch.LongTensor([a2b[a] + [0] * (self.max_num_bonds - len(a2b[a])) for a in range(self.n_atoms)])
        self.b2a = torch.LongTensor(b2a)
        self.b2revb = torch.LongTensor(b2revb)
        self.b2b = None  # try to avoid computing b2b b/c O(n_atoms^3)
        self.a2a = None  # only needed if using atom messages

    def get_components(self, atom_messages: bool = False):
        """
        Returns the components of the :class:`BatchMolGraph`.
        The returned components are, in order:
        * :code:`f_atoms`
        * :code:`f_bonds`
        * :code:`a2b`
        * :code:`b2a`
        * :code:`b2revb`
        * :code:`a_scope`
        * :code:`b_scope`
        :param atom_messages: Whether to use atom messages instead of bond messages. This changes the bond feature
                              vector to contain only bond features rather than both atom and bond features.
        :return: A tuple containing PyTorch tensors with the atom features, bond features, graph structure,
                 and scope of the atoms and bonds (i.e., the indices of the molecules they belong to).
        """
        if atom_messages:
            #TODO: check compatibility with atom messages
            f_bonds = self.f_bonds[:, :self.bond_fdim]
        else:
            f_bonds = self.f_bonds

        return self.f_atoms, f_bonds, self.a2b, self.b2a, self.b2revb, self.a_scope, self.b_scope

    def get_b2b(self):
        """
        Computes (if necessary) and returns a mapping from each bond index to all the incoming bond indices.
        :return: A PyTorch tensor containing the mapping from each bond index to all the incoming bond indices.
        """
        if self.b2b is None:
            b2b = self.a2b[self.b2a]  # num_bonds x max_num_bonds
            # b2b includes reverse edge for each bond so need to mask out
            revmask = (b2b != self.b2revb.unsqueeze(1).repeat(1, b2b.size(1))).long()  # num_bonds x max_num_bonds
            self.b2b = b2b * revmask

        return self.b2b

    def get_a2a(self):
        """
        Computes (if necessary) and returns a mapping from each atom index to all neighboring atom indices.
        :return: A PyTorch tensor containing the mapping from each bond index to all the incoming bond indices.
        """
        if self.a2a is None:
            # b = a1 --> a2
            # a2b maps a2 to all incoming bonds b
            # b2a maps each bond b to the atom it comes from a1
            # thus b2a[a2b] maps atom a2 to neighboring atoms a1
            self.a2a = self.b2a[self.a2b]  # num_atoms x max_num_bonds

        return self.a2a


def _get_bond_attr(a1, a2, mol):
    """
    Returns the bond properties between the two atoms of a given index. If there is no bond between
    a1 and a2, then returns None
    """
    x, edge_attr, edge_index = mol
    found = np.where(np.logical_and(edge_index[0, :] == a1, edge_index[1, :] == a2))[0]
    if len(found) == 0:
        return None
    else:
        return list(edge_attr[found, :].reshape(edge_attr.shape[1]))


def prox2graph(mols) -> BatchProxGraph:
    """
    Converts a directory of raw proximity graphs into BatchMolGraph.
    :param directory: directory containing a PG raw inputs
    :return: A :class:`BatchMolGraph` containing the combined molecular graph for the molecules.
    """
    return BatchProxGraph(mols)


class MolGraphTransform(object):
    def __call__(self, data, transforms=None):
        molgraphs = []
        x_ind, edge_ind = 0, 0
        input_tuples = []
        for molgraph in tqdm(data.molgraph):
            x_size, edge_size, _ = molgraph
            input_tuple = ((data.x.numpy()[x_ind: x_ind + x_size, :]),
                           data.edge_attr.numpy()[edge_ind: edge_ind + edge_size, :],
                           data.edge_index.numpy()[:, edge_ind: edge_ind + edge_size])
            input_tuples.append(input_tuple)
            x_ind += x_size
            edge_ind += edge_size


        # try:
        #     multiprocessing.set_start_method('forkserver')
        #     warnings.filterwarnings("ignore", category=DeprecationWarning)
        # except:
        #     pass
        # TODO: Fix hardcode here
        # with multiprocessing.Pool(processes=32) as p:
        #     molgraphs = list(tqdm(p.imap(_generate_molgraphs, input_tuples), total=len(input_tuples)))

        molgraphs = []
        for input_tuple in tqdm(input_tuples):
            molgraphs.append(_generate_molgraphs(input_tuple))

        data.molgraph = molgraphs

        return data

def _generate_molgraphs(input_tuple):
    return ProxGraph(input_tuple)