<div align="center" style="padding-bottom: 10px">
    <h1>DoNotExpire</h1>
    <img alt="Python" src="https://img.shields.io/badge/python%20-%2314354C.svg?&style=for-the-badge&logo=python&logoColor=white"/>
    <img alt="Django" src="https://img.shields.io/badge/django%20-%23092E20.svg?&style=for-the-badge&logo=django&logoColor=white"/>
    <img alt="HTML" src="https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white">
    <img alt="CSS" src="https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white">
    <img alt="JavaScript" src="https://img.shields.io/badge/javascript%20-%23323330.svg?&style=for-the-badge&logo=javascript&logoColor=%23F7DF1E"/>
    <img alt="Heroku" src="https://img.shields.io/badge/Heroku-430098?style=for-the-badge&logo=heroku&logoColor=white">
</div>

<div align="center">
    <p>DoNotExpire is a website that makes keeping your Diablo 2 accounts safe from expiring much easier.</p>
    <p>Built with Django framework, HTML, CSS, vanilla Javascript and a bit of JQuery.</p>
</div>

# Overview:

Multiplayer Diablo II characters expire if they are inactive for too long. Expired characters cannot be recovered. Single Player characters do not expire.

**Newly created characters will expire after 10 days of inactivity. Characters played for two hours or more will expire after 90 days of inactivity.** To reset the inactivity timer on a character, you need to log in to an active game with that character and buy or sell an item, or kill a monster.

Diablo II **accounts are also deleted after 90 days of inactivity.**

Thanks to DoNotExpire you can keep track of all your accounts. Log in and add your accounts, which hold up to 16 characters, to the database.  
Whenever you log into your Diablo 2 account, open the website and press the button next to the character you have just 'permed' ingame. The expiration date for this character will refresh on the website and you will be able to manually follow those dates.  
Should you not perm your character and update the info on website, you will be sent an email with a notification to do so.

If you keep forgetting to sync your Diablo 2 accounts state with website data, create a simple script to open both your browser with this website and Diablo 2 game instance at the same time. This way you will most likely remember to update the dates.

## Installation (dev)

git clone https://github.com/Alschn/CoreRepetition.git

Set **SECRET_KEY** enviromental variable

    py -3 -m venv venv

    venv\Scripts\activate

    pip install -r requirements.txt

    python manage.py makemigrations

    python manage.py migrate

    python manage.py createsuperuser

    python manage.py runserver
