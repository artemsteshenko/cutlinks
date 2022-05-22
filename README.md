# cutlinks
site of project cutlinks for generation clever links

#### Сервис для создания умных ссылок. Сервис умеет создавать короткие ссылки, которые ведут на заданные страницы. Еще одна важная функция это создания "taplink" страниц, которые агрегируют другие ссылки (соц сети или полезные материалы). 
  
#### Презентация проекта http://cutlinks.ru/2223. 
#### Сайт проекта http://cutlinks.ru.  
#### Доска Trello https://trello.com/b/45RgYOjc/cutlinks


- Запуск проекта локально 
  - установить переменную окружения FLASK_APP
    (export FLASK_APP=cutlinks.py)
  - flask run
  
- Запуск проекта в docker:
    - docker build -t cutlinks .
    - docker run --rm -t -i -p 5000:5000 cutlinks
- Пушить можно только в свою ветку а потом pull request мне (artemsteshenko или Roma646)
