# Files Service

## Как запустить проект:

После клонирования проекта локально необходимо выполнить команду:
```
cp .env.template .env
```
И передать значения переменным, указанным в появившемся файле .env (можно оставить значения по умолчанию)

Затем выполнить команду:
```
docker-compose up [--build]
```

#### Миграции БД (при необходимости):
```
docker-compose exec files-service-web flask db migrate  # создание
docker-compose exec files-service-web flask db upgrade  # применение
```

#### Заливка фикстур с пользователями (при необходимости):
После запуска сервиса перед первым запросом фикстуры с пользователями [отсюда](https://github.com/KonstantinChernov/test_files_service/tree/master/src/db/fixtures) загрузятся автоматически. Также их можно загрузить при помощи команды:
```
docker-compose exec files-service-web flask add_users_from_fixtures
```

#### Запуск тестов:
```
docker-compose -f docker-compose.test.yml up [--build]
```
 
## API
Разработаны эндпоинты: UPLOAD, DOWNLOAD, DELETE
Для доступа к эндпоинтам UPLOAD, DELETE необходима Basic аутентификация. Креды (login, password) доступны в [фикстурах](https://github.com/KonstantinChernov/test_files_service/blob/master/src/db/fixtures/users.json) 

### UPLOAD:
```http
POST /api/v1/files/upload/
```
Файл передается в теле запроса в поле "file". Заголовок Content-type: "multipart/form-data"

#### response:
При успешном запросе ответ следующий:
```javascript
{
  "saved" : string: hash,
}
```
код ответа 201

### DOWNLOAD:
```http
GET /api/v1/files/download/<hash:filename>
```
При успешном запросе отдается файл
код ответа 200

### DELETE:
```http
GET /api/v1/files/delete/<hash:filename>
```
При успешном запросе код ответа 204

### При ошибке запроса возвращается структура
#### response:
```javascript
{
    "error": {
        "code": status_code,
        "message": message
    }
}
```