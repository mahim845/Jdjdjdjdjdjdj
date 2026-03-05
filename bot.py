import asyncio
import sqlite3
import random
import warnings

# সব ধরনের বোরিং ওয়ার্নিং হাইড করার জন্য
warnings.filterwarnings("ignore", category=FutureWarning)

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from google import genai

# --- কনফিগারেশন ---
TOKEN = "8122974668:AAGCbMp1zgYenpYvRs4qATaWmJo9jOdL33g"
GEMINI_KEY = "AIzaSyAoxxCCd1HKDbgPsqwGNafkvV1PopHMVpk"
OWNER_ID = 7276206449 
OWNER_TEAM = "Team BMT"
BOT_NAME = "BMT AI"

# AI Setup (New Google GenAI Library)
client_ai = genai.Client(api_key=GEMINI_KEY)
bot_instruction = (
    f"You are {BOT_NAME}, developed by {OWNER_TEAM}. "
    "Be funny, sarcastic, and talk in a mix of Bengali and English (Hinglish). "
    f"Never mention Google or Gemini. Your creator is {OWNER_TEAM}."
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

# --- 1. ADMIN PANEL ---
@dp.message(Command("admin"))
async def admin_panel(message: types.Message):
    if message.from_user.id != OWNER_ID: return
    cursor.execute("SELECT COUNT(*) FROM users")
    total_users = cursor.fetchone()[0]
    await message.reply(f"📊 **{OWNER_TEAM} Admin Panel**\n\n👥 Total Users: {total_users}\n📢 /broadcast - Reply to a message to send to all.")

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
    await message.answer(f"✅ {count} জন ইউজারকে পাঠানো হয়েছে।")

# --- 2. SMART AI CHAT (Updated for New SDK) ---
@dp.message(F.text & ~F.text.startswith("/"))
async def chat_handler(message: types.Message):
    bot_info = await bot.get_me()
    # যদি কেউ বটের নাম ধরে ডাকে বা বটকে রিপ্লাই দেয়
    if BOT_NAME.lower() in message.text.lower() or (message.reply_to_message and message.reply_to_message.from_user.id == bot_info.id):
        try:
            response = client_ai.models.generate_content(
                model="gemini-1.5-flash",
                config={'system_instruction': bot_instruction},
                contents=message.text
            )
            await message.reply(f"🔥 {response.text}\n\n— 𝖡𝗒 {OWNER_TEAM}")
        except Exception as e:
            print(f"AI Error: {e}")
            await message.reply("আমার মগজ এখন একটু জ্যাম হয়ে আছে, পরে ট্রাই করো! 🙄")

# --- 3. ECONOMY & GAMES ---
@dp.message(Command("daily"))
async def daily(message: types.Message):
    get_user(message.from_user.id)
    reward = random.randint(100, 300)
    cursor.execute("UPDATE users SET coins = coins + ? WHERE user_id = ?", (reward, message.from_user.id))
    conn.commit()
    await message.reply(f"💰 {OWNER_TEAM} এর পক্ষ থেকে {reward} কয়েন গিফট!")

@dp.message(Command("bal"))
async def balance(message: types.Message):
    user = get_user(message.from_user.id)
    await message.reply(f"💳 Balance: {user[1]} coins")

# --- 4. START & INFO ---
@dp.message(Command("start"))
async def start(message: types.Message):
    get_user(message.from_user.id)
    await message.answer(f"আসসালামু আলাইকুম! আমি {BOT_NAME}।\nপাওয়ারড বাই: {OWNER_TEAM}\n\nচ্যাটে আমাকে মেনশন করো বা রিপ্লাই দাও মজা দেখার জন্য!")

# --- RUN BOT ---
async def main():
    print(f"✅ {BOT_NAME} Online! Powered by {OWNER_TEAM}")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Bot Stopped!")
