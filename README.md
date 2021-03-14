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

## Testing

    docker run -p 80:8080 -e SWAGGER_JSON=/swagger.yml -v ${PWD}/messengerapi/api-docs/swagger.yml:/swagger.yml swaggerapi/swagger-ui
