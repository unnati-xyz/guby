
[![unnati-xyz](https://circleci.com/gh/unnati-xyz/guby.svg?style=svg)](<LINK>)

# guby 🦉
Guby.live coming soon.


## How to run guby
Guby app currently is a django application with postgres DB as the database.

### Pre-requisities for running the app

* Docker
* docker-compose

In order to run the app, you need to do the following:

```shell
git clone git@github.com:unnati-xyz/guby.git
cd guby
cp .env.sample .env # change .env as per your liking
mkdir postgres_data
docker-compose build && docker-compose up
```

This will bring up 2 containers, one `guby_web` and the other `postgres:apline` . Once the containers are up, go to your browser and type `localhost:5000`, you should see the djano app.


