### Bu kod bir reverse shell senaryosunu uygular.
####İki sınıf içerir:
MySocket sınıfı: Hedef makinede çalışan bir istemciyi temsil eder. Bir sunucuya bağlanır, sunucudan gelen komutları alır ve çalıştırır. Ayrıca, sunucuya dosya gönderme ve alma gibi işlemleri gerçekleştirebilir.
SocketListener sınıfı: Saldırganın makinesinde çalışan bir dinleyiciyi temsil eder. Hedef makinelerden gelen bağlantıları kabul eder, komutları alır ve bunları hedef makinelerde çalıştırır. Ayrıca, hedef makinelerden dosya indirme ve yükleme işlemlerini yönetir.

Bu iki sınıf arasındaki iletişim, JSON formatında veri alışverişi yaparak gerçekleştirilir. Dinleyici sınıfı, sunucu olarak çalışırken, istemci sınıfı hedef makinelerde çalışır. Bu sayede, saldırgan hedef makineler üzerinde komut çalıştırabilir ve dosya transferi yapabilir.
