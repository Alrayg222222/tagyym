from flask import Flask, request, jsonify
import requests
import os
from datetime import datetime
from dotenv import load_dotenv
import pprint

# تحميل متغيرات البيئة من ملف .env
load_dotenv()

app = Flask(__name__)

# جلب المتغيرات من البيئة
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID1 = os.environ.get("CHAT_ID1")
CHAT_ID2 = os.environ.get("CHAT_ID2")
PORT = int(os.environ.get("PORT", 5000))  # المنفذ الافتراضي 5000

# قائمة المعرفات
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
            response = requests.post(url, data=data)
            if not response.ok:
                print(f"❌ فشل الإرسال إلى {chat_id}: {response.text}")

# استقبال بيانات التقييم من Webhook
@app.route('/webhook', methods=['POST'])
def receive_review():
    print("======================================")
    print("📥 تم استلام طلب Webhook")

    # طباعة البيانات الخام JSON والـ RAW
    print("🔴 Raw request.data:")
    print(request.data)

    print("🔵 Parsed request.json:")
    data = request.json
    pprint.pprint(data)

    # استخراج البيانات من المستوى الأول فقط (مسطحة)
    customer = data.get("name") or data.get("customer_name") or "عميل غير معروف"
    rating = data.get("rating") or "بدون تقييم"
    comment = data.get("comment") or "لا يوجد تعليق"
    product = data.get("product") or data.get("product_name") or "منتج غير معروف"

    # التاريخ الحالي
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    # تنسيق الرسالة
    message = f"""📬 *تقييم جديد من أحد العملاء*

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
