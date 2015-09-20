Environment Variables
====================

There are just a couple of configurations managed as environment variables. In the development environment, these are injected by Docker Compose and managed in the `docker-compose.yml` file.

* `DATABASE_URL` - This is the connection URL for the PostgreSQL database. It is not used in the **development environment**.
* `API_KEY` - A system wide API key validated in the `X-API-Key` header.



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

All routes require that an API Key be included in the `X-API-Key` header.



### Create a new deck

Create a new deck of shuffled cards. The `count` property is a multiplier indicating the number of decks to shuffle together.

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

**Response:**
```json
{
    "id": 1,
    "remaining": 52,
    "removed": 0
}
```

**Status:**

* `201` if successful
* `400` if invalid data
* `401` if invalid API Key



### List decks

List all decks that were created for the API key.

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
        "removed": 0
    }
]
```

**Status:**

* `200` if successful
* `401` if invalid API Key



### Get deck

Get a single deck that was created for the API key.

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

* `200` if successful
* `401` if invalid API Key
* `404` if deck not found



### Shuffle cards in deck

Shuffle all cards in the deck. Any cards that were removed from the deck will be combined with the remaining cards.

**PUT:**
```
/deck/:id/shuffle
```

**Body:** None

**Response:**
```json
{
    "id": 1,
    "remaining": 52,
    "removed": 0
}
```

* `200` if successful
* `401` if invalid API Key
* `404` if deck not found



### Draw cards from deck

Draw a card from the deck. The card drawn will move from remaining to removed. The `count` property indicates the number of cards to draw.

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

**Response:**
```json
{
    "deck": {
        "id": 1,
        "remaining": 51,
        "removed": 1
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

* `200` if successful
* `401` if invalid API Key
* `404` if deck not found
* `409` if deck is empty
