# RPi CPU Temperature Monitoring & Fan Control (Web Hosted)

This repository contains Python scripts for monitoring CPU temperature and displaying the data on a web server
using the Bokeh library.

## Requirements

- Python 3.x
- Bokeh library (`pip install bokeh`)
- gpiozero library (`pip install gpiozero`)
- pytz library (`pip install pytz`)

## File Descriptions

- `temp.py`: This script monitors the CPU temperature and creates a real-time line chart using Bokeh to display
the temperature over time. The chart is saved to an HTML file named `cpu_temp.html`. The script also saves the
temperature data to a file named `cpu_temp_data.txt` and loads any existing data from that file upon startup-
with a mximum of 24 hours worth of data. The maximum number of data points displayed on the chart is set to
show the last 30 minutes of data.

- `server.py`: This script sets up a basic HTTP server to serve the `cpu_temp.html` file which is embedded into
the `index.html` file. It listens on port 3002 and serves the requested files back to the client.

## Usage

1. Install the required Python libraries by running the following command:
```
pip install bokeh gpiozero pytz
```

2. Run the `start.sh` script to start `temp.py` & `server.py` in the background. 
```
bash start.sh
```

**OR**

2. Run the `temp.py` script to start monitoring the CPU temperature and generating the chart:
```
python temp.py
```

The script will continuously update the chart with the current CPU temperature. The chart is saved to
`cpu_temp.html`, and 24 hours worth of temperature data is saved to `cpu_temp_data.txt`.

3. In a separate terminal or web browser, run the `server.py` script to start the HTTP server:
`python server.py`

The server will start running and listening on port 3002. You can access the CPU temperature chart by
navigating to `http://localhost:3002` in your web browser.

4. To stop the scripts, press `Ctrl+C` in the terminal where they are running.

## Fan control (optional)
The fan code is directly from [Howchoo/pi-fan-controller](https://github.com/Howchoo/pi-fan-controller) repo.

```
sudo mv fancontrol.py /usr/local/bin/
````
```
sudo chmod +x /usr/local/bin/fancontrol.py
```
```
sudo mv fancontrol.sh /etc/init.d/
```
```
sudo chmod +x /etc/init.d/fancontrol.sh
```

Register the script to run on boot
```
sudo update-rc.d fancontrol.sh defaults
```

Start it or reboot
```
sudo /etc/init.d/fancontrol.sh start
```


**This README.md was also written by ChatGPT with some minor edits.**
