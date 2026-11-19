## Telegram bot for an online shop
Client didn't have access to database so I scraped all the data directly from the web pages with python script and created own database which was used later in the process of bot creation, storing data of all the shop goods.
Whole web shop menu structure was implemented into bot with all the goods data, the next step would be implementing payment and order systems and it would be finised, but unfortunately project stopped.

## Setup

1. Copy `.env.example` to `.env` and fill in your bot token and PostgreSQL settings.
2. Load the variables, for example `set -a; source .env; set +a` (Linux/macOS).
3. Run `python database_scrap.py` to fill the database, then `python detal_traffic_bot.py` to start the bot.
