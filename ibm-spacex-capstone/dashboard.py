from pathlib import Path
import pandas as pd
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
D=pd.read_csv(Path(__file__).parent/'data/spacex_launch_dash.csv')
app=Dash(__name__)
app.layout=html.Div([html.H1('Falcon 9 Launch Dashboard'),html.P('Historical IBM course dashboard dataset: 56 launches'),dcc.Dropdown(id='site',options=[{'label':'All sites','value':'ALL'}]+[{'label':v,'value':v} for v in sorted(D['Launch Site'].unique())],value='ALL',clearable=False),html.Div([dcc.Graph(id='pie',style={'width':'46%'}),dcc.Graph(id='scatter',style={'width':'54%'})],style={'display':'flex'}),html.P('Payload range (kg)'),dcc.RangeSlider(id='payload',min=0,max=10000,step=1000,value=[0,10000],marks={i:str(i) for i in range(0,10001,2000)})],style={'fontFamily':'Arial','padding':'20px','backgroundColor':'#f7f9fc'})
@app.callback(Output('pie','figure'),Output('scatter','figure'),Input('site','value'),Input('payload','value'))
def update(site,bounds):
 d=D if site=='ALL' else D[D['Launch Site']==site]
 d=d[d['Payload Mass (kg)'].between(*bounds)]
 if site=='ALL':
  p=d[d['class']==1].groupby('Launch Site').size().reset_index(name='Successful landings')
  pie=px.pie(p,names='Launch Site',values='Successful landings',title='Share of successful landings by site')
 else:
  p=d.groupby('class').size().reset_index(name='Launches');p['Outcome']=p['class'].map({0:'Unsuccessful',1:'Successful'})
  pie=px.pie(p,names='Outcome',values='Launches',title=site+' landing outcomes')
 scatter=px.scatter(d,x='Payload Mass (kg)',y='class',color='Booster Version Category',title='Payload and landing outcome',hover_data=['Launch Site'])
 scatter.update_yaxes(tickvals=[0,1],ticktext=['Unsuccessful','Successful'])
 return pie,scatter
if __name__=='__main__':app.run(port=8050,debug=False)
