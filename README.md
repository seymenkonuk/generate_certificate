# Generate Certificate
> Python dilinde, .PDF uzantılı sertifikalar üreten konsol uygulaması.

## Açıklama
Sunduğu özellikler:
- Özelleştirilebilir sertifika tasarımı
- Özelleştirilebilir sertifika metni
- QR kod ile sertifika doğrulama
- [Mail Sender](https://github.com/seymenkonuk/mail_sender) ile entegre olarak, sertifikaları ilgili kişilere hızlı bir şekilde mail olarak gönderebilme

![](assets/demo/running.gif)

## İçindekiler
<ol>
	<li>
		<a href="#başlangıç">Başlangıç</a>
		<ul>
			<li><a href="#bağımlılıklar">Bağımlılıklar</a></li>
			<li><a href="#kurulum">Kurulum</a></li>
			<li><a href="#yapılandırma">Yapılandırma</a></li>
			<li><a href="#çalıştırma">Çalıştırma</a></li>
		</ul>
	</li>
	<li><a href="#dizin-yapısı">Dizin Yapısı</a></li>
	<li><a href="#lisans">Lisans</a></li>
	<li><a href="#Iletişim">İletişim</a></li>
</ol>

## Başlangıç
### Bağımlılıklar
Proje aşağıdaki işletim sistemlerinde test edilmiştir:
- **Debian**

Projenin düzgün çalışabilmesi için aşağıdaki yazılımların sisteminizde kurulu olması gerekir:
- **Python Yorumlayıcısı 3.9**
- **pip**
- **inkscape**
- **Docker** (docker ortamında çalıştıracaksanız)

<p align="right">(<a href="#generate-certificate">back to top</a>)</p>

---

### Kurulum
1. Bu repository'yi kendi bilgisayarınıza klonlayın:
	```bash
	git clone https://github.com/seymenkonuk/generate_certificate.git
	```

2. Projeye gidin:
	```bash
	cd generate_certificate
	```

<p align="right">(<a href="#generate-certificate">back to top</a>)</p>

---

### Yapılandırma
1. Sertifika tasarımınızı yapınız ve .SVG uzantılı olarak dışa aktarınız.
2. Şablonunuzu `assets/templates/certificate` dizinine taşıyınız.
3. Sertifikanızda yazacak yazı için bir şablon oluşturmak için `assets/templates/message/` dizini altına **"<şablon_ismi>"** adında bir dizin oluşturun. 
4. Bu dizinin altına **message.conf** ve **message.txt** adında iki dosya oluşturun.
5. **message.txt** dosyasının içine mesaj olarak yazmasını istediğiniz metni yazınız.
	```
	Example Organizer tarafından 
	01.01.2025 tarihinde gerçekleştirilen
	Example Event etkinliğine katılımınızdan dolayı 
	bu belgeyi almaya hak kazandınız.
	```
6. **message.txt** dosyasında 3 farklı değişken ekleyebilirsiniz:
	- **Mesaj Sabitleri**: her etkinlikte değişen bilgiler için kullanabilirsiniz.
		```
		{{#EVENT_ORGANIZER#}} tarafından 
		{{#EVENT_DATE#}} tarihinde gerçekleştirilen
		{{#EVENT_NAME#}} etkinliğine katılımınızdan dolayı 
		bu belgeyi almaya hak kazandınız.
		```
	- **Kişi Değişkenleri**: kişiye göre değişen veriler için kullanabilirsiniz.
		```
		{{#EVENT_ORGANIZER#}} tarafından 
		{{#EVENT_DATE#}} tarihinde gerçekleştirilen
		{{#EVENT_NAME#}} etkinliğine katılımınızdan dolayı 
		bu belgeyi almaya hak kazandınız.

		Başarı Yüzdesi: {{$BASARI$}}/100
		```
	- **Özel Değişkenler**: hazır olarak 3 değişken sunulmaktadır.
		- `{{CERTIFICATE_ID}}`: rastgele üretilen benzersiz sertifika ID'si
		- `{{QR_CODE}}`: üretilen QR kodun path bilgisi
		- `{{MESSAGE}}`: **message.txt dosyasında bu değişken kullanılmamalıdır!**
7. Mesaj sabitlerini **message.conf** dosyasına tanımlayınız.
	```
	[Constant]
	EVENT_ORGANIZER=Example Community
	EVENT_NAME=Example Event
	EVENT_DATE=01.01.2025
	```
8. Kişi değişkenlerini **inputs/new_participants.tsv** dosyasına tanımlayınız.
	```
	NAME	EMAIL	BASARI
	Deneme1	Deneme1	90
	Deneme2	Deneme2	70
	```
9. Sertifikada da değişkenleri kullanabilirsiniz.
10. Sertifikada mesajın yazmasını istediğiniz yer için `{{MESSAGE}}` değişkenini kullanınız.
11.  `settings/settings.conf` dosyasına kullanacağınız sertifika ve mesaj şablonunu tanımlayınız.
		```
		[General]
		certificate_template_svg=basic.svg

		[Message]
		certificate_message_template=example1
		```
12. `settings/settings.conf` dosyasına `{{MESSAGE}}` ile ilgili ayarları ve doğrulama ile ilgili ayarları ekleyiniz.
	```
	[General]
	certificate_template_svg=basic.svg
	certificate_verification_base_url=https://recepseymenkonuk.com/sertifikalar
	certificate_verification_include_file_extension=true
	certificate_id_length=10
	text_to_path=true

	[Message]
	certificate_message_template=example1
	certificate_message_x_coordinate=144.28885
	certificate_message_y_coordinate=121.16418
	certificate_message_row_height=10
	certificate_message_row_max_length=70
	```

![](assets/demo/config.gif)

<p align="right">(<a href="#generate-certificate">back to top</a>)</p>

---

### Çalıştırma

Uygulama **Docker** üzerinden kolayca çalıştırılabilir.

- **Docker image almak için**:

	```bash
	make build
	```

- **Projeyi çalıştırmak için**:

	```bash
	make run
	```

<p align="right">(<a href="#generate-certificate">back to top</a>)</p>

---

## Dizin Yapısı
```
├── generate_certificate/
│   ├── assets/			
│   │   ├── demo/			#Proje sonuç video ve resimleri
│   │   ├── fonts/			#Sertifikada kullanılan fontların .TTF uzantılı dosyaları
│   │   └── templates/			#şablonlar
│   │       ├── certificate/		#.SVG uzantılı sertifika şablonu
│   │       └── message/		#sertifikanın üzerinde yazacak mesaj için şablon
│   ├── inputs/				#projenin girdi dosyaları
│   ├── outputs/			#projenin çıktı dosyaları
│   │       ├── certificates/		#üretilen sertifikaların yer aldığı dizin
│   │       └── qrcodes/		#üretilen qr kodların yer aldığı dizin
│   ├── settings/			#ayar dosyaları
│   └── src/				#projenin kaynak kodları
```

<p align="right">(<a href="#generate-certificate">back to top</a>)</p>

---

## Lisans
Bu proje [MIT Lisansı](https://github.com/seymenkonuk/generate_certificate/blob/main/LICENSE) ile lisanslanmıştır.

<p align="right">(<a href="#generate-certificate">back to top</a>)</p>

---

## Iletişim
Proje ile ilgili sorularınız veya önerileriniz için bana ulaşabilirsiniz:

GitHub: https://github.com/seymenkonuk

LinkedIn: https://www.linkedin.com/in/recep-seymen-konuk/

Proje Bağlantısı: [https://github.com/seymenkonuk/generate_certificate](https://github.com/seymenkonuk/generate_certificate)

<p align="right">(<a href="#generate-certificate">back to top</a>)</p>

---
