import asyncio
import sqlite3
import random
import google.generativeai as genai
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command

# --- কনফিগারেশন ---
TOKEN = "8122974668:AAGCbMp1zgYenpYvRs4qATaWmJo9jOdL33g"
GEMINI_KEY = "AIzaSyAoxxCCd1HKDbgPsqwGNafkvV1PopHMVpk"
OWNER_ID = 7276206449  # আপনার টেলিগ্রাম আইডি এখানে দিন
OWNER_TEAM = "Team BMT"
BOT_NAME = "BMT AI"

# AI Setup
genai.configure(api_key=GEMINI_KEY)
ai_model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=f"You are {BOT_NAME}, developed by {OWNER_TEAM}. Be funny, sarcastic, and talk in a mix of Bengali and English. Never mention Google. If anyone asks, you are a product of {OWNER_TEAM}."
)

# --- SQLITE DATABASE SETUP ---
conn = sqlite3.connect("bot_data.db")
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS users 
                  (user_id INTEGER PRIMARY KEY, coins INTEGER, warns INTEGER, level INTEGER)''')
conn.commit()

def get_user(user_id):
    cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    res = cursor.fetchone()
    if not res:
        cursor.execute("INSERT INTO users VALUES (?, ?, ?, ?)", (user_id, 500, 0, 1))
        conn.commit()
        return (user_id, 500, 0, 1)
    return res

# --- BOT INITIALIZATION ---
bot = Bot(token=TOKEN)
dp = Dispatcher()

# --- 1. ADMIN PANEL & BROADCAST ---
@dp.message(Command("admin"))
async def admin_panel(message: types.Message):
    if message.from_user.id != OWNER_ID: return
    cursor.execute("SELECT COUNT(*) FROM users")
    total_users = cursor.fetchone()[0]
    await message.reply(f"📊 **{OWNER_TEAM} Admin Panel**\n\n👥 Total Users: {total_users}\n📢 /broadcast - সবার কাছে মেসেজ পাঠাতে\n🚫 /ban - ইউজার ব্যান করতে")

@dp.message(Command("broadcast"))
async def broadcast(message: types.Message):
    if message.from_user.id != OWNER_ID: return
    if not message.reply_to_message:
        return await message.reply("মেসেজটি রিপ্লাই দিন যা ব্রডকাস্ট করতে চান।")
    
    cursor.execute("SELECT user_id FROM users")
    users = cursor.fetchall()
    count = 0
    for user in users:
        try:
            await bot.send_message(user[0], message.reply_to_message.text)
            count += 1
        except: continue
    await message.answer(f"✅ {count} জন ইউজারের কাছে মেসেজ পাঠানো হয়েছে।")

# --- 2. SMART AI CHAT (Funny Reply) ---
@dp.message(F.text & ~F.text.startswith("/"))
async def chat_handler(message: types.Message):
    bot_info = await bot.get_me()
    if BOT_NAME.lower() in message.text.lower() or (message.reply_to_message and message.reply_to_message.from_user.id == bot_info.id):
        res = ai_model.generate_content(message.text)
        await message.reply(f"🔥 {res.text}\n\n— 𝖡𝗒 {OWNER_TEAM}")

# --- 3. ECONOMY & GAMES ---
@dp.message(Command("daily"))
async def daily(message: types.Message):
    get_user(message.from_user.id)
    reward = random.randint(100, 300)
    cursor.execute("UPDATE users SET coins = coins + ? WHERE user_id = ?", (reward, message.from_user.id))
    conn.commit()
    await message.reply(f"💰 {OWNER_TEAM} থেকে {reward} কয়েন গিফট পেলেন!")

@dp.message(Command("bal"))
async def balance(message: types.Message):
    user = get_user(message.from_user.id)
    await message.reply(f"💳 Balance: {user[1]} coins")

# --- 4. MODERATION ---
@dp.message(Command("warn"))
async def warn(message: types.Message):
    if not message.reply_to_message: return
    uid = message.reply_to_message.from_user.id
    get_user(uid)
    cursor.execute("UPDATE users SET warns = warns + 1 WHERE user_id = ?", (uid,))
    conn.commit()
    new_warn = get_user(uid)[2]
    await message.answer(f"⚠️ {message.reply_to_message.from_user.first_name}, Warnings: {new_warn}/3")

# --- 5. START & INFO ---
@dp.message(Command("start"))
async def start(message: types.Message):
    get_user(message.from_user.id)
    await message.answer(f"আসসালামু আলাইকুম! আমি {BOT_NAME}।\nপাওয়ারড বাই: {OWNER_TEAM}\n\nগ্রুপে আমাকে এড করুন আর মজা দেখুন!")

# --- RUN BOT ---
async def main():
    print(f"✅ {BOT_NAME} Online! Powered by {OWNER_TEAM}")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
