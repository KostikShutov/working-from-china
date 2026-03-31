# Настройка https в nginx

1) Устанавливаем пакеты

```bash
apt install certbot python3-certbot-nginx
```

2) Выписываем и прописываем сертификат в nginx

```bash
certbot --nginx -d example.com -d www.example.com --register-unsafely-without-email
```
