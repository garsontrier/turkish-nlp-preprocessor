# Written by Mansur Yeşilbursa and Güray Baydur
import re
import os

import conllu


def check_suffixes(word, vocab, suffix_list):
    if word in vocab:
        return word

    for suffix in suffix_list:
        result = re.sub(suffix+"$", "", word)
        if word != result:
            return result
    return word


def greedy_stemming(word, vocab, suffix_list):
    temp_word = word
    invocab = word in vocab
    for i in range(len(word)):
        if word[i:] in suffix_list:
            temp_word = word[:i]
            break
    if invocab and temp_word in vocab:
        return temp_word
    elif invocab and temp_word not in vocab:
        return word
    else:
        return temp_word




def generate_vocab():
    vocab = []
    with open('../datasets/UD_Turkish-BOUN/' + 'tr_boun-ud-train.conllu', 'r', encoding='utf8') as f:
        for tokenlist in conllu.parse_incr(f):
            for i in tokenlist:
                if i['upos'] != 'AUX' and i['upos'] != 'PUNCT':
                    lemma = i['lemma']
                    if lemma not in vocab and lemma != '_':
                        vocab.append(lemma)
    vocab_dir = '../vocabulary/'
    name = 'lemma_vocab.txt'
    with open(vocab_dir + name, 'w', encoding='utf8') as f:
        for i in vocab:
            f.write('%s\n' % i)


def load_vocab():
    if not (os.path.exists('../vocabulary/lemma_vocab.txt')):
        generate_vocab()
    vocab = []
    with open('../vocabulary/lemma_vocab.txt', 'r', encoding='utf8') as f:
        for i in f.readlines():
            vocab.append(i.rstrip('\n'))
    return vocab


def stemmer(token, stemming_mode='greedy'):
    suffix_list = ['casına', 'çasına', 'cesine', 'çesine', 'sınız', 'siniz', 'sunuz', 'sünüz', 'acak', 'ecek',
            'muş', 'miş', 'müş', 'mış', 'ken', 'sın', 'sin', 'sun', 'sün', 'lar', 'ler', 'nız', 'niz', 'nuz', 'nüz',
            'tır', 'tir', 'tur', 'tür', 'dır', 'dir', 'dur', 'dür', 'ız', 'iz', 'uz', 'üz', 'ım', 'im', 'um', 'üm',
            'dı', 'di', 'du', 'dü', 'tı', 'ti', 'tu', 'tü', 'sa', 'se', 'm', 'n', 'k', 'ndan', 'ntan', 'nden', 'nten',
            'ları', 'leri', 'mız', 'miz', 'muz', 'müz', 'nız', 'niz', 'nuz', 'nüz', 'lar', 'ler', 'nta', 'nte','nda',
            'nde', 'dan', 'tan', 'den', 'ten', 'la', 'le', 'ın', 'in', 'un', 'ün', 'ca', 'ce', 'nı', 'ni', 'nu', 'nü',
            'na', 'ne', 'da', 'de', 'ta', 'te', 'ki', 'sı', 'si', 'su', 'sü', 'yı', 'yi', 'yu', 'yü', 'ya', 'ye',
                   'y','lı', 'li', 'lu', 'lü', 'lik', 'lık', 'luk', 'lük', 'sız', 'siz', 'suz', 'süz']

    vocab = load_vocab()
    temp_token = ''
    if stemming_mode == 'greedy':
        while temp_token != token:
            temp_token = token
            token = greedy_stemming(temp_token, vocab, suffix_list)
    elif stemming_mode == 'suffix_check':
        while temp_token != token:
            temp_token = token
            token = check_suffixes(temp_token, vocab, suffix_list)
    else:
        print('Unrecognized stemming mode')

    return token


if __name__ == '__main__':

    word = "medeniyetsizlik"
    stemmed_word = stemmer(word)
    print('Original Word: ' + word)
    print('Stemmed Word: ' + stemmed_word)