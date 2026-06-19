def detect_leaks(df):

    threshold = (
        df["total_emission"].mean()
        + df["total_emission"].std()
    )

    leaks = df[
        df["total_emission"] > threshold
    ]

    return leaks
