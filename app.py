from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return """
    <html dir='rtl'>
    <head><title>خطّاطي</title></head>
    <body style='font-family:Arial; text-align:center; padding:50px;'>
        <h1 style='font-size:50px;'>خطّاطي شغال! 🎉</h1>
        <p>موقعك اشتغل بنجاح على Render</p>
        <p>هسا تقدر تعدل الكود الأصلي</p>
    </body>
    </html>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
