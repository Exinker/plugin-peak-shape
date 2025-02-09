# PEAK-SHAPE

**PEAK-SHAPE** - плагин для ПО [Атом](https://www.vmk.ru/product/programmnoe_obespechenie/atom.html) для расчета формы контура спектральной линии.


## Author Information:
Павел Ващенко (vaschenko@vmk.ru)
[ВМК-Оптоэлектроника](https://www.vmk.ru/), г. Новосибирск 2024 г.

## Installation
### Установка Python
Для работы требуется установить Python версии 3.12. *Ссылку на последнюю версию можно скачать [здесь](https://www.python.org/downloads/).*


### Установка виртуального окружения
Зависимости, необходимые для работы приложения, необходимо установить в виртуальное окружение `.venv`. Для этого в командной строке необходимо:
1. Зайди в папку с приложением: `cd C:\Atom x64 3.3 (2024.03.02)\Plugins\python`;
2. Клонировать проект: `git clone https://github.com/Exinker/plugin-peak-shape.git .`;
3. Установить пакетный менеджер `uv`: `pip install uv`;
4. Создать виртуальное окружение и установить необходимые зависимости: `uv sync --no-dev`;
