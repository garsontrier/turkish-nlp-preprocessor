# Written by Mansur Yeşilbursa
import numpy as np
import conllu
import os
from spelling_correction import create_predictions
import re
import itertools
from rule_based_tokenizer import rule_based_tokenizer
import string


def generate_vocab():
    vocab = []
    with open('../datasets/UD_Turkish-BOUN/' + 'tr_boun-ud-train.conllu', 'r', encoding='utf8') as f:
        for tokenlist in conllu.parse_incr(f):
            for i in tokenlist:
                if i['upos'] != 'AUX' and i['upos'] != 'PUNCT':
                    word = i['form'].casefold()
                    lemma = i['lemma']
                    if word not in vocab:
                        vocab.append(word)
                    if lemma not in vocab and lemma != '_':
                        vocab.append(lemma)
    vocab_dir = '../vocabulary/'
    name = 'normalization_vocab.txt'
    with open(vocab_dir + name, 'w', encoding='utf8') as f:
        for i in vocab:
            f.write('%s\n' % i)


def load_vocab():
    if not (os.path.exists('../vocabulary/normalization_vocab.txt')):
        generate_vocab()
    vocab = []
    with open('../vocabulary/normalization_vocab.txt', 'r', encoding='utf8') as f:
        for i in f.readlines():
            vocab.append(i.rstrip('\n'))
    return vocab

def load_corpus():
    corpus = open('../datasets/UD_Turkish-BOUN/' + 'tr_boun-ud-train.txt', 'r', encoding='utf8').read().replace('\n', ' ')
    return corpus


def generate_word_probabilities(vocab):
    corpus = load_corpus().split()
    size = len(corpus)
    probs = np.zeros([len(vocab)])
    for i in range(len(vocab)):
        count = corpus.count(vocab[i])
        probs[i] = np.log((count+1)/size)
    np.save('../vocabulary/word_probs.npy', probs)


def load_word_probabilites(vocab):
    if not (os.path.exists('../vocabulary/word_probs.npy')):
        generate_word_probabilities(vocab)
    word_prob = np.load('../vocabulary/word_probs.npy')
    return word_prob


def generate_all_possible_words(vocab):
    '''   This is not an optimal implementation,
    However, there is not any publicly available labeled data for Turkish text normalization.
    Therefore, for every word in vocabulary, we generate words with spelling errors that are
    1 edit distance away from the original word. This data is used as look up table.
    '''
    all_poss = []
    for i in vocab:
        pos = create_predictions(i)
        all_poss.append(pos)
    with open('../vocabulary/all_possible_words.txt', 'w', encoding='utf8') as f:
        for i in all_poss:
            for j in i:
                f.write('%s ' % j)
            f.write('\n')


def load_all_possible_words(vocab):
    all_pos = []
    if not (os.path.exists('../vocabulary/all_possible_words.txt')):
        generate_all_possible_words(vocab)
    with open('../vocabulary/all_possible_words.txt', 'r', encoding='utf8') as f:
        for i in f.readlines():
            all_pos.append(i.split())
    return all_pos



def search_error(word, vocab, word_prob):
    if word in vocab:
        return word
    else:
        indices = []
        pos = create_predictions(word) # for each word in vocab check if it is in the predictions
        for w, i in zip(vocab, range(len(vocab))):
            if w in pos:
                indices.append(i)
        if len(indices) == 0:  # no candidate in the data
            print('No candidate for word ' + word)
            return word
        else: # candidates found
            word_probs = np.argsort(word_prob[indices])
            max_prob_word = vocab[indices[word_probs[-1]]]
            return max_prob_word


def normalize(text):
    '''

    Args:
        text: Input string to be normalized

    Returns: List of normalized tokens

    '''
    punc = string.punctuation
    vocab = load_vocab()
    word_prob = load_word_probabilites(vocab)
    #all_pos = load_all_possible_words(vocab)
    tokens = rule_based_tokenizer(text)
    normalized_tokens = []
    for token in tokens:
        if token not in punc:
            normalized_tokens.append(normalize_token(token, vocab, word_prob))
        else:
            normalized_tokens.append(token)
    return normalized_tokens


def normalize_token(token, vocab, word_prob):
    '''

    Args:
        token: input token to be normalized

    Returns: Normalized token

    '''
    # accent normalization pairs
    pattern_subs = {'ıcam$':'acağım', 'cam$':'acağım', 'icem$':'eceğim', 'cem$':'eceğim', 'om$':'orum', 'ucaz$':'acağız',
                    'icez$':'eceğiz', 'am$':'ayım', 'em$':'eyim', 'mişin$':'mişsin', 'muşun$':'muşsun', 'oz$':'oruz'}
    # ascii pairs
    ascii_pairs = {'i':'ı', 'u':'ü', 'o':'ö', 'g':'ğ', 'c':'ç', 's': 'ş'}

    # normalization

    temp_word = letter_case_transformation(token)
    temp_word = accent_normalization(temp_word, pattern_subs)
    if len(set(temp_word).intersection(set(ascii_pairs.keys()))) > 0:
        temp_word = deascification(temp_word, vocab, ascii_pairs)
    temp_word = search_error(temp_word, vocab, word_prob)

    return temp_word


def letter_case_transformation(word): # performs letter case transformation
    if '\'' not in word:  # might be a proper noun, or sentence beginning
        if not word.islower() and not word.isupper():  # mixed case
            if word[0].isupper() and word[1:].islower():  # first char is upper left is lower assume proper noun or sentence beginning
                return word
        return word.lower() # erroneous mixed case, lowercase the word
    else:
        size = len(word)
        pos = word.find('\'')
        if pos > 0 and pos < size - 1:  # if apostrophe is in the middle assume proper noun
            word = word.capitalize()
        else:
            word = word.lower()
    return word


def accent_normalization(word, patterns):  # normalizes accented writing using set of predefined dictionary
    temp = word
    for key, value in patterns.items(): # find accented writing and substitute with true form
        temp = re.sub(key, value, temp)
        if temp != word:
            break
    return temp


def deascification(word, vocab, ascii_pairs): # generates all possible combinations non-ascii characters until find a match in the vocab
    keys = list(ascii_pairs.keys())
    subset_keys = generate_subsets(keys)
    temp_word = word
    changed = False
    for i in subset_keys:
        for j in i:
            for k in j:
                word = re.sub(k, ascii_pairs[k], word)
            if word in vocab: # if de-asciified word is in the vocab, return it
                changed = True
                break
        if changed:
            break
    if changed:
        return word
    else: # if no combination in the vocab, return original word
        return temp_word




def generate_subsets(values): # creates all subsets of elements in a given list
    subsets = []
    for i in range(len(values)):
        subsets.append(list(itertools.combinations(values, i+1)))
    return subsets




if __name__ == '__main__':
    # data_dir = '../../../UD_Turkish-BOUN/'
    # labelled_data = 'tr_boun-ud-train.conllu'
    # corpus_name = 'tr_boun-ud-train.txt'
    # vocab = load_vocab(data_dir, labelled_data)
    # corpus = open(data_dir + corpus_name, 'r', encoding='utf8').read().replace('\n', ' ')
    # word_prob = load_word_probabilites(corpus, vocab)
    # all_pos = load_all_possible_words(vocab)
    text = 'kac yil oldu sn gelmez oldn'
    new_text = normalize(text)
    print('Orijinal cümle: ' + text)
    print('Normalize edilmiş cümle: ' + new_text)

