from flask import Flask, render_template, request, flash, redirect, url_for

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Зберігання даних для простоти (можна замінити на базу даних)
work_data = []

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Отримання даних з форми
        date = request.form.get("date")
        start_time = request.form.get("start_time")
        end_time = request.form.get("end_time")

        # Перевірка, чи всі поля заповнені
        if date and start_time and end_time:
            # Розрахунок пропрацьованих годин
            start_hours, start_minutes = map(int, start_time.split(":"))
            end_hours, end_minutes = map(int, end_time.split(":"))
            total_hours = (end_hours + end_minutes / 60) - (start_hours + start_minutes / 60)

            # Збереження даних
            work_data.append({"date": date, "hours": round(total_hours, 2)})

            flash(f"Дані збережено. Ви пропрацювали {round(total_hours, 2)} годин у цей день.", "success")
        else:
            flash("Будь ласка, заповніть усі поля форми.", "error")

        return redirect(url_for("index"))

    # Створення звіту за місяць
    monthly_report = {}
    for record in work_data:
        month = record["date"][:7]  # Отримати рік-місяць з дати
        monthly_report[month] = monthly_report.get(month, 0) + record["hours"]

    return render_template("index.html", monthly_report=monthly_report)

if __name__ == "__main__":
    app.run(debug=True)
