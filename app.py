import numpy as np
import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# Генерация случайных данных для примера
np.random.seed(42)
X = np.random.rand(100, 1) * 10
y = 2 * X + 1 + np.random.randn(100, 1) * 2

# Применение метода наименьших квадратов для простой линейной регрессии
coefficients = np.polyfit(X.flatten(), y.flatten(), 1)
slope, intercept = coefficients

# Создание предсказаний для графика
x_range = np.linspace(min(X), max(X), 100)
y_pred = slope * x_range + intercept

# Инициализация Dash
app = dash.Dash(__name__)

# Создание макета
app.layout = html.Div([
    dcc.Graph(
        id='scatter-plot',
        figure={
            'data': [
                {'x': X.flatten(), 'y': y.flatten(), 'mode': 'markers', 'name': 'Data'},
                {'x': x_range, 'y': y_pred, 'mode': 'lines', 'name': 'Regression Line'}
            ],
            'layout': {
                'title': 'Простая линейная регрессия',
                'xaxis': {'title': 'X'},
                'yaxis': {'title': 'Y'}
            }
        }
    )
])

# Запуск приложения Dash
if __name__ == '__main__':
    app.run_server(debug=True)
