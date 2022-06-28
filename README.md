## Setup
To use the script, first install the unofficial coinbase pro python client
- You may manually install the project or use ```pip```:
```python
pip install cbpro
#or
pip install git+git://github.com/danpaquin/coinbasepro-python.git
```

## API Keys **change before using**
edit the API key values in DCA_script.py according to the values at https://pro.coinbase.com/profile/api

## Using the script
Before running the script for the first time, edit your daily buys as you see fit using valid trading pairs (i.e. 'BTC-USD').

Then simply run DCA_script with python while in the project directory
```python
python3 ./DCA_script.py
```


