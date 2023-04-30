# Telegram-бот для мониторинга процесса

Этот Telegram-бот мониторит процесс с наибольшим использованием процессора и оповещает владельца, когда процесс завершается.

## One line run:

```
sudo mkdir -p /opt/nodemonitor && sudo chmod 777 /opt/nodemonitor && curl -o /opt/nodemonitor/start.sh https://raw.githubusercontent.com/underskys/nodemonitor/main/start.sh && sudo chmod +x /opt/nodemonitor/start.sh && /opt/nodemonitor/start.sh
```

## Установка и запуск

1. Скачайте скрипт с GitLab, проверьте его версию и установите необходимые пакеты, используя следующую команду:

```
./start.sh
```

2. Запустите скрипт с аргументом --init для ввода токена Telegram-бота и идентификатора владельца:

```
nohup python your_script_name.py --init &
```

3. Donation 

```
Metamask: 0xa19360Ddd4Fc11b2A0804BAEb9330f4198C2Bc70
```