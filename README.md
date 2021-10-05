# sandcatbot

## setup

```
pip3 install --user -r requirements.txt
cp sandcatbot.example.conf sandcatbot.conf
vim sandcatbot.conf
```

## running

the first parameter is where to find the config file. the second parameter is
a file used to track how many times the bot has been called. treat as an
opaque state file.

```
python3 -m sandcatbot sandcatbot.conf ~/.catstate
```
