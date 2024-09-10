from datetime import datetime
from operator import itemgetter
import pandas as pd
from marketquant.tools.utils.bar_plotter import BarPlotter

class GammaExposure:
    def __init__(self, client):
        """
        Initializes the GammaExposure class with a Schwab API client
        :param client: Initialized Schwab API client
        """
        self.client = client

    @classmethod
    def run(cls, client, symbol, num_strikes=200, barchart=False, positive_color='blue', negative_color='red'):
        """
        Creates an instance and directly calculates the gamma exposure in one step.
        If barchart is True, it will also plot the gamma exposure chart.
        :param client: Initialized Schwab API client
        :param symbol: Stock ticker symbol (e.g., 'AAPL')
        :param num_strikes: Number of strikes closest to the money to fetch
        :param barchart: Whether to plot the gamma exposure chart
        :param positive_color: Color for positive exposure bars (default: 'blue')
        :param negative_color: Color for negative exposure bars (default: 'red')
        :return: Pandas DataFrame with gamma exposure data
        """
        instance = cls(client)
        df = instance.get_gamma_exposure(symbol, num_strikes)

        # If barchart is True, this will validate the data and create the chart
        if barchart:
            plotter = BarChartPlotter(df, x_col="strikePrice", y_col="gammaExposure")
            if plotter.confirm_valid_data():
                plotter.plot_barchart(
                    positive_color=positive_color,
                    negative_color=negative_color,
                    title=f"Gamma Exposure for {symbol}"
                )

        return df

    def get_option_chains(self, symbol, num_strikes=200):
        """
        Fetches option chains for the given symbol.
        :param symbol: Stock ticker symbol (e.g., 'AAPL')
        :param num_strikes: Number of strikes closest to the money to fetch
        :return: Sorted option chains closest to the money
        """
        option_chains_response = self.client.option_chains(symbol).json()

        calls = option_chains_response['callExpDateMap']
        puts = option_chains_response['putExpDateMap']

        options = self.flatten_option_chain(calls) + self.flatten_option_chain(puts)

        spot_price = option_chains_response['underlyingPrice']
        sorted_options = sorted(options, key=lambda x: abs(x['strikePrice'] - spot_price))

        return sorted_options[:num_strikes]

    def flatten_option_chain(self, option_chain):
        """
        Flattens the option chain dictionary into a list of option contracts
        :param option_chain: The option chain dictionary from Schwab
        :return: Flattened list of option contracts
        """
        flattened = []
        for exp_date, strikes in option_chain.items():
            for strike_price, contracts in strikes.items():
                for contract in contracts:
                    contract['expirationDate'] = exp_date
                    contract['strikePrice'] = float(strike_price)
                    flattened.append(contract)
        return flattened

    def calculate_gamma_exposure(self, option_chain):
        """
        Calculates gamma exposure for each option in the chain.
        :param option_chain: List of option contracts
        :return: List of gamma exposures for each contract
        """
        gamma_exposures = []
        for option in option_chain:
            gamma = option['gamma']
            price = option['strikePrice']
            contract_size = 100
            exposure = gamma * price * contract_size

            gamma_exposures.append({
                'symbol': option['symbol'],
                'strikePrice': price,
                'gammaExposure': exposure,
                'expirationDate': option['expirationDate']
            })

        return gamma_exposures

    def get_gamma_exposure(self, symbol, num_strikes=200):
        """
        Gets the gamma exposure for the specified symbol.
        :param symbol: Stock ticker symbol (e.g., 'AAPL')
        :param num_strikes: Number of strikes closest to the money
        :return: Pandas DataFrame with gamma exposure data
        """
        option_chain = self.get_option_chains(symbol, num_strikes)

        gamma_exposure = self.calculate_gamma_exposure(option_chain)

        df = pd.DataFrame(gamma_exposure)
        return df.sort_values(by='gammaExposure', ascending=False)
