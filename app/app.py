import dash
from dash import dcc  # dash core components
from dash import html # dash html components
from dash.dependencies import Input, Output, State
from dash import Dash
import requests
import json
from loguru import logger
import os



#import dash
#import dash_bootstrap_components as dbc

import plotly.express as px
import plotly.colors



#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
external_stylesheets = [dbc.themes.FLATLY]

# app server
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

# PREDICTION API URL 
api_url = os.getenv('API_URL')
api_url = "http://{}:8001/api/v1/predict".format(api_url)

# Layout for the app
app.layout = html.Div(
    [
        html.H6("Selecciona las variables para la predicción de salario:"),
        html.Div(["Título de trabajo: ",
                  dcc.Dropdown(id='my-job-picker',
                               options=[{'label': x, 'value': x} for x in job_unique_val], 
                               value='Software Engineer')]),
        html.Br(),
        html.Div(["Nivel de experiencia: ",
                  dcc.Dropdown(id='my-exp-picker', 
                               options=[{'label': x, 'value': x} for x in exp_unique_val], 
                               value='Mid_level')]),
        html.Br(),
        html.Div(["País de residencia: ",
                  dcc.Dropdown(id='my-res-picker', 
                               options=[{'label': x, 'value': x} for x in res_unique_val], 
                               value='United States')]),
        html.Br(),
        html.Div(["País de la empresa: ",
                  dcc.Dropdown(id='my-cco-picker', 
                               options=[{'label': x, 'value': x} for x in cco_unique_val], 
                               value='United States')]),
        html.Br(),
        html.Button(id='my-button', n_clicks=0, children='Aplicar', className='btn btn-dark'),
        html.Br(),
        html.Div(id='resultado'),
        dbc.Row(
            [
                dbc.Col(dcc.Graph(id='map-fig', style={'height': '300px'}), width=6),
                dbc.Col(dcc.Graph(id='bar-fig', style={'height': '300px'}), width=6),
            ]
        ),
    ]
)

# Callback function to handle the prediction request
@app.callback(
    [Output('resultado', 'children'),
    Output('map-fig', 'figure'),
    Output('bar-fig', 'figure')],
    [Input('my-button', 'n_clicks')],
    [State('my-job-picker', 'value'),
     State('my-exp-picker', 'value'),
     State('my-res-picker', 'value'),
     State('my-cco-picker', 'value')]
)

def update_output_div(n_clicks, job_title, experience_level, employee_country, company_country):
    if n_clicks == 0 or None in [job_title, experience_level, employee_country, company_country]:
        return "Por favor, complete todos los campos."
    
    myreq ={
        "inputs": [
            {
                "job_title": job_title,
                "experience_level": experience_level,
                "employee_country": employee_country,
                "company_country": company_country
            }
        ]
    }
    
    headers =  {"Content-Type":"application/json", "accept": "application/json"}

    try:
        # POST request to the API
        response = requests.post(api_url, data=json.dumps(myreq), headers=headers)
        response.raise_for_status()  # Raise error for bad responses

        # Parse the response from the API
        data = response.json()
        logger.info("Response: {}".format(data))

        predicted_salary = data.get('predicted_salary', 'Desconocido')
        salary_range = data.get('predicted_range', 'Desconocido')

        # Pick result to return from json format
        result = f"El salario predicho es: {predicted_salary} USD, dentro del rango: {salary_range}"

    except requests.exceptions.RequestException as e:
        # Manejo de errores en caso de que falle la solicitud a la API
            logger.error(f"Error en la solicitud a la API: {e}")
            return "Hubo un error al obtener la predicción. Inténtalo de nuevo más tarde.", {}, {}
    
        return result
'''
    # Filter the data for the selected position
    filtered_df = df[df['job_title'] == job_title]

        # Update map figure
        country_median_df = filtered_df.groupby("employee_country", as_index=False).median(numeric_only=True)
        map_fig = px.choropleth(
            country_median_df,
            locations="employee_country",
            locationmode="country names",
            color="salary_in_usd",
            hover_name="employee_country",
            color_continuous_scale="Viridis",
            title=f"Salario promedio por país - Posición : {job_title}",
        )
        map_fig.update_geos(
            projection_type="robinson",
            showcoastlines=True,
            coastlinecolor="Black",
            showland=True,
            landcolor="lightgray",
            showocean=True,
            oceancolor="lightblue",
            showcountries=True,
            countrycolor="Black"
        )
        map_fig.update_layout(
            margin={"r":0, "t":50, "l":0, "b":0},
            height=300
        )

        # Update bar figure
        region_median_df = filtered_df.groupby("employee_residence", as_index=False).median(numeric_only=True)
        bar_fig = px.bar(
            region_median_df,
            x="employee_residence",
            y="salary_in_usd",
            text="salary_in_usd",
            title=f"Salario promedio por continente - Posición: {job_title}"
        )

        # Apply Viridis color scale to bar chart
        color_scale = plotly.colors.sequential.Viridis
        min_salary = region_median_df['salary_in_usd'].min()
        max_salary = region_median_df['salary_in_usd'].max()
        region_median_df['color'] = region_median_df['salary_in_usd'].apply(
            lambda x: color_scale[int((x - min_salary) / (max_salary - min_salary) * (len(color_scale) - 1))])
        bar_fig.update_traces(marker_color=region_median_df['color'])
        bar_fig.update_layout(
            margin={"r":0, "t":50, "l":0, "b":0},
            height=300
        )

        # Return the output message, map figure, and bar chart figure
        return output_message, map_fig, bar_fig
'''

 

if __name__ == '__main__':
    logger.info("Running dash")
    # app.run_server(debug=True, port=5678)
    app.run_server(debug=True)

