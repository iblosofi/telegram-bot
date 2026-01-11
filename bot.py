import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

TOKEN = os.environ.get("BOT_TOKEN")

def main_keyboard():
    return ReplyKeyboardMarkup(
        [
            ["Deposit", "Withdraw"],
            ["History", "Support"],
            ["Start"],
        ],
        resize_keyboard=True
    )

def method_keyboard():
    return ReplyKeyboardMarkup(
        [
            ["Telebirr", "CBE Birr"],
            ["BOA"],
            ["Start"],
        ],
        resize_keyboard=True
    )

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    await update.message.reply_text(
        "👋 እንኳን ደህና መጣህ\nእባክህ አንዱን ምረጥ 👇",
        reply_markup=main_keyboard()
    )

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "Start":
        await start(update, context)
        return

    if text in ["Deposit", "Withdraw"]:
        context.user_data["flow"] = text
        await update.message.reply_text(
            "💳 የክፍያ መንገድ ምረጥ",
            reply_markup=method_keyboard()
        )
        return

    if text in ["Telebirr", "CBE Birr", "BOA"]:
        context.user_data["method"] = text
        await update.message.reply_text("📱 10 አሃዝ ስልክ ቁጥር አስገባ")
        return

    if text.isdigit() and len(text) == 10:
        context.user_data["phone"] = text
        await update.message.reply_text("💰 መጠን አስገባ")
        return

    if text.isdigit():
        context.user_data["amount"] = text
        await update.message.reply_text(
            "✅ ጥያቄህ ተቀብሏል",
            reply_markup=main_keyboard()
        )
        context.user_data.clear()
        return

    await update.message.reply_text("❌ ያልተለመደ ግብዓት")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    app.run_polling()

if __name__ == "__main__":
    main()
