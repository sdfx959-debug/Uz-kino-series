# 🎬 Kino Bot — Telegram Mini App + Admin Panel (Python)

To'liq Python (Flask + pyTelegramBotAPI) da yozilgan. PHP ishlatilmagan — istalgan VPS/serverga muammosiz o'rnatiladi.

## 📁 Struktura
```
kino_bot/
├── bot.py                 # Telegram bot
├── config.py               # Sozlamalar
├── database.py              # SQLite bilan ishlash
├── requirements.txt
├── .env.example             # Shu faylni .env qilib nusxalang
├── web/
│   ├── app.py               # Flask server (Mini App + Admin panel)
│   ├── templates/
│   │   ├── index.html       # Mini App (foydalanuvchi)
│   │   ├── admin_login.html
│   │   └── admin_dashboard.html
│   └── static/
│       ├── css/style.css
│       └── js/app.js
```

## ⚙️ O'rnatish

1. **Python muhitini tayyorlang** (Python 3.10+):
```bash
python3 -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

2. **.env faylini yarating:**
```bash
cp .env.example .env
```
Va ichiga to'ldiring:
- `BOT_TOKEN` — @BotFather dan olingan token
- `BOT_USERNAME` — bot username (@ siz)
- `ADMIN_IDS` — sizning Telegram ID (masalan @userinfobot orqali biling)
- `ADMIN_USERNAME`, `ADMIN_PASSWORD` — admin panelga kirish uchun
- `WEBAPP_URL` — sizning domeningiz, **https bo'lishi shart** (Telegram Web App faqat https qabul qiladi)

3. **Bot va serverni ishga tushiring** (2 ta alohida process kerak):
```bash
# 1-terminal — bot
python bot.py

# 2-terminal — veb server
cd web
python app.py
```

Productionda `web/app.py` ni gunicorn bilan ishga tushiring:
```bash
pip install gunicorn
gunicorn -w 2 -b 0.0.0.0:5000 app:app
```
Va domeningizga Nginx orqali https bilan ulang (Let's Encrypt / certbot tavsiya etiladi).

Botni doim ishlab turishi uchun `systemd` yoki `screen`/`tmux`/`pm2` ishlatishingiz mumkin.

## 🎬 Kino qo'shish tartibi

1. Videongizni botga (o'zingiz `ADMIN_IDS` da bo'lsangiz) yuboring — bot sizga `file_id` qaytaradi.
2. Admin panelga kiring: `https://domeningiz.uz/admin/login`
3. "Yangi kino qo'shish" formasiga kod, nom, janr, yil, poster URL va yuqoridagi `file_id` ni kiriting.
4. Saqlang — kino darhol Mini App katalogida va bot orqali qidirishda ko'rinadi.

## 🔍 Ishlash printsipi

- Foydalanuvchi botda **/start** bosadi → "🎬 Kinolar katalogi" tugmasi (Web App) ochiladi.
- Mini App'da kinolarni qidirish, ko'rish mumkin.
- Kino ustiga bosilganda "▶️ Tomosha qilish" tugmasi bosilsa, bot bilan chat ochiladi va video avtomatik yuboriladi (`?start=kod` deep link orqali).
- Bot orqali to'g'ridan-to'g'ri kod yozib ham (masalan `1001`) kinoni olish mumkin.

## 🎨 Dizayn
Dark theme, gradient (pushti-siyoh) rangli tugmalar, silliq animatsiyalar, mobil uchun moslashgan grid — barchasi `style.css` da sozlanadi.
