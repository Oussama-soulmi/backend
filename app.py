from flask import Flask
import yfinance as yf
import pandas as pd
import plotly
import plotly.express as px
from flask_cors import CORS, cross_origin


app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route("/meta")
@cross_origin()
def meta():
    # Define the ticker symbol for META
    ticker = 'META'
    
    
    # Get the data of the stock
    data=yf.download(ticker,period="1d", interval="1m",prepost=True,actions=True,auto_adjust=True)

    # add Date and company axes
    data= data.reset_index()
    data.columns = ['Time', *data.columns[1:]]
    data.loc[:, "company"] ="META"

    # preparing graphJSON for parsing to react 
    fig = px.line(data, x="Time", y="Close", color="company", line_group="company", hover_name="company",
        line_shape="spline", render_mode="svg")
    fig.update_xaxes(rangeslider_visible=True)
    graphJSON = plotly.io.to_json(fig, pretty=True)

    # return
    return graphJSON

if __name__ == "__main__":
    app.run(debug=True)
