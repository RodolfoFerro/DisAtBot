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
- The official repo: [https://github.com/RodolfoFerro/DisAtBot](https://github.com/RodolfoFerro/DisAtBot)
- More coming soon… (I hope!)

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

The first issue addressed during the development of the Telegram bot was the creation of menu buttons for an easy interaction with the user. The second –*and main*– issue addressed was the conversation handler. A finite state machine was needed in order to preserve the desired flow and the responses needed to be processed for each state.

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

<center>
<img src="https://github.com/RodolfoFerro/DisAtBot/blob/master/imgs/screenshot_menu.jpg" width="35%">
</center>

Following with the code, a `ReplyMarkup` is needed to handle the button responses, and it specifies the layout of the menu: if only one menu is displayed, if it needs to be resized, etc. A logger is used for the bot, and the `update.message.reply(...)` function is used to update the displayed text according to the response from the user. The `SET_STAT` variable returned in this function is an integer variable (predefined at the very beginning) to return the state at that time, in order to follow with the flow.

We now understand the menu creation and handling. The reason of using buttons is that since we want a quick interaction for an emergency situation during the interaction with the bot, this seems to do the trick. This was thought while the UX and UI were importantly considered under the concerned bot usage (again, disaster situations).

Now about the conversation handler... It was the main issue during the development of this first phase. As I mentioned before, a finite state machine is needed. In it we're able to set the state or step of the flow where we're at. The Telegram's `ConversationHandler` takes care about that, and as part of its parameters the set of states have to be passed. This conversation handler ends up being the finite state machine (which handles each state), but also each state needs to handle its respective information (button responses, etc.).

The snippet with the main function that contains the conversation handler is here:

```python
def main():
    """
    Main function.
    This function handles the conversation flow by setting
    states on each step of the flow. Each state has its own
    handler for the interaction with the user.
    """
    global LANG
    # Create the EventHandler and pass it your bot's token.
    updater = Updater(telegram_token)

    # Get the dispatcher to register handlers:
    dp = updater.dispatcher

    # Add conversation handler with predefined states:
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            SET_LANG: [RegexHandler('^(ES|EN)$', set_lang)],

            MENU: [CommandHandler('menu', menu)],

            SET_STAT: [RegexHandler(
                        '^({}|{}|{}|{})$'.format(
                            send_report['ES'], view_map['ES'],
                            view_faq['ES'], view_about['ES']),
                        set_state),
                       RegexHandler(
                        '^({}|{}|{}|{})$'.format(
                            send_report['EN'], view_map['EN'],
                            view_faq['EN'], view_about['EN']),
                        set_state)],

            LOCATION: [MessageHandler(Filters.location, location),
                       CommandHandler('menu', menu)]
        },

        fallbacks=[CommandHandler('cancel', cancel),
                   CommandHandler('help', help)]
    )

    dp.add_handler(conv_handler)

    # Log all errors:
    dp.add_error_handler(error)

    # Start DisAtBot:
    updater.start_polling()

    # Run the bot until the user presses Ctrl-C or the process
    # receives SIGINT, SIGTERM or SIGABRT:
    updater.idle()
```

It might seem a bit confuse since I haven't explained totally the usage of each line, but most of this lines can easily be deducted. Some observations to help with this:

- The conversation handler has the states of the flow.
- It also has entry points (such as the `start` function), and fallbacks (such as the `cancel` and `help` functions).
- This main function also contains some error handlers.
- A global `LANG` variable is used, since the implementation has been done for English and Spanish... Oh, yes, I forgot to mention that...

**You're able to interact with this bot in English or Spanish, since I created dictionaries for each interaction in both languages.**

As I said previously, this hasn't gone very deep with implementation details, but some issues faced during the coding are explained with these snippets. If you want to check the full code of this bot, you can [go here](https://github.com/RodolfoFerro/DisAtBot/tree/master/scripts). There you'll find the main script and the language dictionaries.

Some other features implemented were the geolocation handling and the display of some info with the `About` and `FAQ` sections. But the best way to know about this project is by watching it working, so...

#### A demo of DisAtBot can be seen [in here](https://drive.google.com/file/d/1dOvF17AYKiic85HmzMjnK5Qza2Tg0PNw/view)!

## Future work

You might thought that some of the requirements haven't been mentioned/used so far. The thing is that as part of the improvement of the future development a map visualization it's being thought (any suggestion for this is welcome) and what has been done so far is a system that creates a GeoJSON file from the locations acquired. This leads to think and cook a better solution (as you probably saw in the [demo video](https://drive.google.com/file/d/1dOvF17AYKiic85HmzMjnK5Qza2Tg0PNw/view)).

Another thing to be added might be a website to explain the main use for this bot, you know, maybe a wiki –*kinda*– site? Besides that, the obvious developments are also considered for the future work: Facebook Messenger, Twitter and other platforms.

Any other idea for this? Feel free to [contribute](https://github.com/RodolfoFerro/DisAtBot/blob/master/CONTRIBUTING.md)!


## Contributing

If you're interested in contributing to this project, feel free to take a look in the [CONTRIBUTING](https://github.com/RodolfoFerro/DisAtBot/blob/master/CONTRIBUTING.md) file. I'd be very pleased to see how a project like this could grow in order to solve a real problem that is faced when is less expected.
