# PEAK-SHAPE

**PEAK-SHAPE** - плагин для ПО [Атом](https://www.vmk.ru/product/programmnoe_obespechenie/atom.html) для расчета формы контура пика.


## Author Information:
Павел Ващенко (vaschenko@vmk.ru)
[ВМК-Оптоэлектроника](https://www.vmk.ru/), г. Новосибирск 2024 г.

## Installation

### Установка Git
Для работы требуется установить Git. *Последнюю версию можно скачать [здесь](https://git-scm.com/downloads/win).*

### Установка Python
Для работы требуется установить Python версии 3.12. *Последнюю версию можно скачать [здесь](https://www.python.org/downloads/).*
Установка зависимостей выполняется с использованием пакетного менеджера `uv`, который можно установить командой: `pip install uv`;

### Установка виртуального окружения
Зависимости, необходимые для работы приложения, необходимо установить в виртуальное окружение `.venv`. Для этого в командной строке необходимо:
1. Зайти в папку с плагинами: `cd ATOM_PATH\Plugins\python`;
2. Клонировать проект с удаленного репозитория: `git clone https://github.com/Exinker/plugin-peak-shape.git`;
3. Зайти в папку с плагином для расчета формы контура пика: `cd plugin-peak-shape`;
4. Создать виртуальное окружение и установить необходимые зависимости: `uv sync --no-dev`;

## Usage

### ENV
Преременные окружения плагина:
- `LOGGING_LEVEL: 'DEBUG' | 'INFO' | 'WARNING' | 'ERROR' = 'INFO'` - уровень логгирования;
- `MAX_WORKERS: int = 1` - указать количество процессоров (для параллельных вычислений);

Преременные окружения алгоритма поиска пиков:
- `DRAFT_PEAK_N_COUNTS_MIN=10` - минимальное количество отсчетов пика;
- `DRAFT_PEAK_N_COUNTS_MAX=100` - максимальное количество отсчетов пика;
- `DRAFT_PEAK_EXCEPT_CLIPPED_PEAK=True` - исключить пики с "зашкаленными" отсчетами;
- `DRAFT_PEAK_EXCEPT_WIDE_PEAK=False` - исключить пики с шириной больше установленной;
- `DRAFT_PEAK_EXCEPT_SLOPED_PEAK=True` - исключить пики с наклоном больше установленного;
- `DRAFT_PEAK_EXCEPT_EDGES=False` - исключить крайние отсчеты пика;
- `DRAFT_PEAK_AMPLITUDE_MIN=0` - минимальная амплатуда пика;
- `DRAFT_PEAK_WIDTH_MAX=3.5` - максимальная ширина пика;
- `DRAFT_PEAK_SLOPE_MAX=.25` - максимальный уровень наклона пика;
- `DRAFT_PEAK_NOISE_LEVEL=10` - уровень амплитуды пика относительно шума;

Преременные окружения алгоритма вычисления формы контура пика:
- `RETRIEVE_SHAPE_DEFAULT=2;0;.1` - форма контура пика по умолчанию;
- `RETRIEVE_SHAPE_MIN_WIDTH` - минимальная ширина формы контура пика;
- `RETRIEVE_SHAPE_MAX_WIDTH` - максимальная ширина формы контура пика;
- `RETRIEVE_SHAPE_MAX_ASYMMETRY` - максимальная асимметрия формы контура пика;
- `RETRIEVE_SHAPE_ERROR_MAX=.001` - максимальное отклонение пика от формы;
- `RETRIEVE_SHAPE_ERROR_MEAN=.0001` - среднее отклонение пика от формы;
- `RETRIEVE_SHAPE_N_PEAKS_FILTRATED_BY_WIDTH=None` - фильтрация пиков по ширине;
- `RETRIEVE_SHAPE_N_PEAKS_MIN=10` - минимальное количество пиков;
