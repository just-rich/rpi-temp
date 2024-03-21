from gpiozero import CPUTemperature
from time import sleep, strftime, time
from bokeh.plotting import figure, output_file, save
from bokeh.models import Title, DatetimeTickFormatter, SingleIntervalTicker, Range1d
from bokeh.models import FixedTicker
import pytz
from datetime import datetime, timedelta
import os

cpu = CPUTemperature()

output_file("cpu_temp.html")

max_data_points = 1800  # maximum number of data points to display on the chart
x_range = Range1d(-10, max_data_points * 2)  # x-axis range

p = figure(
    title="CPU Temperature",
    x_axis_label='Time',
    y_axis_label='Temperature (Fahrenheit)',
    x_axis_type='datetime',
    y_axis_location='right',
    x_range=x_range,
    width=900,
    height=900
)
p.background_fill_color = '#000000'
p.border_fill_color = '#000000'
p.title.text_color = 'white'
p.title.background_fill_color = '#222222'
p.xaxis.axis_label_text_color = 'white'
p.xaxis.major_label_text_color = 'white'
p.yaxis.axis_label_text_color = 'white'
p.yaxis.major_label_text_color = 'white'
p.ygrid.minor_grid_line_color = None  # hide minor gridlines
p.xgrid.minor_grid_line_color = 'white'
p.title.align = 'center'
p.title.text_font_size = '20px'
p.add_layout(
    Title(text='Created by rich & ChatGPT', text_font_size='10pt', text_color='white'),
    'below'
)

x = []
y = []

formatter = DatetimeTickFormatter(
    seconds="%I:%M:%S %p", minutes="%I:%M %p", hours="%I:%M %p", days="%m/%d/%Y"
)
p.xaxis.formatter = formatter

ticker = FixedTicker(ticks=list(range(70, 200)))
p.yaxis.ticker = ticker
p.yaxis.major_tick_line_color = 'white'
p.yaxis.minor_tick_line_color = None

max_data_points = 1800  # set to display 30 minutes of data

# Set the desired timezone (Los Angeles Time Zone)
timezone = pytz.timezone('America/Los_Angeles')

# Load existing data from file
try:
    with open("cpu_temp_data.txt", "r") as file:
        for line in file:
            line = line.strip().split(",")
            if len(line) == 2:
                x.append(datetime.fromtimestamp(int(line[0]), timezone))
                y.append(float(line[1]))
except FileNotFoundError:
    pass

def graph(temp):
    now = datetime.now(timezone)
    x.append(now)
    y.append(temp)

    # Save the data to file
    with open("cpu_temp_data.txt", "a") as file:
        file.write(f"{int(now.timestamp())},{temp}\n")

    # Remove data points older than 24 hours from the file
    cutoff_time = now - timedelta(hours=24)
    with open("cpu_temp_data.txt", "r+") as file:
        lines = file.readlines()
        file.seek(0)
        for line in lines:
            timestamp_str, _ = line.strip().split(",")
            timestamp = datetime.fromtimestamp(int(timestamp_str), timezone)
            if timestamp > cutoff_time:
                file.write(line)
        file.truncate()

    # limit the number of data points displayed on the chart
    if len(x) > max_data_points:
        x.pop(0)
        y.pop(0)

    # update the chart range to show the most recent data points
    p.x_range.start = x[-1] - timedelta(seconds=max_data_points)
    p.x_range.end = x[-1] + timedelta(seconds=1000)

    p.line(x, y, line_color='red')
    save(p)

while True:
    temp = cpu.temperature * 1.8 + 32
    graph(temp)
    sleep(60)
