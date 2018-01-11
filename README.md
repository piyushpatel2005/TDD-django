# Django - Test Driven Development

Install Mozilla Firefox and geckodriver

- Download geckodriver-linux64.tar.gz

- Extract the file with
`tar -zxvf geckodriver*`

- Make it executable
`chmod +x geckodriver`

- Move it to PATH location
`sudo mv geckodriver /usr/local/bin`

`geckodriver --version`

### Set up Python Development Environment

`pip install virtualenv`

Create virtualenv named `superlists`.

`virtualenv --python=python3 superlists`

Activate virtualenv using:

`source superlists/bin/activate`

Here, you will have a separate python version as we specified when creating virtualenv.

`python --version`

To deactivate virtualenv type:

`deactivate`

This tutorial uses Django 1.11 and Selenium 3.

Let's install them. Start virtualenv and then type:

`pip install "django<1.12" "selenium<4"`

Go to convenient location and start the project using:

`django-admin.py startproject superlists`

Now, in Django, projects are divided into apps and to create it, go inside superlists directory and find `manage.py` script.

Then, run: `python manage.py startapp lists`. It will create `lists` directory with different files. This is general structure of app. Here, `tests.py` will automatically run.

To run tests, use `manage.py` again. 

`python manage.py test` will run all tests.

To start the app, use `python manage.py runserver`.

Now, tests are written on classes inheriting from TestCase class from Django. For those tests where you do not want to interfere the production database, we can use LiveServerTestCase class. This is run using `manage.py` script.

To run only unit tests for *lists*, use:

`python manage.py test lists`

We can upgrade installed modules using:

`pip install --upgrade selenium`

To setup a relationship between two models, we can use foreign key constraint. This way one model can contain another model. For reverse lookup, we can use `item_set.all` to retrieve all items from a list.