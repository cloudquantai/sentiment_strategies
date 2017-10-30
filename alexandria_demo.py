# Nick Schmandt (n.schmandt@gmail.com), CloudQuant, 10/23/17

# This code is designed to run in the cloudquant environment, at https://info.cloudquant.com/

# Note that sentiment is a feature that is only available in the Elite Version of CloudQuant

from cloudquant.interfaces import Strategy
from cloudquant.util import dt_from_muts
import numpy as np

# WARNING: Currently (10/16/17) running sentiment data with "Enable Fast Simulation" will crash. You must have that option unselected
# to run sentiment scripts.

# you can only query sentiment data over long periods of time in on_start and on_strategy_start.

# Alexandria data is currently (10/23/17) available from 2011 through September of 2017


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
        return {'!sentiment/alexandria': 'on_alexandria_news'}

    def on_finish(self, md, order, service, account):
        print('end of day %s alexandria sentiment score: %.2f' % (self.symbol, self.al_value))

    def on_minute_bar(self, event, md, order, service, account, bar):

        # print('Current alexandria sentiment for %s is %.2f' % (self.symbol, self.al_value))


        # below is filler code not directly related to stock sentiment

        if md.L1.timestamp > 0:
            bar_1 = bar.minute(start=0, include_empty=True)
            bar_close = bar_1.close
            bar_open = bar_1.open
            bar_time = bar_1.timestamp
            bar_high = bar_1.high
            bar_low = bar_1.low

    def on_alexandria_news(self, event, md, order, service, account):

        # this function is called on each alexandria news event

        if event.field['Relevance'] > .3 and event.field[
            'Sentiment'] != 0:  # this is a relevance threshold to prevent irrelevant information from being processed.
            print('Change in %s stock sentiment of %d with confidence %d' % (
            self.symbol, event.field['Sentiment'], event.field['Confidence']))
            self.al_value += (event.field['Sentiment'] * (event.field['Confidence']))
            print('Current alexandria sentiment for %s is %.2f' % (self.symbol, self.al_value))

    def on_start(self, md, order, service, account):

        # the service.query_data function below queries data from the "start_timestamp" value up to the market open on the given day.
        # this can only be called in on_start and on_strategy_start.

        # WARNING: if you do not have stock data for the dates you run your simulation, these functions will crash your script.
        # If you do not have these functions, you will get a warning message at the end of the script that sentiment data was not available.

        data = service.query_data('!sentiment/alexandria', self.symbol,
                                  start_timestamp=md.market_open_time - service.time_interval(
                                      hours=sentiment_hours_prior))

        Score = 0
        for item in data:
            if item[
                'Relevance'] > .3:  # this is a relevance threshold to prevent irrelevant information from being processed.
                Score += (item['Sentiment'] * (item['Confidence']))
        print('stock %s has an overall alexandria sentiment score of %.2f over prior %d hours at market open.' % (
        self.symbol, Score, sentiment_hours_prior))

        # if you want your sentiment values for the day to include values from the time period before market open:
        self.al_value = Score
        # to start clean each day, uncomment the line below.
        # self.al_value=0
