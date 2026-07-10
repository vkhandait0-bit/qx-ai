from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

from config import BOT_TOKEN
from partner import get_trader_info
from sheet import save_license, is_active


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome to Quotex Remix AI\n\n"
        "Send your Quotex Trader ID."
    )


async def trader(update: Update, context: ContextTypes.DEFAULT_TYPE):

    trader_id = update.message.text.strip()

    if not trader_id.isdigit():
        await update.message.reply_text(
            "❌ Please send a valid Trader ID."
        )
        return

    msg = await update.message.reply_text(
        "⏳ Checking Deposit..."
    )

    try:

        data = await get_trader_info(trader_id)

        print("============== DATA ==============")
        print(data)
        print("=================================")

        # Invalid Affiliate
        if data["link_id"] != "2112381":

            keyboard = InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        "🚀 Create Quotex Account",
                        url="https://broker-qx.pro/sign-up/?lid=2112381"
                    )
                ]
            ])

            await msg.edit_text(
                """❌ <b>Invalid Trader ID</b>

Your Trader ID is <b>not linked</b> with our official API.

🎁 <b>Get FREE access to Quotex Remix AI</b>

📌 <b>Steps</b>

1️⃣ Create a Quotex account

2️⃣ Deposit at least <b>$30</b>

3️⃣ Send your Trader ID here

🚀 API activation is automatic after verification.

💬 Support:
@AIQuotexTrader
""",
                parse_mode="HTML",
                reply_markup=keyboard,
                disable_web_page_preview=True
            )
            return

        deposit = float(data["deposit"])

        # Already Active
        if is_active(data["trader_id"]):

            await msg.edit_text(
                f"""⚠️ <b>Trader Already Active</b>

🆔 Trader ID : <code>{data['trader_id']}</code>

This Trader ID already has an active Quotex Remix AI API.

💬 Support:
@AIQuotexTrader
""",
                parse_mode="HTML"
            )
            return

        # Membership
        if deposit >= 1000:
            plan = "Elite"

        elif deposit >= 500:
            plan = "Ultra"

        elif deposit >= 200:
            plan = "Premium"

        elif deposit >= 100:
            plan = "Pro"

        elif deposit >= 30:
            plan = "Core"

        else:
            plan = None

        if plan is None:

            keyboard = InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        "💰 Deposit Now",
                        url="https://broker-qx.pro/sign-up/?lid=2112381"
                    )
                ]
            ])

            await msg.edit_text(
                """❌ Deposit Not Found

Minimum Deposit Required: <b>$30</b>

After depositing, send your Trader ID again.

💬 Support:
@AIQuotexTrader
""",
                parse_mode="HTML",
                reply_markup=keyboard,
                disable_web_page_preview=True
            )
            return

        # Save to Sheet
        save_license(
            data["trader_id"],
            data["country"],
            deposit,
            plan
        )

        await msg.edit_text(
            f"""✅ <b>API Activated Successfully</b>

🆔 <b>API ID:</b>
<code>{data['trader_id']}</code>

🌍 <b>Country:</b>
{data['country']}

💰 <b>Deposit:</b>
${deposit}

👑 <b>Membership:</b>
{plan}

🟢 <b>Status:</b>
ACTIVE

🚀 Your Quotex Remix AI API is ready to use 
https://quotexremixai.vercel.app/
""",
            parse_mode="HTML"
        )

    except Exception as e:

        print(e)

        await msg.edit_text(
            f"❌ Error\n\n<code>{e}</code>",
            parse_mode="HTML"
        )


app = Application.builder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(
    MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        trader
    )
)

print("✅ Bot Running...")

app.run_polling()