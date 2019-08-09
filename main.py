from scrape import parse
from pts_after_n_min import pts_after_n_min as panm
from plot import plot_results

matches = parse("jjl13.htm")
plot_results(matches)