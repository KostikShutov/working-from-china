# Работа из Китая

Если вы когда-нибудь слышали про `Golden Shield Project` или `Великий Китайский Файрвол`, то наверняка уже понимаете, что штука достаточно серьезная, лютый dpi, срез скорости при наличии "зарещенных слов" (например, `google`) и так далее. К тому же файрвол постоянно совершенствуется. Не стоит приезжать в Китай с настроем: "ща загуглю популярный впн в Китае, скачаю и поеду с ним в Китай". Почему? Читаем дальше.

Можно ознакомиться: <https://en.wikipedia.org/wiki/Great_Firewall>

## Как устроен этот монстр

Китайский файрвол напичкан следующими приколами:

- Блокировка ip адресов
- Перехват DNS
- Блокировка vpn протоколов
- Анализ пакетов (DPI)
- Фильтрация трафика по запрещенным словам

Файрвол - это не просто какое-то ПО у провайдера, это туннель во внешний мир, через который проходит вообще весь трафик.

![Коммуникация между городами](https://github.com/KostikShutov/working-from-china/assets/22249844/2161da6b-8af2-4510-98af-93252c57c0fb)

## Vpn

Начнем с того, что vpn в Китае не работает. Да, вообще не работает, никакие протоколы, у вас просто не будет коннекта. Китайцы блокируют, как ip-шники, так и протоколы. Следовательно не стоит обращать внимания на такие платные vpn-ы, как nord vpn, express vpn, surfshark, vypr vpn, private vpn и так далее, какая бы не была реклама. В Китае – это все мусор. Конечно, можно поднять свой vpn (например, wireguard или openvpn), но проработает он не долго.

Что же делать? Выход есть – shadowsocks. Что это такое?

## Shadowsocks

Немного копипасты про shadowsocks:

> Shadowsocks – бесплатный проект протокола шифрования с открытым исходным кодом, широко используемый в Китае для обхода интернет-цензуры. Он был создан в 2012 году китайским программистом по имени "clowwindy", и с тех пор стало доступно множество реализаций протокола. Shadowsocks не является самостоятельным прокси-сервером, а представляет собой клиентское программное обеспечение, помогающее подключиться к стороннему прокси-серверу SOCKS5, который похож на защищенный туннель оболочки. После подключения интернет-трафик затем может направляться через прокси-сервер. В отличие от SSH-туннеля, shadowsocks также может передавать трафик по протоколу дейтаграмм пользователей.

Короче shadowsocks – это наш пацан, с которым мы будем дружить. Все по классике, нам нужен клиент и сервер.

![Shadowsocks](https://github.com/KostikShutov/working-from-china/assets/22249844/b47eb299-fd23-4f15-bdcd-086781a6263a)

### Клиент

Клиент для mac: <https://github.com/shadowsocks/ShadowsocksX-NG>

![NG-1](https://github.com/KostikShutov/working-from-china/assets/22249844/dda925e6-4c3b-4a21-9d30-30c3653d3d9f)

Клиенты для ios: <https://apps.apple.com/ru/app/potatso/id1239860606> / <https://apps.apple.com/ru/app/shadowrocket/id932747118>

![Shadowrocket](https://github.com/KostikShutov/working-from-china/assets/22249844/5bcd34b5-4e5f-4939-b3fd-ceb3855efdeb)

Shadowrocket на самом деле можно использовать и на mac, но ShadowsocksX-NG более гибкий в настройке, а гибкость нам нужна.

### Сервер

Есть 2 стула, на 1-ом развернуть собственный shadowsocks, на 2-ом купить.

Сначала про собственное развертывание. Тут есть много подводных, информация не совсем публичная. Китайцы умеют детектить shadowsocks, хотя этот протокол тяжело выцепить из-за отсутствия сигнатуры.

Подводные:

- У shadowsocks есть несколько реализаций: shadowsocks, shadowsocks-r, shadowsocks-rust и так далее. Необходимо четко понимать отличия одного от другого. Иначе забанит.
- Расположение сервера, выбор страны короче говоря. Необходимо правильно выбрать страну. Знаю, что юзают Японию и Гонконг. Почему Гонконг - понятно (из-за суверенитета), а почему Япония – хз. Иначе забанит.
- Необходимо выбрать правильное шифрование и обфускацию трафика (v2ray / xray). По шифрованию могу посоветовать `chacha20-ietf-poly1305`, этот метод юзают в Китае. Иначе забанит.
- Прокся должна быть на домене, а не на ip. И не на дефолтном порте. Иначе забанит.
- Слышал, что в цепочку как-то еще nginx прикручивают.

Ссылочка на shadowsocks контейнеры для быстрого развертывания: <https://hub.docker.com/u/teddysun>

Все еще хочешь поднимать свой shadowsocks? Если перехотелось, то лови контакты на телеграмовского бота <https://t.me/TopSpeedBot>.

Дальше ничего сложного, прописываете креды shadowsocks в клиенте и подключаетесь. Радуемся.

## Связка с openvpn

Нельзя просто так взять и сначала врубить shadowsocks, а затем vpn. Коннекта не будет. Все что нам нужно – это организовать vpn коннекшен через прокси.

В целом ничего сложно, нужно всего лишь чуть-чуть сконфигурировать ShadowsocksX-NG и поправить конфиг openvpn.

В ShadowsocksX-NG переходим в `Preferences`, далее `Advanced`. Тут проставляем `Local Socks5 Listen Address` = `127.0.0.1` и `Local Socks5 Listen Port` = `1086`. С этой софтинкой все.

![NG-2](https://github.com/KostikShutov/working-from-china/assets/22249844/725498e2-5ea1-4287-9878-69be34fbae15)

Переходим в конфиг openvpn. Меняем протокол на tcp (`proto tcp`). В самом конце дописываем `socks-proxy 127.0.0.1 1086`, но до ключей и сертификатов. Понятно откуда этот ip и порт? Мы их проставили выше.

Ну все, теперь врубаем shadowsocks, а затем подключаемся к openvpn.

## Какие еще ништяки дает shadowsocks?

Shadowsocks дает буст к скорости вашего интернета. В самом начале было сказано про срез скорости интернета при наличии запрещенных слов. Соответственно, если трафик ровный, а значит нет доп. затрат на его анализ файрволом. Это лишь моя догадка, но буст скорости - это факт.
