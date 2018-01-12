# Automatic Deployment

**fabric** is a tool to automate commands to be run on the server. On local machine install fab:

`pip install fabric3`

Usually, you need fabfile.py file which will contain functions that can later be invoked from command-line tool called fab. You can do something like this:

`fab function_name:host=SERVER_ADDRESS`

### Simple fabfile.py

```python
from fabric.contrib.files import append, exists, sed
from fabric.api import env, local, run
import random

REPO_URL = 'REPLACE WITH YOUR .git REPO'

def deploy():
    site_folder = f'/home/{env.user}/sites/{env.host}'
    source_folder = site_folder + '/source'
    _create_directory_structure_if_necessary(site_folder)
    _get_latest_source(source_folder)
    _update_settings(source_folder, env.host)
    _update_virtualenv(source_folder)
    _update_static_files(source_folder)
    _update_database(source_folder)
```

env.host : `live.piyushpatel.tk`
env.user : `USERNAME`

We use fabric command `run` to run shell commands on the server. Check complete [fabfile](fabfile.py).

- fabric `local` command is used to run commands on your local machine.

- fabric `sed` command does a string substitution in a file (change DEBUG=False from DEBUG=True)