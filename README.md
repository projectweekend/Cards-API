Environment Variables
====================

There are just a couple of configurations managed as environment variables. In the development environment, these are injected by Docker Compose and managed in the `docker-compose.yml` file.

* `DATABASE_URL` - This is the connection URL for the PostgreSQL database. It is not used in the **development environment**.
* `DEBUG` - This toggles debug mode for the app to True/False.



Database Migrations
====================

Database migrations are handled by [Flyway](http://flywaydb.org/) and files are stored in the `/sql` directory. Migrations are automatically applied when running tests with Nose. You can run migrations manually in the development environment using `docker-compose` too. The included script `local_migrate.sh` uses an environment variable created by [Docker Compose](https://docs.docker.com/compose/env/) to find the IP address assigned to the database and execute the Flyway command to run migrations.

```
docker-compose run web ./local_migrate.sh
```



Running Tests
====================

Tests, with code coverage reporting can be ran with the following command:
```
./local_test.sh
```



Routes
====================

All routes require that an API Key be included in the `X-API-Key` header. The API Key value is sent via email after registering a new account (**POST:** `/user`).



### Create a new deck

**POST:**
```
/deck
```

**Body:**
```json
{
    "count": 1
}
```

**Notes:**

* `count` - The number of standard 52 card decks to shuffle into the requested deck.

**Response:**
```json
{
    "id": 1,
    "remaining": 52,
    "removed": 52
}
```



### List decks

**GET:**
```
/deck
```

**Response:**
```json
[
    {
        "id": 1,
        "remaining": 52,
        "removed": 52
    }
]
```



### Get deck

**GET:**
```
/deck/:id
```

**Response:**
```json
{
    "id": 1,
    "remaining": 52,
    "removed": 0
}
```



### Shuffle cards in deck

**PUT:**
```
/deck/:id/shuffle
```

**Body:**
```json
{
    "target": "all"
}
```

**Notes:**

* `target` - The target set of cards to shuffle `all` or `remaining`.

**Response:**
```json
{
    "id": 1,
    "remaining": 52,
    "removed": 0
}
```



### Draw cards from deck

**PUT:**
```
/deck/:id/draw
```

**Body:**
```json
{
    "count": 1
}
```

**Notes:**

* `count` - The number of cards to draw from the deck.

**Response:**
```json
{
    "deck": {
        "id": 1,
        "remaining": 52,
        "removed": 52
    },
    "cards": [
        {
            "rank": "2",
            "suit": "SPADES",
            "front": "http://example.com/path/to/front/2-SPADES.png",
            "back": "http://example.com/path/to/back.png"
        }
    ]
}
```
