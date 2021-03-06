'''
Visualize entire move graph and connected components
'''
import os

import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib import pylab
import numpy as np
from tqdm import tqdm

from utils import make_dir
from preproc import relational as rel

class VisualizeGraph(object):
	def __init__(self, config):
		self.cfg = config
		self.task_dir = os.path.join(self.cfg.output_tasks_dir, 'visualize_graph')


	def run(self):
		make_dir(self.task_dir)

		moves = pd.read_csv(self.cfg.move_csv, header=0, sep='\t')
		G = rel.dataframe_to_graph(moves)
		# self.plot(G, 'Parkour Theory')
		
		for i, c in enumerate(tqdm(nx.connected_components(G), total=nx.number_connected_components(G))):
			self.plot(G.subgraph(c), f'Component {i}')


	'''
	Does not display to avoid matplotlib throwing a Segmentation fault

	inputs:
	G     (nx.Graph) Networkx graph
	title (str)      Title of graph and filename to save
	'''
	def plot(self, G, title):
		degrees = dict(nx.degree(G))
		node_size = [v*100 for v in degrees.values()]

		# only label nodes with degree two standard deviations above average
		# to preserve readability
		num_nodes = len(degrees.values())
		st = np.std(np.array(list(degrees.values())))
		avg = sum(degrees.values())/num_nodes
		labels = {}
		if num_nodes > 100: 
			labels = {k:k for k, v in degrees.items() if v > avg + 4 * st}
		else:
			labels = {k:k for k, v in degrees.items()}

		plt.figure(num=None, figsize=(100, 100), dpi=100)
		plt.axis('off')
		fig = plt.figure(1)
		iterations = lambda nodes: int(200 * pow(1.0023, nodes-1100))
		pos = nx.spiral_layout(G, center=[0,0])
		pos = nx.spring_layout(G, k=0.2, iterations=iterations(num_nodes))

		# Adjust label margins to ensure labels are draw in figure
		x_values, y_values = zip(*pos.values())
		x_max = max(x_values)
		x_min = min(x_values)
		x_margin = (x_max - x_min) * 0.25
		plt.xlim(x_min - x_margin, x_max + x_margin)

		plt.figtext(.5, .9, title, fontsize=16, ha='center')

		nx.draw_networkx_nodes(G, pos, nodelist=degrees.keys(), node_size=node_size, alpha=0.25)
		nx.draw_networkx_edges(G, pos, alpha=0.1)
		nx.draw_networkx_labels(G, pos, labels, font_size=8)
		
		save_path = os.path.join(self.task_dir, f"{title.lower().replace(' ', '_')}.pdf")
		plt.savefig(save_path, bbox_inches="tight")
		pylab.close()
		del fig