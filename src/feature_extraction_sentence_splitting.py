# Written by Mansur Yeşilbursa
import conllu
import os
import numpy as np

def sentence_feature_extraction(text):
    '''

    Args:
        text: input sentence, which features to be extracted

    Returns:
        x: features
        y: labels
    '''
    eos_markers = ':.!?'
    quote_count = 0

    x = []
    y = []
    for chr, i  in zip(text, range(len(text))):
        quote_count += int(chr == '\"')
        if chr in eos_markers:  # end of sentence marker is encountered
            if i == len(text) - 1:  # truly end of sentence
                label = 1
                x_c = [quote_count % 2, -0.5, -0.5, -0.5]
            else:  # not the end of sentence
                label = 0
                x_c = [quote_count % 2, int(text[i+1] in eos_markers) - 0.5, int(text[i+1] == '\"') - 0.5,
                     int(text[i+1].isdigit() or text[i-1].isdigit()) - 0.5]
                # booleans are mapped to -0.5 and 0.5
            x.append(x_c)
            y.append(label)
        elif i == len(text) - 1:  # when it is the eos but not with a eos marker
            label = 1
            x_c = [quote_count % 2, -0.5, -0.5, -0.5]
            x.append(x_c)
            y.append(label)

    return x, y



if __name__ == '__main__':
    data_dir = '../../../UD_Turkish-BOUN/'
    train_data = 'tr_boun-ud-train.conllu'
    test_data = 'tr_boun-ud-test.conllu'
    x = []
    y = []
    with open(data_dir + train_data, 'r', encoding='utf8') as f:
        for tokenlist in conllu.parse_incr(f):
            text = tokenlist.metadata['text'] # get the sentence
            x_s, y_s = sentence_feature_extraction(text)
            x.extend(x_s)
            y.extend(y_s)
    x = np.asarray(x).astype(np.float)
    y = np.asarray(y).astype(np.float)
    np.save('../features/sentence_train_features', x)
    np.save('../features/sentence_train_labels', y)
    print('Training features are saved')
    x = []
    y = []
    with open(data_dir + test_data, 'r', encoding='utf8') as f:
        for tokenlist in conllu.parse_incr(f):
            text = tokenlist.metadata['text'] # get the sentence
            x_s, y_s = sentence_feature_extraction(text)
            x.extend(x_s)
            y.extend(y_s)
    x = np.asarray(x).astype(np.float)
    y = np.asarray(y).astype(np.float)
    np.save('../features/sentence_test_features', x)
    np.save('../features/sentence_test_labels', y)
    print('Test features are saved')