# Python 3.9 tabanlı bir imaj kullan
FROM python:3.9-slim

# Gerekli sistem bağımlılıklarını yükle (Inkscape için gerekli)
RUN apt-get update && \
	apt-get install -y inkscape libgtk-3-0 \
	&& rm -rf /var/lib/apt/lists/*

# Çalışma dizinini ayarla
WORKDIR /app

# FONTLARI EKLE
# Font dosyasını konteynıra kopyalayın
COPY ./assets/fonts /usr/share/fonts/truetype/my_fonts/
# Font cache'ini güncelleyin
RUN fc-cache -f -v

# Python bağımlılıklarını kopyala ve yükle
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Çalıştırma
ENTRYPOINT ["python"]
CMD ["src/main.py"]
