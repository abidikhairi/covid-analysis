import torch
import torch.nn.functional as F
from torch import nn
from utils import label2str


class LSTMSentiment(nn.Module):
	def __init__(self, vocab_size: int, embedding_dim: int, hidden_dim: int, num_classes: int, dropout_rate: float = 0.5):
		super().__init__()

		self.word_embedding = nn.Embedding(num_embeddings=vocab_size, embedding_dim=embedding_dim)

		self.lstm = nn.LSTM(input_size=embedding_dim, hidden_size=hidden_dim)

		self.seq2sent = nn.Linear(in_features=hidden_dim, out_features=num_classes)

		self.dropout = dropout_rate

	def forward(self, seq):
		embeddings = self.word_embedding(seq)

		lstm_in = embeddings.view(len(seq), 1, -1)
		lstm_out, _ = self.lstm(lstm_in)
		
		sentiment_space = self.seq2sent(F.dropout(lstm_out[-1], p=self.dropout))
		
		zh = F.relu(sentiment_space)

		scores = F.log_softmax(zh, dim=1)
		
		return scores

	def inference(self, seq):
		self.eval()

		yhat = self(seq)

		label = torch.argmax(yhat).item()
		label_name = label2str[label]

		return label, label_name
		