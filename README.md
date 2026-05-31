# openwrt-passwall2-whitelist-geodata

**Язык:** Русский | [English](README.en.md)

Репозиторий для конвертации whitelist-данных из проекта [hxehex/russia-mobile-internet-whitelist](https://github.com/hxehex/russia-mobile-internet-whitelist) в файлы `geosite.dat` и `geoip.dat`, пригодные для использования в **PassWall2 на OpenWrt**.

Основной сценарий использования: **PassWall2 + Xray** на роутерах с ограниченными ресурсами, где требуется логика: **whitelist-ресурсы идут напрямую, остальное — через прокси/VPN**.

## Зачем нужен проект

Этот проект сделан прежде всего для **роутеров с маленькой памятью и ограниченными ресурсами**, где использование больших универсальных geodata-наборов часто избыточно или просто неудобно.

Поэтому архитектура проекта намеренно ориентирована на **небольшие, целевые и практичные списки**, которые решают конкретную задачу маршрутизации в PassWall2 и лучше подходят для бюджетных OpenWrt-устройств. Иными словами, здесь ставка сделана не на «гигантский справочник на все случаи жизни», а на компактный whitelist, который реально нужен в работе.

## Что делает репозиторий

Репозиторий:

- забирает текстовые whitelist-списки из upstream-проекта [hxehex/russia-mobile-internet-whitelist](https://github.com/hxehex/russia-mobile-internet-whitelist);
- использует следующие upstream-файлы:
  - [`whitelist.txt`](https://github.com/hxehex/russia-mobile-internet-whitelist/blob/main/whitelist.txt) — домены;
  - [`ipwhitelist.txt`](https://github.com/hxehex/russia-mobile-internet-whitelist/blob/main/ipwhitelist.txt) — одиночные IP-адреса;
  - [`cidrwhitelist.txt`](https://github.com/hxehex/russia-mobile-internet-whitelist/blob/main/cidrwhitelist.txt) — CIDR-подсети;
- нормализует входные данные;
- собирает:
  - `geosite.dat` — доменный whitelist для Xray;
  - `geoip.dat` — whitelist IP/CIDR для Xray;
- публикует готовые файлы в GitHub Releases для использования в OpenWrt / PassWall2.

## Что репозиторий не делает

Этот репозиторий **не**:

- поддерживает blacklist-наборы;
- генерирует sing-box-форматы `.json` или `.srs`;
- решает общую маршрутизацию OpenWrt сам по себе;
- заменяет PassWall2, Xray, policy routing, nftables или firewall-конфигурацию.

Он только готовит компактные geodata, которые потом использует PassWall2 / Xray.

## Тестовая платформа

Репозиторий разрабатывался и тестировался в следующей конфигурации:

- **Router:** Asus RT-AX53U / RT-AX1800U
- **SoC / target:** MediaTek MT7621, `ramips/mt7621`
- **Architecture:** `mipsel_24kc`
- **OpenWrt:** 23.05.5
- **PassWall2:** `luci-app-passwall2`
- **Backend:** Xray с использованием `geosite.dat` и `geoip.dat` из `/usr/share/v2ray/`

На других устройствах и версиях OpenWrt всё тоже может работать, но это нужно проверять отдельно.

## Структура репозитория

## Структура репозитория

```text
openwrt-passwall2-whitelist-geodata/
├── README.md
├── README.en.md
├── LICENSE
├── .gitignore
├── .github/
│   └── workflows/
│       └── build.yml
├── data/
│   ├── upstream/                  # upstream txt-источники
│   ├── generated/                 # нормализованные промежуточные данные
│   ├── geosite/                   # исходные текстовые данные для geosite
│   └── geoip/                     # исходные текстовые данные для geoip
├── proto_src/                     # protobuf-описания
├── proto_out/                     # сгенерированные protobuf Python-модули
├── scripts/
│   ├── fetch_sources.sh
│   ├── normalize_sources.py
│   ├── build_geosite_dat.py
│   ├── build_geoip_dat.py
│   ├── build_inputs.py
│   ├── normalize_whitelist.py
│   └── update-openwrt-example.sh
└── tests/
    ├── check_build_inputs.sh
    ├── check_inputs.sh
    ├── check_geosite_dat.py
    └── check_geoip_dat.py
```
## Pipeline

### 1. Загрузка данных

`scripts/fetch_sources.sh` скачивает upstream-списки из GitHub-репозитория источника.

### 2. Нормализация

`scripts/normalize_sources.py`:

- читает домены, IP и CIDR из upstream txt-файлов;
- удаляет комментарии и мусорные строки;
- нормализует домены;
- преобразует одиночные IP в host-CIDR (`/32` для IPv4 и `/128` для IPv6);
- сохраняет промежуточные данные в `data/generated/`.

### 3. Сборка geodata

- `scripts/build_geosite_dat.py` собирает `geosite.dat`;
- `scripts/build_geoip_dat.py` собирает `geoip.dat`.

Оба файла содержат тег `RU-WHITELIST`.

### 4. Публикация

GitHub Actions workflow `.github/workflows/build.yml`:

- запускается по расписанию и вручную;
- скачивает upstream-списки;
- нормализует их;
- собирает `geosite.dat` и `geoip.dat`;
- публикует артефакты в GitHub Releases.

## Почему в whitelist добавляется 2ip.io

Проект **намеренно** добавляет домен `2ip.io` в итоговый whitelist даже в том случае, если его нет в upstream-списках.

Это делается потому, что `2ip.io` используется как **smoke-domain для быстрой проверки работы маршрутизации** на OpenWrt + PassWall2. На практике нужен простой и запоминающийся домен, который можно быстро проверить:

- через браузер;
- через встроенный rule tester в PassWall2;
- через ручную проверку того, что whitelist-маршрут действительно уходит в `direct`.

`2ip.io` удобен именно как технический маркер:

- его легко запомнить;
- его удобно использовать в тестах;
- он помогает быстро убедиться, что правило whitelist реально срабатывает.

При этом `2ip.ru` и `ifconfig.me` проект **специально не добавляет принудительно**, чтобы smoke-проверка оставалась явной и управляемой.

## Использование в OpenWrt / PassWall2

В тестовой конфигурации geodata подключаются через стандартный механизм обновления в PassWall2:

1. Открыть **PassWall2 → Rule Manage**.
2. В блоке обновления GeoIP/Geosite найти **нижние поля Custom**:
   - **GeoIP Update URL (Custom)**
   - **Geosite Update URL (Custom)**
3. В этих полях Custom указать свои значения, указывающие на релиз этого репозитория, например:

   ```text
   GeoIP Update URL (Custom):   https://github.com/web3archi/openwrt-passwall2-whitelist-geodata/releases/download/geodata-latest/geoip.dat
   Geosite Update URL (Custom): https://github.com/web3archi/openwrt-passwall2-whitelist-geodata/releases/download/geodata-latest/geosite.dat
   ```

4. Нажать Enter в каждом поле (чтобы LuCI зафиксировал изменения), затем **Save & Apply**.

После этого PassWall2 будет скачивать и обновлять `geoip.dat` / `geosite.dat` из этого репозитория по встроенному механизму. Дополнительные скрипты на стороне роутера в базовом сценарии не нужны.

Типичная логика маршрутизации в PassWall2 при использовании этих geodata:

- `geosite:RU-WHITELIST` → `direct`
- `geoip:RU-WHITELIST` → `direct`
- всё остальное → через выбранный proxy/VPN-профиль

Точная реализация зависит от локальной конфигурации PassWall2 и порядка правил.

### Рекомендуемый шаблон правила в PassWall2

На практике удобно использовать **одно правило**, в котором одновременно проверяются и доменные, и IP-геоданные:

- `geosite:RU-WHITELIST` → `direct`
- `geoip:RU-WHITELIST` → `direct`

вместо двух разнесённых правил «только geosite» и «только geoip». Такой подход упрощает конфигурацию и снижает риск неожиданных эффектов от порядка правил и пересечений между ними.

### Замечание по применению настроек

Иногда (в зависимости от версии OpenWrt/PassWall2 и конкретной сборки) изменения, связанные с обновлением geodata и правок маршрутизации, не сразу начинают работать после обычного **Save & Apply** в LuCI.

Если после обновления GeoIP/Geosite и сохранения конфигурации ожидаемое поведение правил не проявляется, имеет смысл:

1. убедиться, что новые `geoip.dat` / `geosite.dat` действительно обновились на роутере;
2. при необходимости выполнить **перезагрузку устройства**, чтобы все сервисы PassWall2/Xray точно стартовали уже с новой конфигурацией и geodata.

Для большинства конфигураций достаточно обычного Save & Apply, но в сложных случаях «чистый» restart системы помогает исключить эффекты кэшей и частично перезапущенных демонов.

## Статус проекта

Проект рабочий и протестирован на целевой конфигурации, указанной выше, но его всё же правильнее считать **практическим кастомным решением**, а не универсальным дистрибутивным пакетом.

Текущий фокус проекта:

- компактные whitelist geodata для слабых роутеров;
- воспроизводимая сборка через GitHub Actions;
- стабильные release URL для OpenWrt-интеграции.

## Лицензия и свобода ПО

Проект задуман как **свободное и открытое программное обеспечение**.

- Скрипты, workflow-файлы и проектная обвязка могут использоваться, изменяться и распространяться в рамках лицензии репозитория.
- Исходные whitelist-данные сохраняют привязку к upstream-источнику: [hxehex/russia-mobile-internet-whitelist](https://github.com/hxehex/russia-mobile-internet-whitelist).

## Примечание

Проект не аффилирован с OpenWrt, PassWall2, Xray или upstream-репозиторием со списками.

Используйте его аккуратно, проверяйте правила маршрутизации на своём железе и относитесь к сгенерированным geodata как к рабочему входу для собственных policy rules.
