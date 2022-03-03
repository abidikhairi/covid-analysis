import os
import json
import torch
import matplotlib.pyplot as plt
from tqdm import tqdm
from nltk.tokenize import TweetTokenizer

label2str = {2: "positive", 1: "neutral", 0: "negative"}

def prepare_sequence(sent, word2idx):

	tknzr = TweetTokenizer()
	tokens = tknzr.tokenize(sent.lower())
	
	seq = []

	for token in tokens:
		if token in word2idx:
			seq.append(word2idx[token])
	
	return torch.tensor(seq, dtype=torch.long)

def load_vocab():
	return json.load(open('./data/vocab.json', 'r')) 

def build_word2idx_dict(datasets):
	vocab_path = './data/vocab.json'

	if os.path.exists(vocab_path):
		print(f'loading vocab from {vocab_path}')
		word2idx = json.load(open(vocab_path, 'r'))
		return word2idx

	word2idx = {}
	tknzr = TweetTokenizer()
	
	for dataset in datasets:
		for row in tqdm(dataset, desc=f'build word2idx mapping: {len(datasets)} datasets'):
			tokens = tknzr.tokenize(row['text'].lower())
			for token in tokens:
				if token not in word2idx:
					word2idx[token] = len(word2idx)
	
	with open(vocab_path, 'w') as stream:
		json.dump(word2idx, stream)

	return word2idx

def load_model(path):
	from models import LSTMSentiment

	vocab_size = len(load_vocab())
	embedding_dim = 256
	hidden_dim = 64
	num_classes = len(label2str.keys())

	model = LSTMSentiment(vocab_size=vocab_size, embedding_dim=embedding_dim, hidden_dim=hidden_dim, num_classes=num_classes)

	model.load_state_dict(torch.load(path))

	return model

def save_figure(title: str, xs, ys, xlabel, ylabel, label):
	
	figname = title.lower().replace(' ', '-')
	figpath = f'./figures/{figname}.png'
	
	plt.figure(figsize=(16, 10))
	plt.plot(xs, ys, label=label)
	
	plt.xlabel(xlabel)
	plt.ylabel(ylabel)
	
	plt.legend()
	plt.grid(True)

	plt.savefig(figpath)
