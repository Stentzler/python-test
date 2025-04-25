FROM python:3.11-slim

WORKDIR /code

# Atualiza pacotes e instala dependências de sistema necessárias para Chrome
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget unzip curl gnupg \
    fonts-liberation libnss3 libxss1 libasound2 libatk-bridge2.0-0 libgtk-3-0 libgbm-dev libu2f-udev \
    && rm -rf /var/lib/apt/lists/*

# Instala o Google Chrome
RUN curl -sSL https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
 && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list \
 && apt-get update \
 && apt-get install -y --no-install-recommends google-chrome-stable \
 && rm -rf /var/lib/apt/lists/*

# Define a versão do chromedriver compatível, deixar em variável caso seja necessário alteração
ENV CHROME_VERSION=135.0.7049.114

# Instala o ChromeDriver
RUN wget -q "https://storage.googleapis.com/chrome-for-testing-public/${CHROME_VERSION}/linux64/chromedriver-linux64.zip" \
 && unzip chromedriver-linux64.zip \
 && mv chromedriver-linux64/chromedriver /usr/local/bin/chromedriver \
 && chmod +x /usr/local/bin/chromedriver \
 && rm -rf chromedriver-linux64.zip chromedriver-linux64


COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . /code/worker

CMD ["celery", "-A", "worker.run", "worker", "--loglevel=info", "--concurrency=1", "-Q", "scrape_cnpj_task"]







