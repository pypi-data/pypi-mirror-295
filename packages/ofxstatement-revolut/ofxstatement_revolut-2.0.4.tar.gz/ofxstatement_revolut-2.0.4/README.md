# ofxstatement-revolut

![badge](https://github.com/mlaitinen/ofxstatement-revolut/actions/workflows/build-and-publish.yml/badge.svg)


This is a plugin for [ofxstatement](https://github.com/kedder/ofxstatement). It implements
a parser for the Revolut CSV-formatted bank statement.

Issue reports and pull requests are welcome.

## Installation

### From PyPI repositories
```
pip3 install ofxstatement-revolut
```

### From source
```
git clone https://github.com/mlaitinen/ofxstatement-revolut.git
python3 setup.py install
```

## Configuration options

| Option        | Description                                                                                                                                               |
|---------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------|
| `account`     | Define the account of this bank statement                                                                                                                 |
| `currency`    | The base currency of the account                                                                                                                          |
| `date_format` | The date format in the bank statement. Note that you have to use double `%`-marks in the settings file like this: `date_format = %%Y-%%m-%%d %%H:%%M:%%S` |
