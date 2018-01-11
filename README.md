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

For setting static files, we can set STATIC_ROOT constant in project settings and then apply following command.

    `python manage.py collectstatic`

This will copy all static files from the apps and move them into `../static/` directory.

If we want to run staging server tests, we can use 
`STAGING_SERVER=domain.edu python manage.py test functional_tests`

## Deployment on Server

Sign up for a server on DigitalOcean.

Use `ssh-keygen` to generate ssh key. It will be stored at `~/.ssh/id_rsa.pub`.

Find more information [here](https://www.digitalocean.com/community/tutorials/how-to-use-ssh-keys-with-digitalocean-droplets)

- Create New Droplet

- Add SSH Key and then click **Create**

It will create a new droplet with ubuntu.

If you have used passphrase at the time of creating ssh key. You will need to use it to login as a password.

Find the IP address of the droplet and use following command to connect to the droplet.

`ssh root@your-server-ip-address-here`

Now, it will ask for password, you can give your passphrase that you gave while creating ssh key.

Create non-root user

```shell
useradd -m -s /bin/bash piyushpatel2005 # add user named piyushpatel2005 
# -m creates a home folder, -s sets piyushpatel2005 to use bash by default
usermod -a -G sudo piyushpatel2005 # add piyushpatel2005 to the sudoers group
passwd piyushpatel2005 # set password for piyushpatel2005
su - piyushpatel2005 # switch-user to being piyushpatel2005!
```

**Add public key to non-root user**

Copy your SSH public key to clipboard.

```shell
mkdir -p ~/.ssh echo 'PASTE PUBLIC KEY' >> ~/.ssh/authorized_keys
```

Verify new user setup

`ssh piyushpatel2005@server-ip-address`

Verify sudo privileges

`sudo echo hi`

### Sign in to your server

Now, install nginx:

`sudo apt-get install nginx`

Set up nameserver on your Domain Name registrar to 

`
ns1.digitalocean.com
ns2.digitalocean.com
ns3.digitalocean.com
`

- On DigitalOcean go to Networking and create your DNS record, additionally create hostname `staging` and `live`. This will direct to `live.example.com` and `staging.example.com`

Now, open your registered url, you should see, nginx welcome page.

Install python 3.6 on server.   

```shell
sudo add-apt-repository ppa:jonathonf/python-3.6
sudo apt-get update
sudo apt-get install python3.6 python3.6-venv
sudo apt-get install git
```

I have registered `piyushpatel.tk` and `staging.piyushpatel.tk` for testing.

If everything is configured correctly, Now run from your local console:

`STAGING_SERVER=staging.piyushpatel.tk python manage.py test functional_tests`


### Set up your site to run as non-root user (piyushpatel2005)

The folder structure would be like sites/sitename under your non-root username on the server. Inside this one, create database, source, static directories for one site. `source` contains the source files of the project. For this set up change the database location in the project `settings.py` file and type these commands.

```shell
mkdir ../database
python manage.py migrate --noinput

ls ../database/ # should have db.sqlite3 in there.
```