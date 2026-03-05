import telebot
import random
import re
import time

# --- কনফিগারেশন ---
TOKEN = "8626861144:AAGBFKDBubylAXt2tNpm9iru2pm-P4La4aI"
OWNER_TEAM = "Team BMT"
BOT_NAME = "BMT AI"

bot = telebot.TeleBot(TOKEN)

# --- এডভান্সড স্মার্ট ডাটা (Regex Pattern Based) ---
# এখানে আপনি যত বেশি প্যাটার্ন দিবেন, বট তত বুদ্ধিমান হবে
SMART_RESPONSES = [
    {
        'patterns': [r'\b(hi+|hello|hey+|হাই|হে|হ্যালো)\b'],
        'responses': ["হাই! কি খবর?", "হ্যালো ব্রো! টিম বিএমটি-তে স্বাগতম।", "নক দিলেন কেন? বিরিয়ানি খাওয়াবেন? 🍗"]
    },
    {
        'patterns': [r'kemon (acho|aco|ascho|asoc)', r'কেমন আছ', r'কি অবস্থা'],
        'responses': ["টিম বিএমটি-র পাওয়ারে অস্থির আছি!", "আপনার কথা ভেবে ভেবে দিন পার করছি। 😉", "ভালোই, আপনি কেমন?"]
    },
    {
        'patterns': [r'ki (koro|koros|korchen)', r'কি করো', r'কি করস'],
        'responses': ["বসে বসে আপনার মেসেজগুলো এনালিসিস করছি।", "সিস্টেম আপডেট দিচ্ছি বস!", "তোর জন্য একটা রোস্ট মেসেজ রেডি করছি। 😂"]
    },
    {
        'patterns': [r'(khai|khai|khawa) (hoise|hche)', r'খাওয়াদাওয়া করছ', r'কি খেয়েছ'],
        'responses': ["বটের আবার খাওয়া কি? আমি শুধু বিদ্যুৎ খাই! ⚡", "টিম বিএমটি-র মেমোরি চিবিয়ে খেলাম মাত্র।"]
    },
    {
        'patterns': [r'(gali|sala|kamina|khanki|faltu)', r'গালি', r'বাজে কথা'],
        'responses': ["মুখ সামলে! নাহলে একদম গ্রুপ থেকে কিক মেরে দেব। 🤫", "টিম বিএমটি-র বটকে গালি দেওয়ার সাহস কই পাস?", "তোর ভাষা ঠিক কর, নাহলে এডমিনকে বলছি!"]
    },
    {
        'patterns': [r'(bhalobashi|love|crush|পছন্দ করি)'],
        'responses': ["সরি, আমি শুধু কোডিং ভালোবাসি। ❤️", "আমার ডাটাবেসে আপনার জন্য কোনো জায়গা নেই!", "অই মিয়া! লজ্জা লাগে তো। 😊"]
    }
]

# --- ১. স্মার্ট মেসেজ হ্যান্ডলার ---
@bot.message_handler(func=lambda m: True if (m.text and not m.text.startswith('/')) else False)
def advanced_reply_logic(message):
    user_text = message.text.lower()
    bot_info = bot.get_me()
    sent = False

    # Regex Engine: এটা শব্দের ভেতর থেকে মূল কথা খুঁজে বের করে
    for item in SMART_RESPONSES:
        for pattern in item['patterns']:
            if re.search(pattern, user_text):
                # টাইপিং এনিমেশন (যাতে মনে হয় বট লিখছে)
                bot.send_chat_action(message.chat.id, 'typing')
                time.sleep(1) # ১ সেকেন্ড দেরি করবে রিয়েলিস্টিক করার জন্য
                
                reply = random.choice(item['responses'])
                bot.reply_to(message, f"🔥 {reply}\n\n— 𝖡𝗒 {OWNER_TEAM}")
                sent = True
                break
        if sent: break

    # ২. যদি কোনো প্যাটার্ন না মেলে কিন্তু বটের নাম নেয় বা রিপ্লাই দেয়
    if not sent:
        if BOT_NAME.lower() in user_text or (message.reply_to_message and message.reply_to_message.from_user.id == bot_info.id):
            fallback_replies = [
                "নাম ধরে ডাকলি কেন? কাজ থাকলে বল। 😎",
                "আমি সব বুঝি, কিন্তু এখন উত্তর দিতে ইচ্ছা করছে না।",
                "টিম বিএমটি-র বট সবসময় বিজি থাকে, ফালতু কথা কম বল!",
                "হুম, শুনছি তো? বলো কি বলবে?"
            ]
            bot.reply_to(message, f"🔥 {random.choice(fallback_replies)}\n\n— 𝖡𝗒 {OWNER_TEAM}")

# --- ২. স্টার্ট কমান্ড ---
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, f"আসসালামু আলাইকুম! আমি {BOT_NAME}।\nপাওয়ারড বাই: {OWNER_TEAM}\n\nগ্রুপে কথা বলতে আমাকে গ্রুপে এড দিন এবং আমার নাম নিন বা আমাকে রিপ্লাই দিন! আমি রিপলাই দিবো।")

# --- রান বট ---
print(f"✅ {BOT_NAME} Advance Chat System Online!")
bot.infinity_polling()
