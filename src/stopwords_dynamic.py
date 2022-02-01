# Written by Mansur Yeşilbursa
import math
import numpy as np
import conllu
import os
import nltk
from stemmer import stemmer



def generate_vocab():
    data_dir = '../datasets/UD_Turkish-BOUN/'
    labelled_data = 'tr_boun-ud-train.conllu'
    vocab = []
    with open(data_dir + labelled_data, 'r', encoding='utf8') as f:
        for tokenlist in conllu.parse_incr(f):
            for i in tokenlist:
                if i['upos'] != 'AUX' and i['upos'] != 'PUNCT':
                    word = i['lemma'].lower()
                    if word not in vocab:
                        vocab.append(word)
    vocab_dir = '../vocabulary/'
    name = 'stopword_vocab.txt'
    with open(vocab_dir + name, 'w', encoding='utf8') as f:
        for i in vocab:
            f.write('%s\n' % i)


def load_vocab():
    vocab = []
    if not (os.path.exists('../vocabulary/stopword_vocab.txt')):
        generate_vocab()

    with open('../vocabulary/stopword_vocab.txt', 'r', encoding='utf8') as f:
        for i in f.readlines():
            vocab.append(i.rstrip('\n'))
    return vocab

def load_corpus():
    data_dir = '../datasets/UD_Turkish-BOUN/'
    corpus_name = 'tr_boun-ud-train.txt'
    return open(data_dir + corpus_name, 'r', encoding='utf8').read().replace("\n", " ")

def generate_word_probabilities(corpus, vocab):
    if not os.path.exists('../vocabulary/tfs.npy'):
        corpus = corpus.split()
        size = len(vocab)
        tfs = np.zeros([size])
        for i in range(len(vocab)):
            count = corpus.count(vocab[i])
            tfs[i] = count
        np.save('../vocabulary/tfs.npy', tfs)


def load_word_probabilities():
    if not os.path.exists('../vocabulary/tfs.npy'):
        generate_word_probabilities(load_corpus(), load_vocab())
    else:
        return np.load('../vocabulary/tfs.npy')


def determine_stopwords(n, tfs, vocab):
    sorted_indices = tfs.argsort()
    stopwords = [vocab[i] for i in list(sorted_indices[-n:])]
    return stopwords


def evaluate(true_labels):
    f1_scores = []
    n = range(20, 50) # range of number of stopwords
    tfs = load_word_probabilities()
    vocab = load_vocab()
    for i in n:
        dy_stopwords = determine_stopwords(i, tfs, vocab)
        true_positives = 0
        for elem in dy_stopwords:
            if elem in true_labels:
                true_positives += 1

        precision = true_positives / len(dy_stopwords)
        recall = true_positives / len(true_labels)

        f1_score = (2 * precision * recall) / (precision + recall)
        f1_scores.append(f1_score)

    max_index = f1_scores.index(max(f1_scores)) + 20
    return determine_stopwords(max_index, tfs, vocab), max_index


def dynamic_stopword_eliminate(token_list):
    predefined_stopwords = ['acaba', 'ama', 'aslında', 'az', 'bazı', 'belki', 'biri', 'birkaç', 'birşey', 'biz', 'bu',
                                                    'çok', 'çünkü', 'da', 'daha', 'de', 'defa', 'diye', 'eğer', 'en', 'gibi', 'hem', 'hep',
                                                    'hepsi', 'her', 'hiç', 'için', 'ile', 'ise', 'kez', 'ki', 'kim', 'mı', 'mu', 'mü', 'nasıl',
                                                    'ne', 'neden', 'nerde', 'nerede', 'nereye', 'niçin', 'niye', 'o', 'sanki', 'şey', 'siz',
                                                    'şu', 'tüm', 've', 'veya', 'ya', 'yani']
    dy_stopwords = evaluate(predefined_stopwords)
    stemmed_tokens = []
    for token in token_list:
        stemmed_tokens.append(stemmer(token))
    new_list = []
    for token, i in zip(token_list, range(len(token_list))):
        if token not in dy_stopwords and stemmed_tokens[i] not in dy_stopwords:
            new_list.append(token)

    return token_list


if __name__ == '__main__':
    data_dir = '../../../datasets/ud-treebanks-v2.7/UD_Turkish-BOUN/'
    labelled_data = 'tr_boun-ud-train.conllu'
    corpus_name = 'tr_boun-ud-train.txt'

    print(dynamic_stopword_eliminate(['için', 'nereye', 'olsa', 'da']))

