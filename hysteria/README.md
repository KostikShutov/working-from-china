# Установка и настройка на VPS сервере Hysteria

1. Устанавливаем Hysteria

```bash
bash <(curl -fsSL https://get.hy2.sh/)
```

2. Выписываем сертификат на свой домен по [гайду](../HTTPS.md) и варварски выдаем права доступа:

```bash
sudo chmod -R 777 /etc/letsencrypt
```

Именно свой домен будем прописывать в TLS SNI на клиенте.

3. Настраиваем конфигурацию

```bash
nano /etc/hysteria/config.yaml
```

```yaml
listen: 0.0.0.0:444

tls:
  cert: /etc/letsencrypt/live/<your_domain>/fullchain.pem
  key: /etc/letsencrypt/live/<your_domain>/privkey.pem

auth:
  type: password
  password: <your password>

masquerade:
  type: proxy
  proxy:
    url: https://ya.ru/
    rewriteHost: true
```

4. Запускаем

```bash
systemctl enable hysteria-server.service
systemctl start hysteria-server.service
```
