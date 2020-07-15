# A Company's Simple Flask App

Having a website for businesses is a must now a days. A website allows a company to present itself to the world, to show its products and services, to contact new clients and keep up with the environment evolution. But it is not possible for every company to deploy and maintain its own website, most of the time because the budget does not allow it. Also, in some cases people underestimate the benefits that a website brings to the business, for that reason they prefer invest money in things that are needed more urgently.

This project pretends to bring a solution to these businesses that struggle with its budget, giving an option to deploy a flask app for free. 

This is a guide to deploy a **Flask application** and will cover the following:
    
    * VM setup on Google Cloud (Compute Engine).
    * Flask app layout.
    * uWSGI configuration.
    * Nginx configuration.
    * Domain Name configuration.
    * Create SSL certificate.

The Github repository is https://github.com/Jonathpc/company-flaskapp.git

## VM setup

### Create a project on Google Cloud
You can login to Google cloud with your google account, if it is your first time, Google will give you 300 USD in credits to use their services for one year or until you spend the credits.

1. In the Cloud Console, on the project selector page, select or create a Cloud project.

### Create a VM Instance (Linux)

1. Go to VM Instances under Compute Engine and create an instance.
2. Name the instance.
3. Select Region and Zone according your preferences.
4. In Machine configuration select General-purpose > Series > N1 and Machine type > f1-micro (1 vCPU).
5. In Boot disk select the OS you prefer, this guide use **Ubuntu 18.04 LTS**
6. In Firewall select Allow HTTP/HTTPS traffic.
7. Click Create to create the instance.

Allow a short time for the instance to start. After the instance is ready, it is listed on the VM instances page with a green status icon. Then you can connect to your vm, in the list of virtual machine instances, click SSH in the row of the instance.

You should assign an static IP to VM instance. Go to VPC network > External IP address and reserve the IP for you VM.

### Update the VM

```bash
sudo apt update -y;sudo apt upgrade -y
```

### Creating a SWAP file (Optional)
Swap is a space on a disk that is used when the amount of physical RAM memory is full. With this instance we have little memory ram.

```bash
sudo fallocate -l 1G /swapfile  
sudo dd if=/dev/zero of=/swapfile bs=1024 count=1048576  
sudo chmod 600 /swapfile  
sudo mkswap /swapfile  
sudo swapon /swapfile  
sudo nano /etc/fstab
```
```bash
/swapfile swap swap defaults 0 0
```

### Installing Python
First, we are going to use `pyenv` to manage our Pyhton installation.

```bash
git clone https://github.com/pyenv/pyenv.git ~/.pyenv
```
Then we need to add some lines to `.bashrc` and reload the shell

```bash
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
echo -e 'if command -v pyenv 1>/dev/null 2>&1; then\n  eval "$(pyenv init -)"\nfi' >> ~/.bashrc
exec "$SHELL"
```
And finally install Pyhton, the Pyhton version used in this guide is Pythpn 3.7.2

```bash
sudo apt-get update; sudo apt-get install -y make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev

pyenv install 3.7.2
pyenv global 3.7.2
```
Now you should be able to start python interpreter.

### Firewall configuration
There are some ports that we are going to need in order the app to work

Shell connection
```bash
sudo ufw allow 22/tcp
```
Gmail TLS ports
```bash
sudo ufw allow 587
sudo ufw allow 465
```
Activate the firewall and check its status
```bash
sudo ufw allow status
```
## Flask app layout
The following is ours Flask app layout. You can check [Project Layout](https://flask.palletsprojects.com/en/1.1.x/tutorial/layout/) for more information.

```bash
app
├── app
│   ├── __init__.py
│   ├── templates
│   │   └── public
│   │       ├── layout.html
│   │       ├── index.html
│   │       └── contact.html
│   ├── static
│   │   ├── css
│   │   ├── public
│   │   ├── js
│   │   └── img
│   ├── forms.py
│   └── main.py
├── app.ini
├── config.py
├── readme.md
├── requirements.txt
└── run.py
```
We are going to clone the repo, make sure you are in home directory

```bash
git clone https://github.com/Jonathpc/flaskapp.git
```
We need to rename the parent folder to app

```bash
mv flaskapp/ app
```
Now we are going to create a vitual environment inside the app folder

```bash
cd ~/app
python -m venv env
source env/bin/activate
```
And install the Python dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```
## uWSGI configuration
uWSGI is both a protocol and an application server, that is going to serve our app. You can check [Flask app deployment](https://flask.palletsprojects.com/en/1.0.x/deploying/uwsgi/) for more information.

`run.py` is a entry point file for uWSGI to handle the app.

```python
from app import app

if __name__ == "__main__":
    app.run()
```
`app.ini` is uWSGI configuration file. You can check [uWSGI config file](https://uwsgi-docs.readthedocs.io/en/latest/Configuration.html) for more information.

```bash
[uwsgi]
module = run:app
master = true

processes = 4
threads = 2

socket = app.sock
chmod-socket = 660
vacuum = true
die-on-term = true
```

### Create a systemd unit file
Create a systemd unit file allows system init Ubuntu to start automatically uWSGI.

first we create the file
```bash
sudo nano /etc/systemd/system/app.service
```
And copy the following. You should use <yourusername>

```bash
[Unit]
Description=A Company simple Flask uWSGI application
After=network.target

[Service]
User=<yourusername>
Group=www-data
WorkingDirectory=/home/<yourusername>/app
Environment="PATH=/home/<yourusername>/app/env/bin"
ExecStart=/home/<yourusername>/app/env/bin/uwsgi --ini app.ini

[Install]
WantedBy=multi-user.target
```
Save and close it. Start uWSGI service and enable it
```bash
sudo systemctl start app
sudo systemctl enable app
```
Check its status
```bash
sudo systemctl status app
```
You should see 
```bash
● app.service - A Company simple Flask uWSGI application
   Loaded: loaded (/etc/systemd/system/app.service; enabled; vendor preset: enabled)
   Active: active (running) since Tue 2020-07-14 19:31:30 UTC; 3h 24min ago
 Main PID: 11809 (uwsgi)
    Tasks: 9 (limit: 1967)
   CGroup: /system.slice/app.service
           ├─11809 /home/<yourusername>/app/env/bin/uwsgi --ini app.ini
           ├─11826 /home/<yourusername>/app/env/bin/uwsgi --ini app.ini
           ├─11830 /home/<yourusername>/app/env/bin/uwsgi --ini app.ini
           ├─11831 /home/<yourusername>/app/env/bin/uwsgi --ini app.ini
           └─11833 /home/<yourusername>/app/env/bin/uwsgi --ini app.ini
```
## Nginx configuration
We are going to use Nginx to handle incoming HTTP/HTTPS requests.

### Install Nginx
```bash
sudo apt install nginx
```
### Firewall config
```bash
sudo ufw allow 'Nginx HTTP'
sudo ufw allow 'Nginx HTTPS'
```
### Config Proxy Requests
We are going to configure Nginx to send web request to our uWSGI socket using `uwsgi` protocol.

We need to create a new server block in Nginx's sites-available.
```bash
sudo nano /etc/nginx/sites-available/app
```
And copy the following. You should use <yourusername> and your domain
```bash
server {
    listen 80;
    server_name your_domain www.your_domain;

    location / {
        include uwsgi_params;
        uwsgi_pass unix:/home/<username>/app/app.sock;
    }
}
```

We need to link the server block we've just created in sites-available to sites-enabled
```bash
sudo ln -s /etc/nginx/sites-available/app /etc/nginx/sites-enabled
```

Check for syntax problems
```bash
sudo nginx -t
```
If it is ok restart Nginx service
```bash
sudo systemctl restart nginx
```
## Domain Name configuration
In Google Cloud Platform, go to Network services > Cloud DNS > Create Zone. Here assign a **Zone Name** and a **DNS name** and create.
Then enter to your DNS Zone and **ADD RECORD SET**. Add to records
 ```bash
DNS Name -> your_domain.com; Resource record type -> A; IPv4 Address -> VM External IP address (Static)
DNS Name -> WWW.your_domain.com; Resource record type -> CNAME; Canonical name -> your_domain.com
```
After your create the records, up in the right corner you will find **Register Setup** copy the information under Data, go to you register and configure your domain to point to these addresses.

## Create SSL certificate
We are going to obtain a SSL certify for our domain. We will use a free certify from [Let’s Encrypt](https://letsencrypt.org/).

Add Cerbot repo
```bash
sudo add-apt-repository ppa:certbot/certbot
```
Select ENTER to accept.

Install Cerbot for Nginx
```bash
sudo apt install python-certbot-nginx
```
Select your domain to use the certify
```bash
sudo certbot --nginx -d your_domain -d www.your_domain
```
Cerbot will ask how to handle HTTPS request, select an option.

Now you should be able to access to your app.

## License
[MIT](https://choosealicense.com/licenses/mit/)
