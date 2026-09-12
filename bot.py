import os
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 Spot Crypto Analyzer ишга тушди!\n\n"
        "Команда:\n"
        "/price BTCUSDT\n"
        "/price ETHUSDT\n"
        "/price SOLUSDT"
    )

async def price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Масалан: /price BTCUSDT")
        return

    symbol = context.args[0].upper()

    try:
        url = "https://api.binance.com/api/v3/ticker/24hr"
        data = requests.get(
            url,
            params={"symbol": symbol},
            timeout=10
        ).json()

        price = float(data["lastPrice"])
        change = float(data["priceChangePercent"])

        emoji = "🟢" if change >= 0 else "🔴"

        await update.message.reply_text(
            f"📊 {symbol}\n\n"
            f"💰 Price: {price}\n"
            f"{emoji} 24h: {change:.2f}%\n\n"
            f"Spot signal: {'BUY WATCH' if change > 0 else 'WAIT'}"
        )

    except Exception:
        await update.message.reply_text(
            "❌ Coin топилмади ёки Binance маълумот бермади."
        )

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("price", price))

    app.run_polling()

if __name__ == "__main__":
    main()
