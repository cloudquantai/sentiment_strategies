The Alexandria data includes a sentiment score of -1 or +1 (-1 is bad, and +1 is good) and a decimal confidence value between 
0 and 1 (0-no confidence, 1-completely certain), as well as a decimal relevance factor between 0 and 1 (0-not relevant, 
1-completely relevant). For the demo script, a cutoff of .3 for the relevance values is imposed before adding the value to the 
total, which, like Bloomberg, is the multiple of the sentiment score and the confidence value. An alternative approach might be 
to multiply the relevance by the sentiment and confidence values.

The sentiment stream needs to be initialized as a function:
@classmethod
    def register_event_streams(cls, md, service, account):
        return {'!sentiment/alexandria': 'on_alexandria_news'}

Queries over longer periods of time, prior to the start of the stock market day, can be made in on_start and on_strategy_start

data = service.query_data('!sentiment/alexandria', self.symbol,
                                  start_timestamp=md.market_open_time - service.time_interval(
                                      hours=sentiment_hours_prior))
Score = 0
for item in data:
    if item['Relevance'] > .3:  
        Score += (item['Sentiment'] * (item['Confidence']))
self.al_value = Score

In this particular example, Alexandria data is queried over a certain number of hours (the variable sentiment_hours_prior) before 
market open. The for loop then loops over all sentiment over those periods and adds them to the self.al_value element, which 
represents the net sentiment at the market open. You could extend this time further to gain a better idea of the sentiment 
surrounding a particular stock in the time leading up to market open.

The sentiment of a particular stock is updated by a running total, that begins after the initial call and is updated each time 
a sentiment event occurs.

def on_alexandria_news(self, event, md, order, service, account):

   if event.field['Relevance'] > .3 and event.field['Sentiment'] != 0:  
        self.al_value += (event.field['Sentiment'] * (event.field['Confidence']))


The value self.al_value is a consistently updated value that represents the current net alexandria sentiment for a stock.
