# Written by Mansur Yeşilbursa
import pickle
import numpy as np
from feature_extraction_tokenization import token_feature_extraction


def contains_punctuation(token):
    punc = '\',.\"?!-;:()'
    found = False
    for ch, j in zip(token, range(len(token))):  # iterate through string to detect punctuations
        punc_type = punc.find(ch)
        if punc_type != -1:  # punctuation is found
            found = True
            break
    return found


def ml_tokenizer(text):
    model_dir = '../models/tokenization/tokenization_model_liblinear.pkl'
    with open(model_dir, 'rb') as f:
        model = pickle.load(f)
    init_tokens = text.split()
    tokens = []
    for i in init_tokens:
        if contains_punctuation(i):
            x = np.asarray(token_feature_extraction(i))
            y = model.predict(np.reshape(x, (-1, x.shape[0])))
            if y == 1:  # split by the punctuation
                punc_pos = x[1]
                tokens.append(i[:punc_pos])
                tokens.append(i[punc_pos:])
            else:
                tokens.append(i)
        else:
            tokens.append(i)
    return tokens


if __name__ == '__main__':
    text = 'Tunceli Valiliği\'nden yapılan yazılı açıklamada, "Tunceli İl Jandarma Komutanlığı\'nca devam etmekte olan askeri çalışmalar nedeniyle aşağıda koordinatları belirlenen alanlara İl İdaresi Kanunu\'nun 11. maddesi gereğince, 6 Ekim 2012 günü saat 00.01\'den itibaren 45 gün süreyle yasaklama getirilmiş olup, belirlenen alanlara yaklaşılmaması kamuoyuna saygıyla duyurulur" denildi. Merkeze bağlı Çiçekli, Çılga ve Demirkapı köylerinin boş arazileri ile Zarkovit ve Çaldıran tepeleri arasında kalan bölgeyi de kapsayan bazı tepelik alanlara giriş yasağı konulduğunun belirtildiği açıklamada, bu alanların koordinatlarına da yer verildi.'
    tokens = ml_tokenizer(text)
    # error in 11. and "Tunceli 