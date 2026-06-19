def analyze_root_cause(df):

    emissions = (
        df.groupby("department")["total_emission"]
        .sum()
        .sort_values(ascending=False)
    )

    top_dept = emissions.index[0]
    top_value = emissions.iloc[0]

    contribution = (
        top_value / emissions.sum()
    ) * 100

    dept_data = df[
        df["department"] == top_dept
    ]

    top_activity = (
        dept_data.groupby("activity_type")
        ["total_emission"]
        .sum()
        .idxmax()
    )

    return {
        "department": top_dept,
        "emission": round(top_value,2),
        "contribution": round(contribution,2),
        "driver": top_activity
    }
