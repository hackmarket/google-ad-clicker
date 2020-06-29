# Google Ad Clicker

Python script that auto clicks the first ad presented from google keyword search. Using a custom firefox gecko binary browser, tor for random ip nodes, and selenium for random mouse movement + clicks.

### Setup

requires Python3 and firefox v.77 to run.


```sh
$ brew install tor
$ cp torrc /usr/local/etc/tor/torrc 
or ubuntu
$ sudo apt install tor
$ cp torrc /etc/tor/torrc

$ python3 -m venv env
$ source env/bin/activate
$ pip install -r requirements.txt
$ python script.py
enter search keyword
```

### Discovery
 - google tracks click ip for 24 hours to analyze any malicious activity ~ if found will de monotize click
 - google is likely to report ip if query seach is not first hit from google's homepage or if the device has not first connected to a google service


### Disclaimer

This project is for educational and research purposes only. Any actions and/or activities related to the material contained on this GitHub Repository is solely your responsibility.

