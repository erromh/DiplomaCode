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

    if request.method == 'POST':
        selected_option = request.form.get('option')
        
        if selected_option == 'Обучение':
            
            # Генерация данных для режима "Обучение"
            num_factors = np.random.randint(1, 4)  # Количество переменных-факторов: 1, 2 или 3
            num_observations = np.random.randint(10, 31)  # Количество наблюдений: от 10 до 30
            
            # Создание выборки данных
            data = np.random.rand(num_observations, num_factors)
            
            # Преобразование данных в строку по столбцам
            columns = ['\n'.join(map(str, data[:, i])) for i in range(num_factors)]
            result_text = '\n\n'.join(columns)

            selected_option = f"\nГенерированные данные для {num_factors} факторов и {num_observations} наблюдений: {result_text}"
        
        return render_template('main/index.html', selected_option=selected_option)
    
    return render_template('main/index.html', selected_option=None)

        