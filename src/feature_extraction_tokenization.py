# Written by Mansur Yeşilbursa
import os

def file_feature_extraction(dir, filename):
    '''
    Navigates through tokenized words,
    reconstructs original form by following few rules
    Then, extracts features for that token and adds them to the corresponding list
    All features of the dataset is written in the same txt file.
    Args:
        dir: directory of the given file
        filename: name of the input file

    Returns:

    '''
    punc = '\',.\"?!-;:()'  # % left out for now
    quote_count = 0
    x = []  # features
    y = []  # labels
    tokens = []

    with open(dir+filename, 'r', encoding='utf8') as f:
        for line in f.readlines():  # each token is kept on a different line
            tokens.append(line.rstrip('\n'))
    for token, i in zip(tokens, range(len(tokens))):
        found = False
        if token in punc: # for only punctuation tokens
            if (token == '\'' or token == '\"') and quote_count % 2 == 0:
                quote_count += 1
                punc_type = punc.index(token)
                try:
                    original_form = token + tokens[i + 1] #add try statements
                    label = 1  # punctuation is another token
                    pos = 0
                    found = True
                except IndexError:
                    break
                # send for feature extraction
            elif (token == '\'' or token == '\"') and quote_count % 2 == 1:
                quote_count += 1
                punc_type = punc.index(token)
                original_form = tokens[i - 1] + token
                label = 1  # punctuation is another token
                pos = len(original_form) - 1
                found = True
                # send for feature extraction
            elif token == '.' or token == ',' or token == '?' or token == '!' or token == ';' or token == ':':
                punc_type = punc.index(token)
                original_form = tokens[i - 1] + token
                label = 1
                pos = len(original_form) - 1
                found = True
                #send for feature extraction
            elif token == '(':
                punc_type = punc.index(token)
                try:
                    original_form = token + tokens[i + 1]
                    label = 1
                    pos = 0
                    found = True
                except IndexError:
                    break
            elif token == ')':
                punc_type = punc.index(token)
                original_form = tokens[i - 1] + token
                label = 1
                pos = 0
                found = True

        else: # for not only punctuation tokens
            if token == '...':
                punc_type = punc.index(token[0])
                original_form = tokens[i - 1] + token
                label = 1
                pos = len(original_form) - 1
                found = True
            else:
                for ch, j in zip(token, range(len(token))): # iterate through string to detect punctuations
                    punc_type = punc.find(ch)
                    if punc_type != -1:  # punctuation is found
                        pos = j
                        original_form = token
                        label = 0
                        found = True
                        break
        if found:
            only_punc = True
            for j in original_form:
                if j not in punc:
                    case = int(j.isupper())
                    only_punc = False
                    break
            if not only_punc:
                x.append([punc_type, pos, len(original_form), case])
                y.append(label)
    return x, y


def token_feature_extraction(token):
    '''

    Args:
        token: token whose features are going to be extracted

    Returns:
        features for the token
    used during inference
    '''
    x = None
    punc = '\',.\"?!-;:()'  # % left out for now
    for ch, j in zip(token, range(len(token))):  # iterate through string to detect punctuations
        punc_type = punc.find(ch)
        if punc_type != -1:  # punctuation is found
            pos = j
            original_form = token
            break
    only_punc = True
    for j in original_form:
        if j not in punc:
            case = int(j.isupper())
            only_punc = False
            break
    if not only_punc:
        x = [punc_type, pos, len(original_form), case]
    return x


if __name__ == '__main__':
    x = []
    y = []
    dir = 'D:/Mansur/Boun/CMPE 561/assignments/assignment 1/42bin_haber/news/'
    categories = os.listdir(dir)
    for i in categories:
        category_dir = dir + i + '/'
        category_files = os.listdir(category_dir)
        for j in category_files:
            if '_tokenized' in j:  # take only tokenized files
                x_temp, y_temp = file_feature_extraction(category_dir, j)
                x.extend(x_temp)
                y.extend(y_temp)
    with open('../features/tokenization_features_and_labels.txt', 'r+', encoding='utf8') as f:
        for feature, i in zip(x, range(len(x))):
            for j in feature:
                f.write('%d\t' % j)
            f.write('%d\n' % y[i])

