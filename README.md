<h1>Хранилище файлов с доступом по HTTP</h1>

<h3>Техническое задание:</h3>
Реализовать демон, который предоставит HTTP API для загрузки (upload), скачивания (download) и удаления файлов.


<h4>Upload:</h4>
получив файл от клиента, демон возвращает в отдельном поле HTTP response хэш загруженного файла

демон сохраняет файл на диск в следующую структуру каталогов:

store/ab/abcdef12345...

где "abcdef12345..." - имя файла, совпадающее с его хэшем,

/ab/ - подкаталог, состоящий из первых двух символов хэша файла.

Алгоритм хэширования - на ваш выбор.


<h4>Download:</h4>
Запрос на скачивание: клиент передаёт параметр - хэш файла. Демон ищет файл в локальном хранилище и отдаёт его, если находит.


<h4>Delete:</h4>
Запрос на удаление: клиент передаёт параметр - хэш файла. Демон ищет файл в локальном хранилище и удаляет его, если находит.


<h3>Реализация:</h3>
API реализован с помощью легковесного микрофреймворка Bottle, демонизация осуществлена с помощью внутреннего решения BottleDaemon.

<h4>Запросы:</h4>
<b>Upload:</b>

POST http://host:port/upload



form-data 'file=<файл>'

<b>Download:</b>

GET http://host:port/download?h=<хеш>

<b>Delete:</b>

DELETE http://host:port/remove?h=<хеш>


<h3>Установка и запуск:</h3>
```

    git clone https://github.com/StepanovSerjant/TaskForDoctorWeb.git
    cd TaskForDoctorWeb
    python3 -m venv venv
    venv/bin/activate
    pip3 install -r requirements.txt 
    cd app
    python3 main.py
```

Вышеуказанное приложение будет запущено в фоновом режиме. 
Этот скрипт верхнего уровня можно легко использовать для запуска / остановки фонового процесса:
```
  usage:  main.py [-h] {start,stop}
```

Библиотека гарантирует, что приложение будет запущено только один раз - так что несколько запуском никак не сможет навредить.
