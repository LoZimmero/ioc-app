from flask import Flask, render_template, Response
import pandas as pd
from utils.utils import get_graph_data

app = Flask(__name__)

df = pd.read_csv('data/result.csv', sep=',')
resultwithmatches_df = pd.read_csv('data/resultwithmatches.csv', sep=',')
users_df = pd.read_csv('data/users.csv', sep=',')

TABLES = [
    {
        'name': 'Users table',
        'description': 'Table representing users\'data',
        'id': 0
    },
    {
        'name': 'Results table',
        'description': 'Table representing results',
        'id': 1
    }
]

TABLE_DATA = {
    0: users_df,
    1: resultwithmatches_df
}

def get_table_data(id: int):
    return TABLE_DATA.get(id)
    

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/tables', methods=['GET'])
def tables():
    return render_template('tables.html', data= {'tables': TABLES})

@app.route('/tables/<int:table_id>', methods=['GET'])
def table(table_id):
    
    df = TABLE_DATA.get(table_id)
    table_data = []

    print(table_id, table_data)

    for index, data in df.iterrows():
        obj = {}
        temp_res = []
        for key in data.keys():
            obj[key] = data.get(key) if data.get(key) else ''
        temp_res.append(obj)

        if index > 98:
            table_data.append(temp_res)
            temp_res = []

    # NB: 'table_data' is a list of lists because JS doesen't want a list
    # too long.

    return render_template('table.html', data= {'data':table_data})

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

@app.route('/dashboard/<name>', methods=['GET'])
def dashboard_list(name):

    graph_id = 0
    try:
        graph_id = int(name)
    except:
        return Response(status=404)

    df2 = get_graph_data(df, graph_id)

    # Return bar graph showing how many data grouped by categories
    return render_template('dashboard_list.html', data= {
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