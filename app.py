from flask import Flask, render_template, request
import requests

app = Flask(__name__)

def get_currency_rates():
    url = "https://api.freecurrencyapi.com/v1/latest?apikey=fca_live_BVdLmxLU8wN6ZcnAWW2GsufSvpZkVYiJyhK7hA9o"
    response = requests.get(url)
    data = response.json()
    return data['data']

@app.route("/", methods=["POST", "GET"])
def conversion():
    result = None
    error = None

    if request.method == "POST":
        try:
            amount = float(request.form.get("amount"))
            source_currency = request.form.get("source_currency").upper()
            target_currency = request.form.get("target_currency").upper()

            rates = get_currency_rates()

            if source_currency not in rates or target_currency not in rates:
                error = "Invalid currency code."
            else:
                currency_to_usd = amount / rates[source_currency]
                final_conversion = currency_to_usd * rates[target_currency]

                result = f"{amount} {source_currency} = {round(final_conversion, 2)} {target_currency}"
        except Exception as e:
            error = f"Something went wrong: {str(e)}"

    return render_template("home.html", result=result, error=error)

if __name__ == "__main__":
    app.run(debug=True)