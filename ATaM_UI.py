# -*- coding: utf-8 -*-
"""
Created on Fri Nov 26 23:59:53 2021

@author: sbgadhwa
"""

import dash
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc
import dash_daq as daq
import plotly.graph_objects as go
from random import randrange
import Project_Backend_Main
import numpy as np
import pandas as pd
import dash_table as dt
import dash_bootstrap_components as dbc
#import plotly.express as px



external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

atamActionsData = pd.read_csv(r'ATam_Actions_Data.csv')
atamActionsData = atamActionsData.tail(5)

themes = ['linear-gradient(to right bottom, #ffffff, #eeedfa, #dadcf5, #c5cbf1, #acbced, #94b4e7, #79ace0, #59a4d7, #3aa0c6, #259ab2, #22949c, #2e8c86)', 'linear-gradient(to right bottom, #000000, #362323, #674436, #926c45, #af9d56, #98b260, #71c57d, #00d7ab, #00c4d2, #00aaef, #0089f0, #765ecd)']


app.layout = html.Div(style={
#'background-image': 'linear-gradient(to right, #000000, #27a3a3, #016175), url("https://unsplash.com/photos/EAlbsTo6nuQ")',
#'background-image': 'linear-gradient(to left bottom, #f9ffbb, #fff4c8, #fff0e4, #fff3fa, #fff9ff, #faf3fd, #f3edfc, #eae8fb, #d8d8f8, #c5c8f5, #afb8f3, #97aaf0)',
#'background': 'radial-gradient(circle at 90% 70%, #bdbdbd, #c3c3c3, #cacaca, #d0d0d0, #d6d6d6, #dddddd, #e3e3e3)',
#'background-image': 'linear-gradient(to right bottom, #ffffff, #f0ecf7, #e4d9ee, #dbc5e2, #d4b1d5, #e2aacd, #eea4bf, #f89fae, #ffae9b, #ffc38a, #fcdd85, #def895)',


'background-image': 'linear-gradient(to right bottom, #ffffff, #e3e3e5, #c7c7cc, #abadb3, #90939b, #828a95, #73818f, #637888, #567d8e, #478290, #38878d, #2e8c86)',
#'background-image': 'linear-gradient(to right bottom, #b506c6, #9b3abc, #844cad, #74569a, #685c83, #716a84, #7a7785, #858585, #a2a2a2, #c0c0c0, #dfdfdf, #ffffff)',

'background-repeat': 'no-repeat',
'background-position': 'right top',
'background-attachmenr' : 'fixed',
'background-size': 'cover',
"border":"6px Black solid",
"font-family" : "cursive",
"font-color" : "Blue",
},
    id="dark-light-theme",
    children=[
        html.H2("ATaM Dashboard", style={"color" : "black", "font-family" : "cursive", "textAlign": "center", "border":"3px Black solid", "width":"25%", "margin-left": "37.5%"}),
        html.Div(
            html.Div(
                daq.ToggleSwitch(
                    id="my-toggle-switch", label="Theme 1 | Theme 2", value=True
                ),
                className="two columns",
            ),
            className="row",
        ),
        html.Br(),
        
        html.Div(
            [
                html.Div(
                    daq.Gauge(
                        id="my-daq-gauge1", 
                        color={"gradient":True,"ranges":{"green":[0,60],"yellow":[60,80],"red":[80,100]}},
                        showCurrentValue=True,
                        units="%",
                        style={"margin-top": "10px"},
                        min=0, max=100, value=0, label="CPU"
                    ),
                    className="four columns",
                ),
                html.Div(
                    daq.Gauge(
                        id="my-daq-gauge2",
                        color={"gradient":True,"ranges":{"green":[0,60],"yellow":[60,80],"red":[80,100]}},
                        showCurrentValue=True,
                        units="%",
                        style={"margin-top": "10px"},
                        min=0, max=100, value=0, label="RAM"
                    ),
                    className="four columns",
                ),
                html.Div(
                    daq.Tank(
                        id="my-disk",
                        max=100,
                        value=0,
                        showCurrentValue=True,
                        units="%",
                        style={"margin-left": "50px", "margin-top": "10px"},
                        label = "Disk"
                    ),
                    className="four columns",
                ),
                
            ],
            style={'width': '50%', 'display': 'inline-block', "margin-left": "10px", "border":"4px Black solid"},
            className="row",
        ),
        
        html.Div([
            dbc.Label('5 most recent Actions taken by ATaM : '),
            dt.DataTable(
            id='tbl', data=atamActionsData.to_dict('records'),
            columns=[{"name": i, "id": i} for i in atamActionsData.columns],
            ),
            dbc.Alert(id='tbl_out'),
            
            ],
            style={'width': '40%', 'display': 'inline-block', "border":"4px White solid", 'margin-left' : '55%'},
            className="row"
            ),
        
        #html.Div(
        #    dcc.Graph(id="my-graph", figure={}),
        #    className="two columns",
        #),
        
        html.Div(children=[
                    html.Div([
                        html.Br(),
                        html.Div([
                        dcc.Input(id="inputCpu", type="number", placeholder="Enter CPU Upper Threshold", debounce=True,
                                  style={'width': '25%'}),
                        
                        dcc.Input(id="inputRam", type="number", placeholder="Enter RAM Upper Threshold", debounce=True,
                                  style={'width': '25%', "margin-left": "12.5%"}),
                        
                        dcc.Input(id="inputDisk", type="number", placeholder="Enter Disk Upper Threshold", debounce=True,
                                  style={'width': '25%',  "margin-left": "12.5%"}),
                        ],
                            
                            ),
                        
                        html.Br(),
 #                       html.Br(),

                        
                       # html.Div([
                        dcc.Dropdown(
                            id='cpu_dropdown',
                            options=[
                                {'label': 'Kill', 'value': 'kill'},
                                {'label': 'Restart', 'value': 'restart'}
                                ],
                            placeholder="Action",
                            #value='kill',
                            style={'width': '75px', 'display': 'inline-block'}
                            ),
                        
                        dcc.Dropdown(
                            id='ram_dropdown',
                            options=[
                                {'label': 'Kill', 'value': 'kill'},
                                {'label': 'Restart', 'value': 'restart'}
                                ],
                            placeholder="Action",
                            #value='kill',
                            style={'width': '75px', 'display': 'inline-block', "margin-left": "27.75%"}
                            ),
                        
                        dcc.Dropdown(
                            id='disk_dropdown',
                            options=[
                                {'label': 'Delete', 'value': 'delete'},
                                
                                ],
                            placeholder="Action",
                            #value='kill',
                            style={'width': '75px','display': 'inline-block',  "margin-left": "29%"}
                            ),
                        
                        #],
                           # className = "row",
                          #  ),
                        html.Br(),
                        html.Br(),
                        
                        dcc.Input(id="actionCpu",  placeholder="Enter action applications", 
                                  debounce=True,style={'width': '25%', 'display': 'inline-block', 'vertical-align': 'middle'}),
                        
                        dcc.Input(id="actionRam",  placeholder="Enter action applications", 
                                  debounce=True,style={'width': '25%', 'display': 'inline-block', 'vertical-align': 'middle', "margin-left": "12.5%"}),
                        
                        dcc.Input(id="actionDisk",  placeholder="Enter target directory", 
                                  debounce=True,style={'width': '25%', 'display': 'inline-block', 'vertical-align': 'middle', "margin-left": "12.5%"}),
                        
                        html.Br(),
                        html.Br(),
                        ],
                                        
                        style= {'width': '50%', 'display': 'inline-block', "border":"4px Black solid", "margin-left": "10px", "margin-bottom": "10px"},
                        #className = "two columns"
                        
                        ),
                    
                    ],
                    
                    
                    className = "row" 
                    ),
        
        #html.Div(
          #  dcc.Graph(id="pie-chart", figure={}),
    
            
         #   style= {'width': '30%', 'display': 'inline-block', "border":"4px Black solid", "margin-left": "55%", "margin-bottom": "10px"},
        #),
        
        html.Div([
            html.I("Distribution of Component-wise alerts : "),
            dcc.Graph(id="my-graph", figure={}),
            ],
            style= {'width': '40%', 'height' : '80%', 'display': 'inline-block', "border":"4px Black solid", "margin-left": "55%", "margin-bottom": "10px"},
        ),
                
        dcc.Interval(id="timing", interval=100, n_intervals=-1),
        html.Div(id="output"),
    ],
        #style={"border":"6px Yellow solid"}
)




@app.callback(
    Output("my-daq-gauge1", "value"),
    Output("my-daq-gauge2", "value"),
    Input("timing", "n_intervals"),
)
def update_g(n_intervals):

    val = Project_Backend_Main.runCheck()

    return  val[1], val[2]


@app.callback(
    Output("my-graph", "figure"),
    Input("timing", "n_intervals"),
)
def update_gg(n_intervals):

    a = pd.read_csv(r'ATam_Actions_Data.csv')['Component'].value_counts(ascending=True)
    a0, a1, a2 = 0, 0, 0
    try:
        if a["CPU"] > 0 :
            a0 = a["CPU"]
    except:
        print("CPU Alert not yet arrived")
    
    try:
        if a["Disk"] > 0 :
            a1 = a["Disk"]
    except:
        print("Disk Alert not yet arrived")
        
    try:
        if a["RAM"] > 0 :
            a2 = a["RAM"]
    except:
        print("RAM Alert not yet arrived")
        
    fig = go.Figure(
        [
            go.Bar(
                x=["CPU", "RAM", "Disk"],
                y=[a0, a2, a1],
            )
        ]
    )
    fig.layout.plot_bgcolor = '#D3D3D3'
    return fig




@app.callback(
    Output("tbl", "data"),
    #Output("my-graph", "figure"),
    Input("timing", "n_intervals"),
)
def update_g1(n_intervals):

    return  pd.read_csv(r'ATam_Actions_Data.csv').tail(5).to_dict('records')



@app.callback(
    Output("my-disk", "value"),
    Input("timing", "n_intervals"),
)
def update_g2(n_intervals):
    val1 = Project_Backend_Main.runCheck()
    return round(val1[3], 2)



@app.callback(
    Output("output", "children"),
    Input("inputCpu", "value"),
    Input("inputRam", "value"),
    Input("inputDisk", "value"),
    Input("cpu_dropdown", "value"),
    Input("ram_dropdown", "value"),
    Input("disk_dropdown", "value"),
    Input("actionCpu", "value"),
    Input("actionRam", "value"),
    Input("actionDisk", "value"),
    Input("timing", "n_intervals"),
    )
def update_User_Input(inputCpu, inputRam, inputDisk, cpu_dropdown, ram_dropdown, disk_dropdown, actionCpu, actionRam, actionDisk, n_intervals):
    Project_Backend_Main.takeInputFromUI(inputCpu, inputRam, inputDisk, cpu_dropdown, ram_dropdown, disk_dropdown, actionCpu, actionRam, actionDisk)
    return ""


@app.callback(
    Output("dark-light-theme", "background-image"),
    Input("my-toggle-switch", "value"),
)
def update_g4(toggle):
    if toggle:
        return themes[0]
    else:
        return themes[1]


if __name__ == "__main__":
    app.run_server()

    