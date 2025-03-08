import os

from helper.file import read_file, read_conf_file, read_tsv_file, read_binary_file, read_lst_file, remove_file, write_file, write_lst_file, append_lst_file
from helper.generateId import generateUniqueId
from helper.createQR import createQR
from helper.svg2pdf import svg2pdf
from helper.str2bool import str2bool

info = {
	"settings": {},
	"all_issued_certificates": [],
	"new_participants": [],
	"revoked_certificates": [],
}

settings = {
	"svg_path": "",
	"base_url": "",
	"file_extension": "",
	"id_length": "",
	"text_to_path": ""
}

message = {
	"content": "",
	"temp_path": "",
	"x_coord": "",
	"y_coord": "",
	"row_height": "",
	"row_max_length": ""
}

svg_content = ""

# MESAJIN SATIRLARINI DÖNDÜR
def get_row_message(text, row_max_length):
	while text != "":
		text += " "
		# MAKS UZUNLUKTA SATIR AL
		row = text[:row_max_length+1]
		# SATIRIN İÇİNDE \n VARSA O KISMI DÖNDÜR
		index = row.find("\n")
		if index != -1:
			yield row[:index]
		else:
			index = row.rfind(" ")
			yield row[:index]
		text = text[index+1:]

# METİNİ SVG METNİNE DÖNÜŞTÜRÜR
def convert_formatted_svg_text(text):
	# BAŞLANGIÇ KONUMUNU BUL
	x_coord = float(message["x_coord"])
	y_coord = float(message["y_coord"])
	# SATIR GENİŞLİK VE YÜKSEKLİK BİLGİLERİ
	row_height = float(message["row_height"])
	row_max_length = int(message["row_max_length"])
	# YAZACAK MESAJI SATIRLARA AYIRARAK YAZ
	result = ""
	for row in get_row_message(text, row_max_length):
		result += f"<tspan x='{x_coord}' y='{y_coord}'>"
		result += f"{row}"
		result += f"</tspan>"
		y_coord += row_height
	return result

# MESAJ TEMPLATE'İNİN İÇERİĞİNİ (SABİTLERİ YERİNE KOYAR) HESAPLAR
def get_message_content():
	global svg_content
	# Mesaj Template'ini Oku
	message["content"] = read_file(f"assets/templates/message/{message['temp_path']}/message.txt")
	message_conf = read_conf_file(f"assets/templates/message/{message['temp_path']}/message.conf")
	# Mesaj Template'teki Constant'ları Düzelt
	for key, value in message_conf["Constant"].items():
		message["content"] = message["content"].replace("{{#"+key+"#}}", value)
		svg_content = svg_content.replace("{{#"+key+"#}}", value)

# MESAJ TEMPLATE'İNİ ALIR
def get_message():
	message["temp_path"] = info["settings"]["Message"]["certificate_message_template"]
	message["x_coord"] = info["settings"]["Message"]["certificate_message_x_coordinate"]
	message["y_coord"] = info["settings"]["Message"]["certificate_message_y_coordinate"]
	message["row_height"] = info["settings"]["Message"]["certificate_message_row_height"]
	message["row_max_length"] = info["settings"]["Message"]["certificate_message_row_max_length"]
	#
	get_message_content()

# AYARLAR DOSYASININ REFERE ETTİĞİ DOSYALARI OKU
def get_settings():
	global svg_content
	settings["svg_path"] = info["settings"]["General"]["certificate_template_svg"]
	settings["base_url"] = info["settings"]["General"]["certificate_verification_base_url"]
	settings["file_extension"] = ".pdf" if info["settings"]["General"]["certificate_verification_include_file_extension"] else ""
	settings["id_length"] = int(info["settings"]["General"]["certificate_id_length"])
	settings["text_to_path"] = str2bool(info["settings"]["General"]["text_to_path"])
	svg_content = read_binary_file(f"assets/templates/certificate/{settings['svg_path']}")

# GEREKLİ TÜM DOSYALARI OKUR
def get_info():
	# settings dosyasını oku
	info["settings"] = read_conf_file("settings/settings.conf")
	# output dosyalarını oku
	info["all_issued_certificates"] = list(read_lst_file("outputs/certificates/all_issued_certificates.lst"))
	# input dosyalarını oku
	info["new_participants"] = read_tsv_file("inputs/new_participants.tsv")
	info["revoked_certificates"] = read_lst_file("inputs/revoked_certificates.lst")
	# settings'i detaylı oku
	get_settings()
	# message'i detaylı oku
	get_message()

# SVG DOSYASI OLUŞTUR
def create_svg(certificate_id, participant):
	global svg_content
	new_svg_content = svg_content
	# SVG Dosyasındaki Özel Değişkenleri Düzelt
	new_svg_content = new_svg_content.replace("{{CERTIFICATE_ID}}", certificate_id)
	new_svg_content = new_svg_content.replace("{{QR_CODE}}", os.path.abspath(f"outputs/qrcodes/{certificate_id}.png"))
	# Kişiye Özel Değişkenleri Değiştir
	content = message["content"]
	for key, value in participant.items():
		new_svg_content = new_svg_content.replace("{{$"+key+"$}}", value)
		content = content.replace("{{$"+key+"$}}", value)
	# SVG'nin Son Hali
	new_svg_content = new_svg_content.replace("{{MESSAGE}}", convert_formatted_svg_text(content))
	# SVG Dosyasını Oluştur
	write_file(f"outputs/certificates/{certificate_id}.svg", new_svg_content)

# PARAMETRE OLARAK ALDIĞI KİŞİYE SERTİFİKA OLUŞTURUR
def generate_certificate(participant):
	# Sertifika Numarası Üret
	certificate_id = generateUniqueId(settings["id_length"], info["all_issued_certificates"])
	# QR Kod Oluştur
	createQR(
		qr_data=f"{settings['base_url']}/{certificate_id}{settings['file_extension']}",
		img_path=f"outputs/qrcodes/{certificate_id}.png"
	)
	# SVG Dosyası Oluştur
	create_svg(certificate_id, participant)
	# PDF Dosyası Oluştur
	svg2pdf(f"outputs/certificates/{certificate_id}.svg", f"outputs/certificates/{certificate_id}.pdf", settings["text_to_path"])
	# SVG Dosyasını Sil
	remove_file(f"outputs/certificates/{certificate_id}.svg")
	# latest'a ekle
	append_lst_file("outputs/certificates/latest_issued_certificates.lst", [certificate_id])
	# değişkene ekle
	info["all_issued_certificates"].append(certificate_id)
	# dosyaya ekle
	append_lst_file("outputs/certificates/all_issued_certificates.lst", [certificate_id])
	# mail göndermek için gerekli dosyaya ekle
	append_lst_file("outputs/mailsend.tsv", [f"{participant['EMAIL']}\t{participant['NAME']}\t{certificate_id}.pdf"])

# INPUT DOSYASINDAKİ TÜM KİŞİLERE BİRER SERTİFİKA OLUŞTURUR
def generate_certificates():
	# mail göndermek için gerekli dosyayı sıfırla
	write_file("outputs/mailsend.tsv", "EMAIL\tNAME\tATTACHMENTS\n")
	# latest dosyasını sıfırla
	write_lst_file("outputs/certificates/latest_issued_certificates.lst", [])
	# Sertifikaları Üret
	for participant in info["new_participants"]:
		generate_certificate(participant)

# PARAMETRE OLARAK ALDIĞI ID'LI SERTİFİKAYI İPTAL EDER
def revoked_certificate(certificate_id):
	# Listeden Kaldır
	if certificate_id in info["all_issued_certificates"]:
		info["all_issued_certificates"].remove(certificate_id)
	# QR Kod Dosyasını Sil
	remove_file(f"outputs/qrcodes/{certificate_id}.png")
	# PDF Dosyasını Sil
	remove_file(f"outputs/certificates/{certificate_id}.pdf")

# INPUT DOSYASINDAKİ TÜM SERTİFİKALARI İPTAL EDER
def revoked_certificates():
	# Sertifikaları İptal Et
	for revoked_certificate_id in info["revoked_certificates"]:
		revoked_certificate(revoked_certificate_id)
	# Değişkeni Güncelle
	info["revoked_certificates"] = []
	# Dosyayı Güncelle
	write_lst_file(f"inputs/revoked_certificates.lst", info["revoked_certificates"])
	# all_issued_certificates.lst dosyasını düzelt
	write_lst_file("outputs/certificates/all_issued_certificates.lst", info["all_issued_certificates"])

# INPUT DOSYASINDAKİ SİLİNMESİ GEREKEN SERTİFİKALARI SİLER
# INPUT DOSYASINDAKİ VERİLMESİ GEREKEN SERTİFİKALARI VERİR
def main():
	# Gerekli Yapılandırma/Ayar Dosyalarını Oku
	get_info()
	# revoke işlemlerini yap
	revoked_certificates()
	# generate işlemlerini yap
	generate_certificates()

# RUN
if __name__ == "__main__":
	main()
