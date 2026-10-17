import os

from flask import Flask, render_template, request
from google import genai
app = Flask(__name__)

API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=API_KEY)

MODEL_NAME = "gemini-3.5-flash-lite"

PRESETS = {
    "1. Пояснення": "Поясни поняття штучного інтелекту простою мовою для початківця.",
    "2. Генерація тексту": "Склади короткий фентезі-сценарій про робота, який навчився відчувати емоції (до 100 слів).",
    "3. Переклад": "Переклади наступний текст англійською мовою: 'Штучний інтелект змінює сучасний світ та допомагає вирішувати складні завдання.'",
    "4. Узагальнення": "Скороти та узагальни текст до 1 речення: 'Машинне навчання — це підрозділ штучного інтелекту, що займається створенням алгоритмів, які здатні самостійно навчатися на основі даних без явного програмування кожного кроку.'",
    "5. Генерація списку": "Сформуй список із 5 найпопулярніших мов програмування для роботи з ШІ та вкажи їх основну перевагу.",
    "6. Zero-shot":
        "Визнач рівень мови програмування (High-level або Low-level) за"
        ' описом:\n"Python має простий синтаксис, автоматичне управління'
        ' пам\'яттю та динамічну типізацію."',
    "7. Few-shot": 
        "Визнач рівень мови програмування (High-level або Low-level) за"
        " описом.\n\nПриклад 1: Асемблер використовує мнемоніки для адресації"
        " команд процесора. -> Low-level\nПриклад 2: C++ надає прямий доступ до"
        " пам'яті через вказівники та керування ресурсами. -> Low-level\n\nЗавдання:"
        ' Python має простий синтаксис, автоматичне управління пам\'яттю та'
        " динамічну типізацію. ->",
    "Свій власний запит": ""
}

ROLES = {
    "Без ролі (Стандартний асистент)": None,
    "Викладач": "Ти дружній викладач комп'ютерних наук. Пояснюй наочно та прикладами з реального життя.",
    "Програміст": "Ти Senior Python Developer. Надавай лаконічне пояснення, чистий код та акцентуй увагу на ефективності.",
    "Науковець": "Ти доктор комп'ютерних наук. Відповідай строгою академічною та науковою мовою, висвітлюючи теоретичні підвалини."
}

@app.route('/', methods=['GET', 'POST'])
def index():
    selected_preset = request.form.get('preset', '1. Пояснення')
    prompt = request.form.get('prompt', PRESETS.get(selected_preset, ''))
    selected_role = request.form.get('role', 'Без ролі (Стандартний асистент)')
    
    result = ""

    if request.method == 'POST':
        system_instruction = ROLES.get(selected_role)
        
        config = {}
        if system_instruction:
            config["system_instruction"] = system_instruction

        try:
            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=prompt,
                config=config if config else None
            )
            result = response.text if response and response.text else "Відповідь порожня."
        except Exception as e:
            result = f"Помилка при виконанні запиту:\n{str(e)}"

    return render_template(
        'index.html',
        presets=PRESETS,
        roles=ROLES,
        selected_preset=selected_preset,
        selected_role=selected_role,
        prompt=prompt,
        result=result
    )


if __name__ == '__main__':
    app.run(debug=True, port=5000)