# Written by Mansur Yeşilbursa
import numpy as np
import pickle

def ml_sentence_splitter(text):
    '''

    Args:
        text: given a string
    Returns:
        sentences: list of sentences in the string
    '''
    model_dir = '../models/sentence_splitting/'
    with open(model_dir + 'model_liblinear.pkl', 'rb') as f:
        model = pickle.load(f)
    eos_markers = ':.!?'
    quote_count = 0
    beg_pos = 0
    end_pos = 0
    sentences = []
    for ch, i in zip(text, range(len(text))):
        quote_count += int(ch == '\"')
        if ch in eos_markers and i < len(text) - 1:
            x = [quote_count % 2, int(text[i+1] in eos_markers) - 0.5, int(text[i+1] == '\"') - 0.5,
                int(text[i+1].isdigit()) - 0.5]
            x = np.reshape(np.asarray(x).astype(np.float), (1, -1))
            y = model.predict(x)
            if y == 1: # end of sentence
                end_pos = i + 1
                sentences.append(text[beg_pos:end_pos])
                beg_pos = end_pos
        elif i == len(text) - 1:  # finish the sentence nevertheless
            sentences.append(text[beg_pos:])

    return sentences


if __name__ == '__main__':
    model_dir = '../models/sentence_splitting/'
    with open(model_dir + 'model_liblinear.pkl', 'rb') as f:
        model = pickle.load(f)

    with open('../../../42bin_haber/news/siyaset/1.txt', 'r', encoding='utf8') as f:
        text = f.read()
    sentences = ml_sentence_splitter(text, model)
    print(sentences[0])
    print(sentences[1])
