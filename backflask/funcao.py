import pandas as pd

def minMax(df):
    flipper_length_min = df['flipper_length_mm'].min()
    flipper_length_max = df['flipper_length_mm'].max()
    body_mass_min = df['body_mass_g'].min()
    body_mass_max = df['body_mass_g'].max()

    return {
        'flipper_length_min': flipper_length_min,
        'flipper_length_max': flipper_length_max,
        'body_mass_min': body_mass_min,
        'body_mass_max': body_mass_max
    }