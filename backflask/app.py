from flask import Flask, jsonify, request
import pandas as pd
import plotly.express as px
import json
from flask_cors import CORS
from funcao import minMax

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

df = pd.read_csv('penguins.csv')
min_max_values = minMax(df)

@app.route('/plot', methods=['GET'])
def plot():
    plot_type = request.args.get('type', 'scatter')
    flipper_length_min = float(request.args.get('flipper_length_min', min_max_values['flipper_length_min']))
    flipper_length_max = float(request.args.get('flipper_length_max', min_max_values['flipper_length_max']))
    body_mass_min = float(request.args.get('body_mass_min', min_max_values['body_mass_min']))
    body_mass_max = float(request.args.get('body_mass_max', min_max_values['body_mass_max']))

    filtered_df = df[
        (df['flipper_length_mm'] >= flipper_length_min) &
        (df['flipper_length_mm'] <= flipper_length_max) &
        (df['body_mass_g'] >= body_mass_min) &
        (df['body_mass_g'] <= body_mass_max)
    ]

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
                'y': 0.9,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'
            },
            legend_title_text='Penguin island',
            margin=dict(l=20, r=20, t=50, b=20),
            plot_bgcolor='#f0f0f0',
            paper_bgcolor='#f0f0f0',
            font=dict(color='#7a7777')
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
            height=600,
        )

        fig.update_layout(
            title={
                'text': "Distribution of Body Mass by Penguin Species",
                'y': 0.9,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'
            },
            legend_title_text='Species',
            margin=dict(l=20, r=20, t=50, b=20),
            plot_bgcolor='#f0f0f0',
            paper_bgcolor='#f0f0f0',
            font=dict(color='#7a7777')
        )

    elif plot_type == 'barplot':
        species_count = filtered_df.groupby(['island', 'species']).size().reset_index(name='count')
        fig = px.bar(
            species_count,
            x='island',
            y='count',
            color='species',
            barmode='group',
            title='Count of Penguin Species by Island',
            labels={'count': 'Count of species', 'island': 'Island'},
            height=600
        )
        fig.update_layout(
            title={
                'text': "Count of Penguin Species by Island",
                'y': 0.9,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'
            },
            legend_title_text='Species',
            margin=dict(l=20, r=20, t=50, b=20),
            plot_bgcolor='#f0f0f0',
            paper_bgcolor='#f0f0f0',
            font=dict(color='#7a7777')
        )
    else:
        return jsonify({'error': 'Invalid plot type'}), 400

    return jsonify(json.loads(fig.to_json()))

if __name__ == '__main__':
    app.run(debug=True)
