FinancialAnalysis
=================

Using Python to analyze data from SEC filings

------

Tristan's Objectives:

In undertaking this project, I want to combine my interests in finance, data science, and 
web development to develop an application that will drive decision making for individuals 
in financial markets.

I plan on using Python to extract, process, and analyze data obtained from SEC EDGAR APIs. 
I would also like to include a variety of front end visualizations to portray analysis on 
individual stocks and to compare stocks.

TO START, I am going to work on creating a simple tool that can query EDGAR for a ticker 
and get the most recent 10-K form.

Presently, I have written code that will get the latest filings from the SEC RSS feed, and
I am able to get the individual data points from the filing data. My next step will be to
determine formulas for the ratios that were suggested by Benjamin Graham in The Intelligent
Investor. The rules and ratios are:

    1.  An earnings-to-price yield of twice the triple-A bond yield. The earnings yield is the reciprocal of the price earnings ratio.
    2.  A price/earnings ratio down to four-tenths of the highest average P/E ratio the stock reached in the most recent five years. (Average P/E ratio is the average stock price for a year divided by the earnings for that year.)
    3.  A dividend yield of two-thirds of the triple-A bond yield.
    4.  A stock price down to two-thirds of tangible book value per share.
    5.  A stock price down to two-thirds of net current asset value — current assets less total debt.
    6.  Total debt less than tangible book value.
    7.  Current ratio (current assets divided by current liabilities) of two or more.
    8.  Total debt equal or less than twice the net quick liquidation value as defined in No. 5.
    9.  Earnings growth over the most recent ten years of seven percent compounded—a doubling of earnings in a ten-year period.
    10. Stability of growth in earnings—defined as no more than two declines of five percent or more in year-end earnings over the most recent ten years.

