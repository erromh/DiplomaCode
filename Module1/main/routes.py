from flask import Blueprint, render_template, request
from flask_login import login_required
import numpy as np

main = Blueprint('main', __name__)

@main.route('/')
@main.route('/index')
@login_required
def index():
    return render_template('main/index.html')


@main.route('/mode_selection', methods=['GET', 'POST'])
def mode_selection():

    x_data = None
    
    result_text = (
        "Инструкция:\n"
        "Выберите режим 'Обучение' для генерации данных факторов.\n"
        "Выберите режим 'Экзамен' для прикрепления ссылок."
    )

    if request.method == 'POST':
        selected_option = request.form.get('option')
        
        if selected_option == 'Обучение':
            
            # Генерация данных для режима "Обучение"
            num_factors = np.random.randint(1, 4)  # Количество переменных-факторов: 1, 2 или 3
            num_observations = np.random.randint(10, 31)  # Количество наблюдений: от 10 до 30
            
            # Сгенерировать равномерно распределенные выборки факторов
            x1 = np.random.uniform(0, 100, num_observations)
            x2 = np.random.uniform(0, 10, num_observations) if num_factors > 1 else np.zeros(num_observations)
            x3 = np.random.uniform(0, 1000, num_observations) if num_factors > 2 else np.zeros(num_observations)
            
            x_data = (
                f"x1: {x1}\n"
                f"x2: {x2}\n"
                f"x3: {x3}\n"
            )

            # Сгенерировать равномерно распределенные параметры регрессионной модели
            a0 = np.random.uniform(-100, 100)
            a1 = np.random.uniform(-1, 1)
            a2 = np.random.uniform(-10, 10) if num_factors > 1 else 0
            a3 = np.random.uniform(-0.1, 0.1) if num_factors > 2 else 0
            
            # Рассчитать y_trend как линейную функцию от x с коэффициентами a
            y_trend = a0 + a1 * x1 + a2 * x2 + a3 * x3
            
            # Рассчитать y_trend_mean как среднее арифметическое выборки y_trend
            y_trend_mean = np.mean(y_trend)
            
            # Сгенерировать среднеквадратическое отклонение остатков std_e: 3% … 20% от y_trend_mean
            std_e = np.random.uniform(0.03, 0.2) * y_trend_mean
            
            # Проверка и корректировка std_e
            if std_e < 0:
                std_e = abs(std_e)
            if std_e == 0:
                std_e = 1e-6  

            # Сгенерировать нормально распределённую выборку остатков e с нулевым средним и стандартным отклонением std_e
            e = np.random.normal(0, std_e, num_observations)
            
            # Рассчитать значения показателя y = y_trend + e
            y = y_trend + e
                        
            result_text = (
                f"Сгенерированные данные:\n\n"
                f"Параметры регрессионной модели:\n"
                f"a0: {a0}\n"
                f"a1: {a1}\n"
                f"a2: {a2}\n"
                f"a3: {a3}\n\n"
                f"Рассчитанные значения y_trend:\n{y_trend}\n\n"
                f"Среднее y_trend_mean: {y_trend_mean}\n\n"
                f"Среднеквадратическое отклонение остатков std_e: {std_e}\n\n"
                f"Выборка остатков e:\n{e}\n\n"
                f"Рассчитанные значения y:\n{y}"
            )

            selected_option = result_text
        
        return render_template('main/index.html', selected_option=selected_option)
    
    return render_template('main/index.html', selected_option=None)

        