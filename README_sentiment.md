Stock sentiment represents the attitude or opinions people hold of a particular stock. Since bullish or bearish sentiment will 
certainly affect a stock’s price and trends, traders have developed different ways of creating a numerical index that represents 
public sentiment towards a stock to improve their trading algorithms. There are many different ways to calculate this number, 
but some common features include the number of times a company name appears in headlines, whether positive or negative words are 
occurring in the same context as the company, the changes in sentiment surrounding a stock sector, and in some cases integration 
of social media comments and reactions as well. Each index has a unique way of combining all of these inputs into a number 
representing investor sentiment that can be used as part of a trading strategy.

Three stock sentiment indices are available in Cloudquant: Stock Twit, Alexandria, and Bloomberg

Stock twits are a financially-themed social media platform, and the stock twit sentiment scores stem directly from this platform. 
It will tend to have a much higher volume of comments and sentiment updates, but with a smaller impact that more traditional news 
articles. You can read more about stock twits here: 
https://blog.stocktwits.com/staring-into-the-abyss-with-the-stocktwits-sentiment-screener-d7b04f3ee613
The Stock Twit data simply includes a sentiment score of a decimal value between -1 and +1, with -1 being the worst possible 
sentiment score and +1 being the best.

Bloomberg has created sentiment data based on news stories about companies since 2010. Over time, the data set has been further 
expanded through the addition of more sources for news stories, other entities, as well as sentiment on social media.
The Bloomberg data includes both a sentiment score of -1 or +1 (-1 is bad, and +1 is good) and a confidence value between 1 and 
100, where 1 means almost no confidence, and 100 means high confidence. For the demo script, the sentiment score and confidence 
are multiplied to adjust the total confidence score. I divide the final value by 100 to keep the range similar to the other two 
indices, but this is optional.

The Alexandria data includes a sentiment score of -1 or +1 (-1 is bad, and +1 is good) and a decimal confidence value between 0 
and 1 (0-no confidence, 1-completely certain), as well as a decimal relevance factor between 0 and 1 (0-not relevant, 1-completely 
relevant). For the demo script, a cutoff of .3 for the relevance values is imposed before adding the value to the total, which, 
like Bloomberg, is the multiple of the sentiment score and the confidence value. An alternative approach might be to multiply the 
relevance by the sentiment and confidence values.

There are many ways to incorporate these indices into a trading strategy. In our demo we use a “running sentiment total” wherein 
sentiment from a given source is continually added to a total, and the more positive or negative the total, the more positive or 
negative the overall sentiment. You can begin this sentiment total at the start of the day, or for a given number of hours before 
trading starts. 
Our demo is meant to be a simple implementation of sentiment data that can be further modified with components such as time decays 
of sentiment and different ways of incorporating values for relevance and confidence, so you should feel free to incorporate your 
own ideas into these scripts.

