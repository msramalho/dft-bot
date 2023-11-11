# [WIP] Digital Footprint Tracking Bot

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
- **default**
  - [x] Aleph API

## Things to implement

features:
- dockerize
- scalability
- authentication with token and TOTP
- authentication to enable more features

tools:
- unfurl
- subdomain scan
- wayback-google-analytics
- connect to other bots
- email2phone?
- blackbird?


### Development

```bash
# install dependencies with pipenv
pipenv install

# run it
python bot.py

# or, with hot-reload for development
jurigged -v bot.py

```