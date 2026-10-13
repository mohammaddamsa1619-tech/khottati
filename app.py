from flask import Flask, request, jsonify, send_from_directory
import os
from openai import OpenAI

app = Flask(__name__, static_folder='.')

api_key = os.environ.get("OPENAI_API_KEY")
client = OpenAI(api_key=api_key) if api_key else None

@app.route('/')
def home():
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def static_files(path):
    return send_from_directory('.', path)

@app.route('/api/generate', methods=['POST'])
def generate():
    try:
        data = request.get_json()
        lesson = data.get('lesson', 'درس الجمع')

        explanation = f"شرح مبسط لدرس {lesson} بثلاث خطوات عملية للأطفال مع أمثلة من الحياة اليومية."

        if client:
            try:
                prompt = f"انت معلم أردني للصف الأول. اشرح درس {lesson} في 3 جمل قصيرة بسيطة بالعربي."
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role":"user", "content": prompt}]
                )
                explanation = response.choices[0].message.content
            except Exception as e:
                print(f"OpenAI Error: {e}")

        return jsonify({
            "worksheet": "#",
            "summary": "#",
            "infographic": "#",
            "mindmap": "#",
            "flashcards": "#",
            "explanation": explanation,
            "summary_text": f"ملخص درس {lesson}"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000)
