from collections import Counter

import redis
from nltk import word_tokenize
from nltk.stem import snowball
import string

from .config import *


r_server = redis.Redis(redis_server_ip)
stemmer = snowball.EnglishStemmer()
exclude = set(string.punctuation)


def page_to_index(sender, instance, **kwargs):
    """
    Przyjmuje obiekt Webpage i wyciąga z niego słowa do indeksu
    :param webpage:
    :return:
    """
    zawartosc = instance.content
    zawartosc = ''.join(ch for ch in zawartosc if ch not in exclude)
    lista_slow_strony = word_tokenize(zawartosc)
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