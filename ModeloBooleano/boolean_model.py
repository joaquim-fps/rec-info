# -*- coding: utf-8 -*-

import string
import numpy as np

class BooleanModel(object):
	def tokenize(self, text):
		"""Separa `text` numa lista de tokens, utilizando como delimitadores ',', '.', '!', '?' e ' '."""
		return [tokens.strip().replace(',', ' ').replace('.', ' ').replace('!', ' ').replace('?', ' ').split() for tokens in text]

	def normalize(self, tokens, stopwords):
		"""Remove `stopwords` da lista `tokens`."""
		norm = []
		for phrase in tokens:
			norm.append([token.lower() for token in phrase if token.lower() not in stopwords])

		return np.unique(np.hstack(np.array(norm)))

	def create_index(self, tokens, docs):
		"""Cria matriz de incidência, a partir dos `docs` e `tokens` informados."""

		freq_matrix = {}
		for token in tokens:
			freq_matrix.update({token : np.char.count([doc.lower() for doc in docs], token)})

		return freq_matrix
				
	def query(self, q, matrix, stopwords, tokens, docs):
		"""Realiza consulta `q`, utilizando o modelo booleano para retornar os `docs` relevantes."""

		q = self.normalize(self.tokenize(q), stopwords)
		or_result = set()
		and_result = set()

		doc_index = {}
		for option in q:
			doc_index.update({option : matrix.get(option, np.array([0*len(docs)])).nonzero()})
			
			#operação OR
			for index in doc_index[option]:
				for i in range(len(index)):
					or_result.add(docs[index[i]])

		and_index = doc_index[q[0]][0] if len(q) > 0 else ''
		for i in range(len(q)-1):
			and_index = self.__intersect(and_index, doc_index[q[i+1]][0])

		for index in and_index:
			for i in range(len(index)):
				and_result.add(docs[index[i]])

		return (and_result, or_result)

	def __intersect(self, q1, q2):
		"""Faz a intersecção de dois índices de documentos, `q1` e `q2` (operação AND)"""
		answer = []
		i = 0
		j = 0

		while len(q1) > i and len(q2) > j:
			if q1[i] == q2[j]:
				answer.append(q1[i])
				i += 1
				j += 1
			elif q1[i] < q2[j]:
				i += 1
			else:
				j += 1

		return answer

if __name__ == '__main__':
	bm = BooleanModel()
	text = ['O peã e o caval são pec de xadrez. O caval é o melhor do jog.', 'A jog envolv a torr, o peã e o rei.', 'O peã lac o boi', 'Caval de rodei!', 'Polic o jog no xadrez.']
	stopwords = ['a', 'o', 'e', 'é', 'de', 'do', 'no', 'são']
	q = ['xadrez peã caval torr']

	tokens = bm.normalize(bm.tokenize(text), stopwords)
	fm = bm.create_index(tokens, text)
	result = bm.query(q, fm, stopwords, tokens, text)
	print(result)
