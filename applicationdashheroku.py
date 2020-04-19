import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go

app = dash.Dash()
server = app.server



df = pd.read_csv("/Users/dines/OneDrive/Documents/coursAnneLaure/data/timesData.csv")
df = df.loc[:20, ["num_students", "female_male_ratio","university_name"]]
df['num_students'] = [float(each.replace(',','.')) for each in df.num_students]
df = df.dropna().head(20)
df["female_male_ratio"] = [(each.replace(':','/')) for each in df["female_male_ratio"]]


markdown_text = '''
# Bienvenue 
'''
texte1 = '''
Ceci est une représentation du **nombre d’étudiants total en fonction du Ratio étudiant féminin / étudiant masculin**, pour les 20 premières université du classement mondial.

1- Le premier graphique est un **Scatter plots**, chaque couleur represente une Univertité(legende).

2- Le deuxième graphique est un **Histogramme**.

3- le troisième graphique est un **Bubble Charts**, la couleur et taille des bulles est en fonction du nombre total d'étudiants par university
'''

texte2 = '''
### Le deuxième graphique "Historgamme"
'''

colors = {
    'background': 'white',
    'text': 'black'
}

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash('auth', external_stylesheets=external_stylesheets) 

app.layout = html.Div([
    dcc.Markdown(children=markdown_text, style={'textAlign': 'center', 'color': colors['text']}),
    html.Div([
        dcc.Markdown(children=texte1)
    ]),
    html.Div([
        html.H2(
            children='Scatter Plots',
            style={
                'textAlign': 'center',
                'color': colors['text']
            }
        )
    ]),
    html.Div([
            dcc.Graph(
                id='num',
                figure={
                    'data': [
                        go.Scatter(
                            x=df[df["university_name"]==i]["female_male_ratio"],
                            y=df[df["university_name"]==i]["num_students"],
                            text=df["num_students"],
                            mode='markers',
                            opacity=0.8,
                            marker={
                                'size': 15,
                                'line': {'width': 0.5, 'color': 'white'}
                            },
                            name=i
                            )for i in df.university_name.unique()

                    ],
                    'layout': go.Layout(title="le nombre d’étudiants total en fonction du Ratio (étudiant féminin / étudiant masculin)",
                        xaxis={'title': 'Ratio étudiants féminin / étudiants masculin'},
                        yaxis={'title': 'Nombre étudiants Total'},
                        margin={'l': 40, 'b': 40, 't': 100, 'r': 10},
                        legend={'x': 1.2, 'y': 1},
                        hovermode='closest'
                    )
                }
            )
        ]),

    html.Div([
        dcc.Markdown(children=texte2)
        ]),

    html.Div(style={'backgroundColor': colors['background']}, children=[
        html.H2(
            children='Histogramme',
            style={
                'textAlign': 'center',
                'color': colors['text']
            }
        ),
        html.Div(children="le nombre d’étudiants total en fonction du Ratio étudiant féminin / étudiant masculin", style={
            'textAlign': 'center',
            'color': colors['text']
        }),
        dcc.Graph(
            id='Graph1',
            figure={
                'data': [
                    go.Bar(
                    x = df["female_male_ratio"],
                    y = df["num_students"],
                    name = "university_name",
                    marker = dict(color = 'rgba(241, 136, 187, 5)', line = dict(color ='rgb(0,0,0)',width =1.5)),
                    text = df.university_name)
                ],
                'layout': {
                    'plot_bgcolor': colors['background'],
                    'paper_bgcolor': colors['background'],
                    'font': {
                        'color': colors['text']
                    }
                }
            }
        )
    ]),



    html.Div([
        html.Label('liste des Univerités'),
        dcc.Dropdown(
            id='dropdown',
            options=[
                {'label':'California Institute of Technologiy', 'value': '1'},
                {'label':'Massachussetts Institute of Technology', 'value': '2'},
                {'label':'Standford University', 'value':'3'},
                {'label':'Princeton University', 'value':'4'},
                {'label':'University of Cambridge', 'value':'5'},
                {'label':'University of Oxford', 'value':'6'},
                {'label':'University of California, Bberkeley', 'value':'7'},
                {'label':'Imperial College London', 'value':'8'},
                {'label':'Yale University','value':'9'},
                {'label':'University of California, Los Angeles','value':'10'},
                {'label':'University of Chicago', 'value':'11'},
                {'label':'Johns Hopkings University', 'value':'12'},
                {'label':'Cornell University', 'value':'13'},
                {'label':'ETH Zurich-Swiss Federal Institute of Technology Zurich', 'value':'14'},
                {'label':'University of Michigan','value':'15'},
                {'label':'University of Pennsylvania', 'value': '16'},
                {'label':'Carnegie Mellon University', 'value': '17'},
                {'label':'University of Hong Kong', 'value': '18'}],
            
            value='1'
        ),
        html.Div(id='display-value')
    ]),

    html.Div([
        html.H2(
            children='Bubble Charts',
            style={
                'textAlign': 'center',
                'color': colors['text']
            }
        )
    ]),

    html.Div([
        dcc.Graph(
            figure={
                'data' : [
                    {
                        'y': df.num_students,
                        'x': df.female_male_ratio,
                        'mode': 'markers',
                        'marker': {
                            'color': df.num_students,
                            'size': df.num_students,
                            'showscale': True # c'est la barre de couleur à droite
                        },
                        "text" :  df.university_name
                    }
                ],
                'layout': go.Layout(title = "Le nombre d’étudiants total en fonction du Ratio étudiant féminin / étudiant masculin",
                    xaxis={'title': 'Ratio étudiants féminin / étudiants masculin'},
                    yaxis={'title': 'Nombre étudiants Total'})
            }
                
        )
    ]),

    html.Label('Vous pouvez laisser vos commentaires'),
    dcc.Input(value='Bonjour', type='text')


])

@app.callback(dash.dependencies.Output('display-value', 'children'),
              [dash.dependencies.Input('dropdown', 'value')])

def display_value(value):
    return 'Université numéro {} au classement Mondial'.format(value)






if __name__ == '__main__':
    app.run_server(debug=True)