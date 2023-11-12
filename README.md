# [WIP] Digital Footprint Tracking Bot
#### Making command line tools, APIs, and other services more **accessible**.
This project is a WIP and is intended to bring features that can be accessed via useful CLIs, APIs, ...

## Bots working
- [x] Telegram
- [ ] Discord
- [ ] Slack
- [ ] Signal
- [ ] ...


## Things that are working

- **email** eg `brittany.kaiser@cambridgeanalytica.org`
  - [x] holehe
  - [x] Ghunt
  - [x] HaveIBeenPwned (requires API setup)
  - [x] Aleph API
- **username** eg `/user trump`
  - [x] maigret
- **face comparison** upload 2 photos
  - [x] deepface
  - [x] AwsRekognition (requires API setup)
- **video** `/video https://www.youtube.com/watch?v=QNXvE1BZu8g`
  - [x] yt-dlp
<!-- - **default**
  - [x] Aleph API -->

## Things to implement

features:
- test setup for each tool
- document .env
- enable/disable tools from config file
- dockerize
- scalability
- observability
- authentication

tools:
- unfurl
- subdomain scan
- wayback-google-analytics
- connect to other bots
- email2phone?
- blackbird?
- ... please suggest as issues...


### Development

```bash
# install dependencies with pipenv
pipenv install
# if you're developing also install dev dependencies
pipenv install -d

# run it
python bot.py

# or, with hot-reload for development
jurigged -v bot.py

```