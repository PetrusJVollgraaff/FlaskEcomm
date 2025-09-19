# Flask Ecommerce
Using Python Flask to create an Online Shopping site


create and start Virtual Enviroment

```
python -m venv env

env\Scripts\activate

```

install dependencies

```
    pip install -r requirements.txt
```

first setup database

```
flask db init
flask db migrate -m '<Name>'
flask db upgrade
```

run application

```
python app.py

```
