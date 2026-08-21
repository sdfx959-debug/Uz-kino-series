import telebot
from telebot import types
import database as db
from config import BOT_TOKEN, WEBAPP_URL, ADMIN_IDS

bot = telebot.TeleBot(BOT_TOKEN, parse_mode="HTML")
db.init_db()


def main_menu():
    markup = types.InlineKeyboardMarkup(row_width=1)
    webapp = types.WebAppInfo(url=WEBAPP_URL)
    markup.add(types.InlineKeyboardButton("🎬 Kinolar katalogi", web_app=webapp))
    markup.add(types.InlineKeyboardButton("ℹ️ Yordam", callback_data="help"))
    return markup


def send_movie(chat_id, movie):
    caption = (
        f"🎬 <b>{movie['title']}</b>\n\n"
        f"📝 {movie['description'] or '—'}\n"
        f"🎭 Janr: {movie['genre'] or '—'}\n"
        f"📅 Yil: {movie['year'] or '—'}\n"
        f"🔑 Kod: <code>{movie['code']}</code>\n"
        f"👁 Ko'rishlar: {movie['views']}"
    )
    try:
        bot.send_video(chat_id, movie["video_file_id"], caption=caption)
        db.increment_views(movie["code"])
    except Exception as e:
        bot.send_message(chat_id, f"❌ Kinoni yuborishda xatolik: {e}")


@bot.message_handler(commands=["start"])
def start_handler(message):
    args = message.text.split(maxsplit=1)
    if len(args) > 1:
        code = args[1].strip()
        movie = db.get_movie_by_code(code)
        if movie:
            send_movie(message.chat.id, movie)
            return
        else:
            bot.send_message(message.chat.id, "❌ Bunday kodli kino topilmadi.")

    text = (
        f"👋 Salom, <b>{message.from_user.first_name}</b>!\n\n"
        "🎬 Bu bot orqali siz minglab kinolarni bepul tomosha qilishingiz mumkin.\n\n"
        "🔽 Pastdagi tugma orqali katalogni oching yoki kino kodini yozib yuboring."
    )
    bot.send_message(message.chat.id, text, reply_markup=main_menu())


@bot.message_handler(commands=["admin"])
def admin_handler(message):
    if message.from_user.id in ADMIN_IDS:
        bot.send_message(
            message.chat.id,
            f"🛠 Admin panelga o'tish uchun havola:\n{WEBAPP_URL}/admin/login"
        )
    else:
        bot.send_message(message.chat.id, "⛔ Sizda ruxsat yo'q.")


@bot.callback_query_handler(func=lambda c: c.data == "help")
def help_callback(call):
    bot.answer_callback_query(call.id)
    bot.send_message(
        call.message.chat.id,
        "🔍 Kino topish uchun uning kodini yozing (masalan: <code>1001</code>)\n"
        "🎬 Yoki katalogdan tanlang."
    )


@bot.message_handler(func=lambda m: True, content_types=["text"])
def search_handler(message):
    code = message.text.strip()
    movie = db.get_movie_by_code(code)
    if movie:
        send_movie(message.chat.id, movie)
    else:
        results = db.search_movies(code)
        if results:
            markup = types.InlineKeyboardMarkup()
            for m in results[:10]:
                markup.add(types.InlineKeyboardButton(
                    f"🎬 {m['title']} ({m['code']})", callback_data=f"get_{m['code']}"
                ))
            bot.send_message(message.chat.id, "🔍 Topilgan natijalar:", reply_markup=markup)
        else:
            bot.send_message(message.chat.id, "❌ Kino topilmadi. Kodni tekshirib qayta urinib ko'ring.")


@bot.callback_query_handler(func=lambda c: c.data.startswith("get_"))
def get_movie_callback(call):
    bot.answer_callback_query(call.id)
    code = call.data.replace("get_", "")
    movie = db.get_movie_by_code(code)
    if movie:
        send_movie(call.message.chat.id, movie)


# Admin videoni botga yuborsa, uning file_id sini qaytaradi
# (Admin panelda kino qo'shishda shu file_id kerak bo'ladi)
@bot.message_handler(content_types=["video"])
def video_handler(message):
    if message.from_user.id in ADMIN_IDS:
        file_id = message.video.file_id
        bot.reply_to(
            message,
            f"✅ Video qabul qilindi!\n\n<code>{file_id}</code>\n\n"
            "Bu kodni admin paneldagi 'Video file_id' maydoniga qo'ying."
        )
    else:
        bot.reply_to(message, "⛔ Siz video qo'sha olmaysiz.")


if __name__ == "__main__":
    print("🤖 Bot ishga tushdi...")
    bot.infinity_polling(skip_pending=True)
