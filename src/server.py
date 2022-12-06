from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

df = pd.read_csv('data/result.csv', sep=',')

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/tables', methods=['GET'])
def tables():

    table_data = []

    for index, data in df.iterrows():
        obj = {}
        for key in data.keys():
            obj[key] = data.get(key) if data.get(key) else ''
        table_data.append(obj)

        if index > 98:
            break

    return render_template('tables.html', data= {'data':table_data})

@app.route('/dashboard', methods=['GET'])
def dashboard():

    df2 = df.groupby(['indicator_type'])['indicator'].count()

    print(df2)

    # Return bar graph showing how many data grouped by categories
    return render_template('dashboard.html', data= {
        'graph_title': 'Numero di IoC raggruppati per indicator_type',
        'graph_type': 'bar',
        'labels': list(df2.index),
        'data': list(df2)
    })

if __name__=='__main__':
    app.run(
        host='0.0.0.0',
        port=80,
        debug=True
    )