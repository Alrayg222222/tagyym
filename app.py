from flask import Flask, request, jsonify
import requests
import os
from datetime import datetime
from dotenv import load_dotenv

# تحميل متغيرات البيئة
load_dotenv()

app = Flask(__name__)

# إعدادات من البيئة
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID1 = os.environ.get("CHAT_ID1")
CHAT_ID2 = os.environ.get("CHAT_ID2")
PORT = int(os.environ.get("PORT", 5000))

# قائمة المعرفات
CHAT_IDS = [CHAT_ID1, CHAT_ID2]

# دالة إرسال رسالة Telegram
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

# نقطة استقبال Webhook
@app.route('/webhook', methods=['POST'])
def receive_review():
    data = request.json
    review_data = data.get("data", {})

    customer = review_data.get("customer", {}).get("name", "عميل غير معروف")
    rating = review_data.get("rating", "بدون تقييم")
    comment = review_data.get("content", "لا يوجد تعليق")

    product = "منتج غير معروف"
    order = review_data.get("order", {})
    items = order.get("items", [])
    if items and isinstance(items, list):
        product = items[0].get("name", product)

    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    message = f"""📬 *تقييم جديد من أحد العملاء*

👤 الاسم: **{customer}**
📝 التعليق: {comment}
⭐ عدد النجوم: {rating}
📦 المنتج: {product}
🕒 التاريخ: {now}
"""

    send_telegram_message(message)
    return jsonify({"status": "success"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT)
