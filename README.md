# 🚀 Ubuntu Server Airflow & Postgres 🐘

![Airflow](https://img.shields.io/badge/Apache%20Airflow-017CEE?style=for-the-badge&logo=Apache%20Airflow&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-336791?style=for-the-badge&logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)

---

## 📋Ubuntu Server Airflow

## Крок 1: Підготовка «заліза» (Віртуальна машина в Oracle VirtualBox)
Airflow — хлопець ненажерливий. Щоб він не «гальмував», потрібно виділіти йому такі ресурси в налаштуваннях VirtualBox:

ОС: Завантажте [Ubuntu Server 22.04 LTS](https://ubuntu.com/download/server) вона легша за Desktop версію.

Процесор: Мінімум 2 ядра (краще 4).

Пам'ять (RAM): Мінімум 4 ГБ (для комфортної роботи краще 8ГБ).

Мережа: У налаштуваннях обрати "Мережевий міст" (Bridged Adapter) - так віртуалка отримає власну IP-адресу у вашій домашній мережі, і ви зможете заходити в Airflow через браузер основного ПК.

---

Перевірити IP-адресу: 
```
hostname -I ip a
```


## PuTTy не пускає
Перевірте, чи встановлено SSH-сервер
```
sudo apt update
sudo apt install openssh-server -y
```
Перевірте статус служби
```
sudo systemctl status ssh
```
Дозвольте доступ через Firewall
```
sudo ufw allow ssh
sudo ufw enable
```

## 🛠 Крок 2: Встановлення Docker та Docker Compose
В Ubuntu 24.04 Docker ставиться дуже швидко. Виконайте ці команди по черзі:

Оновіть списки пакетів:
```
sudo apt update
```
Встановіть Docker та плагін Compose:
```
sudo apt install docker.io docker-compose-v2 –y
```
Додайте свого користувача до групи Docker (щоб не писати sudo перед кожною командою):
```
sudo usermod -aG docker $USER
```
Активуйте зміни груп (щоб не перезавантажуватися):
```
newgrp docker
```
Перевірка:
```
docker --version
docker ps
systemctl status docker
```
Якщо не вибило помилку "Permission denied" - ви все зробили правильно.

## 🔄 Крок 3: Розгортання Airflow (Production-лайт версія)
Тепер створимо структуру для вашої майбутньої ETL-системи.

Створіть папку для проекту:
```
mkdir ~/airflow-production && cd ~/airflow-production
```
Створіть необхідні підпапки:
```
mkdir -p ./dags ./logs ./plugins ./config
```
Завантажте офіційний конфіг Airflow:
```
curl -LfO 'https://airflow.apache.org/docs/apache-airflow/stable/docker-compose.yaml'
```
Налаштуйте ідентифікатор користувача, щоб Docker мав доступ до ваших папок:
```
echo -e "AIRFLOW_UID=$(id -u)" > .env
```

## 🐍 Крок 4: Запуск "серця" системи
Тепер найвідповідальніший момент - запуск бази даних PostgreSQL та самого Airflow.

Ініціалізація бази даних (це робиться один раз):
```
docker compose up airflow-init
```
Зачекайте, поки в кінці з'явиться напис, що все "Exited with code 0".
Запуск усіх сервісів у фоновому режимі:
```
docker compose up -d
```
Як перевірити, що все працює? Зачекайте 1-2 хвилини, поки підніметься PostgreSQL та вебсервер. Тепер відкрийте браузер на вашому основному Windows-комп'ютері:

http://192.168.0.223:8080
Логін: airflow
Пароль: airflow

#### 🔗 Посилання

Детальний гайд: [vkm.pp.ua](https://vkm.pp.ua)

Автор: Віктор Калюта
