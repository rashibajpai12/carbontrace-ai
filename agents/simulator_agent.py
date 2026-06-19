def simulate_reduction(df, activity_type, reduction_percent):
    current_emission = df[df["activity_type"] == activity_type]["total_emission"].sum()

    reduced_emission = current_emission * (1 - reduction_percent / 100)
    saved_emission = current_emission - reduced_emission

    total_current = df["total_emission"].sum()
    total_projected = total_current - saved_emission

    return {
        "activity": activity_type,
        "current_emission": round(current_emission, 2),
        "projected_emission": round(reduced_emission, 2),
        "saved_emission": round(saved_emission, 2),
        "total_projected": round(total_projected, 2),
        "saving_percent": round((saved_emission / total_current) * 100, 2)
    }
