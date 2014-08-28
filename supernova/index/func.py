from collections import Counter

import redis
from nltk import word_tokenize
from nltk.stem import snowball

from .config import *
from websites.models import *


r_server = redis.Redis(redis_server_ip)


def szukaj_slowa(slowo):
    """
    Poszukuje słowa w bazie. Zwraca listę krotek (PrimaryKey webpage, ilość wystąpień) lub False, jeśli nie ma go w bazie
    :param slowo: szukane słowo
    :return:
    """
    stemmer = snowball.EnglishStemmer()
    slowo = stemmer.stem(slowo)
    if not r_server.exists(slowo):
        return False
    else:
        lista_krotek = []
        lista_stron = str(r_server.get(slowo).decode()).split(",")
        for krotka in lista_stron:
            if krotka != '':
                web = Webpage.objects.get(pk=krotka)
                lista_wystapien = [stemmer.stem(i) for i in word_tokenize(web.content)]
                slownik_wystapien = Counter(lista_wystapien)
                lista_krotek.append((int(krotka), slownik_wystapien[slowo]))
        return lista_krotek
