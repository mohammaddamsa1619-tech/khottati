from flask import Flask, request, jsonify
import os
from openai import OpenAI

app = Flask(__name__)

api_key = os.environ.get("OPENAI_API_KEY")
client = OpenAI(api_key=api_key) if api_key else None

# صفحة رئيسية بتشتغل دائماً
@app.route('/')
def home():
    # بنحاول نجيب index.html اذا موجود
    if os.path.exists('index.html'):
        with open('index.html', 'r', encoding='utf-8') as f:
            return f.read()
    else:
        # اذا مش موجود، بنعرض صفحة تجريبية
        return """
        <html dir='rtl'><head><title>خطّتي</title>
        <meta charset='utf-8'>
        <meta name='viewport' content='width=device-width'>
        <style>
        body{font-family:Arial; text-align:center; padding:30px; background:#f0f9ff}
       .box{background:white; padding:30px; border-radius:15px; max-width:600px; margin:0 auto; box-shadow:0 4px 10px rgba(0,0,0,0.1)}
        input{padding:12px; width:70%; border:2px solid #0ea5e9; border-radius:8px; margin:10px}
        button{padding:12px 25px; background:#0ea5e9; color:white; border:none; border-radius:8px; cursor:pointer; font-size:16px}
        #result{margin-top:20px; text-align:right; background:#f8fafc; padding:15px; border-radius:8px; display:none}
        </style>
        </head>
        <body>
        <div class='box'>
        <h1>🎉 خطّتي شغال!</h1>
        <p>موقعك على Render اشتغل بنجاح</p>
        <input id='lesson' placeholder='اكتب اسم الدرس مثلا: الجمع'>
        <br><button onclick='generate()'>إنشاء شرح</button>
        <div id='result'></div>
        </div>
        <script>
        async function generate(){
            const lesson = document.getElementById('lesson').value || 'الجمع';
            document.getElementById('result').style.display='block';
            document.getElementById('result').innerHTML='جاري التحضير...';
            const res = await fetch('/api/generate', {
                method:'POST',
                headers:{'Content-Type':'application/json'},
                body: JSON.stringify({lesson})
            });
            const data = await res.json();
            document.getElementById('result').innerHTML = '<b>الشرح:</b><br>' + data.explanation;
        }
        </script>
        </body></html>
        """

@app.route('/api/generate', methods=['POST'])
def generate():
    data = request.get_json()
    lesson = data.get('lesson', 'الجمع')
    explanation = f"شرح مبسط لدرس {lesson}: نشرحه بثلاث خطوات عملية مع أمثلة من حياة الطفل."

    if client:
        try:
            prompt = f"انت معلم أردني للصف الأول، اشرح درس {lesson} في 3 جمل بسيطة بالعربي."
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role":"user", "content": prompt}]
            )
            explanation = response.choices[0].message.content
        except Exception as e:
            explanation = f"شرح {lesson} (وضع تجريبي): {str(e)}"

    return jsonify({"explanation": explanation})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000)
