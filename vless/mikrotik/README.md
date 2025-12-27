# Настройка Mikrotik

## 1. Поднимаем образ для туннелирования vless:

https://github.com/jsonguard/vless-mikrotik (пункт 10 скипнуть)

Потенциальные проблемы:

`ut-interface-list` -> `out-interface-list`

`ram-high` -> `memory-high`

Еще можно настроить DOH: https://github.com/wilmeralmazan/google-doh-mikrotik/blob/main/dns-doh.rsc / https://help.mikrotik.com/docs/pages/viewpage.action?pageId=83099652.

## 2. Отключаем `defconf: fasttrack` (`chain=forward`) в Ip -> Firewall -> Filter Rules.

Есть мнение, что с включенным правилом медленно работает vless. Поэтому отключаем.

Также можно отключить IPv6.

## 3. Настраиваем туннелирование определенных адресов:

Создаем таблицу для маршрутизации (своего рода маркер):

```routeros
/routing table add disabled=no fib name=to_vpn_mark
```

Направляем трафик в туннель (все адреса под маркером `to_vpn_mark` будут направляться в контейнер):

```routeros
/ip route add distance=1 dst-address=0.0.0.0/0 gateway=172.17.0.2 routing-table=to_vpn_mark check-gateway=ping
```

Настраиваем маршруты (адреса, которые будем туннелировать):

```routeros
/ip firewall address-list add address=2ip.ru list=custom
```

Добавляем mangle правила (связываем адреса и маркер):

```routeros
/ip firewall mangle add action=mark-connection chain=prerouting connection-mark=no-mark connection-state=new dst-address-list=custom new-connection-mark=to_vpn_conn_custom passthrough=yes in-interface-list=LAN comment=custom
/ip firewall mangle add action=mark-routing chain=prerouting connection-mark=to_vpn_conn_custom new-routing-mark=to_vpn_mark passthrough=yes in-interface-list=LAN comment=custom
```

## 4. Настраиваем сервисы

Скрипты для получения IPv4 адресов можно создать в System -> Scripts. В идеале для них нужен scheduler (cron) с примерным содержимым:

```routeros
/system/script run youtube
```

### Youtube:

Скрипт:

```routeros
/tool fetch url="https://raw.githubusercontent.com/KostikShutov/working-from-china/refs/heads/main/vless/mikrotik/youtube_cidr_ipv4.rsc" mode=https dst-path=youtube_cidr_ipv4.rsc
/ip firewall address-list remove [find list=YOUTUBE-CIDR]
/import file-name=youtube_cidr_ipv4.rsc
```

Mangle правила:

```routeros
/ip firewall mangle add action=mark-connection chain=prerouting connection-mark=no-mark connection-state=new dst-address-list=YOUTUBE-CIDR new-connection-mark=to_vpn_conn_youtube passthrough=yes in-interface-list=LAN comment=YOUTUBE-CIDR
/ip firewall mangle add action=mark-routing chain=prerouting connection-mark=to_vpn_conn_youtube new-routing-mark=to_vpn_mark passthrough=yes in-interface-list=LAN comment=YOUTUBE-CIDR
```

### Telegram:

Скрипт:

```routeros
/tool fetch url="https://raw.githubusercontent.com/KostikShutov/working-from-china/refs/heads/main/vless/mikrotik/telegram_cidr_ipv4.rsc" mode=https dst-path=telegram_cidr_ipv4.rsc
/ip firewall address-list remove [find list=TELEGRAM-CIDR]
/import file-name=telegram_cidr_ipv4.rsc
```

Mangle правила:

```routeros
/ip firewall mangle add action=mark-connection chain=prerouting connection-mark=no-mark connection-state=new dst-address-list=TELEGRAM-CIDR new-connection-mark=to_vpn_conn_telegram passthrough=yes in-interface-list=LAN comment=TELEGRAM-CIDR
/ip firewall mangle add action=mark-routing chain=prerouting connection-mark=to_vpn_conn_telegram new-routing-mark=to_vpn_mark passthrough=yes in-interface-list=LAN comment=TELEGRAM-CIDR
```

### Jetbrains:

Скрипт:

```routeros
/tool fetch url="https://raw.githubusercontent.com/KostikShutov/working-from-china/refs/heads/main/vless/mikrotik/jetbrains_cidr_ipv4.rsc" mode=https dst-path=jetbrains_cidr_ipv4.rsc
/ip firewall address-list remove [find list=JETBRAINS-CIDR]
/import file-name=jetbrains_cidr_ipv4.rsc
```

Mangle правила:

```routeros
/ip firewall mangle add action=mark-connection chain=prerouting connection-mark=no-mark connection-state=new dst-address-list=JETBRAINS-CIDR new-connection-mark=to_vpn_conn_jetbrains passthrough=yes in-interface-list=LAN comment=JETBRAINS-CIDR
/ip firewall mangle add action=mark-routing chain=prerouting connection-mark=to_vpn_conn_jetbrains new-routing-mark=to_vpn_mark passthrough=yes in-interface-list=LAN comment=JETBRAINS-CIDR
```

### Chatgpt:

Скрипт:

```routeros
/tool fetch url="https://raw.githubusercontent.com/KostikShutov/working-from-china/refs/heads/main/vless/mikrotik/chatgpt_cidr_ipv4.rsc" mode=https dst-path=chatgpt_cidr_ipv4.rsc
/ip firewall address-list remove [find list=CHATGPT-CIDR]
/import file-name=chatgpt_cidr_ipv4.rsc
```

Mangle правила:

```routeros
/ip firewall mangle add action=mark-connection chain=prerouting connection-mark=no-mark connection-state=new dst-address-list=CHATGPT-CIDR new-connection-mark=to_vpn_conn_chatgpt passthrough=yes in-interface-list=LAN comment=CHATGPT-CIDR
/ip firewall mangle add action=mark-routing chain=prerouting connection-mark=to_vpn_conn_chatgpt new-routing-mark=to_vpn_mark passthrough=yes in-interface-list=LAN comment=CHATGPT-CIDR
```

### Meta (Instagram, Facebook, WhatsApp):

Скрипт:

```routeros
/tool fetch url="https://raw.githubusercontent.com/KostikShutov/working-from-china/refs/heads/main/vless/mikrotik/meta_cidr_ipv4.rsc" mode=https dst-path=meta_cidr_ipv4.rsc
/ip firewall address-list remove [find list=META-CIDR]
/import file-name=meta_cidr_ipv4.rsc
```

Mangle правила:

```routeros
/ip firewall mangle add action=mark-connection chain=prerouting connection-mark=no-mark connection-state=new dst-address-list=META-CIDR new-connection-mark=to_vpn_conn_meta passthrough=yes in-interface-list=LAN comment=META-CIDR
/ip firewall mangle add action=mark-routing chain=prerouting connection-mark=to_vpn_conn_meta new-routing-mark=to_vpn_mark passthrough=yes in-interface-list=LAN comment=META-CIDR
```

### Twitter

```routeros
/tool fetch url="https://raw.githubusercontent.com/KostikShutov/working-from-china/refs/heads/main/vless/mikrotik/twitter_cidr_ipv4.rsc" mode=https dst-path=twitter_cidr_ipv4.rsc
/ip firewall address-list remove [find list=TWITTER-CIDR]
/import file-name=twitter_cidr_ipv4.rsc
```

Mangle правила:

```routeros
/ip firewall mangle add action=mark-connection chain=prerouting connection-mark=no-mark connection-state=new dst-address-list=TWITTER-CIDR new-connection-mark=to_vpn_conn_twitter passthrough=yes in-interface-list=LAN comment=TWITTER-CIDR
/ip firewall mangle add action=mark-routing chain=prerouting connection-mark=to_vpn_conn_twitter new-routing-mark=to_vpn_mark passthrough=yes in-interface-list=LAN comment=TWITTER-CIDR
```

### Medium

```routeros
/tool fetch url="https://raw.githubusercontent.com/KostikShutov/working-from-china/refs/heads/main/vless/mikrotik/medium_com_cidr_ipv4.rsc" mode=https dst-path=medium_com_cidr_ipv4.rsc
/ip firewall address-list remove [find list=MEDIUM_COM-CIDR]
/import file-name=medium_com_cidr_ipv4.rsc
```

Mangle правила:

```routeros
/ip firewall mangle add action=mark-connection chain=prerouting connection-mark=no-mark connection-state=new dst-address-list=MEDIUM_COM-CIDR new-connection-mark=to_vpn_conn_medium_com passthrough=yes in-interface-list=LAN comment=MEDIUM_COM-CIDR
/ip firewall mangle add action=mark-routing chain=prerouting connection-mark=to_vpn_conn_medium_com new-routing-mark=to_vpn_mark passthrough=yes in-interface-list=LAN comment=MEDIUM_COM-CIDR
```

### Linkedin

```routeros
/tool fetch url="https://raw.githubusercontent.com/KostikShutov/working-from-china/refs/heads/main/vless/mikrotik/linkedin_cidr_ipv4.rsc" mode=https dst-path=linkedin_cidr_ipv4.rsc
/ip firewall address-list remove [find list=LINKEDIN-CIDR]
/import file-name=linkedin_cidr_ipv4.rsc
```

Mangle правила:

```routeros
/ip firewall mangle add action=mark-connection chain=prerouting connection-mark=no-mark connection-state=new dst-address-list=LINKEDIN-CIDR new-connection-mark=to_vpn_conn_linkedin passthrough=yes in-interface-list=LAN comment=LINKEDIN-CIDR
/ip firewall mangle add action=mark-routing chain=prerouting connection-mark=to_vpn_conn_linkedin new-routing-mark=to_vpn_mark passthrough=yes in-interface-list=LAN comment=LINKEDIN-CIDR
```

Запускаем каждый скрипт и создаем mangle правила по каждому сервису.
