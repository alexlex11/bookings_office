##API бронирования офисов

Единственным неясным моментом для меня стало то, как реализовать флаг занятости комнаты в модели и хранить его в виде отдельного поля в базе данных.

Поэтому я реализовал это как логику на сервере: при запросе бронирования проверяется текущая занятость комнаты, и флаг хранится только в памяти сервера.

В остальном к API не возникло вопросов.

##Документация

Вся документация по API доступна в Swagger.

