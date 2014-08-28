# Instrukcja obsługi indeksu

	from index import func
	
	szukaj_slowa("szukane_slowo")
	Zwraca:
	* False - nie ma słowa w indeksie
	* [(pk1, ilosc_wystąpień1), (pk2, ilosc_wystąpień2)] - lista krotek (pk_obiektu_strony, ilość_wystąpień), 
		jeśli znaleziono słowa
	
## nltk wymaga instalacji Punkt Tokenizer Models
	python -m nltk.downloader punkt
	
	OR GUI
	import nltk
	nltk.download()
	
	http://www.nltk.org/data.html
	