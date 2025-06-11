import pandas as pd
from flask import Blueprint, render_template, request
from .modelo import modelo
import sqlite3
from datetime import datetime


main = Blueprint('main',__name__)

def get_connection():
    return sqlite3.connect('casos_covid19_colombia.db')

def get_departamentos():
    conn = sqlite3.connect('casos_covid19_colombia.db')
    cursor = conn.cursor()
    cursor.execute("SELECT departamento, departamento_nom FROM departamentos ORDER BY departamento_nom")
    departamentos = cursor.fetchall() 
    conn.close()
    return departamentos

@main.route('/', methods=['GET', 'POST'])
def index():
    prediccion = None
   

    if request.method == 'POST':
        fecha = request.form['fecha']
        fecha_dt = datetime.strptime(fecha, '%Y-%m-%d')
        data = {
            'año': fecha_dt.year,
            'mes': fecha_dt.month,
            'dia': fecha_dt.day,
            'departamento':int(request.form['departamento']),
            'edad':int(request.form['edad']),
            'sexo_F':int(request.form['sexo'] == 'Femenino'),
            'sexo_M':int(request.form['sexo'] == 'Masculino'),
            'fuente_tipo_contagio':int(request.form['fuente_tipo_contagio'])
        }

        df = pd.DataFrame([data], columns=list(data.keys()))
        print(df)

        print("ayayay")

        prediccion = modelo.predict(df)[0]
        print(prediccion)

    departamentos = get_departamentos()
    return render_template('index.html', prediccion=prediccion, departamentos=departamentos)
