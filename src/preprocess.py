# Written by Mansur Yeşilbursa
import os

if __name__ == '__main__':
    data_dir = 'D:/Mansur/Boun/CMPE 561/assignments/assignment 1/42bin_haber/news/'
    categories = os.listdir(data_dir)
    for i in categories:
        cat_dir = data_dir + i + '/'
        for j in os.listdir(cat_dir):
            with open(cat_dir + j, 'r+', encoding='utf8') as f:
                text = ''
                #lineNo = 0
                for line in f:
                    for j in range(len(line) - 1):
                        try:
                            if line[j] == '\'' and line[j+1] == '\'':
                                temp = list(line)
                                temp[j] = '\"'
                                temp[j+1] = ''
                                line = ''.join(temp)
                        except IndexError:
                            break
                    no_break = (line.rstrip('\n')).lstrip() + ' '
                    text += no_break
                f.seek(0)
                f.truncate()
                f.flush()
                f.write(text)

            # with open(cat_dir + j[:-4] + '_tokenized.txt', 'w', encoding='utf8') as f:
            #     for i in tokens:
            #         f.write('%s\n' % i)