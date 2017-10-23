# Nick Schmandt (n.schmandt@gmail.com), CloudQuant, 10/23/17

from cloudquant.interfaces import Strategy
from cloudquant.util import dt_from_muts
import numpy as np

# WARNING: Currently (10/16/17) running sentiment data with "Enable Fast Simulation" will crash. You must have that option unselected
# to run sentiment scripts.

# you can only query sentiment data over long periods of time in on_start and on_strategy_start.

# bloomberg data runs from


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
        return {'!sentiment/bloomberg/story/news': 'on_bloomberg_news'}

    def on_finish(self, md, order, service, account):
        print('end of day %s bloomberg sentiment score: %.2f' % (self.symbol, self.bb_value))

    def on_minute_bar(self, event, md, order, service, account, bar):

        # print('Current bloomberg sentiment for %s is %.2f' % (self.symbol, self.bb_value/100)) Bloomberg values are 100x other stock values

        # below is filler code not directly related to stock sentiment

        if md.L1.timestamp > 0:
            bar_1 = bar.minute(start=0, include_empty=True)
            bar_close = bar_1.close
            bar_open = bar_1.open
            bar_time = bar_1.timestamp
            bar_high = bar_1.high
            bar_low = bar_1.low

    def on_bloomberg_news(self, event, md, order, service, account):

        # this function is called on each bloomberg news event

        # bloomberg news events include a Score, +1 or -1, and a Confidence Value that represents the percent
        # certainty of their prediction (between 1 and 100)

        if event.field['Score'] != 0:
            print('Bloomberg event: ' + event.field['Headline'])
            print('Change in %s stock sentiment of %d with confidence %d' % (
            self.symbol, event.field['Score'], event.field['Confidence']))
            self.bb_value += (event.field['Score'] * (event.field['Confidence']))
            print('Current bloomberg sentiment for %s is %.2f' % (self.symbol, self.bb_value / 100))

    def on_start(self, md, order, service, account):

        data = service.query_data('!sentiment/bloomberg/story/news', self.symbol,
                                  start_timestamp=md.market_open_time - service.time_interval(
                                      hours=sentiment_hours_prior))

        Score = 0
        for item in data:
            if item['Score'] != 0:
                # print(item['Headline'])
                # print(service.time_to_string(item['timestamp']))
                # print(item['Score'])
                # print(item['Confidence'])
                Score += (item['Score'] * (item['Confidence']))
        print('stock %s has an overall bloomberg sentiment score of %.2f over prior %d hours at market open.' % (
        self.symbol, Score / 100, sentiment_hours_prior))

        self.bb_value = Score
        # to start clean each day, uncomment the line below.
        # self.bb_value=0