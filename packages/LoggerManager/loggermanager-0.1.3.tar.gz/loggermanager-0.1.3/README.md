# LoggerManager

LoggerManager - это гибкая система управления логированием с поддержкой логирования в консоль и файл. Система позволяет настраивать уровни логирования, фильтры и формат вывода.

_____

## Установка

Установить можно с помощью `pip`:

```bash
pip install LoggerManager
```
_____

## Использование

```python
from LoggerManager import LoggerManager

logger_manager = LoggerManager(name='MyLogger', log_to_file=True)
logger = logger_manager.logger

logger.debug("This is a debug message")
logger.info("This is an info message")
logger.warning("This is a warning message")
```

_____

## Документация методов

#### Методы:

- **`set_name(name: str)`**
  - Изменяет имя логгера.
  - **Пример использования:**
    ```python
    logger_manager.set_name('NewLoggerName')
    ```

- **`set_filter(level: LogLevel)`**
  - Устанавливает фильтр для логирования на определённом уровне.
  - **Пример использования:**
    ```python
    logger_manager.set_filter('ERROR')
    ```

- **`set_filter_list(levels: Sequence[LogLevel])`**
  - Устанавливает список уровней фильтрации.
  - **Пример использования:**
    ```python
    logger_manager.set_filter_list(['INFO', 'ERROR'])
    ```

- **`clear_filter()`**
  - Очищает текущие фильтры логирования.
  - **Пример использования:**
    ```python
    logger_manager.clear_filter()
    ```

- **`enable_logging()`**
  - Включает логирование.
  - **Пример использования:**
    ```python
    logger_manager.enable_logging()
    ```

- **`disable_logging()`**
  - Отключает логирование.
  - **Пример использования:**
    ```python
    logger_manager.disable_logging()
    ```
    
- **`enable_internal_logging()`**
  - Включает внутреннее логирование для отладки работы `LoggerManager`.
  - **Пример использования:**
    ```python
    logger_manager.enable_internal_logging()
    ```

- **`disable_internal_logging()`**
  - Отключает внутреннее логирование.
  - **Пример использования:**
    ```python
    logger_manager.disable_internal_logging()
    ```

____

- **`enable_file_logging(file_name: str = 'app.log', log_dir: str = 'logs')`**
  - Включает логирование в файл.
  - **Пример использования:**
    ```python
    logger_manager.enable_file_logging(file_name='logfile.log', log_dir='log_dir')
    ```

- **`disable_file_logging()`**
  - Отключает логирование в файл.
  - **Пример использования:**
    ```python
    logger_manager.disable_file_logging()
    ```

- **`set_file_handler_params(max_bytes: int, backup_count: int)`**
  - Настраивает параметры для ротации логов (размер файла и количество резервных копий).
  - **Пример использования:**
    ```python
    logger_manager.set_file_handler_params(max_bytes=1024 * 1024, backup_count=5)
    ```

- **`set_file_level(level: LogLevel)`**
  - Устанавливает уровень логирования для файлового обработчика.
  - **Пример использования:**
    ```python
    logger_manager.set_file_level('INFO')
    ```

- **`set_file_filter(level: LogLevel)`**
  - Устанавливает фильтр для файлового логирования на указанном уровне.
  - **Пример использования:**
    ```python
    logger_manager.set_file_filter('ERROR')
    ```

- **`set_file_filter_list(levels: List[str])`**
  - Фильтрует уровни логирования, которые будут записываться в файл. Можно указать уровни, такие как `"DEBUG"`, `"INFO"`, `"WARNING"`, `"ERROR"`, `"CRITICAL"`.
  - **Пример использования:**
    ```python
    logger_manager.set_file_filter_list(["WARNING", "ERROR", "CRITICAL"])
    ```
    Это позволит логировать в файл только сообщения с уровнями `"WARNING"`, `"ERROR"` и `"CRITICAL"`.


- **`set_file_format(format_string: str)`**
  - Устанавливает формат вывода для файлового логирования.
  - **Пример использования:**
    ```python
    logger_manager.set_file_format("%(asctime)s - %(levelname)s - %(message)s")
    ```
    
______

 - **`enable_console_logging()`**
  - Включает логирование сообщений в консоль.
  - **Пример использования:**
    ```python
    logger_manager.enable_console_logging()
    ```

- **`disable_console_logging()`**
  - Отключает логирование в консоль.
  - **Пример использования:**
    ```python
    logger_manager.disable_console_logging()
    ```

- **`set_console_level(level: LogLevel)`**
  - Устанавливает уровень логирования для консоли.
  - **Пример использования:**
    ```python
    logger_manager.set_console_level('INFO')
    ```
    
- **`set_console_filter(level: LogLevel)`**
  - Устанавливает фильтр для консольного логирования.
  - **Пример использования:**
    ```python
    logger_manager.set_console_filter('WARNING')
    ```
 
- **`set_console_filter_list(levels: List[str])`**
  - Фильтрует уровни логирования, которые будут отображаться в консоли. Можно указать список уровней, таких как `"DEBUG"`, `"INFO"`, `"WARNING"`, `"ERROR"`, `"CRITICAL"`.
  - **Пример использования:**
    ```python
    logger_manager.set_console_filter_list(["INFO", "ERROR"])
    ```
    В этом случае в консоль будут логироваться только сообщения с уровнями `"INFO"` и `"ERROR"`.

  
- **`set_console_format(format_string: str)`**
  - Устанавливает формат вывода для консольного логирования.
  - **Пример использования:**
    ```python
    logger_manager.set_console_format("%(asctime)s - %(message)s")
    ```

- **`set_console_color(level: LogLevel, color: ColorName)`**
  - Устанавливает цвет для указанного уровня консольного логирования.
  - **Пример использования:**
    ```python
    logger_manager.set_console_color('ERROR', 'red')
    ```

_____

- **`set_all_level(level: LogLevel)`**
  - Устанавливает единый уровень логирования для всех обработчиков.
  - **Пример использования:**
    ```python
    logger_manager.set_all_level('WARNING')
    ```

- **`set_all_filter(level: LogLevel)`**
  - Устанавливает единый фильтр для всех обработчиков.
  - **Пример использования:**
    ```python
    logger_manager.set_all_filter('ERROR')
    ```

- **`clear_all_filter()`**
  - Очищает все фильтры для всех обработчиков.
  - **Пример использования:**
    ```python
    logger_manager.clear_all_filter()
    ```
    
_____

- **`time_execution()`**
  - Контекстный менеджер для логирования времени выполнения блока кода.
  - **Пример использования:**
    ```python
    with logger_manager.time_execution():
        # код, время выполнения которого нужно логировать
        pass
    ```
---