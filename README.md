# Messenger API

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
