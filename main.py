import math
from flask import Flask
import threading
import re
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = "8616036912:AAGsQzGbM86qVOqFt2fcTAGF3qkGaLbE62I"

# ========== বাংলা + English Keyword ==========
LOMBO = ["lombo", "height", "h", "উচ্চতা"]
VUMI = ["vumi", "base", "b", "ভূমি"]
OTIVUJ = ["otivuj", "hypotenuse", "hyp", "অতিভুজ"]

def detect_lang(text):
    eng_words = ["height", "base", "hypotenuse", "find", "what", "calculate"]
    if any(word in text.lower() for word in eng_words):
        return "en"
    return "bn"

def find_numbers(text):
    nums = re.findall(r'\d+\.?\d*', text)
    return [float(n) for n in nums]

def find_keyword(text, word_list):
    text = text.lower()
    for word in word_list:
        if word in text:
            return True
    return False

# ========== Ch-9 Math Functions ==========
def calc_hypotenuse(a, b):
    return math.sqrt(a**2 + b**2)

def calc_area(a, b):
    return 0.5 * a * b

def calc_sin(a, c):
    return a / c

def calc_cos(b, c):
    return b / c

def calc_tan(a, b):
    return a / b

# ========== Bot Commands ==========
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = """👋 **Sir AI তে স্বাগতম!** আমি SSC Math Ch-9 ত্রিকোণমিতি সলভ করি। **কেমনে লিখবেন:** বাংলা: `lombo 5 vumi 12` English: `height 5 base 12` **আমি বের করবো:** অতিভুজ, ক্ষেত্রফল, sin, cos, tan ট্রাই করেন 👇"""
    await update.message.reply_text(msg)

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = """**Sir AI Help 📐** **Example 1:** `lombo 5 vumi 12` **Example 2:** `height 5 base 12` **Example 3:** `otivuj 13 lombo 5` যেকোনো 2টা বাহু দিলেই হবে।"""
    await update.message.reply_text(msg)

async def solve_math(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    lang = detect_lang(text)
    nums = find_numbers(text)
    if len(nums) < 2:
        if lang == "en":
            await update.message.reply_text("Please give 2 numbers. Ex: height 5 base 12")
        else:
            await update.message.reply_text("দয়া করে 2টা সংখ্যা দিন। যেমন: lombo 5 vumi 12")
        return

    has_lombo = find_keyword(text, LOMBO)
    has_vumi = find_keyword(text, VUMI)
    has_otivuj = find_keyword(text, OTIVUJ)

    try:
        if has_lombo and has_vumi:
            a, b = nums[0], nums[1]
            c = calc_hypotenuse(a, b)
            area = calc_area(a, b)
            sin_a = calc_sin(a, c)
            cos_a = calc_cos(b, c)
            tan_a = calc_tan(a, b)
            if lang == "en":
                reply = f"""**Right Triangle Solved 📐** Height = {a}, Base = {b} **Hypotenuse** = {c:.2f} **Area** = {area:.2f} sq unit **sin θ** = {sin_a:.3f} **cos θ** = {cos_a:.3f} **tan θ** = {tan_a:.3f}"""
            else:
                reply = f"""**সমকোণী ত্রিভুজ সমাধান 📐** লম্ব = {a}, ভূমি = {b} **অতিভুজ** = {c:.2f} **ক্ষেত্রফল** = {area:.2f} বর্গ একক **sin θ** = {sin_a:.3f} **cos θ** = {cos_a:.3f} **tan θ** = {tan_a:.3f}"""

        elif has_lombo and has_otivuj:
            a, c = nums[0], nums[1]
            if c <= a: raise ValueError("Hypotenuse must be bigger")
            b = math.sqrt(c**2 - a**2)
            area = calc_area(a, b)
            if lang == "en":
                reply = f"""**Right Triangle Solved 📐** Height = {a}, Hypotenuse = {c} **Base** = {b:.2f} **Area** = {area:.2f} sq unit"""
            else:
                reply = f"""**সমকোণী ত্রিভুজ সমাধান 📐** লম্ব = {a}, অতিভুজ = {c} **ভূমি** = {b:.2f} **ক্ষেত্রফল** = {area:.2f} বর্গ একক"""

        elif has_vumi and has_otivuj:
            b, c = nums[0], nums[1]
            if c <= b: raise ValueError("Hypotenuse must be bigger")
            a = math.sqrt(c**2 - b**2)
            area = calc_area(a, b)
            if lang == "en":
                reply = f"""**Right Triangle Solved 📐** Base = {b}, Hypotenuse = {c} **Height** = {a:.2f} **Area** = {area:.2f} sq unit"""
            else:
                reply = f"""**সমকোণী ত্রিভুজ সমাধান 📐** ভূমি = {b}, অতিভুজ = {c} **লম্ব** = {a:.2f} **ক্ষেত্রফল** = {area:.2f} বর্গ একক"""
        else:
            if lang == "en":
                reply = "Can't understand. Try: height 5 base 12"
            else:
                reply = "বুঝি নাই। এভাবে লিখুন: lombo 5 vumi 12"

        await update.message.reply_text(reply)

    except Exception as e:
        if lang == "en":
            await update.message.reply_text("Math error! Check your numbers. Hypotenuse must be largest.")
        else:
            await update.message.reply_text("অঙ্কে ভুল! সংখ্যা চেক করেন। অতিভুজ সবচেয়ে বড় হবে।")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, solve_math))
    print("Sir AI is Running...")
    app.run_polling()

# === Render Free Hack এর জন্য Flask Code ===
flask_app = Flask(__name__)

@flask_app.route('/')
def home():
    return "Sir AI is Alive!"

def run_flask():
    flask_app.run(host='0.0.0.0', port=10000)

if __name__ == "__main__":
    threading.Thread(target=run_flask).start()
    main()
