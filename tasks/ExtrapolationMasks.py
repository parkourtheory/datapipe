'''
Generate graph masks for extrapolation task. Here the traininig mask is the largest component, and validation and testing are nodes outside this main component.
This is supposed to simulate new node entering the graph that have no prerequisite moves.

Note:
1. Execute Name2Int, GenerateGraph and RelabelGraph tasks before executing this to get nodes relabeled as consecutive intgers. 
2. Whenever generating masks, must also generate labels which is canonical ordering for masks.
'''
import os
import json
import numpy as np
import pandas as pd
import networkx as nx

from utils import *

class ExtrapolationMasks(object):
	def __init__(self, config):
		self.cfg = config


	'''
	Masks for training on largest connected component and validation on all other components.

	inputs:
	G           (nx.Graph) Graph data with nodes relabeled as consecutive integers starting from zero
	train_split (float)    Training split percentage
	val_split   (float)    Validation split percentage
	test_split  (float)    Test split percentage

	outputs:
	train_mask  (ndarray) Binary mask containing 1 at positions corresponding to nodes to train on
	val_mask    (ndarray) Binary mask containing 1 at positions correpsonding to nodes to validate on
	test_mask   (ndarray) Binary mask containing 1 at positions correpsonding to nodes to test on
	'''
	def run(self):
		task_dir = os.path.join(self.cfg.output_tasks_dir, self.__class__.__name__)
		save_path = lambda path: os.path.join(task_dir, path)

		G, node_map = None, None
		with open(os.path.join(self.cfg.output_tasks_dir, 'GenerateGraph', self.cfg.graph), 'r') as file:
			G = nx.Graph(json.load(file))

		with open(os.path.join(self.cfg.output_tasks_dir, 'Name2Int', self.cfg.node_map), 'r') as file:
			node_map = {k: v for k, v in json.load(file).items()}

		'''
		nx.relabel is converting keys in adjacency list to string integer ids and edges to integer ids,
		so need the second nx.relabel_nodes to convert all nodes to interger ids. If don't do this, then
		there was be a doubling of nodes.
		'''
		G = nx.relabel_nodes(G, node_map)
		G = nx.relabel_nodes(G, {i: int(i) for i in G.nodes()})

		num_nodes = len(G.nodes())
		train_mask = np.zeros(num_nodes)
		test_mask = np.zeros(num_nodes)

		# create training mask from largest connected component
		for i in max(nx.connected_components(G), key=len):
			train_mask[int(i)] = 1

		val_mask = 1-train_mask

		orig = sum(val_mask)

		if self.cfg.test_split:
			val_idx = np.where(val_mask == 1)[0]
			test_idx = np.random.choice(val_idx, int(self.cfg.test_split*num_nodes))
			test_mask[test_idx] = 1
			val_mask[test_idx] = 0

		assert num_nodes == sum(map(sum, [train_mask, val_mask, test_mask]))

		train_mask = pd.Series(train_mask, dtype=bool)
		val_mask = pd.Series(val_mask, dtype=bool)
		test_mask = pd.Series(test_mask, dtype=bool)

		train_mask.to_csv(save_path(self.cfg.train_mask), sep='\t', index=False)
		val_mask.to_csv(save_path(self.cfg.val_mask), sep='\t', index=False)
		test_mask.to_csv(save_path(self.cfg.test_mask), sep='\t', index=False)