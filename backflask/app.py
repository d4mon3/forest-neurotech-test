from flask import Flask, jsonify, request
import pandas as pd
import plotly.express as px
import json
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

df = pd.read_csv('penguins.csv')
# df = pd.read_csv('https://github.com/mwaskom/seaborn-data/blob/master/penguins.csv?raw=true')
# print("-------------------------df--------------------", df)
@app.route('/plot', methods=['GET'])
def plot():
    plot_type = request.args.get('type', 'scatter')
    flipper_length_min = request.args.get('flipper_length_min', 0, type=float)
    flipper_length_max = request.args.get('flipper_length_max', df['flipper_length_mm'].max(), type=float)
    
    filtered_df = df[(df['flipper_length_mm'] >= flipper_length_min) & (df['flipper_length_mm'] <= flipper_length_max)]

    if plot_type == 'scatter':
        fig = px.scatter(
            filtered_df,
            x='flipper_length_mm',
            y='body_mass_g',
            color='island',
            symbol='species',
            title='Penguin size, Palmer Station LTER',
            labels={'flipper_length_mm': 'Flipper length (mm)', 'body_mass_g': 'Body mass (g)'},
            height=600
        )      
        fig.update_layout(
            title={
                'text': "Penguin size, Palmer Station LTER",
                'y':0.9,
                'x':0.5,
                'xanchor': 'center',
                'yanchor': 'top'
            },
            legend_title_text='Penguin island',
            margin=dict(l=20, r=20, t=50, b=20),
        )

        fig.update_traces(marker=dict(size=12), selector=dict(mode='markers'))
        fig.update_traces(marker=dict(line=dict(width=1, color='DarkSlateGrey')))
    
    elif plot_type == 'histogram':
        fig = px.histogram(
            filtered_df,
            x='species',
            y='body_mass_g',
            color='species',
            title='Distribution of Body Mass by Penguin Species',
            labels={'body_mass_g': 'Body mass (g)', 'species': 'Penguin species'},
            height=600
        )
        
        fig.update_layout(
            title={
                'text': "Distribution of Body Mass by Penguin Species",
                'y':0.9,
                'x':0.5,
                'xanchor': 'center',
                'yanchor': 'top'
            },
            legend_title_text='Species',
            margin=dict(l=20, r=20, t=50, b=20),
        )

    return jsonify(json.loads(fig.to_json()))

@app.route('/summary', methods=['GET'])
def summary():
    summary_stats = df.groupby('species').describe().to_dict()
    # Convert tuple keys to strings
    summary_stats_str_keys = {str(k): v for k, v in summary_stats.items()}
    return jsonify(summary_stats_str_keys)

if __name__ == '__main__':
    app.run(debug=True)