from collections import Counter

import redis
from nltk import word_tokenize
from nltk.stem import snowball

from .config import *


r_server = redis.Redis(redis_server_ip)


def strona_do_zindeksowania(sender, instance, **kwargs):
    """
    Przyjmuje obiekt Webpage i wyciąga z niego słowa do indeksu
    :param webpage:
    :return:
    """
    print("Szukam")
    zawartosc = instance.content
    lista_slow_strony = word_tokenize(zawartosc)
    stemmer = snowball.EnglishStemmer()
    lista_ujednoliconych_slow = [stemmer.stem(i) for i in lista_slow_strony]
    slownik_wystopien = Counter(lista_ujednoliconych_slow)
    for s in slownik_wystopien.keys():
        dodaj_lub_uaktualnij_slowo_w_bazie(s, instance.pk)


def dodaj_lub_uaktualnij_slowo_w_bazie(slowo, web_pk):
    if r_server.exists(slowo):
        lista_wystapien = str(r_server.get(slowo).decode()).split(",")
        if not lista_wystapien.__contains__(str(web_pk)):
            lista_wystapien.append(web_pk)
            r_server.set(slowo, ",".join(str(i) for i in lista_wystapien if i != ''))
    else:
        r_server.set(slowo, "%d," % (web_pk))