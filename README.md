# Mortfors bus

Dummy-app where customers can book bus trips from a company called Mortfors bus.

## The app

Written in Python using Flask.

## Installations

The app uses the following dependencies which has to be installed:

### Install Python 3.7 to your computer
Python 3.7 is the language that the server is written in. Follow the instructions at https://www.python.org/downloads/ and install Python version 3.7 to your computer.

**Then create a project folder and cd into it:**

```
$ mkdir <project-name>
$ cd <project-name>
```

### Virtual environment
It's a good idea to create a virtual environment where all dependencies for the project are installed. By doing this dependencies for different projects won't interfere with each other.

**Ubuntu Linux**

If you are using Ubuntu Linux you will first have to install the virtual environment module before you can create one:

```
$ sudo apt-get install python3-venv
```

Then create a virtual environment in the project folder that you created earlier:

**Mac & Linux:**
```
$ python3 -m venv <venv-name>
```

**Windows:**
```
$ py -3 -m venv <venv-name>
```

Now activate the virtual environment with the following command:

**Mac & Linux:**
```
$ . venv/bin/activate
```

**Windows:**
```
$ venv\Scripts\activate
```

When the virtual environment is activate its name will be visible to the far left in the search path in the terminal / command prompt.

### Install Flask
The Python framework Flask is used to build the web server. Install Flask within the virtual environment. The virtual environment must be activated.
Install the Flask framework with the following command:

```
$ pip install flask
```

### Psycopg2

Psycopg2 is the PostgreSQL adapter that the Python server uses to talk to a PostgreSQL database server. Install it with the following command:

```
$ pip install psycopg2
```

### Flask-bcrypt

Flask-bcrypt is used to encrypt passwords stored in the database. Install flask-bcrypt with the following command:

```
$ pip install flask-bcrypt
```

### Flask-WTF

 Install Flask-WTF with the following command:

```
$ pip install flask-wtf
```

### WTForms

WTForms is used to create classes for the forms that are used to get user input. It is also used to get different kinds of input fields and validators for those fields. Install WTForms with the following command:

```
pip install wtforms
```
