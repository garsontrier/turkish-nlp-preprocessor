# Written by Mansur Yeşilbursa
from rule_based_tokenizer import rule_based_tokenizer
from rule_based_sentence_splitter import rule_based_sentence_splitter
from ml_tokenizer import ml_tokenizer
from ml_sentence_splitter import ml_sentence_splitter
from normalization import normalize
from stemmer import stemmer
from stopwords import static_eliminate_stopwords
from stopwords_dynamic import dynamic_stopword_eliminate
import time


def print_operation_list():
    print('Possible processing options:')
    print('1) Tokenization')
    print('2) Sentence Segmentation')
    print('3) Normalization')
    print('4) Stemming')
    print('5) Stopword Elimination')
    print('Type \'text\' if you want to enter a new text')
    print('Type \'exit\' if you want to terminate the program')
    print('Enter the operation number (1-5) or a command to continue')


def read_input():
    '''

    Args:

    Returns:  -2 if text command is given
              -1 if input is not appropriate
              0 if exit command is given

    '''
    user_input = input('Command: ')
    print()
    if user_input == 'exit' or user_input == 'Exit':
        return 0
    elif user_input == 'text':
        return -2
    else:
        try:
            choice = int(user_input)
        except ValueError:
            return -1
    return choice


if __name__ == '__main__':
    print('Welcome to Basic Text Preprocessing Tool')
    print('This program was implemented by Mansur Yeşilbursa and Güray Baydur as a course assignment in CMPE 561')
    time.sleep(2)
    user_input = ''
    text = input('Enter the text you want to process\n')

    while True:
        processed_text = []
        print_operation_list()
        user_input = read_input()
        if user_input == -1:
            print('Invalid input')
            continue
        elif user_input == 0:
            break
        elif user_input == -2:
            text = input('Enter the text you want to process\n')
        else:

            if user_input == 1:  # Tokenization
                print('There are two types of tokenization:')
                print('1) Rule-based Tokenization')
                print('2) Logistic Regression Based Tokenization')
                print('Which type of tokenization do you want to use? (1 or 2)')
                user_input = read_input()
                if user_input == -1:
                    print('Invalid input')
                    continue
                elif user_input == 0:
                    break
                else:
                    if user_input == 1:  # rule based tokenization
                        processed_text = rule_based_tokenizer(text)
                    elif user_input == 2:
                        processed_text = ml_tokenizer(text)
                    else:
                        print('Invalid input')
                        continue
            elif user_input == 2:  # sentence splitting
                print('There are two types of sentence segmentation:')
                print('1) Rule-based Sentence Segmentation')
                print('2) Logistic Regression Based Sentence Segmentation')
                print('Which type of segmentation do you want to use? (1 or 2)')
                user_input = read_input()
                if user_input == -1:
                    print('Invalid input')
                    continue
                elif user_input == 0:
                    break
                else:
                    if user_input == 1:
                        processed_text = rule_based_sentence_splitter(text)
                    elif user_input == 2:
                        processed_text = ml_sentence_splitter(text)
                    else:
                        print('Invalid Choice')
                        continue

            elif user_input == 3:  # normalization
                processed_text = normalize(text)
            elif user_input == 4: # stemmer
                print('There are two types of stemming:')
                print('1) Greedy Stemming')
                print('2) Suffix list Stemming')
                print('Which type of stemming do you want to use? (1 or 2)')
                user_input = read_input()
                if user_input == -1:
                    print('Invalid input')
                    continue
                elif user_input == 0:
                    break
                else:
                    if user_input == 1:
                        token_list = rule_based_tokenizer(text)
                        for token in token_list:
                            processed_text.append(stemmer(token, stemming_mode='greedy'))
                    elif user_input == 2:
                        token_list = rule_based_tokenizer(text)
                        for token in token_list:
                            processed_text.append(stemmer(token, stemming_mode='suffix_check'))
                    else:
                        print('Invalid Choice')
                        continue
            elif user_input == 5:  # stopword elimination
                print('There are two types of stopword removal technique:')
                print('1) Static')
                print('2) Dynamic')
                print('Which type of elimination do you want to use? (1 or 2)')
                user_input = read_input()
                if user_input == -1:
                    print('Invalid input')
                    continue
                elif user_input == 0:
                    break
                else:
                    token_list = rule_based_tokenizer(text)
                    if user_input == 1:
                        for token in token_list:
                            processed_text = static_eliminate_stopwords(token_list)
                    elif user_input == 2:
                        for token in token_list:
                            processed_text = dynamic_stopword_eliminate(token_list)
                    else:
                        print('Invalid Choice')
                        continue

        print(processed_text)
        print('-------------- ** ----------------')
    print('Program finished')