## TDK-12
Bu projede Güncel Türkçe Sözlük'ün 12. baskisi bulunmaktadir. Bu proje @ogun'un [guncel-turkce-sozluk](https://github.com/ogun/guncel-turkce-sozluk) projesi tarafindan esinlenmistir. 

Bu sözlük 99,182 madde içermektedir. Bu 11. baskidan 6776 kelime daha fazladir. Bir çok maddenin tanimi guncellenmistir.

Tüm tanimlari içeren JSON dosyasini `tdk-12` klasörünün içinde bulabilirsiniz. Bu dosya sikistirildigi için 11.8 MB boyutundadir. Açildiktan sonra 124.8 MB boyutuna sahip olacaktir.

## Kindle
Bu sözlügun Kindle ve Kobo port'u hazirlanmaktadir. Bu bitince buraya linki konulacaktir.

## Kod
Ilgilenenler için bu sözlügü yapan kod, `src` dosyasinin içinde bulunmaktadir. 

Bu kod 3 Python script'ine bölünmüstür:
- `get_all_words.py`: Tüm kelimeleri `autocomplete.json` dosyasina kaydeder. Sözlük çok büyük oldugu için bu script sözlügü 20 dosyaya böler. Bu, sonraki asamalari kolaylastirir. Ayni zamanda concurrency'i mümkün kilar.
- `make_dictionary.py`: Bir dosya numarasi alir, ve o dosyadaki sözcüklerin tanimini baska bir dosyaya yazar. Tanimi bulunamayan sözcükler de baska bir dosyaya yazilir.
- `combine_results.py`: Tüm dosyalar doldurulduktan sonra, bu script tüm tanimlari ayni dosyaya yazar. Ondan sonra tanimi bulunamayan sözcükleri yeniden dener, gerekirse tanimi tdk-11'den alir.

