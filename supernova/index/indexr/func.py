import redis
from .config import *
from nltk import word_tokenize
from nltk.stem import snowball
from collections import Counter
from websites.models import *

r_server = redis.Redis(redis_server_ip)


def czy_odwiedzona_strona(adres_strony):
    u"""
    Sprawdza, czy dana strona została odwiedzona w ostatnim czasie
    :param adres_strony:
    :return: True (ta strona była już odwiedzona), False (strona nie odwiedzona lub dawno)
    """

    if r_server.exists(adres_strony):
        return True

    else:
        return False


def zglos_odwiedzona_strone(adres_strony):
    """
    Zapisuje informację o odwiedzeniu strony do indeksu
    :param adres_strony: adres odwiedzanej strony
    :return:
    """
    r_server.setex(adres_strony, "1", czas_do_ponownego_odwiedzenia_strony)


def strona_do_zindeksowania(webpage):
    """
    Przyjmuje obiekt Webpage i wyciąga z niego słowa do indeksu
    :param webpage:
    :return:
    """
    zawartosc = webpage.content
    lista_slow_strony = word_tokenize(zawartosc)
    stemmer = snowball.EnglishStemmer()
    lista_ujednoliconych_slow = [stemmer.stem(i) for i in lista_slow_strony]
    slownik_wystopien = Counter(lista_ujednoliconych_slow)
    for s in slownik_wystopien.keys():
        dodaj_lub_uaktualnij_slowo_w_bazie(s, webpage.pk)


def dodaj_lub_uaktualnij_slowo_w_bazie(slowo, web_pk):
    if r_server.exists(slowo):
        lista_wystapien = [str(r_server.get(slowo)).split(",")]
        if not lista_wystapien.__contains__(str(web_pk)):
            lista_wystapien.append(web_pk)
            r_server.set(slowo, ",".join(i for i in lista_wystapien))
    else:
        r_server.set(slowo, "%d," % (web_pk))


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
        lista_stron = [str(r_server.get(slowo)).split(",")]
        for pk in lista_stron:
            web = Webpage.objects.get(int(pk))
            lista_wystapien = [stemmer.stem(i) for i in word_tokenize(web.content)]
            slownik_wystapien = Counter(lista_wystapien)
            lista_krotek.append((slowo, slownik_wystapien[slowo]))
        return lista_krotek
