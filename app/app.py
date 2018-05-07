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
df_option['days'] = df_option.index.day
df_option['day'] = df_option.index.day.astype(str)
df_option = df_option.groupby('day').mean()

# available_indicators = df['Indicator Name'].unique()

app.layout = html.Div([
    html.H1(['Big Data Analytics option task'],
    style={'margin-left': '10%', 'margin-bottom': '7%', 'font-weight': 'bold'}),

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
            html.P(['choose trace2'], style={'margin-right': '5%', 'float': 'left', 'font-size': '20px'}),
            dcc.RadioItems(
                id='xaxis-type2',
                options=[{'label': i, 'value': i} for i in ['v1', 'v2', 'v3', 'v4']],
                value='v1',
                labelStyle={'display': 'inline-block'}
            )
        ],
        style={'width': '80%', 'position': 'auto', 'margin': 'auto'}),

        html.Div([
            dcc.Graph(id='indicator-graphic'),

            dcc.Slider(
                id='time-slider',
                min=df_option['days'].min(),
                max=df_option['days'].max(),
                value=df_option['days'].max(),
                step=None,
                marks={str(time): str(time) for time in df_option['days'].unique()}
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
    dff = df_option[df_option['days'] <= time_value]

    return {
        'data': [
        go.Scatter(
            x=dff['days'],
            y=dff[xaxis_type],
            # text=dff[dff['Indicator Name'] == yaxis_column_name]['Country Name'],
            # mode='markers',
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }),
        go.Scatter(
            x=dff['days'],
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
                'title': 'days - mean',
                'type': 'linear'
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
