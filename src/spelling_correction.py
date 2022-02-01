# Written by Mansur Yeşilbursa for another project
import os
import string
import re
import time
import numpy as np
import math
import matplotlib.pyplot as plt
import sys


def get_corpus():  # Tokenizes corpus and returns it
    corpus_path = '../'
    transform = str.maketrans('', '', string.punctuation)
    with open(corpus_path + 'corpus.txt', 'r', ) as f:
        corpus = f.read().casefold().split()
    corpus = [i.translate(transform) for i in corpus] # removes ' and - as well which can exist in correct spelling

    return corpus


def get_spelling_errors():
    spell_path = '../'
    errors = []
    with open(spell_path + 'spell-errors.txt', 'r', ) as f:
        spell = re.split(r'[\n]', f.read())
    for i in range(len(spell)):
        temp = []
        errors.append([])
        temp.extend(re.split(r'[:/,]', spell[i]))
        errors[i].append(temp)
    return errors


def process_spelling_errors():  # duplicates multiple instances of error
    errors = get_spelling_errors()
    for i in errors:
        for j in i:
            for k in j:
                if '*' in k:
                    index = k.find('*')
                    num = int(k[index+1:])
                    j[j.index(k)] = k[:index]
                    for t in range(num-1):
                        j.append(k[:index])
    return errors


def corpus_probability():  # calculates probability of each word in the corpus and saves it
    corpus = get_corpus()
    words = []
    prob = []
    for i in corpus:
        if i not in words:
            words.append(i)
            prob.append((corpus.count(i))/len(corpus))
    with open('../corpus_word_list.txt', 'w') as f:
        for i in words:
            f.write('%s\n' % i)
    with open('../corpus_prob_list.txt', 'w') as f:
        for i in prob:
            f.write('%s\n' % i)
    return words, prob


def load_corpus_prob():  # since it takes long time to compute
    path = '../'
    if not os.path.exists(path + 'corpus_word_list.txt') or not os.path.exists(path + 'corpus_prob_list.txt'):
        words, prob = corpus_probability()
    else:
        with open(path + 'corpus_word_list.txt', 'r') as f:
            words = f.read().split()
        with open(path + 'corpus_prob_list.txt', 'r') as f:
            prob = f.read().split()
    prob = np.asarray(prob, dtype=float)
    return words, prob


def compute_posterior(possible, word):  # This method is used to implement an alternative method which is not a correct implementation of noisy channel model
    errors = process_spelling_errors()
    correct = []
    posterior = []
    word = ' ' + word
    for i in possible:
        for j in errors:
            for k in j:
                correct.append(k[0])
                if k[0] == i:
                    num = k.count(word)
                    prob = num/(len(k)-1)
                    posterior.append(prob)
                else:
                    posterior.append(0)
    return posterior, correct


def produce_correction(possible, word):  # This method is used to implement an alternative method which is not a correct implementation of noisy channel model
    posterior, correct = compute_posterior(possible, word)
    corpus_words, prob = load_corpus_prob()
    prior = []
    num = 0
    for i in range(len(posterior)):
        if posterior[i] != 0:
            num += 1
            true_spell = correct[i]
            if corpus_words.__contains__(true_spell):
                prior_index = corpus_words.index(true_spell)
                prior.append(prob[prior_index])
            else:
                prior.append(0)
        else:
            prior.append(0)
    prior = np.asarray(prior, dtype=float)
    posterior = np.asarray(posterior, dtype=float)
    total = np.multiply(prior, posterior)
    if np.max(total) == 0:
        corrected_spelling = ''
    else:
        true_index = np.argmax(total)
        corrected_spelling = correct[true_index]
    return corrected_spelling


def create_predictions(word):  # This function creates all 1 Damerau-Levenshtein edit distance words for the given word.
    possible = []
    possible = insertion(word, possible)
    possible = deletion(word, possible)
    possible = substitution(word, possible)
    possible = transpose(word, possible)
    return possible


def get_alphabet():  # returns alphabet
    list = [i for i in 'abcçdefgğhıijklmnoöprsştuüvyz']
    return list


def insertion(word, possible):  # (N+1)*alphabet insertion
    n = len(word)
    alph = get_alphabet()
    for i in range(n+1):
        for j in alph:
            temp = word[0:i] + j + word[i:]
            possible.append(temp)
    return possible


def deletion(word, possible):  # N deletion
    n = len(word)
    for i in range(n):
        temp = word[0:i] + word[i+1:]
        possible.append(temp)
    return possible


def substitution(word, possible):  # N*alphabet substitution
    n = len(word)
    alph = get_alphabet()
    for i in range(n):
        for j in alph:
            temp = word[0:i] + j + word[i+1:]
            possible.append(temp)
    return possible


def transpose(word, possible):  # N-1 transpose
    n = len(word)
    for i in range(n-1):
        p1 = word[i]
        p2 = word[i+1]
        temp = word[0:i] + p2 + p1 + word[i+2:]
        possible.append(temp)
    return possible


def confusion_insertion(correct, errors):
    alph = get_alphabet()
    c_insertion = np.zeros([28, 28])
    for i in range(len(correct)):
        true_temp = correct[i]
        for j in errors[i]:
            for k in range(len(j)):
                temp = j[0:k] + j[k+1:]
                if temp == true_temp:
                    if k+1 == len(j):
                        try:
                            fc = alph.index(j[k])
                            tc = alph.index(j[k - 1])
                            c_insertion[fc][tc] += 1
                        except ValueError:
                            break
                        break
                    else:
                        if j[k] != j[k+1]:
                            try:
                                fc = alph.index(j[k])
                                tc = alph.index(j[k - 1])
                                c_insertion[fc][tc] += 1
                            except ValueError:
                                break
                            break
    return c_insertion


def confusion_deletion(correct, errors):
    alph = get_alphabet()
    c_deletion = np.zeros([28, 28])
    for i in range(len(correct)):
        true_temp = correct[i]
        for j in errors[i]:
            for k in range(len(j)):
                for l in range(len(alph)):
                    temp = j[0:k+1] + alph[l] + j[k+1:]
                    if temp == true_temp:
                        try:
                            tc = alph.index(j[k])
                            fc = l
                            c_deletion[fc][tc] += 1
                        except ValueError:
                            break
                        break
    return c_deletion


def confusion_substitution(correct, errors):
    alph = get_alphabet()
    c_subs = np.zeros([28, 28])
    for i in range(len(correct)):
        true_temp = correct[i]
        for j in errors[i]:
            for k in range(len(j)):
                for l in range(len(alph)):
                    temp = j[0:k] + alph[l] + j[k+1:]
                    if true_temp == temp:
                        try:
                            tc = l
                            fc = alph.index(j[k])
                            c_subs[fc][tc] += 1
                        except ValueError:
                            break
                        break
    return c_subs


def confusion_transposition(correct, errors):
    alph = get_alphabet()
    t_subs = np.zeros([28, 28])
    for i in range(len(correct)):
        true_temp = correct[i]
        for j in errors[i]:
            for k in range(len(j)-1):
                p1 = j[k]
                p2 = j[k+1]
                temp = j[0:k] + p2 + p1 + j[k+2:]
                if true_temp == temp:
                    try:
                        tc = alph.index(p2)
                        fc = alph.index(p1)
                        t_subs[fc][tc] += 1
                    except ValueError:
                        break
                    break
    return t_subs


def get_correct_words(errors):
    correct = []
    for i in errors:
        for j in i:
            correct.append(j[0])
            j.remove(j[0])
    errors = remove_spaces(errors)
    return correct, errors


def remove_spaces(errors):
    e = []
    for i in range(len(errors)):
        e.append([])
        for j in (errors[i]):
            for k in j:
                e[i].append(k[1:].casefold())
    return e


def count_correct(correct):  # counts usage of single and double letters and saves it
    if os.path.exists('../characters.npy') and os.path.exists('../bigram.npy'):
        characters = np.load('../characters.npy')
        bigram = np.load('../bigram.npy')
    else:
        alph = get_alphabet()
        characters = np.zeros([28, 1])
        bigram = np.zeros([28, 28])
        for i in range(len(alph)):
            for j in correct:
                num1 = j.count(alph[i])
                characters[i] += num1
        for i in range(len(alph)):
            for j in range(len(alph)):
                for k in correct:
                    num2 = k.count(alph[i]+alph[j])
                    bigram[i][j] += num2
        np.save(file='../characters.npy', arr=characters)
        np.save(file='../bigram.npy', arr=bigram)
    return characters, bigram


def correction(word, correct, errors, smoothing=False):
    alph = get_alphabet()
    alph_size = len(alph)
    corpus_words, corpus_prob = load_corpus_prob()
    letters, d_letters = count_correct(correct)
    c_deletion = confusion_deletion(correct, errors)
    c_insertion = confusion_insertion(correct, errors)
    c_subs = confusion_substitution(correct, errors)
    c_trans = confusion_transposition(correct, errors)
    if smoothing:
        c_deletion += 1
        c_insertion += 1
        c_subs += 1
        c_trans += 1
        letters += alph_size
        d_letters += alph_size
    corrected_words = []
    for k in word:
        possible = create_predictions(k)
        max_len = max(len(i) for i in possible)
        correct_prob = np.zeros([4, max_len])
        for i in range(len(possible)):
            for j in range(len(possible[i])):
                possible_word = possible[i][j]

                if possible_word in corpus_words and possible_word in correct:  # possible_word in corpus_words and correct vocabulary:
                    apriori_prob = corpus_prob[corpus_words.index(possible_word)]
                    if i == 0:  # insertion corrected the error
                        word_index = j//alph_size
                        prev_letter = alph.index(k[word_index-1])  # position of the addition
                        inserted_letter = j - word_index*alph_size  # index of the inserted letter in the alphabet
                        no_confusion = c_deletion[inserted_letter, prev_letter]
                        posterior_prob = no_confusion/d_letters[prev_letter, inserted_letter]
                        prob = apriori_prob*posterior_prob
                        correct_prob[i, j] = prob
                    elif i == 1:  # deletion corrected the error
                        try:
                            prev_letter = alph.index(k[j-1])  # position of the deletion
                            inserted_letter = alph.index(possible_word[j])  # following letter
                            no_confusion = c_insertion[prev_letter, inserted_letter]
                            posterior_prob = no_confusion / letters[alph.index(possible_word[j-1])]
                            prob = apriori_prob*posterior_prob
                        except IndexError:
                            prob = 0
                        correct_prob[i, j] = prob
                    elif i == 2:  # substitution corrected the error
                        word_index = j // alph_size
                        prev_letter = alph.index(k[word_index])
                        subs_letter = j - word_index*alph_size
                        no_confusion = c_subs[prev_letter, subs_letter]
                        posterior_prob = no_confusion / letters[subs_letter]
                        if not math.isinf(posterior_prob):
                            prob = apriori_prob*posterior_prob
                        else:
                            prob = 0
                        correct_prob[i, j] = prob

                    else:  # transposition corrected the error
                        current_letter = alph.index(possible_word[j])
                        next_letter = alph.index(possible_word[j + 1])
                        no_confusion = c_trans[next_letter, current_letter]
                        posterior_prob = no_confusion/d_letters[current_letter, next_letter]
                        prob = apriori_prob * posterior_prob
                        correct_prob[i, j] = prob
                else:
                    correct_prob[i, j] = 0

        col = np.argmax(np.max(correct_prob, axis=0))
        row = np.argmax(np.max(correct_prob, axis=1))
        if correct_prob[row, col] == 0:
            corrected_word = ''
        else:
            corrected_word = possible[row][col]
        corrected_words.append(corrected_word)
    return corrected_words, c_deletion, c_insertion, c_subs, c_trans


if __name__ == '__main__':
    start = time.time()
    if len(sys.argv) > 2:
        input_name = sys.argv[1]
        correct_name = sys.argv[2]
    else:
        input_name = "test-words-misspelled.txt"
        correct_name = "test-words-correct.txt"
    errors = process_spelling_errors()
    correct, errors = get_correct_words(errors)
    smoothing = [False, True]
    save_imgs = False
    for k in smoothing:
        txt = "without_smoothing" if not k else "with_smoothing"
        corrected = []
        with open('../' + input_name, 'r') as f:
            word = f.read().split()
        corrected, c_deletion, c_insertion, c_subs, c_trans = correction(word, correct, errors, smoothing=k)
        with open('../' + txt + '_output.txt', 'w') as f:
            for j in corrected:
                f.write('%s\n' % j)
        with open('../' + correct_name, 'r') as f:
            true_correction = f.read().split()
        if save_imgs:
            plt.imshow(c_deletion)
            plt.savefig('deletion' + txt + '.png')
            plt.imshow(c_insertion)
            plt.savefig('insertion' + txt + '.png')
            plt.imshow(c_subs)
            plt.savefig('subs' + txt + '.png')
            plt.imshow(c_trans)
            plt.savefig('trans' + txt + '.png')
        common = 0
        if len(true_correction) == len(corrected):
            for i in range(len(true_correction)):
                if true_correction[i] == corrected[i]:
                    common += 1
        success_percentage = (common/len(corrected))*100
        print("Accuracy " + txt + " : %" + str(success_percentage))
    print("%s minutes" % ((time.time() - start)/60))
