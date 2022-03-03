import pandas as pd
from nltk.tokenize import RegexpTokenizer
	
from utils import load_vocab, prepare_sequence, load_model


def process_text(df: pd.DataFrame):
	word2idx = load_vocab()
	model_path = './data/lstm-sentiment-54.15.pt'
	model = load_model(model_path)
	
	labels = []
	label_names = []
	
	for index, row in df.iterrows():
		seq = prepare_sequence(row['text'], word2idx)
		
		if len(seq) == 0:
			df.drop([index], axis=0, inplace=True)
			continue

		label, label_name = model.inference(seq)
		
		labels.append(label)
		label_names.append(label_name)

	df['label'] = labels
	df['sentiment'] = label_names

	return df

def wordcount(df):
	text = df['text']
	tknzr = RegexpTokenizer(r'\w+')
	words = {}

	for sent in text:
		for word in tknzr.tokenize(sent):
			if len(word) < 5:
				continue

			if word not in words:
				words[word] = 1
			else:
				words[word] += 1
	
	words = dict(sorted(words.items(), key=lambda item: item[1], reverse=True))
	
	words = pd.DataFrame({
		'word': words.keys(),
		'frequency': words.values() 
	})
	
	return words[:10]

def save_triplets(wordcount_df, output_file, predicate):
	words = list(wordcount_df['word'])
	
	with open(output_file, 'w') as stream:
		for src in words:
			for dst in words:
				stream.write(f'{src},{predicate},{dst}\n')


if __name__ == '__main__':
	filename = './data/tweets-2022-02-21-01:02.csv'
	
	df = pd.read_csv(filename, header=0)
	
	df = process_text(df)

	pos_df = df[df['sentiment'] == 'positive']
	neg_df = df[df['sentiment'] == 'negative']
	neut_df = df[df['sentiment'] == 'neutral']

	pos_wordcount_df = wordcount(pos_df)
	neg_wordcount_df = wordcount(neg_df)
	neut_wordcount_df = wordcount(neut_df)
	
	save_triplets(pos_wordcount_df, './data/positive_triplets.txt', 'positive')
	save_triplets(neg_wordcount_df, './data/negative_triplets.txt', 'negative')
	save_triplets(neut_wordcount_df, './data/neutral_triplets.txt', 'neutral')
