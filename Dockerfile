FROM python:3.12-slim-bookworm

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN playwright install --with-deps chromium-headless-shell

RUN apt-get update && apt-get install -y \
    wget \
    default-jre-headless

RUN wget https://github.com/allure-framework/allure2/releases/download/2.36.0/allure_2.36.0-1_all.deb
RUN dpkg -i allure_2.36.0-1_all.deb
RUN rm allure_2.36.0-1_all.deb

COPY . .

CMD ["python", "main.py"]
