# Настройка Mikrotik

## 1. Поднимаем образ для туннелирования vless:

https://github.com/jsonguard/vless-mikrotik (пункт 10 скипнуть)

Потенциальные проблемы:

`ut-interface-list` -> `out-interface-list`

`ram-high` -> `memory-high`

## 2. Отключаем `defconf: fasttrack` (`chain=forward`) в Ip -> Firewall -> Filter Rules.

Есть мнение, что с включенным правилом медленно работает vless. Поэтому отключаем.

## 3. Настраиваем туннелирование определенных адресов:

Создаем таблицу для маршрутизации (своего рода маркер):

```
/routing table add disabled=no fib name=to_vpn_mark
```

Направляем трафик в туннель (все адреса под маркером `to_vpn_mark` будут направляться в контейнер):

```
/ip route add distance=1 dst-address=0.0.0.0/0 gateway=172.17.0.2 routing-table=to_vpn_mark check-gateway=ping
```

Настраиваем маршруты (адреса, которые будем туннелировать):

```
/ip firewall address-list add address=2ip.ru list=custom
```

Добавляем mangle правила (связываем адреса и маркер):

```
/ip firewall mangle add action=mark-routing chain=prerouting dst-address-list=custom new-routing-mark=to_vpn_mark passthrough=yes
/ip firewall mangle add action=mark-routing chain=output dst-address-list=custom new-routing-mark=to_vpn_mark passthrough=yes
```

## 4. Настраиваем сервисы

Скрипты для получения IPv4 адресов можно создать в System -> Scripts. В идеале для них нужен cron.

### Youtube:

Скрипт:

```
/tool fetch url="https://raw.githubusercontent.com/touhidurrr/iplist-youtube/refs/heads/main/lists/routerosv4.rsc" mode=https dst-path=routerosv4.rsc
/import file-name=routerosv4.rsc
```

Mangle правила:

```
/ip firewall mangle add action=mark-routing chain=prerouting dst-address-list=youtube new-routing-mark=to_vpn_mark passthrough=yes
/ip firewall mangle add action=mark-routing chain=output dst-address-list=youtube new-routing-mark=to_vpn_mark passthrough=yes
```

### Whatsapp:

Скрипт:

```
/tool fetch url="https://raw.githubusercontent.com/HybridNetworks/whatsapp-cidr/refs/heads/main/WhatsApp/whatsapp_cidr_ipv4.rsc" mode=https dst-path=whatsapp_cidr_ipv4.rsc
/ip firewall address-list remove [find list=WHATSAPP-CIDR]
/import file-name=whatsapp_cidr_ipv4.rsc
```

Mangle правила:

```
/ip firewall mangle add action=mark-routing chain=prerouting dst-address-list=WHATSAPP-CIDR new-routing-mark=to_vpn_mark passthrough=yes
/ip firewall mangle add action=mark-routing chain=output dst-address-list=WHATSAPP-CIDR new-routing-mark=to_vpn_mark passthrough=yes
```

### Telegram:

Скрипт:

```
/tool fetch url="https://raw.githubusercontent.com/KostikShutov/working-from-china/refs/heads/main/vless/mikrotik/telegram_cidr_ipv4.rsc" mode=https dst-path=telegram_cidr_ipv4.rsc
/ip firewall address-list remove [find list=TELEGRAM-CIDR]
/import file-name=telegram_cidr_ipv4.rsc
```

Mangle правила:

```
/ip firewall mangle add action=mark-routing chain=prerouting dst-address-list=TELEGRAM-CIDR new-routing-mark=to_vpn_mark passthrough=yes
/ip firewall mangle add action=mark-routing chain=output dst-address-list=TELEGRAM-CIDR new-routing-mark=to_vpn_mark passthrough=yes
```

### Jetbrains:

Скрипт:

```
/tool fetch url="https://raw.githubusercontent.com/KostikShutov/working-from-china/refs/heads/main/vless/mikrotik/jetbrains_cidr_ipv4.rsc" mode=https dst-path=jetbrains_cidr_ipv4.rsc
/ip firewall address-list remove [find list=JETBRAINS-CIDR]
/import file-name=jetbrains_cidr_ipv4.rsc
```

Mangle правила:

```
/ip firewall mangle add action=mark-routing chain=prerouting dst-address-list=JETBRAINS-CIDR new-routing-mark=to_vpn_mark passthrough=yes
/ip firewall mangle add action=mark-routing chain=output dst-address-list=JETBRAINS-CIDR new-routing-mark=to_vpn_mark passthrough=yes
```

### Chatgpt:

Скрипт:

```
/tool fetch url="https://raw.githubusercontent.com/KostikShutov/working-from-china/refs/heads/main/vless/mikrotik/chatgpt_cidr_ipv4.rsc" mode=https dst-path=chatgpt_cidr_ipv4.rsc
/ip firewall address-list remove [find list=CHATGPT-CIDR]
/import file-name=chatgpt_cidr_ipv4.rsc
```

Mangle правила:

```
/ip firewall mangle add action=mark-routing chain=prerouting dst-address-list=CHATGPT-CIDR new-routing-mark=to_vpn_mark passthrough=yes
/ip firewall mangle add action=mark-routing chain=output dst-address-list=CHATGPT-CIDR new-routing-mark=to_vpn_mark passthrough=yes
```

### Meta (Instagram, Facebook):

Скрипт:

```
/tool fetch url="https://raw.githubusercontent.com/KostikShutov/working-from-china/refs/heads/main/vless/mikrotik/meta_cidr_ipv4.rsc" mode=https dst-path=meta_cidr_ipv4.rsc
/ip firewall address-list remove [find list=META-CIDR]
/import file-name=meta_cidr_ipv4.rsc
```

Mangle правила:

```
/ip firewall mangle add action=mark-routing chain=prerouting dst-address-list=META-CIDR new-routing-mark=to_vpn_mark passthrough=yes
/ip firewall mangle add action=mark-routing chain=output dst-address-list=META-CIDR new-routing-mark=to_vpn_mark passthrough=yes
```

### Twitter

```
/tool fetch url="https://raw.githubusercontent.com/KostikShutov/working-from-china/refs/heads/main/vless/mikrotik/twitter_cidr_ipv4.rsc" mode=https dst-path=twitter_cidr_ipv4.rsc
/ip firewall address-list remove [find list=TWITTER-CIDR]
/import file-name=twitter_cidr_ipv4.rsc
```

Mangle правила:

```
/ip firewall mangle add action=mark-routing chain=prerouting dst-address-list=TWITTER-CIDR new-routing-mark=to_vpn_mark passthrough=yes
/ip firewall mangle add action=mark-routing chain=output dst-address-list=TWITTER-CIDR new-routing-mark=to_vpn_mark passthrough=yes
```

Запускаем каждый скрипт и создаем mangle правила по каждому сервису.
