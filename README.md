# blocket-watcher

Fetches search results from blocket.se and sends out a SMS when it finds new objects.

## Setup

- Install the pip dependencies from ``requirements.txt`` (``pip3 install -r requirements.txt``)
- Copy config.py.sample to config.py and add your 46elks credentials and phone number
- Add the search links you are interested in in the list
- You probably want to uncomment the "dryrun" line in send_sms the first time you run the script, otherwise you will get a SMS for each of the current blocket ads in the search.
- run ``python3 blocket-watcher.py``

I suggest you set it up with cron or similar to run at regular intervals.

More information on how it works can be found [here](https://alge.se/blocket-notifier.html).
