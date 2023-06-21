# Base image olarak Python kullanın
FROM python:3.9

# Çalışma dizinini /app olarak ayarlayın
WORKDIR /app

# Gerekli dosyaları kopyalayın
COPY requirements.txt .

# Bağımlılıkları yükleyin
RUN pip install -r requirements.txt

# Diğer dosyaları kopyalayın
COPY . .

# Flask uygulamasını çalıştırın
CMD [ "python", "brandefense.py" ]

# Diğer dosyaları kopyalayın
COPY brandefense.py .

