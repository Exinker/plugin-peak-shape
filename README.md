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
- `MAX_WORKERS: int = 1` - запустить в многопроцессном режиме;

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

- `RETRIEVE_SHAPE_DEFAULT=2;0;.1` - формы контура линии по умолчанию;
- `RETRIEVE_SHAPE_ERROR_MAX=.001` - максимальное отклонение пика от формы;
- `RETRIEVE_SHAPE_ERROR_MEAN=.0001` - среднее отклонение пика от формы;
- `RETRIEVE_SHAPE_N_PEAKS_FILTRATED_BY_WIDTH=None` - фильтрация пиков по ширине;
- `RETRIEVE_SHAPE_N_PEAKS_MIN=10` - минимальное количество пиков;


Преременные окружения алгоритма вычисления формы контура пика:
- `DEFAULT_SHAPE: Shape = 2;0;0.1)` - 
- `ERROR_MAX: float = 0.001` - 
- `ERROR_MEAN: float = 0.0001` - 
- `N_PEAKS_MIN: int = 10,` - 
