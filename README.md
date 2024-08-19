Taş Kağıt Makas Oyunu
Bu proje, bir el hareketi tanıma sistemi kullanarak Taş-Kağıt-Makas oyununu oynatır. Mediapipe ve OpenCV kütüphanelerini kullanarak gerçek zamanlı el hareketlerini algılar ve kullanıcıya karşı bilgisayar ile karşılaştırma yapar.

Özellikler
Gerçek Zamanlı El Hareketi Tanıma: Mediapipe kullanılarak el hareketleri tanımlanır.
Taş-Kağıt-Makas Oyunu: Kullanıcı ve bilgisayar arasında Taş-Kağıt-Makas oyunu oynanır.
Kullanıcı Arayüzü: OpenCV kullanılarak basit bir kullanıcı arayüzü oluşturulmuştur.
Skor Takibi: Oyuncu ve bilgisayarın skorları takip edilir.
Oyun Sonu ve Devam Etme: Oyun bittikten sonra kullanıcıya devam etmek isteyip istemediği sorulur.

Gereksinimler
Bu projeyi çalıştırmak için aşağıdaki kütüphanelerin yüklü olması gerekmektedir:

Python 3.x
OpenCV (opencv-python)
Mediapipe (mediapipe)

Gerekli kütüphaneleri yüklemek için:
pip install opencv-python mediapipe

Kullanım
Python dosyasını çalıştırarak oyunu başlatın:

python tas_kagit_makas.py
Kameranızın karşısında el hareketlerinizi yaparak oyunu oynayın.

Oyun sonunda, devam etmek isteyip istemediğiniz sorulacak. Evet veya Hayır butonlarına tıklayarak yanıt verin.
