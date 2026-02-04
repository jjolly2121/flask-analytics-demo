from flask import Flask, render_template, request
import matplotlib

# IMPORTANT: use a non-GUI backend for Flask threads
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)


def generate_bar_chart(categories, values):
    """
    Generate a bar chart and return it as a base64-encoded PNG string.
    """
    plt.figure(figsize=(8, 5))
    plt.bar(categories, values)
    plt.xlabel("Categories")
    plt.ylabel("Values")
    plt.title("User-Generated Bar Chart")
    plt.tight_layout()

    buffer = io.BytesIO()
    plt.savefig(buffer, format="png")
    plt.close()

    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.read()).decode("utf-8")
    return image_base64


@app.route("/", methods=["GET", "POST"])
def index():
    chart_url = None
    error = None

    if request.method == "POST":
        try:
            # Parse and clean categories
            categories = [
                c.strip()
                for c in request.form.get("categories", "").split(",")
                if c.strip()
            ]

            # Parse and clean values (floats allowed)
            values = [
                float(v.strip())
                for v in request.form.get("values", "").split(",")
                if v.strip()
            ]

            if not categories or not values:
                raise ValueError("Both categories and values are required.")

            if len(categories) != len(values):
                raise ValueError(
                    "Categories and values must contain the same number of items."
                )

            chart_url = generate_bar_chart(categories, values)

        except ValueError as e:
            error = str(e)

    return render_template(
        "index.html",
        chart_url=chart_url,
        error=error
    )


if __name__ == "__main__":
    app.run(debug=True)
