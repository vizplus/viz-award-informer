# vizplus-award-informer

Скрипт для определения и публикации значения показателя award on capital в блокчейне VIZ.

Каждые 6 часов аккаунт @award-on-capital с социальным капиталом 10000 viz награждает аккаунт @committee с энергией 5% и проверяет размер награды. Полученная награда нормируется на 1 viz и 100% энергии и публикуется в виде custom-записи.

На основе данного показателя можно вычислить условную эффективность социального капитала в VIZ за любой период. Например, годовой процент считается по формуле: (1+AOC)^73-1, где AOC - текущее значение award on capital.

### Installing:

    $ git clone https://github.com/vizplus/vizplus-award-informer
    $ cd vizplus-award-informer
    $ sudo apt-get install libffi-dev libssl-dev python-dev python3-dev python3-pip python3-venv
    $ pip3 install --upgrade requests
    $ python3 -m venv venv
    $ . venv/bin/activate
    $ pip install bitshares
    $ deactivate

### Using:

    $ cp settings.json.example settings.json
    
Edit login and key of the VIZ account in the settings.json file

Add crontab task

    $ * * * * * /path/to/vizplus-award-informer/venv/bin/python /path/to/vizplus-award-informer/award_informer.py
