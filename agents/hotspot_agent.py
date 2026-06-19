def identify_hotspots(df):

    hotspots = (
        df.groupby("department")["total_emission"]
        .sum()
        .sort_values(ascending=False)
    )

    return hotspots
