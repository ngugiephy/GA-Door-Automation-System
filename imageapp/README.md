## Imageapp
#### This is a simple flask application to demonstrate image storage using the file system hand in hand with a database

Storing images directly in the database is a rather tricky approach as this will unnecessarily overload the database
It would thus make sense to utilise the server's file system to store the actual images and the database to store the image names
Images will then be sourced using their paths after obtaining their names from the database

Host providers such as [Linode](https://www.linode.com/) have a dedicated static folder to store static content such as images

To implement the above desired image storage we will make use of the python os library as well as the send_from_directory method in flask to serve files.
The os library will enable us obtain the root path of our module
We can then feed this path to our custom url endpoint that makes use of the send_from_directory method when we want to serve our images

* [send_from_directory documentation](https://flask.palletsprojects.com/en/2.1.x/api/)
* [os module](https://www.geeksforgeeks.org/os-module-python-examples/)


## Trying out the app
So, considering you want to try out the app on localhost you just have to clone it, install the requirements and run it
This mini tutorial will use commands on the git bash terminal

Clone it as follows on your desired working directory
```bash
$ git clone https://github.com/Donatussss/imageapp.git
```

Change directory into the imageapp directory
```bash
$ cd imageapp
```
Install requirements as follows. We will need to create a virtual environment where our packages will go and activate it in order to use it.
In this app I happen to use another package I created called [flask-dt](https://github.com/GreatDt1/flaskdt)
```bash
$ python -m venv venv
$ source venv/bin/activate
(venv)$ pip install -r requirements.txt
```
We need to initialize the db, i.e, create all the tables. There is a python file with this code already so we will just run it as a module
```bash
(venv)$ python -m myimageapp.esntls
```

Finally run the app as follows. Make sure the virtual environment is still activated.
```bash
(venv)$ python run.py
```


## Accessing the app
Currently the configuration of the app makes the server externally visible to devices connected to the same local network
If you wish to do this it is thus necessary to know the ip of the device you are running the app in
This can be obtained as follows
```bash
$ ipconfig
```
Take note of the IPv4 address of the Wireless LAN adapter
One can thus access the running app from another device on the same network using the following format
http://ip:5000/
e.g. http://172.20.10.1:5000/
