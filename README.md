# openwrt-passwall2-whitelist-geodata

Репозиторий для **конвертации белых списков (whitelist) из проекта `hxehex/russia-mobile-internet-whitelist`**
в файлы `geosite.dat` и `geoip.dat`, пригодные для использования в **PassWall2 на OpenWrt**.

Основной сценарий: PassWall2 (Xray backend) на роутерах класса Asus RT‑AX53U / RT‑AX1800U (ramips/mt7621),
где требуется режим «только whitelisting‑ресурсы идут напрямую, остальное через прокси».

## Цели и ограничения

### Что делает этот репозиторий

- Забирает whitelist‑данные из проекта
  [`hxehex/russia-mobile-internet-whitelist`](https://github.com/hxehex/russia-mobile-internet-whitelist):
  - домены (`whitelist.txt`);
  - IP‑адреса (`ipwhitelist.txt`);
  - CIDR‑диапазоны (`cidrwhitelist.txt`).
- Дополняет их локальными списками администратора (дополнительные домены и CIDR).
- Генерирует из них:
  - `geosite.dat` — доменный whitelist для Xray;
  - `geoip.dat` — whitelist IP/CIDR для Xray.
- Публикует эти файлы в GitHub Releases, чтобы их можно было использовать в PassWall2 через обновление geodata.

### Чего этот репозиторий НЕ делает

- Не генерирует и не поддерживает чёрные списки (blacklist).
- Не работает напрямую с sing-box (`.json` / `.srs`).
- Не решает общую маршрутизацию OpenWrt — только предоставляет geodata, которые далее использует PassWall2.

## Целевая платформа

Репозиторий разрабатывается и тестируется в следующей конфигурации:

- Router: Asus RT‑AX53U / RT‑AX1800U (Wi‑Fi 6, ramips/mt7621, mipsel_24kc)
- OpenWrt: 23.05.5 (официальные образы для `ramips/mt7621`)
- PassWall2: luci-app-passwall2
- Backend: Xray (использующий `geosite.dat` / `geoip.dat` из каталога `/usr/share/v2ray/`)

Использование на других устройствах и версиях OpenWrt возможно, но требует отдельной проверки.

## Структура репозитория

```text
openwrt-passwall2-whitelist-geodata/
├── README.md
├── domains/
│   ├── whitelist-hxehex.txt      # домены из hxehex/whitelist.txt (сырой импорт)
│   └── custom.txt                # дополнительные домены администратора
├── ip/
│   ├── whitelist-ip.txt          # IP из hxehex/ipwhitelist.txt
│   ├── whitelist-cidr.txt        # CIDR из hxehex/cidrwhitelist.txt
│   └── custom-cidr.txt           # дополнительные CIDR администратора
├── xray/
│   ├── geosite.dat               # сгенерированный доменный whitelist
│   └── geoip.dat                 # сгенерированный IP/CIDR whitelist
├── scripts/
│   ├── fetch-hxehex.sh           # загрузка данных из hxehex-репозитория
│   ├── build-geodata.py          # сборка geosite.dat / geoip.dat
│   └── update-openwrt-example.sh # пример обновления geodata на OpenWrt
└── .github/
    └── workflows/
        └── build.yml             # CI: fetch → build → release
```

## Поток данных (pipeline)

1. **Импорт whitelists**

   `scripts/fetch-hxehex.sh`:

   - скачивает `whitelist.txt` → `domains/whitelist-hxehex.txt`;
   - скачивает `ipwhitelist.txt` → `ip/whitelist-ip.txt`;
   - скачивает `cidrwhitelist.txt` → `ip/whitelist-cidr.txt`.

2. **Сборка geodata**

   `scripts/build-geodata.py`:

   - читает:
     - `domains/whitelist-hxehex.txt` и `domains/custom.txt`;
     - `ip/whitelist-ip.txt`, `ip/whitelist-cidr.txt`, `ip/custom-cidr.txt`;
   - нормализует домены и адреса;
   - генерирует:
     - `xray/geosite.dat`;
     - `xray/geoip.dat`.

3. **Публикация релиза**

   GitHub Actions (`.github/workflows/build.yml`):

   - запускает `fetch-hxehex.sh` и `build-geodata.py`;
   - создаёт релиз с файлами `geosite.dat` и `geoip.dat`.

## Использование на OpenWrt с PassWall2

### Обновление geodata

```sh
#!/bin/sh
set -e

BASE_URL="https://github.com/web3archi/openwrt-passwall2-whitelist-geodata/releases/latest/download"

wget -O /usr/share/v2ray/geoip.dat "${BASE_URL}/geoip.dat"
wget -O /usr/share/v2ray/geosite.dat "${BASE_URL}/geosite.dat"

service passwall2 restart
```

### Логика маршрутизации в PassWall2

- категории geosite/geoip, соответствующие whitelist‑набору (из `geosite.dat` / `geoip.dat` этого репозитория), направляются в `direct`;
- весь остальной трафик, не попадающий в whitelist‑категории, направляется через выбранный proxy‑/VPN‑профиль.

Конкретные настройки задаются в конфигурации PassWall2.

## Статус проекта

Проект находится в стадии начальной реализации и тестирования на связке:

- Asus RT‑AX53U / RT‑AX1800U (ramips/mt7621);
- OpenWrt 23.05.5;
- PassWall2 (Xray backend).

Поддержка других устройств и версий OpenWrt требует отдельной проверки.
