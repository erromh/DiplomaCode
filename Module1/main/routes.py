from flask import Blueprint, render_template, request
from flask_login import login_required
import statsmodels.api as sm
from scipy import stats
import numpy as np

main = Blueprint('main', __name__)

@main.route('/')
@main.route('/index')
@login_required
def index():
    return render_template('main/index.html')


@main.route('/mode_selection', methods=['GET', 'POST'])
def mode_selection():

    selected_option = None
    x_data = None
    
    result_text = None

    if request.method == 'POST':
        selected_option = request.form.get('option')
        tab_selected = request.form.get('tab_selected')

        if selected_option == 'Обучение':
            
            # Генерация данных для режима "Обучение"
            num_factors = np.random.randint(1, 5)  # Количество переменных-факторов: 1, 2, 3, 4
            num_observations = np.random.randint(10, 31)  # Количество наблюдений: от 10 до 30
            
            # Сгенерировать равномерно распределенные выборки факторов
            x1 = np.random.uniform(0, 100, num_observations)
            x2 = np.random.uniform(0, 10, num_observations) if num_factors > 1 else np.zeros(num_observations)
            x3 = np.random.uniform(0, 1000, num_observations) if num_factors > 2 else np.zeros(num_observations)
            x4 = np.random.uniform(0, 100, num_observations) if num_factors > 2 else np.zeros(num_observations)

            x_data = (
                f"\nПостроить модель регрессии из исходных данных, оценить качество модели, построить прогноз.\n\n"

                f"Рассчитать y_trend как линейную функцию от x с коэффициентами a\n\n"
                f"Рассчитать y_trend_mean как среднее арифметическое выборки y_trend\n\n"
                f"Сгенерировать среднеквадратическое отклонение остатков std_e: 3% … 20% от y_trend_mean\n\n"
                f"Сгенерировать нормально распределённую выборку остатков e с нулевым средним и стандартным отклонением std_e\n\n"
                f"Рассчитать значения показателя y = y_trend + e\n\n"
                f"Построить диаграммы y(x1), y(x2), y(x3), визуально проверить наличие тренда и случайности в этих зависимостях.\n\n"

                f"Исходные данные:\n\n"
                
                "x1:\n" + "\n".join([f"{x:.10f}" for x in x1]) +
                "\n\nx2:\n" + "\n".join([f"{x:.10f}" for x in x2]) +
                "\n\nx3:\n" + "\n".join([f"{x:.10f}" for x in x3]) 
                # "\n\nx4:\n" + "\n".join([f"{x:.10f}" for x in x4])
            )

            # Сгенерировать равномерно распределенные параметры регрессионной модели
            a0 = np.random.uniform(-100, 100)
            a1 = np.random.uniform(-1, 1)
            a2 = np.random.uniform(-10, 10) if num_factors > 1 else 0
            a3 = np.random.uniform(-0.1, 0.1) if num_factors > 2 else 0
            
            # Рассчитать y_trend как линейную функцию от x с коэффициентами a
            y_trend = a0 + a1 * x1 + a2 * x2 + a3 * x3
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
                        
            data_matrix = np.array([x1, x2, x3, y])

            # Матрица коэффициентов парной корреляции
            correlation_matrix = np.corrcoef(data_matrix)

            # Построение модели регрессии
            X = sm.add_constant(np.column_stack((x1, x2, x3)))  # Добавляем константу
            model = sm.OLS(y, X).fit()

            # Вывод результатов регрессии
            model_summary = model.summary().as_text()

            # Расчетное значение F-критерия
            F_value = model.fvalue

            # Табличное значение F-критерия для выбранного уровня значимости и степеней свободы
            alpha = 0.05
            df_reg = model.df_model
            df_resid = model.df_resid
            F_table = stats.f.ppf(1 - alpha, df_reg, df_resid)

            # Вывод о значимости модели
            if F_value > F_table:
                significance_model = "Модель является статистически значимой"
            else:
                significance_model = "Модель не является статистически значимой"

            # Вычисление t-статистики и p-значения для каждого параметра модели
            t_values = model.tvalues
            p_values = model.pvalues

            # Табличное значение t-критерия для выбранного уровня значимости и количества степеней свободы
            t_table = stats.t.ppf(1 - alpha / 2, df_resid)  # Для двустороннего теста

            # Вывод о значимости каждого параметра модели
            significance_params = []
            for i in range(len(t_values)):
                if abs(t_values[i]) > t_table:
                    significance_params.append("Значимый")
                else:
                    significance_params.append("Незначимый")

            # Критерий детерминации R^2
            R_squared = model.rsquared

            # Фактические значения
            actual_values = np.array(y)

            # Прогнозируемые значения
            predicted_values = model.predict()

            # Средняя относительная ошибка
            MRE = np.mean(np.abs((actual_values - predicted_values) / actual_values)) * 100

            # Максимальные наблюдаемые значения x
            max_x1 = max(x1)
            max_x2 = max(x2)
            max_x3 = max(x3)

            # Увеличение значений x на 10% и 20%
            new_x1_10 = max_x1 * 1.1
            new_x1_20 = max_x1 * 1.2

            new_x2_10 = max_x2 * 1.1
            new_x2_20 = max_x2 * 1.2

            new_x3_10 = max_x3 * 1.1
            new_x3_20 = max_x3 * 1.2

            # Прогнозирование значений y для новых значений x
            predicted_y_10 = model.predict([1, new_x1_10, new_x2_10, new_x3_10])
            predicted_y_20 = model.predict([1, new_x1_20, new_x2_20, new_x3_20])

            # Подготовить текст для вывода в textarea
            correlation_matrix
            model_summary 
            F_value
            F_table
            significance_model
            
            result_text = (
                f"\nПараметры регрессионной модели:\n"
                f"a0: {a0}\n"
                f"a1: {a1}\n"
                f"a2: {a2}\n"
                f"a3: {a3}\n\n"
                f"Рассчитанные значения y_trend:\n{y_trend}\n\n"
                f"Среднее y_trend_mean: {y_trend_mean}\n\n"
                f"Среднеквадратическое отклонение остатков std_e: {std_e}\n\n"
                f"Выборка остатков e:\n{e}\n\n"
                f"Рассчитанные значения y:\n{y}\n\n"
                "Матрица коэффициентов парной корреляции:\n"
                f"{correlation_matrix}\n\n"
                "Результаты регрессии:\n"
                f"{model_summary}\n\n"
                "Критерий использован: F-критерий\n"
                f"Расчетное значение F-критерия: {F_value}\n"
                f"Табличное значение F-критерия: {F_table}\n"
                f"Вывод о значимости модели: {significance_model}\n\n"
                "Критерий использован: t-статистика\n"
            )

            selected_option = x_data    #result_text
            
            return render_template('main/index.html', selected_option=selected_option, x_data=x_data, result_text=result_text, tab_selected=tab_selected)

    return render_template('main/index.html', selected_option=None, tab_selected='home')

        