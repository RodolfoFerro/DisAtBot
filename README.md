# DABOT: Disaster Attention Bot

Since [September 19th, 2017](https://en.wikipedia.org/wiki/2017_Central_Mexico_earthquake) ([The Guardian](https://www.theguardian.com/world/live/2017/sep/20/mexico-city-earthquake-dozens-dead-powerful-quake-live-updates), [CNN](http://edition.cnn.com/2017/09/19/americas/mexico-earthquake/index.html)), and the following dates in which Mexico has faced several earthquakes, I've been wondering how could reports of damaged zones, people buried under rests of building, injuried people in need of medicines and other situations could be handled.

What was created by that time, *"[Verificado 19s](http://www.verificado19s.org/)"*, was an immediate solution to follow up reports from social media and visualize the info on a map embeded in a website. The thing is that there were a lot of people that were all the time monitoring posts (of people, in real time) of all social media and the data was updated every ~10 minutes.

I've been thinking about trying to optimize this process for future situations, not only for earthquakes, but for other natural disasters. This is why I'm trying to create a solution for this, and wanted to work specifically in this bot.

## About DABOT 🤖

DABOT would automate the process of reporting incidents via messaging platforms, such as Telegram, Facebook Messenger, Twitter, etc. ***This first approach is considering only Telegram as the messaging platform for this initial phase of implementation.***

A general process of DABOT is described in the following flow (wireframing):

<img src="https://github.com/RodolfoFerro/dabot/blob/master/imgs/flow.png" alt="DABOT's main flow" width="70%">

------

## Requirements ⚙️

Besides [Python 3.6](https://www.python.org/downloads/) we will be using the following packages:

* [pandas](http://pandas.pydata.org/)
* [geopandas](http://geopandas.org/)
* [geocoder](http://geocoder.readthedocs.io/)
* [googlemaps](https://developers.google.com/maps/documentation/)
* [geojsonio](http://geojson.io/)
* [Shapely](https://shapely.readthedocs.io/en/latest/)
* [python-telegram-bot](https://python-telegram-bot.org/)

You can simply install each package using `pip` as follows:
```bash
pip install <package>
```

Or you can install all the packages needed with the [`requirements.txt`](https://github.com/RodolfoFerro/dabot/blob/master/requirements.txt) file by running:
```bash
pip install -r requirements.txt
```

------

## Structure 🗂

The structure of this repo is as follows:

- The [img](https://github.com/RodolfoFerro/dabot/tree/master/imgs) folder contains all images of this repo.
- The [maps](https://github.com/RodolfoFerro/dabot/tree/master/maps) folder contains any map/geo-spacial document, such as geoJSON, etc.
- The [scripts](https://github.com/RodolfoFerro/dabot/tree/master/scripts) folder contains all the scripts developed so far. Inside, a folder for each messaging platform can be found.
- The [`requirements.txt`](https://github.com/RodolfoFerro/dabot/blob/master/requirements.txt) file contains a listing of the required packages with their respective versions for an easy `pip` installation. *Recommended.*

------

## Implementations so far 💻

## Future work 📈

[ ] Create CONTRIBUTING file.
[ ] Create LICENSE file.
[ ] Create `geo`/`map` structure.
[ ] Create DABOT with [BotFather](https://t.me/BotFather).
[ ] ...

------

## Contributing 👩🏽‍💻👨🏻‍💻

Please check our [CONTRIBUTING]() file.

#### Contributors list:
* [Rodolfo Ferro](https://github.com/RodolfoFerro)

---

## License 📄

Please read the [LICENSE]() provided in this repo.
