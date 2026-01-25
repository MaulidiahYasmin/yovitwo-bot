from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from config import BOT_TOKEN, SHEET_NAME

scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

creds = ServiceAccountCredentials.from_json_keyfile_name("gcredentials.json", scope)
client = gspread.authorize(creds)
sheet = client.open(SHEET_NAME).sheet1

async def recapvisit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.replace("/recapvisit", "").strip()

    if not text:
        await update.message.reply_text(
            "Format:\n/recapvisit Customer | Jenis Kegiatan | Aktivitas | Hasil | Nama PIC | No PIC"
        )
        return

    parts = [p.strip() for p in text.split("|")]

    if len(parts) != 6:
        await update.message.reply_text(
            "Harus 6 data:\nCustomer | Jenis Kegiatan | Aktivitas | Hasil | Nama PIC | No PIC"
        )
        return

    # AUTO NUMBER
    current_rows = len(sheet.get_all_values())
    no = current_rows

    row = [no] + parts

    sheet.append_row(row)

    await update.message.reply_text("✅ Recap visit tersimpan.")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("recapvisit", recapvisit))
app.run_polling()
