import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go

app = dash.Dash()

df_option = pd.read_csv('data/data.csv',
                 encoding='Shift_JIS',
                 names=('date', 'v1', 'v2', 'v3', 'v4'),
                 index_col = 'date',
                 parse_dates=True)
# parse time
df_option['time'] = df_option.index
# prepare YYYY-MM-DD-HH
df_option['year'] = df_option['time'].map(lambda x: x.year).astype(str)
df_option['month'] = df_option['time'].map(lambda x: x.month).astype(str)
df_option['day'] = df_option['time'].map(lambda x: x.day).astype(str)
df_option['hour'] = df_option['time'].map(lambda x: x.hour).astype(str)
df_option['YMDH'] = pd.to_datetime(df_option[['year','month','day','hour']], format='%Y%m%d%h').astype(object)
# Aggregate by hour
df_option = df_option.groupby('YMDH', as_index=False).mean()
# make key variable
df_option['key'] = df_option['YMDH'].astype(str)
# make row number
df_option['row_n'] = range(len(df_option))
# astype(object)
df_option['YMDH'] = df_option['YMDH'].astype(object)


# available_indicators = df['Indicator Name'].unique()

app.layout = html.Div([
    html.H1(['Big Data Analytics option task'],
    style={'margin-left': '10%', 'margin-bottom': '7%', 'font-size': '50px'}),

    html.Div([

        html.Div([
            html.P(['choose trace1'], style={'margin-right': '5%', 'float': 'left', 'font-size': '20px'}),
            dcc.RadioItems(
                id='xaxis-type',
                options=[{'label': i, 'value': i} for i in ['v1', 'v2', 'v3', 'v4']],
                value='v1',
                labelStyle={'display': 'inline-block'}
            ),
            html.Br(),
            html.P(['choose trace2'], style={'margin-right': '4.3%', 'float': 'left', 'font-size': '20px'}),
            dcc.RadioItems(
                id='xaxis-type2',
                options=[{'label': i, 'value': i} for i in ['v1', 'v2', 'v3', 'v4']],
                value='v1',
                labelStyle={'display': 'inline-block'}
            ),
            html.Br()
        ],
        style={'width': '80%', 'position': 'auto', 'margin': 'auto'}),

        html.Div([
            dcc.Graph(id='indicator-graphic'),
            html.Br(),html.Br(),
            dcc.RangeSlider(
                id= 'time-slider',
                # min=df_option.YMDH.min(),
                # max=df_option.YMDH.max(),
                # value=[df_option.YMDH.min(), df_option.YMDH.max()]

                min=df_option['row_n'].min(),
                max=df_option['row_n'].max(),
                value=[df_option['row_n'].min(), df_option['row_n'].max()],
                step=15,
                marks={
                    0:  {'label': '04.11:18', 'style': {'color': '#77b0b1','transform': 'rotate(-45deg)'}},
                    15: {'label': '04.12:09', 'style': {'color': '#77b0b1','transform': 'rotate(-45deg)'}},
                    30: {'label': '04.13:00', 'style': {'color': '#77b0b1','transform': 'rotate(-45deg)'}},
                    45: {'label': '04.13:15', 'style': {'color': '#77b0b1','transform': 'rotate(-45deg)'}},
                    60: {'label': '04.14:06', 'style': {'color': '#77b0b1','transform': 'rotate(-45deg)'}},
                    75: {'label': '04.14:23', 'style': {'color': '#77b0b1','transform': 'rotate(-45deg)'}},
                    90: {'label': '04.15:12', 'style': {'color': '#77b0b1','transform': 'rotate(-45deg)'}},
                    105:{'label': '04.16:03', 'style': {'color': '#77b0b1','transform': 'rotate(-45deg)'}},
                    120:{'label': '04.16:18', 'style': {'color': '#77b0b1','transform': 'rotate(-45deg)'}},
                    135:{'label': '04.17:09', 'style': {'color': '#77b0b1','transform': 'rotate(-45deg)'}},
                    150:{'label': '04.18:00', 'style': {'color': '#77b0b1','transform': 'rotate(-45deg)'}},
                    165:{'label': '04.18:15', 'style': {'color': '#77b0b1','transform': 'rotate(-45deg)'}},
                    180:{'label': '04.19:06', 'style': {'color': '#77b0b1','transform': 'rotate(-45deg)'}},
                    195:{'label': '04.19:21', 'style': {'color': '#77b0b1','transform': 'rotate(-45deg)'}},
                    210:{'label': '04.20:12', 'style': {'color': '#77b0b1','transform': 'rotate(-45deg)'}},
                    225:{'label': '04.21:03', 'style': {'color': '#77b0b1','transform': 'rotate(-45deg)'}},
                    240:{'label': '04.21:18', 'style': {'color': '#77b0b1','transform': 'rotate(-45deg)'}},
                    255:{'label': '04.22:09', 'style': {'color': '#77b0b1','transform': 'rotate(-45deg)'}},
                    270:{'label': '04.23:00', 'style': {'color': '#77b0b1','transform': 'rotate(-45deg)'}},
                    282:{'label': '04.23:12', 'style': {'color': '#77b0b1','transform': 'rotate(-45deg)'}}
                }
            )
        ],
        style={'width': '80%', 'position': 'auto', 'margin': 'auto'})
        ])
],
style={'position': 'relative', 'width': '100%', 'margin': '60px 0', 'font-family': 'Dosis'})

@app.callback(
    dash.dependencies.Output('indicator-graphic', 'figure'),
    [dash.dependencies.Input('xaxis-type', 'value'),
     dash.dependencies.Input('xaxis-type2', 'value'),
     dash.dependencies.Input('time-slider', 'value')])
def update_graph(xaxis_type, xaxis_type2, time_value):
    transformed_value = [v for v in time_value]
    # dff = df_option[df_option['row_n'] <= time_value]
    dff = df_option[df_option.row_n >= time_value[0]]
    dff = dff[dff.row_n <= time_value[1]]

    return {
        'data': [
        go.Scatter(
            x=dff['YMDH'],
            y=dff[xaxis_type],
            # text=dff[dff['Indicator Name'] == yaxis_column_name]['Country Name'],
            # mode='markers',
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }),
        go.Scatter(
            x=dff['YMDH'],
            y=dff[xaxis_type2],
            # text=dff[dff['Indicator Name'] == yaxis_column_name]['Country Name'],
            # mode='markers',
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        )],
        'layout': go.Layout(
            xaxis={
                'title': 'hour - mean'
            },
            yaxis={
                'title': 'value',
                'type': 'linear'
            },
            margin={'l': 40, 'b': 40, 't': 10, 'r': 0},
            hovermode='closest'
        )
    }

external_css = [
    # dash stylesheet
    'https://fonts.googleapis.com/css?family=Raleway',
    'https://codepen.io/chriddyp/pen/bWLwgP.css'
]
for css in external_css:
    app.css.append_css({'external_url': css})


if __name__ == '__main__':
    app.run_server(debug=True, port=5000, host='0.0.0.0')
