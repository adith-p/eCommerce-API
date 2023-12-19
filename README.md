# Ecommmerce API
First Clone the repository 
```
git clone git@github.com:adith-p/eCommerce-API.git
```
Create a virtualenv 
- 
* Win
  ```
  python3 -m venv venv
  ```
* Linux
  ```
  virtualenv venv
  ```
  Note: Activate the venv
  
Install the requirements
-
```
pip install -r requirements.txt
```
Run migrations
-
```
python manage.py migrate
```
Run server
-
```
python manage.py runserver
```
Note:
- goto: ```127.0.0.1:8000/api/v1/swagger/``` For documentation
- The debug mode is on
