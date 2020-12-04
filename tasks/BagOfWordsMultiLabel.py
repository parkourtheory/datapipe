'''
Bag of words
'''
import os
import json
import pandas as pd
from collections import defaultdict
from pprint import pprint

class BagOfWordsMultiLabel(object):
	def __init__(self, config):
		self.cfg = config


	def run(self):
		df = pd.read_csv(self.cfg.move_csv, sep='\t', header=0)
		features = defaultdict(list)

		# build bag-of-words map
		terms = set(term for move in df['name'] for term in move.split())
		term2index = {term: i for i, term in enumerate(list(terms))}

		# single label classification
		unique_labels = set(label for type_ in df['type'] for label in str(type_).split('/'))
		type2id = {str(m):i for i, m in enumerate(list(set(unique_labels)))}
		
		for i, sample in enumerate(zip(df['name'], df['type'])):
			move, type_ = sample
			bag = [0]*len(term2index)
			label = [0]*len(type2id)

			for term in move.split(): bag[term2index[term]] += 1
			for lab in str(type_).split('/'): label[type2id[lab]] = 1

			features[i] = (move, bag, label)

		with open(os.path.join(self.cfg.video_csv_out, 'bag-of-words-multi-binary-label.json'), 'w') as file:
			json.dump(features, file, ensure_ascii=False, indent=4)