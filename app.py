from flask import Flask, render_template, request
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)


def generate_bar_chart(categories, values):
    """
    Generates a bar chart and returns it as a base64-encoded string
    so it can be embedded directly in an HTML page.
    """
    plt.figure()
    plt.bar(categories, values)

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
            categories = [c.strip() for c in request.form["categories"].split(",")]
            values = [int(v.strip()) for v in request.form["values"].split(",")]

            if len(categories) != len(values):
                error = "Categories and values must be the same length."
            else:
                chart_url = generate_bar_chart(categories, values)

        except ValueError:
            error = "Values must be integers separated by commas."

    return render_template("index.html", chart_url=chart_url, error=error)


if __name__ == "__main__":
    app.run(debug=True)
