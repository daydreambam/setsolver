# setsolver
Automatically solves the set puzzle at:
https://www.setgame.com/set/puzzle

Requires selenium and whatever webdriver you need for your default browser (I tested with Firefox and geckodriver).
You also need BeautifulSoup4 and requests.

To run simply run:
@py setsolver.py

This will scrapy today's puzzle for the current board state, solve it, launch a browser, and click the necessary cards to win.
