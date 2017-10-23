# Nick Schmandt (n.schmandt@gmail.com), CloudQuant, 10/23/17

from cloudquant.interfaces import Strategy
from cloudquant.util import dt_from_muts
import numpy as np

# WARNING: Currently (10/23/17) running sentiment data with "Enable Fast Simulation" will crash. You must have that option unselected
# to run sentiment scripts.

# you can only query sentiment data over long periods of time in on_start and on_strategy_start.

# not all dates are available. Currently (10/23/17) stock twits only goes from to 8/25/17.


# this value determines how long before market open to look and include sentiment data in the simulation.
# 17.5 hours should encompass all hours from prior market close to next market opening.
sentiment_hours_prior = 17.5


class CQ972aa4942cc7490cb3ac23f0c347fe35(Strategy):
    @classmethod
    def is_symbol_qualified(cls, symbol, md, service, account):
        return symbol == 'AAPL'

    # the event stream function below is necessary to query sentiment data throughout the day.

    @classmethod
    def register_event_streams(cls, md, service, account):
        return {'!sentiment/stocktwits': 'on_stocktwits'}

    def on_finish(self, md, order, service, account):
        print('end of day %s stock twit sentiment score: %.2f' % (self.symbol, self.st_value))

    def on_minute_bar(self, event, md, order, service, account, bar):

        # print('Current stock twit sentiment for %s is %.2f' % (self.symbol, self.st_value))

        # below is filler code not directly related to stock sentiment

        if md.L1.timestamp > 0:
            bar_1 = bar.minute(start=0, include_empty=True)
            bar_close = bar_1.close
            bar_open = bar_1.open
            bar_time = bar_1.timestamp
            bar_high = bar_1.high
            bar_low = bar_1.low

    def on_stocktwits(self, event, md, order, service, account):

        # this function is called on each stock twit event, note that for it to work you must have stock twit
        # included in the register event stream function above.

        # each stock twit event includes a number between -1 and +1 that represents the change to the sentiment value

        if event.field['sentiment_score'] != 0:
            print('Change in %s stock twit sentiment of %.2f' % (self.symbol, event.field['sentiment_score']))
            self.st_value += event.field['sentiment_score']
            print('Current sentiment for %s is %.2f' % (self.symbol, self.st_value))

    def on_start(self, md, order, service, account):

        # the service.query_data function below queries stock twit data from the "start_timestamp" value up to the market open on the given day.
        # this can only be called in on_start and on_strategy_start.

        # WARNING: if you do not have stock data for the dates you run your simulation, these functions will crash your script.
        # If you do not have these functions, you will get a warning message at the end of the script that sentiment data was not available.

        data = service.query_data('!sentiment/stocktwits', self.symbol,
                                  start_timestamp=md.market_open_time - service.time_interval(
                                      hours=sentiment_hours_prior))

        # the function below sums over the stock twit sentiment for the time period set by the variable sentiment_hours_prior and
        # reports total sentiment for a stock at market open.
        # the script below is if you want your sentiment to incorporate events during market close.
        Score = 0
        for item in data:
            if item['sentiment_score'] != 0:
                Score += item['sentiment_score']
        print('stock %s has an overall stock twit sentiment score of %.2f over prior %d hours at market open.' % (
        self.symbol, Score, sentiment_hours_prior))

        self.st_value = Score
        # to start clean each day, uncomment the line below.
        # self.st_value=0