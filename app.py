import dash
import pandas as pd

import get_data
from dash import dash_table
from dash.dash_table.Format import Format
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from dash import html, dcc, Input, Output, State
from apps import graph_settings
from datetime import date, timedelta
import base64

logo = '/Users/l/Library/Mobile Documents/com~apple~CloudDocs/code/covid/assets/kd_logo.png'
# logo = 'assets/kd_logo.png'
encoded_image = base64.b64encode(open(logo, 'rb').read())

app = dash.Dash(__name__, suppress_callback_exceptions=True)
server = app.server

app.layout = html.Div(
    [
        html.Div(
            [  # first row - navbar
                html.Div(
                    [  # extRactor logo
                        html.Img(
                            id='fp-logo',
                            src='data:image/png;base64,{}'.format(encoded_image.decode()),
                            style={
                                # 'width': '25%',
                                'width': '180px',
                            },
                        ),
                        # html.H1('kovidata')
                    ],
                    id='extRactor-logo',
                    className='pretty_container ten columns m_bottom',
                ),
            ],
        ),
        html.Div(
            [
                dcc.DatePickerRange(
                    id='date-picker',
                    # start_date='2022-01-01',
                    start_date=date.today() - timedelta(days=182),
                    end_date=date.today(),
                    display_format='YYYY-MM-DD',
                    start_date_placeholder_text='2022-01-01',
                    min_date_allowed=date(2000, 3, 1),
                    max_date_allowed=date.today()
                ),
            ],
            className="pretty_container_left eleven columns",
            style={
                # DatePickerRange is link between callbacks thus hidden
                'display': 'none'
            }
        ),
        html.Div(
            [
                dcc.DatePickerRange(
                    id='date-picker-2',
                    start_date=date.today() - timedelta(days=182),
                    end_date=date.today(),
                    display_format='YYYY-MM-DD',
                    start_date_placeholder_text='2022-01-01',
                    min_date_allowed=date(2000, 3, 1),
                    max_date_allowed=date.today()
                ),
            ],
            className="pretty_container_left eleven columns",
            style={
                # DatePickerRange is link between callbacks thus hidden
                'display': 'none'
            }
        ),
        html.Div(
            [
                dcc.DatePickerRange(
                    id='date-picker-3',
                    start_date=date.today() - timedelta(days=14),
                    end_date=date.today(),
                    display_format='YYYY-MM-DD',
                    start_date_placeholder_text='2022-01-01',
                    min_date_allowed=date(2000, 3, 1),
                    max_date_allowed=date.today()
                ),
            ],
            className="pretty_container_left eleven columns",
            style={
                # DatePickerRange is link between callbacks thus hidden
                'display': 'none'
            }
        ),
        html.Div(
            [
                dcc.DatePickerRange(
                    id='date-picker-4',
                    start_date=date.today() - timedelta(days=14),
                    end_date=date.today(),
                    display_format='YYYY-MM-DD',
                    start_date_placeholder_text='2022-01-01',
                    min_date_allowed=date(2000, 3, 1),
                    max_date_allowed=date.today()
                ),
            ],
            className="pretty_container_left eleven columns",
            style={
                # DatePickerRange is link between callbacks thus hidden
                'display': 'none'
            }
        ),
        html.Div(
            [
                dcc.DatePickerRange(
                    id='date-picker-5',
                    start_date=date.today() - timedelta(days=14),
                    end_date=date.today(),
                    display_format='YYYY-MM-DD',
                    start_date_placeholder_text='2022-01-01',
                    min_date_allowed=date(2000, 3, 1),
                    max_date_allowed=date.today()
                ),
            ],
            className="pretty_container_left eleven columns",
            style={
                # DatePickerRange is link between callbacks thus hidden
                'display': 'none'
            }
        ),
        html.Div(
            [  # hidden cache table for data storage
                html.Div(
                    [
                        dash_table.DataTable(
                            id='table-nvut')
                    ],
                    id='div-table-nvut',
                    style={
                        'display': 'none'
                    }
                ),
                html.Div(
                    [
                        dash_table.DataTable(
                            id='table-hosp')
                    ],
                    id='div-table-hosp',
                    style={
                        'display': 'none'
                    }
                ),
                html.Div(
                    [
                        dash_table.DataTable(
                            id='table-ock-hosp')
                    ],
                    id='div-table-ock-hosp',
                    style={
                        'display': 'none'
                    }
                ),
                html.Div(
                    [
                        dash_table.DataTable(
                            id='table-incidence')
                    ],
                    id='div-table-incidence',
                    style={
                        'display': 'none'
                    }
                ),
                html.Div(
                    [
                        dash_table.DataTable(
                            id='table-inc-kraje')
                    ],
                    id='div-table-inc-kraje',
                    style={
                        'display': 'none'
                    }
                ),
                html.Div(
                    [
                        dash_table.DataTable(
                            id='table-ock-demo')
                    ],
                    id='div-table-ock-demo',
                    style={
                        'display': 'none'
                    }
                ),
                html.Div(
                    [
                        dash_table.DataTable(
                            id='table-neco')
                    ],
                    id='div-table-neco',
                    style={
                        'display': 'none'
                    }
                )
            ]
        ),
        html.Div(
            [ # div with main stats
                dcc.Loading(
                    [
                        html.Div(
                            [
                            ],
                            id='div-table-celkem',
                            className='pretty_container ten columns',
                        ),
                        html.Div(
                            [
                            ],
                            id='div-table-vcera',
                            className='pretty_container ten columns',
                        ),

                    ],
                    color='red',
                    type='circle'
                )
            ]
        ),
        html.Div(
            [
                dcc.Loading(
                    [

                    ],
                    color='red',
                    type='circle'
                ),
                html.Div(
                    [
                        html.P('! = neaktualizovaná hodnota')
                    ],
                    id='div-container-old',
                    className='pretty_container_old ten columns',
                    style={'display': 'none'}
                ),
            ]
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.Div(
                            [
                                html.H3('Celkové stavy'),
                            ],
                            className='flex-display bar-left',
                        ),
                        html.Div(
                            [
                                html.Button(
                                    'Zobrazeni:',
                                    id='btn-zob',
                                    n_clicks=1,
                                    className='round-border btn-zob'
                                ),
                                html.Button(
                                    'Posledních 14 dní',
                                    id='btn-14',
                                    n_clicks=1,
                                    className='round-border btn-gradient'
                                ),
                                html.Button(
                                    'Poslední měsíc',
                                    id='btn-28',
                                    n_clicks=1,
                                    className='round-border btn-gradient'
                                ),
                                html.Button(
                                    'Poslední půlrok',
                                    id='btn-182',
                                    n_clicks=1,
                                    className='round-border btn-gradient'
                                ),
                                html.Button(
                                    'Od začátku epidemie',
                                    id='btn-all',
                                    n_clicks=1,
                                    className='round-border btn-gradient'
                                ),
                            ],
                            className='row flex-display bar-right',
                        ),
                    ],
                ),

            ],
            className='pretty_container_zob ten columns'
        ),
        html.Div(
            [
                html.Div(
                    [  # nvut pretty container
                        dcc.Loading(
                            [
                                dcc.Tabs(
                                    id="tabs-nvut-graph",
                                    parent_className='custom-tabs',
                                    value='tab-1-nvut-graph', children=[
                                        dcc.Tab(label='Nakažení', value='tab-1-nvut-graph',
                                                className='custom-tab', selected_className='custom-tab--selected'),
                                        dcc.Tab(label='Vyléčení', value='tab-2-nvut-graph',
                                                className='custom-tab', selected_className='custom-tab--selected'),
                                        dcc.Tab(label='Zemřelí', value='tab-3-nvut-graph',
                                                className='custom-tab', selected_className='custom-tab--selected'),
                                        dcc.Tab(label='Testovaní', value='tab-4-nvut-graph',
                                                className='custom-tab', selected_className='custom-tab--selected'),
                                        dcc.Tab(label='Testovaní-AG', value='tab-5-nvut-graph',
                                                className='custom-tab', selected_className='custom-tab--selected'),
                                    ]
                                ),
                                html.Div(id='tabs-content-nvut-graph')
                            ],
                            color='red',
                            type='circle',
                        )
                    ],
                    className="pretty_container ten columns",
                )
            ]
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.Div(
                            [
                                html.H3('Hospitalizace'),
                            ],
                            className='flex-display bar-left',
                        ),
                        html.Div(
                            [
                                html.Button(
                                    'Zobrazeni:',
                                    id='btn-zob-2',
                                    n_clicks=1,
                                    className='round-border btn-zob'
                                ),
                                html.Button(
                                    'Posledních 14 dní',
                                    id='btn-14-2',
                                    n_clicks=1,
                                    className='round-border btn-gradient'
                                ),
                                html.Button(
                                    'Poslední měsíc',
                                    id='btn-28-2',
                                    n_clicks=1,
                                    className='round-border btn-gradient'
                                ),
                                html.Button(
                                    'Poslední půlrok',
                                    id='btn-182-2',
                                    n_clicks=1,
                                    className='round-border btn-gradient'
                                ),
                                html.Button(
                                    'Od začátku epidemie',
                                    id='btn-all-2',
                                    n_clicks=1,
                                    className='round-border btn-gradient'
                                ),
                            ],
                            className='flex-display bar-right',
                        ),
                    ],
                    className='row menu',
                ),

            ],
            className='pretty_container_zob ten columns'
        ),
        html.Div(
            [  # hospitalizace
                html.Div(
                    [  # buttons
                        dcc.Loading(
                            [
                                dcc.Tabs(id="tabs-hosp-graph",
                                            value='tab-1-hosp-graph',
                                            parent_className='custom-tabs',
                                            className='custom-tabs-container',
                                            children=[
                                                dcc.Tab(label='Hospitalizace podle příznaků', value='tab-1-hosp-graph',
                                                        className='custom-tab',
                                                        selected_className='custom-tab--selected'),
                                                dcc.Tab(label='Hospitalizace podle očkování', value='tab-2-hosp-graph',
                                                        className='custom-tab',
                                                        selected_className='custom-tab--selected'),
                                            ]
                                         ),
                                html.Div(id='tabs-content-hosp-graph')
                            ],
                            color='red',
                            type='circle',
                        ),
                    ],
                    className="pretty_container ten columns",
                )
            ],
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.Div(
                            [
                                html.H3('Incidence a očkování'),
                            ],
                            className='flex-display bar-left',
                        ),
                        html.Div(
                            [
                                html.Button(
                                    'Zobrazeni:',
                                    id='btn-zob-3',
                                    n_clicks=1,
                                    className='round-border btn-zob'
                                ),
                                html.Button(
                                    'Posledních 14 dní',
                                    id='btn-14-3',
                                    n_clicks=1,
                                    className='round-border btn-gradient'
                                ),
                                html.Button(
                                    'Poslední měsíc',
                                    id='btn-28-3',
                                    n_clicks=1,
                                    className='round-border btn-gradient'
                                ),
                                html.Button(
                                    'Poslední půlrok',
                                    id='btn-182-3',
                                    n_clicks=1,
                                    className='round-border btn-gradient'
                                ),
                                html.Button(
                                    'Od začátku epidemie',
                                    id='btn-all-3',
                                    n_clicks=1,
                                    className='round-border btn-gradient'
                                ),
                            ],
                            className='row flex-display bar-right',
                        ),
                    ],
                ),
            ],
            className='pretty_container_zob ten columns'
        ),
        html.Div(
            [  # incidence + ockovani (demografie)
                html.Div(
                    [  # buttons
                        dcc.Loading(
                            [
                                dcc.Tabs(id="tabs-incidence-graph",
                                         parent_className='custom-tabs',
                                         value='tab-1-incidence-graph', children=[
                                            dcc.Tab(label='Incidence (ČR)',
                                                    value='tab-1-incidence-graph',
                                                    className='custom-tab',
                                                    selected_className='custom-tab--selected'
                                                    ),
                                            dcc.Tab(label='Očkování - demografie (věk)',
                                                    value='tab-2-demografie-graph',
                                                    className='custom-tab',
                                                    selected_className='custom-tab--selected'
                                                    ),
                                            dcc.Tab(label='Očkování - demografie (typ vakcíny)',
                                                    value='tab-3-demografie-graph',
                                                    className='custom-tab',
                                                    selected_className='custom-tab--selected'
                                                    )
                                            ]
                                         ),
                                html.Div(id='tabs-content-incidence-graph')
                            ],
                            color='red',
                            type='circle',
                        )
                    ],
                    className="pretty_container ten columns",
                )
            ]
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.Div(
                            [
                                html.H3('Incidence v krajích'),
                            ],
                            className='flex-display bar-left',
                        ),
                        html.Div(
                            [
                                html.Button(
                                    'Zobrazeni:',
                                    id='btn-zob-4',
                                    n_clicks=1,
                                    className='round-border btn-zob'
                                ),
                                html.Button(
                                    'Posledních 14 dní',
                                    id='btn-14-4',
                                    n_clicks=1,
                                    className='round-border btn-gradient'
                                ),
                                html.Button(
                                    'Poslední měsíc',
                                    id='btn-28-4',
                                    n_clicks=1,
                                    className='round-border btn-gradient'
                                ),
                                html.Button(
                                    'Poslední půlrok',
                                    id='btn-182-4',
                                    n_clicks=1,
                                    className='round-border btn-gradient'
                                ),
                                html.Button(
                                    'Od začátku epidemie',
                                    id='btn-all-4',
                                    n_clicks=1,
                                    className='round-border btn-gradient'
                                ),
                            ],
                            className='row flex-display bar-right',
                        ),
                    ],
                ),
            ],
            className='pretty_container_zob ten columns'
        ),
        html.Div(
            [
                html.Div(
                    [  # buttons
                        dcc.Loading(
                            [
                                dcc.Tabs(id="tabs-inc_kraje-graph",
                                         parent_className='custom-tabs',
                                         value='tab-1-inc_kraje-graph', children=[
                                        dcc.Tab(label='PHA', value='tab-1-inc_kraje-graph',
                                                className='custom-tab', selected_className='custom-tab--selected'),
                                        dcc.Tab(label='STC', value='tab-2-inc_kraje-graph',
                                                className='custom-tab', selected_className='custom-tab--selected'),
                                        dcc.Tab(label='ULK', value='tab-3-inc_kraje-graph',
                                                className='custom-tab', selected_className='custom-tab--selected'),
                                        dcc.Tab(label='MSK', value='tab-4-inc_kraje-graph',
                                                className='custom-tab', selected_className='custom-tab--selected'),
                                        dcc.Tab(label='JHM', value='tab-5-inc_kraje-graph',
                                                className='custom-tab', selected_className='custom-tab--selected'),
                                        dcc.Tab(label='OLK', value='tab-6-inc_kraje-graph',
                                                className='custom-tab', selected_className='custom-tab--selected'),
                                        dcc.Tab(label='HKK', value='tab-7-inc_kraje-graph',
                                                className='custom-tab', selected_className='custom-tab--selected'),
                                        dcc.Tab(label='LBK', value='tab-8-inc_kraje-graph',
                                                className='custom-tab', selected_className='custom-tab--selected'),
                                        dcc.Tab(label='VYS', value='tab-9-inc_kraje-graph',
                                                className='custom-tab', selected_className='custom-tab--selected'),
                                        dcc.Tab(label='JHC', value='tab-10-inc_kraje-graph',
                                                className='custom-tab', selected_className='custom-tab--selected'),
                                        dcc.Tab(label='ZLK', value='tab-11-inc_kraje-graph',
                                                className='custom-tab', selected_className='custom-tab--selected'),
                                        dcc.Tab(label='PAK', value='tab-12-inc_kraje-graph',
                                                className='custom-tab', selected_className='custom-tab--selected'),
                                        dcc.Tab(label='PLK', value='tab-13-inc_kraje-graph',
                                                className='custom-tab', selected_className='custom-tab--selected'),
                                        dcc.Tab(label='KVK', value='tab-14-inc_kraje-graph',
                                                className='custom-tab', selected_className='custom-tab--selected'),
                                    ]
                                         ),
                                html.Div(id='tabs-content-inc_kraje-graph')
                            ],
                            color='red',
                            type='circle',
                        )
                    ],
                    className="pretty_container ten columns",
                )
            ]
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.Div(
                            [
                                html.H3('Počet aplikovaných dávek v krajích')
                            ],
                            className='flex-display bar-left',
                        ),
                        html.Div(
                            [
                                html.Button(
                                    'Zobrazeni:',
                                    id='btn-zob-5',
                                    n_clicks=1,
                                    className='round-border btn-zob'
                                ),
                                html.Button(
                                    'Posledních 14 dní',
                                    id='btn-14-5',
                                    n_clicks=1,
                                    className='round-border btn-gradient'
                                ),
                                html.Button(
                                    'Poslední měsíc',
                                    id='btn-28-5',
                                    n_clicks=1,
                                    className='round-border btn-gradient'
                                ),
                                html.Button(
                                    'Poslední půlrok',
                                    id='btn-182-5',
                                    n_clicks=1,
                                    className='round-border btn-gradient'
                                ),
                                html.Button(
                                    'Od začátku epidemie',
                                    id='btn-all-5',
                                    n_clicks=1,
                                    className='round-border btn-gradient'
                                ),
                            ],
                            className='row flex-display bar-right',
                        ),
                    ],
                ),
            ],
            className='pretty_container_zob ten columns'
        ),
        html.Div(
            [
                html.Div(
                    [  # buttons
                        dcc.Loading(
                            [
                                dcc.Tabs(id="tabs-ockovani-graph",
                                         parent_className='custom-tabs',
                                         value='tab-1-ockovani-graph', children=[
                                            dcc.Tab(label='PHA', value='tab-1-ockovani-graph',
                                                    className='custom-tab', selected_className='custom-tab--selected'),
                                            dcc.Tab(label='STC', value='tab-2-ockovani-graph',
                                                    className='custom-tab', selected_className='custom-tab--selected'),
                                            dcc.Tab(label='ULK', value='tab-3-ockovani-graph',
                                                    className='custom-tab', selected_className='custom-tab--selected'),
                                            dcc.Tab(label='MSK', value='tab-4-ockovani-graph',
                                                    className='custom-tab', selected_className='custom-tab--selected'),
                                            dcc.Tab(label='JHM', value='tab-5-ockovani-graph',
                                                    className='custom-tab', selected_className='custom-tab--selected'),
                                            dcc.Tab(label='OLK', value='tab-6-ockovani-graph',
                                                    className='custom-tab', selected_className='custom-tab--selected'),
                                            dcc.Tab(label='HKK', value='tab-7-ockovani-graph',
                                                    className='custom-tab', selected_className='custom-tab--selected'),
                                            dcc.Tab(label='LBK', value='tab-8-ockovani-graph',
                                                    className='custom-tab', selected_className='custom-tab--selected'),
                                            dcc.Tab(label='VYS', value='tab-9-ockovani-graph',
                                                    className='custom-tab', selected_className='custom-tab--selected'),
                                            dcc.Tab(label='JHC', value='tab-10-ockovani-graph',
                                                    className='custom-tab', selected_className='custom-tab--selected'),
                                            dcc.Tab(label='ZLK', value='tab-11-ockovani-graph',
                                                    className='custom-tab', selected_className='custom-tab--selected'),
                                            dcc.Tab(label='PAK', value='tab-12-ockovani-graph',
                                                    className='custom-tab', selected_className='custom-tab--selected'),
                                            dcc.Tab(label='PLK', value='tab-13-ockovani-graph',
                                                    className='custom-tab', selected_className='custom-tab--selected'),
                                            dcc.Tab(label='KVK', value='tab-14-ockovani-graph',
                                                    className='custom-tab', selected_className='custom-tab--selected'),
                                            ]
                                         ),
                                html.Div(id='tabs-content-ockovani-graph')
                            ],
                            color='red',
                            type='circle',
                        )
                    ],
                    className="pretty_container ten columns",
                )
            ]
        ),

    ]
)


def get_fig_ockovani(region, start_date, end_date):
    df = get_data.get_ockovani_kraje()
    dff = df[(df['Datum'] >= start_date) & (df['Datum'] <= end_date)]
    dff = dff[(dff['Kraj'] == region)]
    dff = dff.sort_values(by='Vakcína', ascending=False)
    fig = px.bar(dff,
                 x='Datum',
                 y='Celkem davek',
                 color='Vakcína',
                 color_discrete_sequence=graph_settings.final_pal
                 )
    fig.update_layout(
        title_x=0.5,  # center
        height=700,
        xaxis_title="Datum",
        margin=graph_settings.tight_layout,
        template=graph_settings.template_dark,
        legend=dict(
            orientation='h',
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01
        )
    )
    fig.update_yaxes(title_text="Počet aplikovaných dávek", secondary_y=False)
    return fig


def get_fig_incidence(region, start_date, end_date):
    df = get_data.get_inc_kraje_new()
    dff = df[(df['Datum'] >= start_date) & (df['Datum'] <= end_date)]
    dff = dff[(dff['Kraj'] == region)]
    fig = go.Figure(
        data=[
            go.Bar(name='týdenní/100 000 obyv.',
                   x=dff['Datum'],
                   y=dff['incidence 7 na 100 000'],
                   marker=dict(color=graph_settings.final_pal[0])
                   ),
            go.Bar(name='čtrnáctidenní/100 000 obyv.',
                   x=dff['Datum'],
                   y=dff['incidence 14 na 100 000'],
                   marker=dict(color=graph_settings.final_pal[1])
                   ),
            go.Bar(name='týdenní',
                   x=dff['Datum'],
                   y=dff['incidence 7'],
                   marker=dict(color=graph_settings.final_pal[2])
                   ),
            go.Bar(name='čtrnáctidenní',
                   x=dff['Datum'],
                   y=dff['incidence 14'],
                   marker=dict(color=graph_settings.final_pal[3])
                   ),
        ]
    )
    fig.update_layout(
        # title='Hospitalizace',
        title_x=0.5,  # center
        height=700,
        xaxis_title="Datum",
        yaxis_title="Počet",
        margin=graph_settings.tight_layout,
        template=graph_settings.template_dark,
        legend_title_text='',
        legend=dict(
            orientation='h',
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01
        )
    )
    return fig


# - - - - - - CALLBACKSSSS - - - - - -

# select range
@app.callback(
    [
        Output('btn-14', 'n_clicks'),
        Output('btn-28', 'n_clicks'),
        Output('btn-182', 'n_clicks'),
        Output('btn-all', 'n_clicks'),
        Output('date-picker', 'start_date'),
        Output('date-picker', 'end_date'),
    ],
    [
        Input('btn-14', 'n_clicks'),
        Input('btn-28', 'n_clicks'),
        Input('btn-182', 'n_clicks'),
        Input('btn-all', 'n_clicks'),
    ],
    prevent_initial_call=True
)
#  every callback needs at least one Input, its needed, but not used
def button_pressed(n_click14, n_click28, n_click182, n_clickall):
    n_click14, n_click28, n_click182, n_clickall = (0, 0, 0, 0)
    trigger = dash.callback_context.triggered[0]['prop_id'].split('.')[0]
    if trigger == 'btn-14':
        start = date.today() - timedelta(days=14)
        end = date.today()
    elif trigger == 'btn-28':
        start = date.today() - timedelta(days=28)
        end = date.today()
    elif trigger == 'btn-182':
        start = date.today() - timedelta(days=182)
        end = date.today()
    elif trigger == 'btn-all':
        start = '2020-03-01'
        end = date.today()
    else:
        start = '2020-03-01'
        end = date.today()

    return n_click14, n_click28, n_click182, n_clickall, start, end


@app.callback(
    [
        Output('btn-14-2', 'n_clicks'),
        Output('btn-28-2', 'n_clicks'),
        Output('btn-182-2', 'n_clicks'),
        Output('btn-all-2', 'n_clicks'),
        Output('date-picker-2', 'start_date'),
        Output('date-picker-2', 'end_date'),
    ],
    [
        Input('btn-14-2', 'n_clicks'),
        Input('btn-28-2', 'n_clicks'),
        Input('btn-182-2', 'n_clicks'),
        Input('btn-all-2', 'n_clicks'),
    ],
    prevent_initial_call=True
)
#  every callback needs at least one Input, its needed, but not used
def button_pressed_hosp(n_click14, n_click28, n_click182, n_clickall):
    n_click14, n_click28, n_click182, n_clickall = (0, 0, 0, 0)
    trigger = dash.callback_context.triggered[0]['prop_id'].split('.')[0]
    if trigger == 'btn-14-2':
        start = date.today() - timedelta(days=14)
        end = date.today()
    elif trigger == 'btn-28-2':
        start = date.today() - timedelta(days=28)
        end = date.today()
    elif trigger == 'btn-182-2':
        start = date.today() - timedelta(days=182)
        end = date.today()
    elif trigger == 'btn-all-2':
        start = '2020-03-01'
        end = date.today()
    else:
        start = '2020-03-01'
        end = date.today()

    return n_click14, n_click28, n_click182, n_clickall, start, end


@app.callback(
    [
        Output('btn-14-3', 'n_clicks'),
        Output('btn-28-3', 'n_clicks'),
        Output('btn-182-3', 'n_clicks'),
        Output('btn-all-3', 'n_clicks'),
        Output('date-picker-3', 'start_date'),
        Output('date-picker-3', 'end_date'),
    ],
    [
        Input('btn-14-3', 'n_clicks'),
        Input('btn-28-3', 'n_clicks'),
        Input('btn-182-3', 'n_clicks'),
        Input('btn-all-3', 'n_clicks'),
    ],
    prevent_initial_call=True
)
#  every callback needs at least one Input, its needed, but not used
def button_pressed_hosp(n_click14, n_click28, n_click182, n_clickall):
    n_click14, n_click28, n_click182, n_clickall = (0, 0, 0, 0)
    trigger = dash.callback_context.triggered[0]['prop_id'].split('.')[0]
    if trigger == 'btn-14-3':
        start = date.today() - timedelta(days=14)
        end = date.today()
    elif trigger == 'btn-28-3':
        start = date.today() - timedelta(days=28)
        end = date.today()
    elif trigger == 'btn-182-3':
        start = date.today() - timedelta(days=182)
        end = date.today()
    elif trigger == 'btn-all-3':
        start = '2020-03-01'
        end = date.today()
    else:
        start = '2020-03-01'
        end = date.today()

    return n_click14, n_click28, n_click182, n_clickall, start, end


@app.callback(
    [
        Output('btn-14-4', 'n_clicks'),
        Output('btn-28-4', 'n_clicks'),
        Output('btn-182-4', 'n_clicks'),
        Output('btn-all-4', 'n_clicks'),
        Output('date-picker-4', 'start_date'),
        Output('date-picker-4', 'end_date'),
    ],
    [
        Input('btn-14-4', 'n_clicks'),
        Input('btn-28-4', 'n_clicks'),
        Input('btn-182-4', 'n_clicks'),
        Input('btn-all-4', 'n_clicks'),
    ],
    prevent_initial_call=True
)
#  every callback needs at least one Input, its needed, but not used
def button_pressed_hosp(n_click14, n_click28, n_click182, n_clickall):
    n_click14, n_click28, n_click182, n_clickall = (0, 0, 0, 0)
    trigger = dash.callback_context.triggered[0]['prop_id'].split('.')[0]
    if trigger == 'btn-14-4':
        start = date.today() - timedelta(days=14)
        end = date.today()
    elif trigger == 'btn-28-4':
        start = date.today() - timedelta(days=28)
        end = date.today()
    elif trigger == 'btn-182-4':
        start = date.today() - timedelta(days=182)
        end = date.today()
    elif trigger == 'btn-all-4':
        start = '2020-03-01'
        end = date.today()
    else:
        start = '2020-03-01'
        end = date.today()

    return n_click14, n_click28, n_click182, n_clickall, start, end


@app.callback(
    [
        Output('btn-14-5', 'n_clicks'),
        Output('btn-28-5', 'n_clicks'),
        Output('btn-182-5', 'n_clicks'),
        Output('btn-all-5', 'n_clicks'),
        Output('date-picker-5', 'start_date'),
        Output('date-picker-5', 'end_date'),
    ],
    [
        Input('btn-14-5', 'n_clicks'),
        Input('btn-28-5', 'n_clicks'),
        Input('btn-182-5', 'n_clicks'),
        Input('btn-all-5', 'n_clicks'),
    ],
    prevent_initial_call=True
)
#  every callback needs at least one Input, its needed, but not used
def button_pressed_hosp(n_click14, n_click28, n_click182, n_clickall):
    n_click14, n_click28, n_click182, n_clickall = (0, 0, 0, 0)
    trigger = dash.callback_context.triggered[0]['prop_id'].split('.')[0]
    if trigger == 'btn-14-5':
        start = date.today() - timedelta(days=14)
        end = date.today()
    elif trigger == 'btn-28-5':
        start = date.today() - timedelta(days=28)
        end = date.today()
    elif trigger == 'btn-182-5':
        start = date.today() - timedelta(days=182)
        end = date.today()
    elif trigger == 'btn-all-5':
        start = '2020-03-01'
        end = date.today()
    else:
        start = '2020-03-01'
        end = date.today()

    return n_click14, n_click28, n_click182, n_clickall, start, end


# overview
@app.callback(
    Output('div-table-celkem', 'children'),
    Output('div-table-vcera', 'children'),
    Output('div-container-old', 'style'),
    Input('tabs-ockovani-graph', 'value'),
    Input('date-picker', 'start_date'),
    Input('date-picker', 'end_date')

)
def render_prehled(tab, start_date, end_date):
    show = {'display': 'block'}
    hide = {'display': 'none'}
    set_text_old = hide

    df = get_data.get_prehled()
    # delete
    df_celkem = df.iloc[:, [3, 4, 5, 6]]

    # pick relevant columns
    df_vcera_jeden = df.iloc[:, [8, 14, 12, 16, 7, 10]]
    df_vcera_celkem = df.iloc[:, [2, 13, 11, 15, 1, 9]]
    datumy = df.iloc[:, [17, 18, 19, 20, 21, 22]]
    # rename columns
    df_vcera_jeden = df_vcera_jeden.set_axis(['A', 'B', 'C', 'D', 'E', 'F'], axis=1, inplace=False)
    df_vcera_celkem = df_vcera_celkem.set_axis(['A', 'B', 'C', 'D', 'E', 'F'], axis=1, inplace=False)
    datumy = datumy.set_axis(['A', 'B', 'C', 'D', 'E', 'F'], axis=1, inplace=False)
    # iterate dates and mark old values
    columns = list(datumy)
    for i in columns:
        date_from_df = datumy[i][0]
        yesterday = date.today() - timedelta(days=1)
        if str(yesterday) != str(date_from_df):
            df_vcera_jeden[i][0] = str(df_vcera_jeden[i][0]) + '!'
            set_text_old = show
    df_vcera = df_vcera_celkem.append(df_vcera_jeden)
    df_vcera = df_vcera.set_axis([
                                'Potvrzené případy',
                                'Potvrzené případy 65+',
                                'Vykázaná očkování',
                                'Očkované osoby',
                                'Provedené PCR testy',
                                'Provedené AG testy'
                                ], axis=1, inplace=False
                            )
    vcera = date.today() - timedelta(days=1)
    df_vcera['období'] = ['celkem', vcera]
    # last column to first position
    cols = df_vcera.columns.tolist()
    cols = cols[-1:] + cols[:-1]
    df_vcera = df_vcera[cols]
    return dash_table.DataTable(
        id='table',
        columns=[{"name": i,
                  "id": i,
                  "type": 'numeric',
                  "format": Format(
                      group_delimiter=" "
                  ).group(True),
                  } for i in df_celkem.columns],
        data=df_celkem.to_dict('records'),
        page_size=2,
        fixed_columns={  # fixed first column when scrolling horizontaly
            'headers': True,
            'data': 1
        },
        style_table={
            'overflowX': 'auto',
            'minWidth': '100%',
        },
        style_cell={
            'width': '50px', 'minWidth': '50px', 'maxWidth': '50px',
            'textAlign': 'center',
            'font-family': 'sans-serif',
            'fontSize': '20px',
            'backgroundColor': '#111111',
            'color': '#CECECE',
            'border': '10px solid #010101',
        },
        style_header={
            'color': '#CECECE',
            'backgroundColor': '#111111',
            'border': '10px solid #010101',
            'fontSize': '20px',
        }
    ), dash_table.DataTable(
        id='table',
        columns=[{"name": i,
                  "id": i,
                  "type": 'numeric',
                  "format": Format(
                      group_delimiter=" "
                  ).group(True),
                  } for i in df_vcera.columns],
        data=df_vcera.to_dict('records'),
        page_size=2,
        fixed_columns={  # fixed first column when scrolling horizontaly
            'headers': True,
            'data': 1
        },
        style_table={
            'minWidth': '100%',
        },
        style_cell={
            'overflow': 'hidden',
            'width': '200px', 'minWidth': '200px', 'maxWidth': '200px',
            'textOverflow': 'elipsis',
            'textAlign': 'center',
            'font-family': 'sans-serif',
            'fontSize': '20px',
            'backgroundColor': '#111111',
            'color': '#CECECE',
            'border': '10px solid #010101',
        },
        style_header={
            'color': '#CECECE',
            'backgroundColor': '#111111',
            'border': '10px solid #010101',
            'fontSize': '20px',
        }
    ), set_text_old


# hospitalizace
@app.callback(
    Output('tabs-content-hosp-graph', 'children'),
    Input('tabs-hosp-graph', 'value'),
    Input('date-picker-2', 'start_date'),
    Input('date-picker-2', 'end_date')

)
def render_hosp(tab, start_date, end_date):
    if tab == 'tab-1-hosp-graph':
        df = get_data.get_hosp()
        dff = df[(df['Datum'] >= start_date) & (df['Datum'] <= end_date)]
        fig = px.bar(dff,
                     x='Datum',
                     y=['bez příznaků', 'lehký stav', 'střední stav', 'těžký stav'],
                     color_discrete_sequence=graph_settings.red_end_palette
                     )
        fig.update_layout(
            title_x=0.5,    # center
            height=700,
            xaxis_title="Datum",
            yaxis_title="Počet",
            margin=graph_settings.tight_layout,
            template=graph_settings.template_dark,
            legend_title_text='Příznaky',
            legend=dict(
                orientation='h',
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=0.01
            )
        )

        return dcc.Graph(
                        id='graph-1-tabs',
                        figure=fig
                    )

    elif tab == 'tab-2-hosp-graph':
        df = get_data.get_hosp_ocko()
        dff = df[(df['Datum'] >= start_date) & (df['Datum'] <= end_date)]
        fig = px.bar(dff,
                     x='Datum',
                     y=['bez očkování', 'nedokončené očkování', 'dokončené očkování', 'posilující dávka'],
                     color_discrete_sequence=graph_settings.red_start_palette
                     )
        fig.update_layout(
            title_x=0.5,    # center
            height=700,
            xaxis_title="Datum",
            yaxis_title="Počet",
            margin=graph_settings.tight_layout,
            template=graph_settings.template_dark,
            legend_title_text='Očkování',
            legend=dict(
                orientation='h',
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=0.01
            )
        )

        return dcc.Graph(
                    id='graph-1-tabs',
                    figure=fig
                )


# incidence
@app.callback(
    Output('tabs-content-incidence-graph', 'children'),
    Input('tabs-incidence-graph', 'value'),
    Input('date-picker-3', 'start_date'),
    Input('date-picker-3', 'end_date')

)
def render_incidence(tab, start_date, end_date):
    if tab == 'tab-1-incidence-graph':
        print('1')
        print(start_date)
        df = get_data.get_incidence_cr()
        dff = df[(df['Datum'] >= start_date) & (df['Datum'] <= end_date)]
        fig = go.Figure(
            data=[
                go.Bar(name='týdenní',
                       x=dff['Datum'],
                       y=dff['incidence 7'],
                       marker=dict(color=graph_settings.red_start_palette[1])),
                go.Bar(name='čtrnáctidenní',
                       x=dff['Datum'],
                       y=dff['incidence 14'],
                       marker=dict(color=graph_settings.red_start_palette[3]))
        ]
        )
        fig.update_layout(
            title_x=0.5,    # center
            height=700,
            xaxis_title="Datum",
            yaxis_title="Počet",
            margin=graph_settings.tight_layout,
            template=graph_settings.template_dark,
            legend_title_text='',
            legend=dict(
                orientation='h',
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=0.01
            )
        )

        return dcc.Graph(
                    id='graph-1-tabs',
                    figure=fig,
        )

    elif tab == 'tab-2-demografie-graph':
        df = get_data.get_ock_demo()
        dff = df[(df['Datum'] >= start_date) & (df['Datum'] <= end_date)].dropna()
        dff = dff.sort_values(by=['věková skupina'])
        fig = px.bar(dff,
                     x='Datum',
                     y='počet dávek',
                     facet_row='pohlaví',
                     barmode='group',
                     color='věková skupina',
                     color_discrete_sequence=px.colors.qualitative.Light24,
                     )
        fig.update_layout(
            title_x=0.5,    # center
            height=700,
            margin=graph_settings.tight_layout,
            template=graph_settings.template_dark,
            legend_title_text='Věk',
            legend_traceorder='normal',
            legend=dict(
                orientation='h',
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=0.01
            )
        )

        return dcc.Graph(
                    id='graph-1-tabs',
                    figure=fig
                )

    elif tab == 'tab-3-demografie-graph':
        df = get_data.get_ock_demo()
        dff = df[(df['Datum'] >= start_date) & (df['Datum'] <= end_date)].dropna()
        dff = dff.sort_values(by=['věková skupina'])
        fig = px.bar(dff,
                     x='Datum',
                     y='počet dávek',
                     facet_row='pohlaví',
                     barmode='group',
                     color='vakcína',
                     color_discrete_sequence=graph_settings.final_pal
                     )
        fig.update_layout(
            title_x=0.5,    # center
            height=700,
            margin=graph_settings.tight_layout,
            template=graph_settings.template_dark,
            legend_title_text='Věk',
            legend_traceorder='normal',
            legend=dict(
                orientation='h',
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=0.01
            )
        )

        return dcc.Graph(
            id='graph-1-tabs',
            figure=fig
        )


# nvut
@app.callback(
    Output('tabs-content-nvut-graph', 'children'),
    Output('div-table-nvut', 'children'),
    Input('tabs-nvut-graph', 'value'),
    Input('date-picker', 'start_date'),
    Input('date-picker', 'end_date'),
    State('table-nvut', 'derived_virtual_data')

)
def render_nvut(tab, start_date, end_date, rows):
    row_check, dt_content = [], []
    if rows == row_check or rows is None:
        df = get_data.get_nvut()
        dt_content = dash_table.DataTable(
            id='table-nvut',
            columns=[{"name": i, "id": i} for i in df.columns],
            data=df.to_dict('records'))
        # print(f'data from API')
    else:
        df = pd.DataFrame(rows)
        dt_content = dash_table.DataTable(
            id='table-nvut',
            columns=[{"name": i, "id": i} for i in df.columns],
            data=df.to_dict('records'))
        # print(f'data from table-nvut')

    if tab == 'tab-1-nvut-graph':
        dff = df[(df['Datum'] >= start_date) & (df['Datum'] <= end_date)]

        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(
            go.Bar(name='Denní přírůstky', x=dff['Datum'], y=dff['Nakažení'], text=dff['Nakažení']),
            secondary_y=False,
        )
        fig.add_trace(
            go.Scatter(name='Kumulativní přírůstek',
                       x=dff['Datum'],
                       y=dff['Nakažení_k'],
                       mode='lines',
                       line=dict(color='#e63946', width=5)
                       ),
            secondary_y=True,
        )
        fig.update_layout(
            title_x=0.5,    # center
            height=700,
            xaxis_title="Datum",
            margin=graph_settings.tight_layout,
            template=graph_settings.template_dark,
            legend=dict(
                orientation='h',
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=0.01
            )
        )
        fig.update_traces(marker_color='lightgrey')

        fig.update_yaxes(title_text="<b>Přírůstkový</b> počet nakažených", secondary_y=False)
        fig.update_yaxes(title_text="<b>Kumulativní</b> počet nakažených", secondary_y=True)

        return dcc.Graph(
                    id='graph-1-tabs',
                    figure=fig
                ), dt_content

    elif tab == 'tab-2-nvut-graph':
        dff = df[(df['Datum'] >= start_date) & (df['Datum'] <= end_date)]

        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(
            go.Bar(name='Denní přírůstky', x=dff['Datum'], y=dff['Vyléčení']),
            secondary_y=False,
        )
        fig.add_trace(
            go.Scatter(name='Kumulativní přírůstek',
                       x=dff['Datum'],
                       y=dff['Vyléčení_k'],
                       mode='lines',
                       line=dict(color='#e63946', width=5)
                       ),
            secondary_y=True,
        )
        fig.update_layout(
            title_x=0.5,    # center
            height=700,
            xaxis_title="Datum",
            margin=graph_settings.tight_layout,
            template=graph_settings.template_dark,
            legend=dict(
                orientation='h',
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=0.01
            )
        )
        fig.update_traces(marker_color='lightgrey')

        fig.update_yaxes(title_text="<b>Přírůstkový</b> počet vyléčených", secondary_y=False)
        fig.update_yaxes(title_text="<b>Kumulativní</b> počet vyléčených", secondary_y=True)

        return dcc.Graph(
            id='graph-1-tabs',
            figure=fig
        ), dt_content

    elif tab == 'tab-3-nvut-graph':
        dff = df[(df['Datum'] >= start_date) & (df['Datum'] <= end_date)]

        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(
            go.Bar(name='Denní přírůstky', x=dff['Datum'], y=dff['Zemřelí']),
            secondary_y=False,
        )
        fig.add_trace(
            go.Scatter(name='Kumulativní přírůstek',
                       x=dff['Datum'],
                       y=dff['Zemřelý_k'],
                       mode='lines',
                       line=dict(color='#e63946', width=5)
                       ),
            secondary_y=True,
        )
        fig.update_layout(
            title_x=0.5,    # center
            height=700,
            xaxis_title="Datum",
            margin=graph_settings.tight_layout,
            template=graph_settings.template_dark,
            legend=dict(
                orientation='h',
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=0.01
            )
        )
        fig.update_traces(marker_color='lightgrey')

        fig.update_yaxes(title_text="<b>Přírůstkový</b> počet zemřelých", secondary_y=False)
        fig.update_yaxes(title_text="<b>Kumulativní</b> počet zemřelých", secondary_y=True)

        return dcc.Graph(
            id='graph-1-tabs',
            figure=fig
        ), dt_content

    elif tab == 'tab-4-nvut-graph':
        dff = df[(df['Datum'] >= start_date) & (df['Datum'] <= end_date)]

        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(
            go.Bar(name='Denní přírůstky', x=dff['Datum'], y=dff['Testovaní']),
            secondary_y=False,
        )
        fig.add_trace(
            go.Scatter(name='Kumulativní přírůstek',
                       x=dff['Datum'],
                       y=dff['Testovaní_k'],
                       mode='lines',
                       line=dict(color='#e63946', width=5)
                       ),
            secondary_y=True,
        )
        fig.update_layout(
            title_x=0.5,    # center
            height=700,
            xaxis_title="Datum",
            margin=graph_settings.tight_layout,
            template=graph_settings.template_dark,
            legend=dict(
                orientation='h',
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=0.01
            )
        )
        fig.update_traces(marker_color='lightgrey')

        fig.update_yaxes(title_text="<b>Přírůstkový</b> počet testovaných", secondary_y=False)
        fig.update_yaxes(title_text="<b>Kumulativní</b> počet testovaných", secondary_y=True)

        return dcc.Graph(
            id='graph-1-tabs',
            figure=fig
        ), dt_content

    elif tab == 'tab-5-nvut-graph':
        dff = df[(df['Datum'] >= start_date) & (df['Datum'] <= end_date)]

        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(
            go.Bar(name='Denní přírůstky', x=dff['Datum'], y=dff['Testovaní (AG)']),
            secondary_y=False,
        )
        fig.add_trace(
            go.Scatter(name='Kumulativní přírůstek',
                       x=dff['Datum'],
                       y=dff['Testovaní_k (AG)'],
                       mode='lines',
                       line=dict(color='#e63946', width=5)
                       ),
            secondary_y=True,
        )
        fig.update_layout(
            title_x=0.5,    # center
            height=700,
            xaxis_title="Datum",
            margin=graph_settings.tight_layout,
            template=graph_settings.template_dark,
            legend=dict(
                orientation='h',
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=0.01
            )
        )
        fig.update_traces(marker_color='lightgrey')

        fig.update_yaxes(title_text="<b>Přírůstkový</b> počet testovaných AG", secondary_y=False)
        fig.update_yaxes(title_text="<b>Kumulativní</b> počet testovaných AG", secondary_y=True)

        return dcc.Graph(
            id='graph-1-tabs',
            figure=fig
        ), dt_content


# ockovani v krajich
@app.callback(
    Output('tabs-content-ockovani-graph', 'children'),
    Input('tabs-ockovani-graph', 'value'),
    Input('date-picker-5', 'start_date'),
    Input('date-picker-5', 'end_date')

)
def render_ockovani(tab, start_date, end_date):
    if tab == 'tab-1-ockovani-graph':
        fig = get_fig_ockovani('Hlavní město Praha', start_date, end_date)
        return dcc.Graph(
            id='graph-1-tabs',
            figure=fig
        )
    elif tab == 'tab-2-ockovani-graph':
        fig = get_fig_ockovani('Středočeský kraj', start_date, end_date)
        return dcc.Graph(
            id='graph-1-tabs',
            figure=fig
        )
    elif tab == 'tab-3-ockovani-graph':
        fig = get_fig_ockovani('Ústecký kraj', start_date, end_date)
        return dcc.Graph(
            id='graph-1-tabs',
            figure=fig
        )
    elif tab == 'tab-4-ockovani-graph':
        fig = get_fig_ockovani('Moravskoslezský kraj', start_date, end_date)
        return dcc.Graph(
            id='graph-1-tabs',
            figure=fig
        )
    elif tab == 'tab-5-ockovani-graph':
        fig = get_fig_ockovani('Jihomoravský kraj', start_date, end_date)
        return dcc.Graph(
            id='graph-1-tabs',
            figure=fig
        )
    elif tab == 'tab-6-ockovani-graph':
        fig = get_fig_ockovani('Olomoucký kraj', start_date, end_date)
        return dcc.Graph(
            id='graph-1-tabs',
            figure=fig
        )
    elif tab == 'tab-7-ockovani-graph':
        fig = get_fig_ockovani('Královéhradecký kraj', start_date, end_date)
        return dcc.Graph(
            id='graph-1-tabs',
            figure=fig
        )
    elif tab == 'tab-8-ockovani-graph':
        fig = get_fig_ockovani('Liberecký kraj', start_date, end_date)
        return dcc.Graph(
            id='graph-1-tabs',
            figure=fig
        )
    elif tab == 'tab-9-ockovani-graph':
        fig = get_fig_ockovani('Kraj Vysočina', start_date, end_date)
        return dcc.Graph(
            id='graph-1-tabs',
            figure=fig
        )
    elif tab == 'tab-10-ockovani-graph':
        fig = get_fig_ockovani('Jihočeský kraj', start_date, end_date)
        return dcc.Graph(
            id='graph-1-tabs',
            figure=fig
        )
    elif tab == 'tab-11-ockovani-graph':
        fig = get_fig_ockovani('Zlínký kraj', start_date, end_date)
        return dcc.Graph(
            id='graph-1-tabs',
            figure=fig
        )
    elif tab == 'tab-12-ockovani-graph':
        fig = get_fig_ockovani('Pardubický kraj', start_date, end_date)
        return dcc.Graph(
            id='graph-1-tabs',
            figure=fig
        )
    elif tab == 'tab-13-ockovani-graph':
        fig = get_fig_ockovani('Plzeňský kraj', start_date, end_date)
        return dcc.Graph(
            id='graph-1-tabs',
            figure=fig
        )
    elif tab == 'tab-14-ockovani-graph':
        fig = get_fig_ockovani('Karlovarský kraj', start_date, end_date)
        return dcc.Graph(
            id='graph-1-tabs',
            figure=fig
        )


# incidence v krajich
@app.callback(
    Output('tabs-content-inc_kraje-graph', 'children'),
    Input('tabs-inc_kraje-graph', 'value'),
    Input('date-picker-4', 'start_date'),
    Input('date-picker-4', 'end_date')

)
def render_inc_kraje(tab, start_date, end_date):
    if tab == 'tab-1-inc_kraje-graph':
        fig = get_fig_incidence('Hlavní město Praha', start_date, end_date)
        return dcc.Graph(
            id='graph-1-tabs',
            figure=fig
        )
    elif tab == 'tab-2-inc_kraje-graph':
        fig = get_fig_incidence('Středočeský kraj', start_date, end_date)
        return dcc.Graph(
            id='graph-1-tabs',
            figure=fig
        )
    elif tab == 'tab-3-inc_kraje-graph':
        fig = get_fig_incidence('Ústecký kraj', start_date, end_date)
        return dcc.Graph(
            id='graph-1-tabs',
            figure=fig
        )
    elif tab == 'tab-4-inc_kraje-graph':
        fig = get_fig_incidence('Moravskoslezský kraj', start_date, end_date)
        return dcc.Graph(
            id='graph-1-tabs',
            figure=fig
        )
    elif tab == 'tab-5-inc_kraje-graph':
        fig = get_fig_incidence('Jihomoravský kraj', start_date, end_date)
        return dcc.Graph(
            id='graph-1-tabs',
            figure=fig
        )
    elif tab == 'tab-6-inc_kraje-graph':
        fig = get_fig_incidence('Olomoucký kraj', start_date, end_date)
        return dcc.Graph(
            id='graph-1-tabs',
            figure=fig
        )
    elif tab == 'tab-7-inc_kraje-graph':
        fig = get_fig_incidence('Královéhradecký kraj', start_date, end_date)
        return dcc.Graph(
            id='graph-1-tabs',
            figure=fig
        )
    elif tab == 'tab-8-inc_kraje-graph':
        fig = get_fig_incidence('Liberecký kraj', start_date, end_date)
        return dcc.Graph(
            id='graph-1-tabs',
            figure=fig
        )
    elif tab == 'tab-9-inc_kraje-graph':
        fig = get_fig_incidence('Kraj Vysočina', start_date, end_date)
        return dcc.Graph(
            id='graph-1-tabs',
            figure=fig
        )
    elif tab == 'tab-10-inc_kraje-graph':
        fig = get_fig_incidence('Jihočeský kraj', start_date, end_date)
        return dcc.Graph(
            id='graph-1-tabs',
            figure=fig
        )
    elif tab == 'tab-11-inc_kraje-graph':
        fig = get_fig_incidence('Zlínský kraj', start_date, end_date)
        return dcc.Graph(
            id='graph-1-tabs',
            figure=fig
        )
    elif tab == 'tab-12-inc_kraje-graph':
        fig = get_fig_incidence('Pardubický kraj', start_date, end_date)
        return dcc.Graph(
            id='graph-1-tabs',
            figure=fig
        )
    elif tab == 'tab-13-inc_kraje-graph':
        fig = get_fig_incidence('Plzeňský kraj', start_date, end_date)
        return dcc.Graph(
            id='graph-1-tabs',
            figure=fig
        )
    elif tab == 'tab-14-inc_kraje-graph':
        fig = get_fig_incidence('Karlovarský kraj', start_date, end_date)
        return dcc.Graph(
            id='graph-1-tabs',
            figure=fig
        )


if __name__ == '__main__':
    app.run_server(debug=True)
