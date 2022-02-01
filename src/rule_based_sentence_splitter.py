# Written by Mansur Yeşilbursa
from rule_based_tokenizer import rule_based_tokenizer

def rule_based_sentence_splitter(text): #takes a list of tokens, splits it into sentences.
    # assumes that tokenization is correct
    text = rule_based_tokenizer(text)
    in_quote = 0 # false
    sentences = []
    pos = 0
    end_punc = '.!?'
    for i, j in zip(text, range(len(text))):
        if i != '':
            if ('\'' == i[-1] or '\"' == i[-1] or '\'' == i[0] or '\"' == i[0]) and not (text[j+1] == '\'' or text[j+1] == '\"') :
                # to not confuse with kesme isareti and also consecutive apostrophes should be taken as one
                in_quote = (in_quote + 1) % 2 # if in quatation ignore punctuations
            if j+1 != len(text):
                if i in end_punc and in_quote == 0 and text[j+1] not in end_punc: # not in quote and next token also not end_punc
                    # split the sentence
                    sentences.append(text[pos:j+1])
                    pos = j+1
            else:
                sentences.append(text[pos:])
    return sentences



if __name__ == '__main__': # adjust directory names later on
    no_space_punct = '\'\"' #before and after these no space
    after_space_punct = ',.?!'
    #space_punct = '.?!' # after these punct there is space
    with open('./42bin_haber/news/siyaset/15_tokenized.txt', 'r', encoding='utf8') as f:
        lines = (line.rstrip() for line in f)
        text = list(line for line in lines if line)
    splitted = rule_based_sentence_splitter(text)
    with open('./15_sentence_deneme.txt', 'w', encoding='utf8') as f:
        for i in splitted:
            line = ''
            for j, k in zip(i, range(len(i))):
                if line == '': # satır boşsa boşluk bırakmadan basla
                    line = j
                else:
                    line += j + ' '

            f.write('%s\n' % line)



