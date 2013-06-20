killall python
#./manage.py runserver 0.0.0.0:8000
./manage.py runfcgi host=localhost port=8000 maxrequest=500 maxspare=1 minspare=1 maxchildren=1

