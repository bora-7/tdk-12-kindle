ğıöşüç
![TDK-12 Logo](/static/TDK12.png)
[![en](https://img.shields.io/badge/lang-en-red.svg)](https://github.com/bora-7/tdk-12/blob/main/README.en.md) 
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
![Static Badge](https://img.shields.io/badge/total_definitions-99,182-brightgreen)

Bu projede Güncel Türkçe Sözlük'ün 12. baskısı bulunmaktadır. JSON dosyası halinde ve Kindle sözlüğü halinde bulunmaktadır.

Bu sözlük 99,182 madde içermektedir. Bu 11. baskıdan 6776 kelime daha fazladır. Bir çok maddenin tanımı güncellenmiştir.

Tüm tanımlari içeren JSON dosyasini `tdk-12` klasörünün içinde bulabilirsiniz. Bu dosya sıkıştırıldığı için 11.8 MB boyutundadır. Açıldıktan sonra 124.8 MB boyutuna sahip olacaktır.

## Kindle

Bu sözlügun Kindle versiyonunu `kindle` klasörünün içinde bulabilirsiniz.

Bu dosyayı açtıktan sonra bir `.mobi` dosyası çıkacaktır. Bu dosyayı kindle'a aktarmanız yeterlidir. Sözlük otomatik olarak aktif olacaktır.

Kindle versiyonunu yaparken Anezih tarafından yazılan [guncel-turkce-sozluk-kindle-kobo-stardict](https://github.com/anezih/guncel-turkce-sozluk-kindle-kobo-stardict) projedeki Python betiği kullanılmıştır.

Detaylı aşamalar için bu linke bakınız: https://tdk.boraakyuz.me/

## Kod

İlgilenenler için bu sözlüğü yapan kod, `src` dosyasının içinde bulunmaktadır.

Bu kod 3 Python script'ine bölünmüştür:

- `get_all_words.py`: Tüm kelimeleri `autocomplete.json` dosyasına kaydeder. Sözlük çok büyük olduğu için bu script sözlüğü 20 dosyaya böler. Bu, sonraki aşamaları kolaylaştırır. Aynı zamanda concurrency'i mümkün kılar.
- `make_dictionary.py`: Bir dosya numarası alır, ve o dosyadakı sözcüklerin tanımını başka bir dosyaya yazar. Tanımı bulunamayan sözcükler de başka bir dosyaya yazılır.
- `combine_results.py`: Tüm dosyalar doldurulduktan sonra, bu script tüm tanımları aynı dosyaya yazar. Ondan sonra tanımı bulunamayan sözcükleri yeniden dener, gerekirse tanımı tdk-11'den alır.

## Lisans
MIT