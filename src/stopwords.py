
def static_eliminate_stopwords(token_list):
    predefined_stopwords = ['acaba', 'ama', 'aslında', 'az', 'bazı', 'belki', 'biri', 'birkaç', 'birşey', 'biz', 'bu',
                                                    'çok', 'çünkü', 'da', 'daha', 'de', 'defa', 'diye', 'eğer', 'en', 'gibi', 'hem', 'hep',
                                                    'hepsi', 'her', 'hiç', 'için', 'ile', 'ise', 'kez', 'ki', 'kim', 'mı', 'mu', 'mü', 'nasıl',
                                                    'ne', 'neden', 'nerde', 'nerede', 'nereye', 'niçin', 'niye', 'o', 'sanki', 'şey', 'siz',
                                                    'şu', 'tüm', 've', 'veya', 'ya', 'yani']
    for token in token_list:
        if token in predefined_stopwords:
            token_list.remove(token)
    return token_list

