# Messenger API

## Development

    python manage.py loaddata messengerapi/fixtures/data.json

## Resources

### Messages

#### GET /messages
Default sort by date descending, default limit 100 / 30 days

    ```
    /messages?sender=susan
    ```

    ```
    /messages?recipient=ralph
    ```


#### POST /messages

    ```
    /messages

    {
        "sender": "susan",
        "recipient": "ralph"
    }
    ```

#### PUT /messages/:messageId
#### DELETE /messages/:messageId

## TODO
1. Swagger doc
2. Dockerize
