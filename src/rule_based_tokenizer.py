# Written by Güray Baydur
import re
import os


def identify_unambiguous_punctuations(document):
    unambiguous_punctuations = ['?', ';', '(', ')', '!', ':', '[', ']', '{', '}', '"']
    unambiguous_punctuations_locations = []

    for charIndex in range(0, len(document)):
        is_found = 0
        for punctuation in unambiguous_punctuations:
            if document[charIndex] == punctuation:
                is_found = 1
                break
        if is_found:
            # print("Punctuation " + punctuation + " detected ")
            unambiguous_punctuations_locations.append((charIndex, charIndex))
    return unambiguous_punctuations_locations


def identify_proper_commas_and_dots(document):
    proper_commas_and_dots_locations = []
    for char_index in range(0, len(document)):
        if document[char_index] == ',' or document[char_index] == '.':
            if char_index - 1 >= 0 and char_index + 1 < len(document):
                is_between_numbers = (document[char_index - 1].isnumeric() and document[char_index + 1].isnumeric())
                if not is_between_numbers:
                    # print("Punctuation " + document[char_index] + " detected at index " + str(char_index) + " and it is not between numbers")
                    proper_commas_and_dots_locations.append((char_index, char_index))
    return proper_commas_and_dots_locations


def identify_urls(document):
    regex = r"(http:\/\/www\.|https:\/\/www\.|http:\/\/|https:\/\/|HTTP:\/\/WWW\.|HTTPS:\/\/WWW\.|HTTP:\/\/|HTTPS:\/\/)?[A-Za-z0-9]+([\-\.]{1}[A-Za-z0-9]+)*\.[A-Za-z]{2,5}(:[0-9]{1,5})?(\/.[^\s]*)?"
    urls = [(m.start(0), m.end(0)) for m in re.finditer(regex, document)]
    return urls


def identify_emails(document):
    regex = r'[\w\.-]+@[\w\.-]+'
    emails = [(m.start(0), m.end(0)) for m in re.finditer(regex, document)]
    return emails


def identify_hashtags(document):
    regex = r"\B#([^\s])*\b"
    hashtags = [(m.start(0), m.end(0)) for m in re.finditer(regex, document)]
    return hashtags


def identify_multi_word_expressions(document):
    input_file_name = "../vocabulary/verbal_mwe_lexicon.txt"
    all_mwe_locations = []

    with open(input_file_name, 'r', encoding='utf8') as f:
        mwes = f.read().splitlines()

    for mwe in mwes:
        mwe_locations = [(m.start(0), m.end(0)-1) for m in re.finditer(r'\b%s\b' % mwe, document)]
        for i in range(len(mwe_locations)):
            mwe_locations[i] += (-1,)


        all_mwe_locations.extend(mwe_locations)

    return all_mwe_locations


# print("String is: \n" + document)
def identify_single_quote_tokens(document):
    single_quote_locations = []
    for char_index in range(0, len(document)):
        # case for consecutive single quote detection e.g. ''Mavi Marmara''
        if document[char_index] == "'" and char_index + 1 < len(document) and document[char_index + 1] == "'":
            # print("here")
            # print(document[char_index:char_index+2])
            single_quote_locations.append((char_index, char_index + 2))
        elif document[char_index] == "'" and char_index - 1 >= 0 and document[char_index - 1] == "'":
            continue

        indexes = ()
        # case for catching beginning single quote: " 'hissedildi' "
        if (document[char_index] == "'" and char_index - 1 > 0 and document[char_index - 1] == " ") or (document[char_index] == "'" and char_index == 0):
            indexes = (char_index,)
            found = False
            while not found and char_index < len(document):
                char_index += 1
                if char_index < len(document) and document[char_index] == "'":
                    if char_index + 1 < len(document) and (
                            document[char_index + 1] == " " or document[char_index + 1] == ","):
                        indexes += (char_index + 1,)
                        found = True


        if char_index == len(document):
            break
        elif indexes != ():
            single_quote_locations.append(indexes)

    final_single_quote_locations = set()
    for elem in single_quote_locations:
        print(elem)
        final_single_quote_locations.add((elem[0], elem[0]))
        final_single_quote_locations.add((elem[1] - 1, elem[1] - 1))

    single_quote_locations = list(final_single_quote_locations)

    return single_quote_locations


def split_document(document, tuple_list):
    result = ""
    start = 0

    for tup, i in zip(tuple_list, range(len(tuple_list))):
        end = tup[0]
        result = result + document[start:end] + ' '
        start = tup[0]
        end = tup[1] + 1
        if tup[2] == -1:  #mwe
            temp = document[start:end].replace(' ', '|')
            result += temp + ' '
        else:
            result += document[start:end] + ' '
        start = tup[1] + 1

    result += document[start:]
    token_list = result.split()
    for i in range(len(token_list)):
        if '|' in token_list[i]:
            token_list[i] = token_list[i].replace('|', ' ')
    return token_list




def rule_based_tokenizer(document):
    all_locations = []

    hashtags_tuple = identify_hashtags(document)
    urls_tuple = identify_urls(document)
    emails_tuple = identify_emails(document)
    mwes_tuple = identify_multi_word_expressions(document)
    single_quotes_tuple = identify_single_quote_tokens(document)
    unambiguous_punctuations_tuple = identify_unambiguous_punctuations(document)
    proper_commas_and_dots_tuple = identify_proper_commas_and_dots(document)

    if hashtags_tuple:
        all_locations = all_locations + hashtags_tuple
    if urls_tuple:
        all_locations = all_locations + urls_tuple
    if emails_tuple:
        all_locations = all_locations + emails_tuple
    if mwes_tuple:
        all_locations = all_locations + mwes_tuple
    if single_quotes_tuple:
        all_locations = all_locations + single_quotes_tuple
    if unambiguous_punctuations_tuple:
        all_locations = all_locations + unambiguous_punctuations_tuple
    if proper_commas_and_dots_tuple:
        all_locations = all_locations + proper_commas_and_dots_tuple

    for i in range(len(all_locations)):
        if len(all_locations[i]) == 2:
            all_locations[i] += (1,)

    all_locations.sort()

    single_token_locations = []
    other_token_locations = []

    for tuple in all_locations:
        [start, end,_] = [*tuple]
        if end == start:
            single_token_locations.append(tuple)
        else:
            other_token_locations.append(tuple)

    single_token_locations_copy = single_token_locations.copy()
    other_token_locations_copy = other_token_locations.copy()

    for single_token in single_token_locations_copy:
        for other_token in other_token_locations_copy:
            if single_token[0] in range(*other_token):
                print(single_token)
                if single_token in single_token_locations:
                    single_token_locations.remove(single_token)
                else:
                    if other_token in other_token_locations:
                        other_token_locations.remove(other_token)

    all_locations = single_token_locations + other_token_locations
    all_locations.sort()
    return split_document(document, all_locations)


def write_tokens_to_file(output_file_name, tokenlist):
    f = open(output_file_name, "a", encoding='utf8')
    for mwe in tokenlist:
        f.write(mwe + "\n")
    f.close()


if __name__ == '__main__':

    folder_name = "../"

    for file in os.listdir(folder_name):
        print(file)
        if '.txt' in file:
            with open(folder_name + file, 'r', encoding='utf8') as f:
                document = f.read()
                tokenlist = rule_based_tokenizer(document)
                write_tokens_to_file(folder_name + file[0:len(file)-4] + "rule_based_tokenized.txt", tokenlist)
                print("\n")
