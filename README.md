# **Find Available Slot in Google Calendar using Gemini**

<p align="center"> 🚀 This script is designed to get Google Calendar events, find gaps in a given time range using Gemini, and create a test event in that range if the user accepts  </p>

Execution Example

![execution example](docs/images/example1.png)

Event Created

![event created](docs/images/example2.png)

<h3>🏁 Table of Contents</h3>

<br>

===================

<!--ts-->

💻 [Dependencies and Environment](#dependenciesandenvironment)

☕ [Using](#using)

👷 [Author](#author)

<!--te-->

===================

<div id="dependenciesandenvironment"></div>

## 💻 **Dependencies and Environment**

Dependencies and versions

- Python 3.10.12

<div id="using"></div>

## ☕ **Using**

First, check the [dependencies](#dependenciesandenvironment) process

you will need to enable the google calendar api and get the credentials.json file, [look the doc](https://developers.google.com/workspace/calendar/api/quickstart/python?hl=pt-br)

this project uses the paid Google Gemini API, it's necessary to configure a valid Gemini API Key. Ensure you have a `.env` file with the environment variable **API_KEY**.

You can clean the environment using

```
$ make clean
```

to exec:

```
$ make run
```

Below are the arguments that can be used when running the script, with a brief explanation of each:

- `-s`, `--start`: Sets the start time to search for availability (default: **9:00 AM**).
- `-e`, `--end`: Sets the end time to search for availability (default: **6:00 PM**).
- `-d`, `--duration`: Duration of each event in minutes (default: **60**).
- `-n`, `--name`: Name of the event to be created (default: **"Event created by Gemini"**).
- `-id`, `--id`: Calendar ID where the event will be created (default: **"primary"**).
- `-w`, `--waiting`: Waiting time (in minutes) to look for available slots (default: **30**).
- `-i`, `--invites`: List of emails (comma-separated) to invite to the event (optional).

Example executing with all arguments:

```
$ make run ARGS="--start '8:00 AM' --end '6:00 PM' --duration '45' --name 'Reunião de Projeto' --id 'your_calendar_id@group.calendar.google.com' --waiting '15' --invites 'email1@example.com,email2@example.com'"
```

<div id="author"></div>

#### **👷 Author**

Made by Glener Pizzolato! 🙋

[![Linkedin Badge](https://img.shields.io/badge/-Glener-blue?style=flat-square&logo=Linkedin&logoColor=white&link=https://www.linkedin.com/in/glener-pizzolato/)](https://www.linkedin.com/in/glener-pizzolato-6319821b0/)
[![Gmail Badge](https://img.shields.io/badge/-glenerpizzolato@gmail.com-c14438?style=flat-square&logo=Gmail&logoColor=white&link=mailto:glenerpizzolato@gmail.com)](mailto:glenerpizzolato@gmail.com)
