import random
import statistics
import numpy as np
import dash
from dash import dcc, html, Input, Output, State
import plotly.graph_objs as go
import statsmodels.api as sm
from scipy import stats

app = dash.Dash(__name__)

# Генерация данных
m = random.randint(1, 3)
n = random.randint(10, 30)

x1 = [random.uniform(0, 100) for _ in range(n)]
x2 = [random.uniform(0, 10) for _ in range(n)]
x3 = [random.uniform(0, 1000) for _ in range(n)]

a0 = random.uniform(-100, 100)
a1 = random.uniform(-1, 1)
a2 = random.uniform(-10, 10)
a3 = random.uniform(-0.1, 0.1)

y_trend = [a0 + a1 * x1[i] + a2 * x2[i] + a3 * x3[i] for i in range(n)]
y_trend_mean = statistics.mean(y_trend)

std_e_percent_range = (3, 20)
std_e_min = y_trend_mean * (std_e_percent_range[0] / 100)
std_e_max = y_trend_mean * (std_e_percent_range[1] / 100)
std_e = random.uniform(std_e_min, std_e_max)

e = [random.normalvariate(0, std_e) for _ in range(n)]
y = [y_trend[i] + e[i] for i in range(n)]

# Матрица, включающая x1, x2, x3, y
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

# Форматирование текстовых данных
text_data = [
    f"Количество переменных - факторов x: {m}",
    f"Количество наблюдений n в выборке: {n}",
    f"Выборка для x1: {x1}",
    f"Выборка для x2: {x2}",
    f"Выборка для x3: {x3}",
    f"Параметр a0: {a0:.2f}",
    f"Параметр a1: {a1:.2f}",
    f"Параметр a2: {a2:.2f}",
    f"Параметр a3: {a3:.2f}",
    f"Среднее значение y_trend: {y_trend_mean:.2f}",
    f"Среднеквадратическое отклонение остатков std_e: {std_e:.2f}",
    f"Выборка остатков e: {e}",
    f"Значения показателя y: {y}",
    "Матрица коэффициентов парной корреляции:",
    f"{correlation_matrix}",
    "Результаты регрессии:",
    f"{model_summary}",
    f"Критерий использован: F-критерий",
    f"Расчетное значение F-критерия: {F_value}",
    f"Табличное значение F-критерия: {F_table}",
    f"Вывод о значимости модели: {significance_model}",
    "Критерий использован: t-статистика",
]

for i in range(len(t_values)):
    text_data.extend([
        f"Параметр a{i}:",
        f"  Расчетное значение t-статистики: {t_values[i]}",
        f"  Табличное значение t-критерия: {t_table}",
        f"  P-значение: {p_values[i]}",
        f"  Вывод о значимости параметра модели: {significance_params[i]}"
    ])

text_data.extend([
    f"Критерий детерминации R^2: {R_squared}",
    f"Средняя относительная ошибка: {MRE}%",
    f"Прогнозное значение y при увеличении x на 10%: {predicted_y_10}",
    f"Прогнозное значение y при увеличении x на 20%: {predicted_y_20}"
])

app.layout = html.Div([
    html.H1('Диаграммы распределения y от x1, x2 и x3'),

    # Вывод текстовых данных
    html.Div([html.P(text) for text in text_data]),

    dcc.Graph(
        id='y-x1',
        figure={
            'data': [
                go.Scatter(
                    x=x1,
                    y=y,
                    mode='markers',
                    marker={'color': 'blue'},
                    name='y(x1)'
                )
            ],
            'layout': go.Layout(
                title='Диаграмма y(x1)',
                xaxis={'title': 'x1'},
                yaxis={'title': 'y'},
                legend={'x': 0, 'y': 1},
                hovermode='closest'
            )
        }
    ),

    dcc.Graph(
        id='y-x2',
        figure={
            'data': [
                go.Scatter(
                    x=x2,
                    y=y,
                    mode='markers',
                    marker={'color': 'red'},
                    name='y(x2)'
                )
            ],
            'layout': go.Layout(
                title='Диаграмма y(x2)',
                xaxis={'title': 'x2'},
                yaxis={'title': 'y'},
                legend={'x': 0, 'y': 1},
                hovermode='closest'
            )
        }
    ),

    dcc.Graph(
        id='y-x3',
        figure={
            'data': [
                go.Scatter(
                    x=x3,
                    y=y,
                    mode='markers',
                    marker={'color': 'green'},
                    name='y(x3)'
                )
            ],
            'layout': go.Layout(
                title='Диаграмма y(x3)',
                xaxis={'title': 'x3'},
                yaxis={'title': 'y'},
                legend={'x': 0, 'y': 1},
                hovermode='closest'
            )
        }
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
