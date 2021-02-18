import numpy as np
from scipy.stats import norm
from flask import jsonify

# PACKAGES : numpy, scipy, flask
# TO RUN : OPEN A COMMAND PROMPT WRITE
# "cd (path where the file is)"
# "set FLASK_APP=server.py"
# "python -m flask run"
# SERVER SHOULD BE RUNNING
#
# YOU CAN CHECK THE JSON OUTPUT IN WEB BROWSER AT http://127.0.0.1:5000/price/type/spot/strike/time/rate/vol (replace all values from type to vol with pricing values)
# example pricing : http://127.0.0.1:5000/price/call/100.0/100.0/12.0/5.0/30.0
# example strike variable : http://127.0.0.1:5000/variable/strike/100.0/150.0/call/100.0/12.0/5.0/30.0
# example spot variable : http://127.0.0.1:5000/variable/strike/100.0/150.0/call/100.0/12.0/5.0/30.0
# example sigma variable : http://127.0.0.1:5000/variable/sigma/100.0/150.0/call/100.0/100.0/12.0/5.0

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


#Setting up server
from flask import Flask
app = Flask(__name__)

# Calculus of one price with all parameters defined
@app.route('/price/<type>/<float:S>/<float:K>/<float:T>/<float:r>/<float:sigma>')
def answer(type, S, K, T, r, sigma):
    option = VanillaOption(type, S, K, T, r, sigma)
    jsoption = {"type_option": option.option_type, "payoff": option.euro_payoff(), "delta: ": option.delta(), "gamma: ": option.gamma(), "vega: ": option.vega(), "theta: ": option.theta(), "rho: ": option.rho()}
    return jsonify(jsoption)

# Calculus of several possible values of greeks / price, depending on strike price variation
@app.route('/variable/strike/<float:min>/<float:max>/<type>/<float:S>/<float:T>/<float:r>/<float:sigma>')
def answerstrike(type, S, T, r, sigma, min, max):
    x = np.linspace(min, max, 500)
    myanswer = []
    for i in range(len(x)):
        option = VanillaOption(type, S, x[i], T, r, sigma)
        jsoption = {"type_option": option.option_type, "payoff": option.euro_payoff(), "delta: ": option.delta(), "gamma: ": option.gamma(), "vega: ": option.vega(), "theta: ": option.theta(), "rho: ": option.rho()}
        myanswer.append(jsoption)
    return jsonify(myanswer)

# Calculus of several possible values of greeks / price, depending on spot price variation
@app.route('/variable/spot/<float:min>/<float:max>/<type>/<float:K>/<float:T>/<float:r>/<float:sigma>')
def answerspot(type, K, T, r, sigma, min, max):
    x = np.linspace(min, max, 500)
    myanswer = []
    for i in range(len(x)):
        option = VanillaOption(type, x[i], K, T, r, sigma)
        jsoption = {"type_option": option.option_type, "payoff": option.euro_payoff(), "delta: ": option.delta(), "gamma: ": option.gamma(), "vega: ": option.vega(), "theta: ": option.theta(), "rho: ": option.rho()}
        myanswer.append(jsoption)
    return jsonify(myanswer)

# Calculus of several possible values of greeks / price, depending on sigma variation
@app.route('/variable/sigma/<float:min>/<float:max>/<type>/<float:S>/<float:K>/<float:T>/<float:r>')
def answersigma(type, S, K, T, r, min, max):
    x = np.linspace(min, max, 500)
    myanswer = []
    for i in range(len(x)):
        option = VanillaOption(type, S, K, T, r, x[i])
        jsoption = {"type_option": option.option_type, "payoff": option.euro_payoff(), "delta: ": option.delta(), "gamma: ": option.gamma(), "vega: ": option.vega(), "theta: ": option.theta(), "rho: ": option.rho()}
        myanswer.append(jsoption)
    return jsonify(myanswer)
