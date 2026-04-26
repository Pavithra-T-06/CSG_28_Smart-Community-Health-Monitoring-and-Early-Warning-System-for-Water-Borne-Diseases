def generate_explanation(data, risk):
    ph, turbidity, tds, coliform, rainfall, temperature = data[0]

    explanation = "💧 Water Quality Analysis:\n\n"

    if risk == "High":
        explanation += "The water is unsafe for consumption.\n"
    elif risk == "Medium":
        explanation += "The water may pose health risks.\n"
    else:
        explanation += "The water appears safe.\n"

    explanation += "\nKey Observations:\n"

    if coliform > 0:
        explanation += "- Bacterial contamination detected\n"
    if tds > 500:
        explanation += "- High dissolved solids\n"
    if turbidity > 5:
        explanation += "- Poor water clarity\n"
    if ph < 6.5 or ph > 8.5:
        explanation += "- Unsafe pH levels\n"

    explanation += "\nRecommended Action:\n"

    if risk == "High":
        explanation += "Avoid drinking. Boil or purify immediately."
    elif risk == "Medium":
        explanation += "Use filtered or boiled water."
    else:
        explanation += "Safe for normal use."

    return explanation