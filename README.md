# Will You Marry Me? Bot

A simple Telegram bot that lets users send and respond to proposals via inline keyboard buttons. This bot is built using Python and the `python-telegram-bot` library with SQLite as the database backend.

## Features

- **User Registration**:
  - Registers users by saving their `chat_id` and `username` when they start the bot.
- **Proposal System**:
  - Users can propose to others by their Telegram username.
  - Sends proposals with inline keyboard buttons for "Yes" and "No" responses.
  - Notifies proposers of the response.
- **Database Integration**:
  - Stores user data (`chat_id`, `username`) in an SQLite database.
- **Async Operations**:
  - Fully asynchronous, leveraging `asyncio` for efficient handling of Telegram API requests.

## Setup

### Prerequisites

- Python 3.9 or higher
- Telegram bot token (create a bot via [BotFather](https://core.telegram.org/bots#botfather))
- Required Python libraries (install with the steps below)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/nightfullstar/willyoumarryme_bot_telegram.git
   cd willyoumarryme_bot_telegram
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Replace `YOUR_BOT_TOKEN` in the code with your Telegram bot token.

4. Run the bot:
   ```bash
   python wymm_bot.py
   ```

### Additional Setup (Optional)

If you are running the bot in a Jupyter Notebook or an environment with an existing event loop, `nest_asyncio` is used to allow nested event loops.

## Commands

### `/start`
- Registers the user in the database.
- Sends a welcome message.

### `/propose <username>`
- Sends a proposal to the specified username.
- The target user receives a message with "Yes" and "No" buttons.
- Notifies the proposer of the response.

## How It Works

1. **User Registration**:
   - When a user sends `/start`, their `chat_id` and `username` are stored in an SQLite database.
2. **Sending Proposals**:
   - The `/propose <username>` command fetches the target user’s `chat_id` from the database and sends a proposal message.
   - Inline keyboard buttons allow the recipient to accept or decline the proposal.
3. **Callback Responses**:
   - Handles button presses to notify the proposer of the recipient’s decision.

## Error Handling

- Notifies the sender if the target user hasn’t registered with the bot.
- Handles exceptions during message sending or database operations.

## Database Schema

The SQLite database (`users.db`) contains a single table:

```sql
CREATE TABLE users (
    chat_id INTEGER PRIMARY KEY,
    username TEXT
);
```

## Development

### Dependencies

Install the required libraries:

```bash
pip install python-telegram-bot nest-asyncio
```

### Project Structure

- `bot.py`: Main script containing the bot logic.
- `users.db`: SQLite database file for storing user data.
- `requirements.txt`: Dependencies for the project.

### Running the Bot

Run the bot with:

```bash
python bot.py
```

### Testing

- Start a conversation with the bot using `/start`.
- Use `/propose <username>` to send a proposal to another registered user.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request with improvements or bug fixes.

## Acknowledgments

- Built with the [python-telegram-bot](https://python-telegram-bot.org/) library.
- Inspired by the need for fun and interactive Telegram experiences, used it on my wife(she said yes)

