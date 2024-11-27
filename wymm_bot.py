import sqlite3
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackContext, CallbackQueryHandler
import asyncio

# Initialize SQLite database
conn = sqlite3.connect('users.db', check_same_thread=False)
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                    chat_id INTEGER PRIMARY KEY, 
                    username TEXT
                 )''')
conn.commit()

# Handler for /start command
async def start(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    username = update.effective_user.username

    # Save chat_id and username to the database
    cursor.execute("REPLACE INTO users (chat_id, username) VALUES (?, ?)", (chat_id, username))
    conn.commit()

    await update.message.reply_text(
        "Hi! You've been registered. Others can now send proposals to you!"
    )

# Handler for /propose command
async def send_proposal(update: Update, context: CallbackContext):
    if len(context.args) != 1:
        await update.message.reply_text("Usage: /propose <username>")
        return

    target_username = context.args[0]

    # Fetch chat_id from the database
    cursor.execute("SELECT chat_id FROM users WHERE username = ?", (target_username,))
    result = cursor.fetchone()

    if result:
        chat_id = result[0]

        # Encode proposer_id in the callback data
        proposer_id = update.effective_chat.id
        yes_callback_data = f"yes_{proposer_id}"
        no_callback_data = f"no_{proposer_id}"

        # Prepare proposal message with inline buttons
        keyboard = [
            [InlineKeyboardButton("Yes", callback_data=yes_callback_data), InlineKeyboardButton("No", callback_data=no_callback_data)],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        try:
            await context.bot.send_message(
                chat_id=chat_id,
                text=f"{update.effective_user.first_name} wants to propose to you! Do you accept?",
                reply_markup=reply_markup,
            )
            await update.message.reply_text("Proposal sent successfully!")
        except Exception as e:
            await update.message.reply_text(f"Failed to send proposal: {e}")
    else:
        await update.message.reply_text(
            "The user has not started the bot yet. Ask them to send /start to the bot."
        )

# Handler for button press responses
async def handle_button(update: Update, context: CallbackContext):
    query = update.callback_query
    callback_data = query.data
    # Extract proposer_id from the callback data
    response, proposer_id = callback_data.split("_")

    # Respond based on user's button choice
    if response == "yes":
        message = "accepted"
    else:
        message = "declined"

    # Send response to the proposer
    try:
        await context.bot.send_message(
            chat_id=int(proposer_id),  # Send to the proposer
            text=f"Your proposal was {message}",
        )
        await query.answer()  # Acknowledge the callback
    except Exception as e:
        await query.answer(f"Error sending response: {e}")

# Main application setup
async def main():
    app = ApplicationBuilder().token("YOUR_BOT_TOKEN").build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("propose", send_proposal))
    app.add_handler(CallbackQueryHandler(handle_button))  # Handle button responses

    print("Bot is running...")

    try:
        await app.run_polling()  # Run the bot
    finally:
        await app.shutdown()  # Ensure graceful shutdown

# Entry point for the application
if __name__ == "__main__":
    import nest_asyncio

    nest_asyncio.apply()  # Allows nesting event loops (useful for environments like Jupyter)

    try:
        # Check if there is an existing event loop (for environments where the event loop is running)
        loop = asyncio.get_event_loop()
        if loop.is_running():
            # In this case, just run the main function directly in the running loop
            asyncio.ensure_future(main())  # This will schedule the main task in the running loop
        else:
            loop.run_until_complete(main())  # If there's no loop, run the main function as usual
    except RuntimeError:
        # Fallback to running main if no event loop exists
        asyncio.run(main())
