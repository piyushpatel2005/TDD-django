# Deploy on Server

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

**On server console** use these commands:

```shell
export SITENAME=staging.piyushpatel.tk
echo $SITENAME # staging.piyushpatel.tk
mkdir -p ~/sites/$SITENAME/database
mkdir -p ~/sites/$SITENAME/static
mkdir -p ~/sites/$SITENAME/virtualenv
git clone https://github.com/piyushpatel2005/TDD-django.git ~/sites/$SITENAME/source
```

Now, this $SITENAME is available only for this console session, so the next time you start the session, make sure to redfine this sessoin if you want to use it.

To setup `virtualenv` on server, we'll copy our local setup to `requirements.txt` file.

```shell
echo "django==1.11" > requirements.txt
```

We can also create separate file for test-requirements.txt including test dependencies.

On **server** use, git pull in the source directory to pull down `requirements.txt` file. From the *source* directory, type following command to create `virtualenv`.

```shell
python3.6 -m venv ../virtualenv
ls ../virtualenv/bin
../virtualenv/bin/pip install -r requirements.txt
../virtualenv/bin/python manage.py runserver
```

Depending on your firewall settings, you can visit `http://staging.piyushpatel.tk:8000`.

### Nginx server configuration (Not recommended for production)

Minimal server configuration for nginx

`
server {
    listen 80;
    server_name staging.piyushpatel.tk;

    location / {
        proxy_pass http://localhost:8000;
    }
}
`

Create a file at `/etc/nginx/sites-available/` named `staging.piyushpatel.tk` and paste the above configuration in there and save. You might need to use `sudo` for this operation.

Now make sure $SITENAME exists in this session.

```shell
echo $SITENAME
sudo ln -s ../sites-available/$SITENAME /etc/nginx/sites-enabled/$SITENAME  # symbolic link
sudo rm /etc/nginx/sites-enabled/default  # remove default nginx welcome page

# Now reload the nginx
sudo systemctl reload nginx
../virtualenv/bin/python manage.py runserver
```

Now, you can visit `http://staging.piyushpatel.tk` without specific port number. Sometimes, it is required to change /etc/nginx/nginx.conf` file and uncomment `server_names_hash_bucket_size 64;` to get long domain names to work.

To test nginx configuration, we can use `nginx -t` command which will test configuration and warn us if something is wrong.

Now if we run the tests from local server, 

`STAGING_SERVER=staging.piyushpatel.tk python manage.py test funct
ional_tests`

it throws errors. Make migrations on server and then try the same tests again.

## Gunicorn settings for production

```shell
../virtualenv/bin/pip install gunicorn

# give path to WSGI server
../virtualenv/bin/gunicorn superlists.wsgi:application
```

Gunicorn doesn't serve static files magically. We need to configure nginx to do that.

```shell
../virtualenv/bin/python manage.py collectstatic --noinput
ls ../static
```

Now configure nginx to server static files from this location.

```javascript
server {
    listen 80;
    server_name staging.piyushpatel.tk;

    location /static {
        alias /home/piyushpatel/sites/superlists-staging.piyushpatel.tk/static;
    }

    location / {
        proxy_pass http://localhost:8000;
    }
}
```

Reload nginx and restart gunicorn:

```shell
sudo systemctl reload nginx
../virtualenv/bin/gunicorn superlists.wsgi:application
```

We cannot run multiple sites on the same port `live` and `staging`. So, we use socket from unix systems. To store sockets at /tmp/ directory use following settings in nginx configuration.

```
... ... 
location / {
    proxy_set_header Host $host;
    proxy_pass http://unix:/tmp/staging.piyushpatel.tk.socket;
}
...
```

Now, reload the nginx server and gunicorn

```shell
sudo systemctl reload nginx
../virtualenv/bin/gunicorn --bind unix:/tmp/staging.piyushpatel.tk.socket superlists.wsgi:application
```

Change these settings in `superlists/settings.py` file on server.

```python
...
DEBUG = False
TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = ['staging.piyushpatel.tk']
...
```

Now, the website is working again.

### Make Gunicorn autostart on Reboot

Create this file in `/etc/systemd/system/gunicorn-staging.piyushpatel.tk.service`. Systemd scripts live in `/etc/systemd/system` directory and their names end with `.service`

You might need to change permission for this file.

```
Description=Gunicorn server for staging.piyushpatel.tk

[Service]
Restart=on-failure
User=piyushpatel2005
WorkingDirectory=/home/piyushpatel2005/sites/staging.piyushpatel.tk/source
ExecStart=/home/piyushpatel2005/sites/staging.piyushpatel.tk/virtualenv/bin/gunicorn \
--bind unix:/tmp/staging.piyushpatel.tk.socket superlists.wsgi:application

[Install]
WantedBy=multi-user.target 
```

Now, we need to inform systemd to start Gunicorn:

```shell
sudo systemctl daemon-reload # load new config file
systemctl status gunicorn-staging.piyushpatel.tk.service # check status
sudo systemctl enable gunicorn-staging.piyushpatel.tk # load our service on boot
sudo systemctl start gunicorn-staging.piyushpatel.tk # start our service
```

Check systemd logs for this service using `sudo journalctl -u gunicorn-staging.piyushpatel.tk`

If you change systemd config file, make sure use `systemctl daemon-reload` and then `systemctl restart`

