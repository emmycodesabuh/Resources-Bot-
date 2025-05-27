import logging
import json
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Define API token and admin ID
TOKEN = '7462030528:AAEg_uOsrQedNM-fa_T_m2q3Sqhv2u06n90'
ADMIN_ID = 7130438750

# File storage
FILE_STORAGE = "files.json"

# Load files from storage
def load_files():
    global files
    try:
        with open(FILE_STORAGE, "r") as f:
            files = json.load(f)
    except FileNotFoundError:
        files = {}

# Save files to storage
def save_files():
    with open(FILE_STORAGE, "w") as f:
        json.dump(files, f, indent=4)

# Initialize files dictionary
files = {}
load_files()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        await update.message.reply_text(
            "Welcome!\nAvailable Commands:\n"
            "/start — Start Bot\n"
            "/list — List Available Resources for Download\n"
            "/developer — Developer information\n"
            "/suggest — Suggest an idea or addition of resources\n"
            "/support — Support the development of this project and more."
        )
    except Exception as e:
        logging.error(f"Error in start command: {e}")

async def upload_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if update.effective_user.id == ADMIN_ID:
            if update.message.document:
                file = await context.bot.get_file(update.message.document)
                files[update.message.document.file_name] = file.file_id
                save_files()
                await update.message.reply_text("File uploaded successfully!")
            else:
                await update.message.reply_text("Please upload a file.")
        else:
            await update.message.reply_text("You are not authorized to upload files.")
    except Exception as e:
        logging.error(f"Error in upload_file function: {e}")
        await update.message.reply_text("Error uploading file.")

async def list_files(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        load_files()  # Reload file list from JSON before listing

        if files:
            keyboard = [
                [InlineKeyboardButton(file[:64], callback_data=file[:64])] for file in files.keys()
            ]  # Limit text length to prevent callback errors

            reply_markup = InlineKeyboardMarkup(keyboard)
            await update.message.reply_text("Available files:", reply_markup=reply_markup)
        else:
            await update.message.reply_text("No files available.")
    except Exception as e:
        logging.error(f"Error in list_files function: {e}")
        await update.message.reply_text("Error listing files.")

async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    file_name = query.data

    load_files()  # Ensure latest files are loaded

    if file_name in files:
        try:
            await query.message.reply_document(files[file_name])
        except Exception as e:
            logging.error(f"Error sending file: {e}")
            await query.message.reply_text("Error sending the file.")
    else:
        await query.message.reply_text("File not found.")

    await query.answer()

async def developer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        await update.message.reply_text(
            "© EmmycodezStudio\n"
            "Email: emmycodezstudio@gmail.com\n"
            "Whatsapp: +2349019029931\n"
            "SMS: +2349037411860 \n")
    except Exception as e:
        logging.error(f"Error in developer command: {e}")

async def suggest(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        await update.message.reply_text(
            "Contact Us to make a Suggestion\n"
            "Email: emmycodezstudio@gmail.com\n"
            "Whatsapp: +2349019029931\n")
    except Exception as e:
        logging.error(f"Error in start command: {e}")

async def support(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        await update.message.reply_text(
                "Support The Development of this Project and more... 😊 !\n"
            "Bank Name: Palmpay\n"
            "Account no.: 9037411860\n"
            "Account Name: Emmanuel Abuh\n"
            "\nThank you For Your Support 😊\n")
    except Exception as e:
        logging.error(f"Error in start command: {e}")

def main():
    try:
        application = ApplicationBuilder().token(TOKEN).build()

        application.add_handler(CommandHandler("start", start))
        application.add_handler(MessageHandler(filters.Document.ALL, upload_file))
        application.add_handler(CommandHandler("list", list_files))
        application.add_handler(CallbackQueryHandler(button_click))
        application.add_handler(CommandHandler("developer", developer))
        application.add_handler(CommandHandler("suggest", suggest))
        application.add_handler(CommandHandler("support", support))

        application.run_polling()
    except Exception as e:
        logging.error(f"Error in main function: {e}")

if __name__ == '__main__':
    main()
