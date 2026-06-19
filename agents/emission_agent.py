import pandas as pd

def calculate_emissions(df):

    df["total_emission"] = (
        df["units"] * df["emission_factor"]
    )

    return df
