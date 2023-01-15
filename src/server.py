from flask import Flask, render_template, Response, make_response
import pandas as pd
from utils.utils import get_graph_data, get_all_graphs_reducted
from dotenv import load_dotenv
import os
from dateutil.parser import parse

app = Flask(__name__)

load_dotenv()

# Read variables from .env file
HOST = os.getenv('HOST') or '0.0.0.0'
DEBUG = os.getenv('DEBUG') or False
PORT = os.getenv('PORT') or 80

df = pd.read_csv('data/result.csv', sep=',')
resultwithmatches_df = pd.read_csv('data/resultwithmatches.csv', sep=',')
users_df = pd.read_csv('data/users.csv', sep=',')

def process_csv(df: pd.DataFrame) -> None:
    # Convert date columns of df into dates
    dates_columns = [d for d in df.columns if '_date' in d]
    for d in dates_columns:
        # replace "None" string with None
        col = df[d].replace('None', '')
        df[d] = pd.to_datetime(col)
    df['tw_to_mwbazar'] = (df['twitter_date'] - df['mwbazar_date']).dt.seconds
    df['is_mwbazar_before'] = df['tw_to_mwbazar'] > 0
    # Add computed fields for MWBAZAAR


process_csv(df)

for index, row in resultwithmatches_df.iterrows():
    tw_date = parse(row['twitter_date']).timestamp() if not row['twitter_date'] in ['','None'] else 0
    mw_date = parse(row['mwbazar_date']).timestamp() if not row['mwbazar_date'] in ['','None'] else 0
    if tw_date == mw_date == 0:
        res = 'None'
    else:
        res = tw_date - mw_date
    row['tw_to_mwbazar'] = res
    row['is_mwbazar_before'] = row['tw_to_mwbazar'] > 0
"""
# Convert date columns of df into dates
dates_columns = [d for d in df.columns if '_date' in d]
for d in dates_columns:
    # replace "None" string with None
    col = df[d].replace('None', '')
    df[d] = pd.to_datetime(col)

dates_columns = [d for d in resultwithmatches_df.columns if '_date' in d]
for d in dates_columns:
    # replace "None" string with None
    col = resultwithmatches_df[d].replace('None', '')
    resultwithmatches_df[d] = pd.to_datetime(col)

# Add computed fields for MWBAZAAR
df['tw_to_mwbazar'] = df['twitter_date'] - df['mwbazar_date']
df['is_mwbazar_before'] = True if df['tw_to_mwbazar'] > 0 else False

df['tw_to_mwbazar'] = df['twitter_date'] - df['mwbazar_date']
df['is_mwbazar_before'] = True if df['tw_to_mwbazar'] > 0 else False
"""
TABLES = [
    {
        'name': 'Users table',
        'description': 'Table representing users\'data',
        'id': 0
    },
    {
        'name': 'Results table',
        'description': 'Table representing results got from data analysis',
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
    return render_template('tables.html', data={'tables': TABLES})


@app.route('/tables/<int:table_id>', methods=['GET'])
def table(table_id):
    df = TABLE_DATA.get(table_id)
    if df is None or df.empty:
        # Create error 404
        res = make_response(render_template('404.html', reason='Invalid table id passed'))
        res.status_code = 404
        return res
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
    table = TABLES[table_id]
    return render_template('table.html', data={'data': table_data}, title=table['name'],
                           description=table['description'])


@app.route('/dashboards', methods=['GET'])
def dashboards():
    graphs = get_all_graphs_reducted()
    graphs = [e.to_json() for e in graphs]
    # print(graphs,'\n')

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


if __name__ == '__main__':
    app.run(
        host=HOST,
        port=PORT,
        debug=DEBUG
    )
