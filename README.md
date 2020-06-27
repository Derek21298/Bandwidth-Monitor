# Bandwidth Monitor

The bandwidth monitor is meant to inform the user of their computers network usage.  Simple statistics will be gathered such as bytes sent, bytes received, upload speed, download speed, ping, etc.  These statistics will be gathered once a minute to give the user an idea of how the network behaves throughout a day.

(time frequency variable to change)

## Requirements

Use the package manager pip to install psutil if not already installed

```bash
pip install psutil
```

To use the internet speedtest, setup the speedtest CLI

```bash
git clone https://github.com/sivel/speedtest-cli.git
cd speedtest-cli
python setup.py install
```

## Usage

Use python3 to use bandwidth monitor and python 2.7 to use internet speedtest.

## Contributing

The end goal of this project would be to have a nice web interface to diplay all the results.  Any experience web development would be nice :)
