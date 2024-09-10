# Code adapted from chemprop to use our argument structure.
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.nn import ReLU, Dropout

import numpy as np

from torch_pgn.data.dmpnn_utils import BatchProxGraph
from torch_pgn.models.nn_utils import index_select_ND

#TODO: Add references to code source
class MPNEncoder(torch.nn.Module):
    """An :class:`MPNEncoder` is a message passing neural network for encoding a molecule."""

    def __init__(self, args, atom_fdim: int, bond_fdim: int):
        """
        :param args: A :class:`TrainArgs` object containing model arguments.
        :param atom_fdim: Atom feature vector dimension.
        :param bond_fdim: Bond feature vector dimension.
        """
        super(MPNEncoder, self).__init__()
        self.args = args
        self.atom_fdim = atom_fdim
        self.bond_fdim = bond_fdim + atom_fdim
        self.atom_messages = False
        self.hidden_size = args.hidden_dim
        self.bias = False
        self.depth = 3
        self.dropout = args.nn_conv_dropout_prob
        self.layers_per_message = 1
        self.undirected = args.mpnn_directed
        self.use_input_features = False
        self.device = args.device
        self.aggregation = args.nn_conv_aggr

        # Dropout
        self.dropout_layer = Dropout(p=self.dropout)

        # Activation
        self.act_func = ReLU()

        # Cached zeros
        self.cached_zero_vector = nn.Parameter(torch.zeros(self.hidden_size), requires_grad=False)

        # Input
        input_dim = self.atom_fdim if self.atom_messages else self.bond_fdim
        self.W_i = nn.Linear(input_dim, self.hidden_size, bias=self.bias)

        if self.atom_messages:
            w_h_input_size = self.hidden_size + self.bond_fdim
        else:
            w_h_input_size = self.hidden_size

        # Shared weight matrix across depths (default)
        self.W_h = nn.Linear(w_h_input_size, self.hidden_size, bias=self.bias)

        self.W_o = nn.Linear(self.atom_fdim + self.hidden_size, self.hidden_size)

    def forward(self,
                molgraph,
                features_batch=None):
        """
        Encodes a batch of molecular graphs.
        :param mol_graph: A :class:`~chemprop.features.featurization.BatchMolGraph` representing
                          a batch of molecular graphs.
        :param features_batch: A list of numpy arrays containing additional features.
        :param atom_descriptors_batch: A list of numpy arrays containing additional atomic descriptors
        :return: A PyTorch tensor of shape :code:`(num_molecules, hidden_size)` containing the encoding of each molecule.
        """
        if self.args.multi_gpu:
            self.device = molgraph.x.device
            molgraph = molgraph.molgraph
        mol_graph = BatchProxGraph(molgraph, self.atom_fdim, self.bond_fdim)
        f_atoms, f_bonds, a2b, b2a, b2revb, a_scope, b_scope = mol_graph.get_components(
            atom_messages=self.atom_messages)
        f_atoms, f_bonds, a2b, b2a, b2revb = f_atoms.to(self.device), f_bonds.to(self.device), a2b.to(
            self.device), b2a.to(self.device), b2revb.to(self.device)

        if self.atom_messages:
            a2a = mol_graph.get_a2a().to(self.device)

        # Input
        if self.atom_messages:
            input = self.W_i(f_atoms)  # num_atoms x hidden_size
        else:
            input = self.W_i(f_bonds)  # num_bonds x hidden_size
        message = self.act_func(input)  # num_bonds x hidden_size

        # Message passing
        for depth in range(self.depth - 1):
            if self.undirected:
                message = (message + message[b2revb]) / 2

            if self.atom_messages:
                nei_a_message = index_select_ND(message, a2a)  # num_atoms x max_num_bonds x hidden
                nei_f_bonds = index_select_ND(f_bonds, a2b)  # num_atoms x max_num_bonds x bond_fdim
                nei_message = torch.cat((nei_a_message, nei_f_bonds),
                                        dim=2)  # num_atoms x max_num_bonds x hidden + bond_fdim
                message = nei_message.sum(dim=1)  # num_atoms x hidden + bond_fdim
            else:
                # m(a1 -> a2) = [sum_{a0 \in nei(a1)} m(a0 -> a1)] - m(a2 -> a1)
                # message      a_message = sum(nei_a_message)      rev_message
                nei_a_message = index_select_ND(message, a2b)  # num_atoms x max_num_bonds x hidden
                a_message = nei_a_message.sum(dim=1)  # num_atoms x hidden
                rev_message = message[b2revb]  # num_bonds x hidden
                message = a_message[b2a] - rev_message  # num_bonds x hidden

            message = self.W_h(message)
            message = self.act_func(input + message)  # num_bonds x hidden_size
            message = self.dropout_layer(message)  # num_bonds x hidden

        a2x = a2a if self.atom_messages else a2b
        nei_a_message = index_select_ND(message, a2x)  # num_atoms x max_num_bonds x hidden
        a_message = nei_a_message.sum(dim=1)  # num_atoms x hidden
        a_input = torch.cat([f_atoms, a_message], dim=1)  # num_atoms x (atom_fdim + hidden)
        atom_hiddens = self.act_func(self.W_o(a_input))  # num_atoms x hidden
        atom_hiddens = self.dropout_layer(atom_hiddens)  # num_atoms x hidden

        # Readout
        mol_vecs = []
        for i, (a_start, a_size) in enumerate(a_scope):
            if a_size == 0:
                mol_vecs.append(self.cached_zero_vector)
            else:
                cur_hiddens = atom_hiddens.narrow(0, a_start, a_size)
                mol_vec = cur_hiddens  # (num_atoms, hidden_size)
                if self.aggregation == 'mean':
                    mol_vec = mol_vec.sum(dim=0) / a_size
                elif self.aggregation == 'sum':
                    mol_vec = mol_vec.sum(dim=0)
                elif self.aggregation == 'norm':
                    mol_vec = mol_vec.sum(dim=0) / self.aggregation_norm
                mol_vecs.append(mol_vec)

        mol_vecs = torch.stack(mol_vecs, dim=0)  # (num_molecules, hidden_size)

        return mol_vecs  # num_molecules x hidden