from flask import Flask, render_template, Response, make_response
import pandas as pd
from utils.utils import get_graph_data, get_all_graphs_reducted

app = Flask(__name__)

df = pd.read_csv('data/result.csv', sep=',')
resultwithmatches_df = pd.read_csv('data/resultwithmatches.csv', sep=',')
users_df = pd.read_csv('data/users.csv', sep=',')

# Convert date columns of df into dates
dates_columns = [d for d in df.columns if '_date' in d]
for d in dates_columns:
    # replace "None" string with None
    col = df[d].replace('None', '')
    df[d] = pd.to_datetime(col)

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

@app.route('/dashboards', methods=['GET'])
def dashboards():

    graphs = get_all_graphs_reducted()
    graphs = [e.to_json() for e in graphs]
    print(graphs,'\n')

    # Return bar graph showing how many data grouped by categories
    return render_template('dashboards.html', graphs=graphs)

@app.route('/dashboards/<int:id>', methods=['GET'])
def dashboard(id):

    graph_id = None
    try:
        graph_id = int(id)
    except:
        # Throw 404
        response = make_response(render_template('404.html', reason='Invalid graph_id passed'))
        response.status_code = 404
        return response

    graph_data = get_graph_data(df, graph_id)
    if not graph_data:
        # Throw 404
        response = make_response(render_template('404.html', reason='Graph not found'))
        response.status_code = 404
        return response

    # Return bar graph showing how many data grouped by categories
    return render_template('dashboard.html', data=graph_data.to_json())

if __name__=='__main__':
    app.run(
        host='0.0.0.0',
        port=80,
        debug=True
    )