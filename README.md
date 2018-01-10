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


