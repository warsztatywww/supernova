# Instrukcja obsługi indeksu

	from index import func
	
	szukaj_slowa("szukane_slowo")
	Zwraca:
	* False - nie ma słowa w indeksie
	* [(pk1, ilosc_wystąpień1), (pk2, ilosc_wystąpień2)] - lista krotek (pk_obiektu_strony, ilość_wystąpień), 
		jeśli znaleziono słowa
	
## Wymaga w websites.models:

	from django.db.models.signals import post_save
	from index import index_page
	
	post_save.connect(index_page.strona_do_zindeksowania, sender=Webpage, dispatch_uid="post_save_index")
	
## nltk wymaga instalacji Punkt Tokenizer Models
	
	http://www.nltk.org/data.html
	