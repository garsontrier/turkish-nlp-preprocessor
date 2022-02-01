# Written by Güray Baydur

import conllu

def search_mwe_tags(mwe_tags):
    data_dir = '../datasets/parseme_corpus_tr-master/'
    filename_begin = "train_00"
    filename_end = ".cupt"

    final_mwe_lexicon = set()

    for mwe_tag in mwe_tags:
        mwe_lexicon = set()
        for j in range(1, 5):
            print(filename_begin + str(j) + filename_end)
            with open(data_dir + filename_begin + str(j) + filename_end, 'r', encoding='utf8') as f:
                for tokenlist in conllu.parse_incr(f):
                    visited_ids = []
                    for i in range(0, len(tokenlist)):
                        # dict_keys(['id', 'form', 'lemma', 'upos', 'xpos', 'feats', 'head', 'deprel', 'deps', 'misc', 'parseme:mwe'])
                        parseme_column = tokenlist[i]['parseme:mwe']
                        token_id = tokenlist[i]['id']
                        if mwe_tag in parseme_column and token_id not in visited_ids:
                            visited_ids.append(token_id)
                            mwe = [tokenlist[i]['form']]
                            search_nums = [parseme_column.split(':')[0]]
                            while i + 1 != len(tokenlist) and search_nums[0] not in tokenlist[i + 1]['parseme:mwe']:
                                if str(int(search_nums[0]) + 1) in tokenlist[i + 1]['parseme:mwe']:
                                    mwe.append(tokenlist[i + 1]['form'])
                                    visited_ids.append(tokenlist[i + 1]['id'])
                                i += 1
                            if len(mwe) > 1:
                                mwe[1] += " " + tokenlist[i + 1]['form']
                            if i + 1 != len(tokenlist):
                                mwe[0] += " " + tokenlist[i + 1]['form']
                            mwe_lexicon.update(mwe)
        final_mwe_lexicon = final_mwe_lexicon.union(mwe_lexicon)
    return final_mwe_lexicon

def clean_mwe_lexicon(mwe_lexicon):
    mwe_lexicon_copy = mwe_lexicon.copy()
    for elem in mwe_lexicon_copy:
        if " " not in elem:
            mwe_lexicon.remove(elem)
        for suffix in [" lı", " li", " lu", " lü"]:
            if suffix in elem:
                # print("suffix: " + suffix + " removed from " + elem )
                mwe_lexicon.remove(elem)
    return mwe_lexicon

def write_mwe_lexicon_to_file(output_file_name,mwe_lexicon):
    f = open(output_file_name, "a")
    for mwe in mwe_lexicon:
        f.write(mwe + "\n")
    f.close()

if __name__ == '__main__':

    mwe_tags = ['LVC.full',':VID']
    mwe_lexicon = search_mwe_tags(mwe_tags)
    mwe_lexicon = clean_mwe_lexicon(mwe_lexicon)

    output_file_name = "../vocabulary/verbal_mwe_lexicon.txt"
    write_mwe_lexicon_to_file(output_file_name,mwe_lexicon)

