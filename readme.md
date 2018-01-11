#Notifier_OTRS_package

This package gets info about the Tickets from the OTRS and send it to the Telegram_bot_Server

You can find the docs about Telegram_bot_Server and Notifier_Zabbix_package on the https://github.com/Alexander35/Telegram_bot_Server.git package page.

You can work with this package like with Notifier_Zabbix_package.

Previously, You should have installed and running Telegram_bot_Server.

# 1. Install this package

```
git clone https://github.com/Alexander35/Notitfier_OTRS_package.git
```
```
pip install python-otrs
```
```
pip install git+https://github.com/Alexander35/general_server_client.git
```
```
pip install git+https://github.com/Alexander35/protobuf_asset.git
```
```
pip install protobuf
```


# 2. Configure

```
mv .config.ini config.ini
```

Edit the config file: 
Url param - URL of your otrs server without /otrs/
Webservice - the web service in otrs server
I recommend you read the official docs (we use the SOAP)
http://doc.otrs.com/doc/manual/admin/6.0/en/html/genericinterface.html


# 3. Work
move it into any scheduler and run with params:

get a help message:

```
python otrs_notifier.py
```

get all tickets with status new

```
python otrs_notifier.py --state_type new
``` 

get all tickets with status open from few queues:

``` 
 python otrs_notifier.py --state_type new --queues "first queue" --queue NewGueue --queue "Supa dupa Queue"
```

Enjoy!

for any quastions, please send me a E-mail : alexander.ivanov.35(AT).gmail.com 