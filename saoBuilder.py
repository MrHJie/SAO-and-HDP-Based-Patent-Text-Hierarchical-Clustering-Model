import nltk
from nltk import pos_tag
from nltk.tokenize import word_tokenize,sent_tokenize

def extract_SAO(sentence):
	words = word_tokenize(sentence)
	pos_tags = pos_tag(words)

	subject = None
	verb = None
	object_ = None

	for word, tag in pos_tags:
		if tag.startswith('NN'):  # 名词
			if not subject:
				subject = word
			else:
				object_ = word
		elif tag.startswith('VB'):  # 动词
			verb = word

	return subject, verb, object_


def process_sao(text):
	sentences = sent_tokenize(text)  # 使用nltk的sent_tokenize分句
	SAO_network = []
	for sentence in sentences:
		subject, verb, object_ = extract_SAO(sentence)
		if subject and verb and object_:
			SAO_network.append((subject, verb, object_))

	SAO_networks = []
	for triple in SAO_network:
		SAO_networks.append([triple[0],triple[1],triple[2]])
	return SAO_networks





