import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import numpy as np
import statsmodels.api as sm
from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder_unfiltered.csv')

app = Dash(__name__)

app.layout = html.Div([
    html.H1(children='App', style={'textAlign':'center'}),
    dcc.Dropdown(df.country.unique(), 'Ciii', id='dropdown-selection'),
    dcc.Graph(id='graph-content')
])

@callback(
    Output('graph-content', 'figure'),
    Input('dropdown-selection', 'value')
)
def update_graph(value):
    dff = df[df.country==value]
    return px.line(dff, x='year', y='pop')

if __name__ == '__main__':
    app.run(debug=True)
# Генерация псевдослучайных данных
np.random.seed(0)
n = 100
x = np.random.rand(n)
y = 2 * x + np.random.randn(n)

data = pd.DataFrame({'X': x, 'Target_Variable': y})

# Создание Dash-приложения
app = dash.Dash(__name__)

# Определение макета приложения
app.layout = html.Div([
    dcc.Graph(id='scatter-plot'),
    html.Div([
        html.Label('Выберите переменную X:'),
        dcc.Dropdown(
            id='dropdown-x',
            options=[{'label': col, 'value': col} for col in data.columns],
            value='X'
        ),
    ])
])

# Определение callback для обновления графика рассеяния
@app.callback(
    Output('scatter-plot', 'figure'),
    [Input('dropdown-x', 'value')]
)
def update_scatter_plot(selected_x):
    # Построение модели парной регрессии
    X = sm.add_constant(data[selected_x])
    y = data['Target_Variable']
    model = sm.OLS(y, X).fit()

    # Отображение графика рассеяния и регрессионной прямой
    fig = px.scatter(x=data[selected_x], y=y, trendline="ols", trendline_color_override="red")
    fig.update_layout(title=f'Парная регрессия: {selected_x} vs Target Variable',
                      xaxis_title=selected_x,
                      yaxis_title='Target Variable')
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
