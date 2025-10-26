# ❓ QUIZ BOT

The site allows order or come to our restaurant and eat special food. Foods are unique you cant find this in another restaurant.

---

## 📌 Main features

* ✅ User registration and authorization
* ✅ Unique login
* ✅ Quizs
* ✅ Score
* ✅ Filters
* ✅ Admin Panel

---

## ⚙️ Environment variables

The project uses the ``environs`` library and reads settings from the ``.env`` file, which must be located in the root of the project.

Пример файла .env:
```
SECRET_KEY=your_secret_key
ALLOWED_HOSTS = [hosts]
DEBUG = True or False
TG_TOKEN=bot_token
```

### Variables used:

| Variable      | Purpose                                                                               |
|---------------|---------------------------------------------------------------------------------------|
| SECRET_KEY    | Flask Secret Key                                                                      |
| ALLOWED_HOSTS | It ensures your Django app only responds to requests from trusted domains. "*" is all |
| DEBUG         | Controls whether the app is in development or production mode                         |
| TG_TOKEN      | Connect to bot                                                                        |

---

## 🐍 Virtual environment (venv)

It is recommended to use ``venv`` to isolate project dependencies.

### Creating an Environment:
```bash
python -m venv venv
```
### Activation:

* Windows:

```bash
source venv\Scripts\activate
```

* Mac/Linux:

```bash
source venv/bin/activate
```

---

## 🚀 Project launch

1. Clone the repository:


```bash
git clone https://github.com/kerem212012/Game_Anime_Bot.git
cd Game_Anime_Bot
```

2. Create and activate a virtual environment (see above)

3. Install dependencies:


```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root of the project and specify the variables (`SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`,`TG_TOKEN`)

5. Migrate project and create superuser:


```bash
python manage.py makemigration
python manage.py migrate
python manage.py createsuperuser
```

6. Start the server:


```bash
python manage.py runserver
```

7. Go to the browser:

[http://127.0.0.1:8000](http://127.0.0.1:8000)

---


## 🎯 Project goal

The Bot was created for money making(fake)

## 📲 Deploying to internet

### 💳 Buy site

You need buy site from services I prefer [TimeWeb Cloud](https://timeweb.cloud/?utm_source=vh76046&utm_medium=timeweb&utm_campaign=timeweb-bring-a-friend)

### 🚶‍➡️ Enter to your site
You need [git bash](https://git-scm.com/downloads),
open git bash and print ```ssh 'your ip'``` then he asks yes or no say yes.
Then give him password of site.
After enter write ```reboot```.
Open ```.ssh``` file open file ```config``` in notebook.
And write:
```
Host 'name'
    HostName 'your ip'
    User root
```
Now you can enter your server like ```ssh 'name'```.
### 📑 Copying project
In your site(in git bash) you need come to ```opt``` file. For this you need do:
```bash
cd ..
cd opt/
```
After it, you need copy project. Example:
```bash
git clone https://github.com/kerem212012/Game_Anime_Bot.git
```
### 👹 Add Daemon

Install gunicorn to do it enter to your project in bash from ```opt``` add venv:
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
Now installing gunicorn:
```bash
apt update
pip install gunicorn
```
Now to add daemon we need go to ```system``` file:
```bash
cd ..
cd ..
cd /etc/systemd/system
```
We need add file we can do it with ````nano````:
```bash
nano name_tg.service
```
In this file add:
```
[Unit]
After=network.target name_django.service

[Service]
WorkingDirectory=/opt/Game_Anime_Bot
Environment="PATH=/opt/Game_Anime_Bot/venv/bin"
ExecStart=/opt/Game_Anime_Bot/venv/bin/python /opt/Game_Anime_Bot/quiz/bot.py
Restart=always
RestartSec=5
[Install]
WantedBy=multi-user.target
```
Then add this file:
```
[Unit]
After=network.target

[Service]
WorkingDirectory=/opt/Game_Anime_Bot
Environment="PATH=/opt/Game_Anime_Bot/venv/bin"
ExecStart=/opt/Game_Anime_Bot/venv/bin/python /opt/Game_Anime_Bot/manage.py runserver 127.0.0.1:8080
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target

```

Then lets start it:
```bash
systemctl daemon-reload
systemctl enable name_django.service
systemctl enable name_tg.service
systemctl start name_django.service
systemctl start name_tg.service
```

## SUBSCRIBE
[Chipsinka](https://www.youtube.com/channel/UC8WEUnlETWORTIWI4jb339A)
