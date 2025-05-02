
from flask import Flask, request, jsonify
import requests
import os
from datetime import datetime
from dotenv import load_dotenv

# تحميل متغيرات البيئة من ملف .env
load_dotenv()

app = Flask(__name__)

# جلب المتغيرات من البيئة
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID1 = os.environ.get("CHAT_ID1")
CHAT_ID2 = os.environ.get("CHAT_ID2")
PORT = int(os.environ.get("PORT", 5000))  # المنفذ الافتراضي 5000

# قائمة المعرفات (يمكنك الإضافة إذا عندك أكثر من شخص)
CHAT_IDS = [CHAT_ID1, CHAT_ID2]

# دالة إرسال رسالة لتليجرام
def send_telegram_message(message):
    for chat_id in CHAT_IDS:
        if chat_id:
            url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
            data = {
                "chat_id": chat_id,
                "text": message,
                "parse_mode": "Markdown"
            }
            requests.post(url, data=data)

# استقبال بيانات التقييم من Webhook
@app.route('/webhook', methods=['POST'])
def receive_review():
    data = request.json

    # استخراج البيانات المطلوبة
    customer = data.get("customer", {}).get("name", "عميل غير معروف")
    rating = data.get("review", {}).get("rating", "بدون تقييم")
    comment = data.get("review", {}).get("comment", "لا يوجد تعليق")
    product = data.get("product", {}).get("name", "منتج غير معروف")

    # التاريخ الحالي
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    # تنسيق الرسالة النهائية
    message = f"""تقييم جديد من أحد العملاء


\n\n\n
👤 الاسم: **{customer}**
📝 التعليق: {comment}
⭐ عدد النجوم: {rating}
📦 المنتج: {product}

🕒 التاريخ: {now}
"""

    # إرسال الرسالة
    send_telegram_message(message)
    return jsonify({"status": "success"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT)
