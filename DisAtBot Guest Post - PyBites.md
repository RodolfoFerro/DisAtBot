# DisAtBot: Disaster Attention Bot

*By Rodolfo Ferro*

> *"¿Quién convocó a tanto muchacho, de dónde salió tanto voluntario, cómo fue que la sangre sobró en los hospitales, quién organizó las brigadas que dirigieron el tránsito de vehículos y de peatones por toda la zona afectada? No hubo ninguna convocatoria, no se hizo ningún llamado y todos acudieron"*
>
> **"El jueves negro que cambió a México"**
> – Emilio Viale, 1985.

## A bit of context...
Since [September 19th, 2017](https://en.wikipedia.org/wiki/2017_Central_Mexico_earthquake) ([The Guardian](https://www.theguardian.com/world/live/2017/sep/20/mexico-city-earthquake-dozens-dead-powerful-quake-live-updates), [CNN](http://edition.cnn.com/2017/09/19/americas/mexico-earthquake/index.html)), and the following dates in which Mexico has faced several earthquakes, I've been wondering how could damaged zones reports, people buried under rests of buildings, injured people in need of medicines and other situations could be handled.

What was created by that time, "[Verificado 19s](http://www.verificado19s.org/)", was an immediate solution to follow up reports from social media and visualize the info on a map embedded in a website. The thing is that there were a lot of people needed, that were all the time (24/7) monitoring posts in social networks (a.k.a. Facebook and Twitter) from people that were located in the damaged zone (in real time), and then the data was updated every ~10 minutes.

I've been thinking about a way to optimize this process for future situations, not only for earthquakes, but for other disaster situations (like, more in general). This is why I'm trying to create a solution, and why I wanted to work specifically with this bot, which will automate this task into a better way to face this situations in the future.

## What’s the idea of DisAtBot?

DisAtBot would automate the process of reporting incidents via messaging platforms, such as Telegram, Facebook Messenger, Twitter, etc. This project may take several phases of development and a lot of contributions, too. So, at this time ***this first approach is considering only Telegram as the messaging platform only for this initial phase of implementation.***

Until now, you can find DisAtBot in...

- Telegram: [https://t.me/DisAtBot](https://t.me/DisAtBot)
- More coming soon… (I hope!)

- The official repo: [https://github.com/RodolfoFerro/DisAtBot](https://github.com/RodolfoFerro/DisAtBot)

The idea would be to have a simple flow that allow disaster reports be quick and easy. A general process of DisAtBot is described in the following (wireframing) flow:

![DisAtBot main flow](https://github.com/RodolfoFerro/DisAtBot/blob/master/imgs/flow.png)

About use cases, the idea is that any user would interact by selecting options from button menus in the conversation (at least in Telegram and Facebook Messenger). This lets people report incidents in a quick n’ easy way.

The next step would be that an open ticket would be created, and it’d end in a database which will be accessed by the corresponding government instance/public organization/NGO/etc. to validate the data and send the corresponding assistance. When no more help is needed, or the situation is under absolutely control, then it’d turn into a closed ticket.

## Requirements for DisAtBot

First of all, we will need several requirements. You’re able to clone the repo ([https://github.com/RodolfoFerro/DisAtBot](https://github.com/RodolfoFerro/DisAtBot)) and have the code. Besides [Python 3.6](https://www.python.org/downloads/) (the version that I’m using for this project) we will be using the following packages:
* [pandas](http://pandas.pydata.org/)
* [geopandas](http://geopandas.org/)
* [geocoder](http://geocoder.readthedocs.io/)
* [googlemaps](https://developers.google.com/maps/documentation/)
* [geojsonio](http://geojson.io/)
* [Shapely](https://shapely.readthedocs.io/en/latest/)
* [python-telegram-bot](https://python-telegram-bot.org/)

All of them are "*pip installable*", and a `requirements.txt` file can be found in the main folder of the repo, so you can simply run:

```bash
pip install -r requirements.txt
```
And install all packages needed. Now we’re able to access the scripts folder and run the bot as follows:

```bash
python DisAtBot.py
```

## Implementing DisAtBot

The first issue addressed during the development of the Telegram bot was the creation of menu buttons for an easy interaction with the user. The second –and main– issue addressed was the conversation handler. A finite state machine was needed in order to preserve the desired flow and the responses needed to be processed for each state.

I won’t go too deep in the explanation, but the following snippets will show how these issues were solved.

First of all, Telegram’s library has several methods to create button menus for user responses during the conversation flow. The idea is to create a Keyboard Markup which can be Inline (which means that buttons will appear in the conversation window) or as a Reply Keyboard (which means that buttons will be displayed under the textbox to write messages). This will handle the responses through buttons.

An example can be seen in the menu function:
```python
def menu(bot, update):
    """
    Main menu function.
    This will display the options from the main menu.
    """
    # Create buttons to select language:
    keyboard = [[send_report[LANG], view_map[LANG]],
                [view_faq[LANG], view_about[LANG]]]

    reply_markup = ReplyKeyboardMarkup(keyboard,
                                       one_time_keyboard=True,
                                       resize_keyboard=True)

    user = update.message.from_user
    logger.info("Menu command requested by {}.".format(user.first_name))
    update.message.reply_text(main_menu[LANG], reply_markup=reply_markup)

    return SET_STAT
```

As you can see, the `keyboard` variable is a list that contains the four buttons to be displayed, and the layout can be set by nesting lists inside. In this case the **Report** and **Map** buttons are in the first row, while **FAQ** and **About** buttons are in the second row. This will be displayed as follows:

<img src="https://github.com/RodolfoFerro/DisAtBot/blob/master/imgs/screenshot_menu.jpg" width="50%">

A demo of DisAtBot can be seen [in here](https://drive.google.com/file/d/1dOvF17AYKiic85HmzMjnK5Qza2Tg0PNw/view)!

## Future work



## Contributing

If you're interested in contributing to this project, feel free to take a look in the [CONTRIBUTING](https://github.com/RodolfoFerro/DisAtBot/blob/master/CONTRIBUTING.md) file. I'd be very pleased to see how a project like this could grow in order to solve a real problem that is faced when is less expected.
