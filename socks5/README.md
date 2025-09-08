# Установка и настройка на VPS сервере SOCKS5

1) Устанавливаем dante

    ```bash
    apt update
    apt install dante-server
    ```

2) Проверяем установку

    ```bash
    systemctl status danted.service
    ```

3) Создаем чистую конфигурацию

    ```bash
    rm /etc/danted.conf
    nano /etc/danted.conf
    ```

    и вставляем

    ```text
    logoutput: syslog
    user.privileged: root
    user.unprivileged: nobody

    # The listening network interface or address.
    internal: 0.0.0.0 port=1080

    # The proxying network interface or address.
    external: eth0

    # socks-rules determine what is proxied through the external interface.
    socksmethod: username

    # client-rules determine who can connect to the internal interface.
    clientmethod: none

    client pass {
        from: 0.0.0.0/0 to: 0.0.0.0/0
    }

    socks pass {
        from: 0.0.0.0/0 to: 0.0.0.0/0
    }
    ```

4) Создаем пользователя для dante

    ```bash
    useradd -r -s /bin/false proxy_user
    passwd proxy_user
    ```

5) Перезапускаем и проверяем

    ```bash
    sudo systemctl restart danted.service
    systemctl status danted.service
    ```

Подключение:

```bash
curl -v -x socks5://proxy_user:your_dante_password@your_server_ip:1080 http://www.google.com/
```
