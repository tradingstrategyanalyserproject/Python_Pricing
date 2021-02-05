import numpy as np
from scipy.stats import norm
from flask import jsonify

#  REQUIREMENTS :
#  PACKAGES : numpy, scipy, flask
#  TO RUN : OPEN A COMMAND PROMPT
#  WRITE "cd (path where the file is)"
# "set FLASK_APP=server.py"
# "python -m flask run"
# SERVER SHOULD BE RUNNING
#
# YOU CAN CHECK THE JSON OUTPUT IN WEB BROWSER AT http://127.0.0.1:5000/price/type/spot/strike/time/rate/vol
# (replace all values from type to vol with pricing values)
# example : http://127.0.0.1:5000/price/call/100/100/12/5/30

class VanillaOption:

    def __init__(self, type_option, spotPrice, strikePrice, timeToMaturity=1, interestRate=2, volatility=20):
        self.S = float(spotPrice)
        self.K = float(strikePrice)
        self.T = float(timeToMaturity) / 12  # in month
        self.r = float(interestRate) / 100
        self.sigma = float(volatility) / 100
        self.option_type = type_option

    # Calculates d1 in the BSM equation
    def d1(self):
        _d1 = (np.log(self.S / self.K) + (self.r + 0.5 * self.sigma ** 2) * self.T) / (self.sigma * np.sqrt(self.T))
        return float(_d1)

    def d2(self):
        _d2 = self.d1() - self.sigma * np.sqrt(self.T)
        return float(_d2)

    def euro_payoff(self):
        if self.option_type == "call":
            return self.S * norm.cdf(self.d1()) - self.K * np.exp(-self.r * self.T) * \
                   norm.cdf(self.d2())

        elif self.option_type == "put":
            return -self.S * norm.cdf(-self.d1()) + self.K * np.exp(-self.r * self.T) * \
                   norm.cdf(-self.d2())

    def delta(self):
        if self.option_type == "call":
            return norm.cdf(self.d1())

        elif self.option_type == "put":
            return norm.cdf(self.d1() - 1)

    def gamma(self):
        return norm.pdf(self.d1()) / (self.S * self.sigma * np.sqrt(self.T))

    def vega(self):
        return self.S * norm.pdf(self.d1()) * np.sqrt(self.T)

    def theta(self):
        if self.option_type == "call":
            return -(self.S * norm.pdf(self.d1()) * self.sigma) / (2 * np.sqrt(self.T)) - self.r * self.K * \
                   np.exp(-self.r * self.T) * norm.cdf(self.d2())

        elif self.option_type == "put":
            return -(self.S * norm.pdf(self.d1()) * self.sigma) / (2 * np.sqrt(self.T)) + self.r * self.K * \
                   np.exp(-self.r * self.T) * norm.cdf(-self.d2())

    def rho(self):
        if self.option_type == "call":
            return self.K * self.T * np.exp(-self.r * self.T) * norm.cdf(self.d2())

        elif self.option_type == "put":
            return -self.T * self.K * np.exp(-self.r * self.T) * norm.cdf(-self.d2())



from flask import Flask
app = Flask(__name__)

@app.route('/price/<type>/<S>/<K>/<T>/<r>/<sigma>')
def answer(type, S, K, T, r, sigma):
    option = VanillaOption(type, S, K, T, r, sigma)
    jsoption = {"type_option": option.option_type, "payoff": option.euro_payoff(), "delta: ": option.delta(), "gamma: ": option.gamma(), "vega: ": option.vega(), "theta: ": option.theta(), "rho: ": option.rho()}
    return jsonify(jsoption)
