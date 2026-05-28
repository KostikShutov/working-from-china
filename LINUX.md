# Linux гайды

## Отключение журналирования

```bash
sudo nano /etc/systemd/journald.conf
```

Выставить:

```conf
[Journal]
Storage=none
```

Перезапустить сервис:

```bash
sudo systemctl restart systemd-journald
```

Очистить старые логи:

```bash
sudo journalctl --rotate
sudo journalctl --vacuum-time=1s
```

Проверяем:

```bash
sudo journalctl --disk-usage
sudo journalctl -n 20
```
