### INF601 - Advanced Programming in Python
### Sergio Gabriel Jiawei Kun
### Final_project

## Description
Prototype Openweather API DJango web application. Currently contains a working forecast dashboard for temperature and humidity in the searched city or location in metric measurements. In the future there will be imperial units options and map oriented dashboards.
## Getting Started

### pip install instructions
Ensure that the following lines are run for the program to function.
This pip installs all the required packages listed in the requirements.txt file.
```python
pip install -r requirements.txt
```

### Dependencies

* This version was developed using Python 3.11, and will run best in this version.

### Installing
* Python 3.11

### Executing program
Run the following in the bash terminal
```
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser (this will create the administrator login for your /admin side of your project)

python manage.py runserver (This brings your web application up)
```
Once running, you should be able to see the web application run in:
http://127.0.0.1:8000/
or
http://127.0.0.1:8000/main/
* If there is an error, please refer to the above required packages in order for the program to run smoothly.

## Help

## Authors

Contributors names and contact info
* Sergio Gabriel Jiawei Kun
  * kunsergio117@outlook.com

## Version History
* 0.1
    * Initial Release

## License
* No licencing
## Acknowledgments
* [DJango app tutorial](https://docs.djangoproject.com/en/4.2/intro/tutorial08/)
* [OpenweatherAPI](https://openweathermap.org/api/one-call-3#current)
