from flask import Flask, render_template, request
from forex_python.converter import CurrencyRates
import datetime
import matplotlib.pyplot as plt

app = Flask(__name__)
c = CurrencyRates()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    from_currency = request.form['from_currency'].upper()
    to_currency = request.form['to_currency'].upper()
    amount = float(request.form['amount'])

    try:
        result = c.convert(from_currency, to_currency, amount)
    except:
        result = 'Conversion failed. Please check currency codes.'

    # Generate 30-day exchange rate trend
    today = datetime.datetime.now()
    dates, rates = [], []
    for i in range(30, 0, -1):
        date = today - datetime.timedelta(days=i)
        try:
            rate = c.get_rate(from_currency, to_currency, date)
            dates.append(date.strftime('%Y-%m-%d'))
            rates.append(rate)
        except:
            continue

    if dates and rates:
        plt.figure(figsize=(10, 4))
        plt.plot(dates, rates, marker='o')
        plt.xticks(rotation=45)
        plt.title(f'Exchange Rate: {from_currency} to {to_currency} (Last 30 Days)')
        plt.xlabel('Date')
        plt.ylabel('Rate')
        plt.tight_layout()
        plt.savefig('static/rate_plot.png')
        plt.close()
        graph_path = 'static/rate_plot.png'
    else:
        graph_path = None

    return render_template('index.html', result=result, graph=graph_path)

if __name__ == '__main__':
    app.run(debug=True)
