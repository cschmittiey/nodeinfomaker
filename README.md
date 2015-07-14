#nodeinfomaker
Tries to autogenerate a bit of nodeinfo.json to get you started. Based off of @thefinn93's cjdnsadminmaker.py

##Instructions

Before running this script, edit the variables at the top of your script to properly reflect where your cjdroute binary and related config are. 

You can also pass a location as an argument to have nodeinfo.json placed elsewhere.

##End Result

You should end up with something that looks a bit like this.
```json
{
    "hostname": "localhost.localdomain",
    "contact": {
        "name": "Your Name",
        "email": "you@you.you"
    },
    "addr": "this will be your cjdns IP",
    "key": "not my publick key.k",
    "last_modified": "2015-07-14T22:57:51.013013"
}
```
