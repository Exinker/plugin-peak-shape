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
1. Зайти в папку с плагинами: `cd ATOM_PATH\Plugins\python`;
2. Установить пакетный менеджер `uv`: `pip install uv`;
3. Клонировать проект с удаленного репозитория: `git clone https://github.com/Exinker/plugin-peak-shape.git`;
4. Зайти в папку с плагином для расчета формы контура линии: `cd plugin-peak-shape`;
5. Создать виртуальное окружение и установить необходимые зависимости: `uv sync --no-dev`;

## Usage

### ENV
Преременные окружения плагина:
- `LOGGING_LEVEL: 'DEBUG' | 'INFO' | 'WARNING' | 'ERROR' = 'INFO'` - уровень логгирования;
- `MAX_WORKERS: int = 1` - запустить в многопроцессном режиме; ==- не поддерживается!==
- `DEFAULT_SHAPE: str = 2;0;.1` - формы контура линии по умолчанию;

Преременные окружения алгоритма поиска пиков:
- `N_COUNTS_MIN: int = 10` - минимальное количество отсчетов пика;
- `N_COUNTS_MAX: int = 100` - максимальное количество отсчетов пика;
- `EXCEPT_CLIPPED_PEAK: int = True` - исключить пики с "зашкаленными" отсчетами;
- `EXCEPT_SLOPED_PEAK: int = True` - исключить пики с большим наклоном;
- `EXCEPT_EDGES: int = False` - исключить крайние отсчеты пика;
- `SLOPE_MAX: float = 1` - максимальный уровень наклона пика;
- `AMPLITUDE_MIN: float = 1` - минимальная амплатуда пика;
- `NOISE_LEVEL: int = 10` - уровень амплитуды пика относительно шума;
