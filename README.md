 # Gems deals history API (тестовое задание)
Вариант решения для [тестового задания](./task.txt) по созданию веб-сервиса на Django (DRF),
предоставляющего REST-api для загрузки и отображения данных из CSV файла,
содержащего информацию об истории сделок. Реализованы все основные и
дополнительные требования.

* Для запуска клонировать репозиторий. Далее собрать и запустить контейнеры:
  ```shell
  docker-compose up
  ```
Отображаемое API доступно по адресу http://localhost/

Работа с сервисом предполагает отправку запросов при помощи любого HTTP-клиента:
- GET:
`curl http://localhost/`
- POST:
`curl -F "deals=@gems/csv_data/deals.csv" http://localhost/`
