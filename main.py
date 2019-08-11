#from scrape import parse
from bbc_scrape import parse
from plot import plot_results

matches = parse('2018-08', '2019-05')
plot_results(matches)