from flask import Flask, request, jsonify, send_from_directory
import os

app = Flask(__name__)

@app.route('/')
def home():
    if os.path.exists('index.html'):
        with open('index.html', 'r', encoding='utf-8') as f:
            return f.read()
    return "index.html not found"

@app.route('/<path:path>')
def static_files(path):
    return send_from_directory('.', path)

@app.route('/api/generate', methods=['POST'])
def generate():
    data = request.get_json()
    lesson = data.get('lesson', 'الجمع')

    # قوالب جاهزة بتشتغل بدون OpenAI
    templates = {
        "الجمع": "1️⃣ نجمع الأشياء مع بعض. 2️⃣ نعد كم صاروا. 3️⃣ مثال: 2 تفاحة + 1 تفاحة = 3 تفاحات!",
        "الطرح": "1️⃣ كان عندنا كثير. 2️⃣ أخذنا منهم. 3️⃣ مثال: كان عندنا 5 حلوى، أكلنا 2، بقي 3!",
        "default": f"📚 درس {lesson}: 1️⃣ نقرأ اسم الدرس. 2️⃣ نفهم الفكرة بكلمات بسيطة. 3️⃣ نطبق بمثال من حياتنا اليومية. مثال: لو درسنا {lesson}، نفكر كيف نستخدمه في البيت!"
    }

    # نحاول نستخدم OpenAI اذا في رصيد
    explanation = templates.get(lesson, templates["default"])

    try:
        from openai import OpenAI
        api_key = os.environ.get("OPENAI_API_KEY")
        if api_key:
            client = OpenAI(api_key=api_key)
            prompt = f"اشرح درس {lesson} لطفل صف أول في 3 جمل بسيطة"
            res = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role":"user","content":prompt}]
            )
            explanation = res.choices[0].message.content
    except Exception as e:
        print(f"Using fallback: {e}")
        # بنستخدم القالب الجاهز

    return jsonify({
        "explanation": explanation,
        "summary": f"ملخص {lesson}",
        "worksheet": "#",
        "infographic": "#"
    })

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000)
