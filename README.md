# SPFLDataAnalysis

In August 2019, Steven Gerrard said that "having analysed last season, if the games finished after 86 minutes we'd have won the league. That's the brutal truth."

I heard this, and decided to analyse how the final standings would look if games ended early. Which teams are best at closing out games? How are goals distributed in games? These are the questions I wanted to find out.

This program scrapes data from [Soccerbot](http://soccerbot.com/), a website containing football data from many different leagues across the world. This website is no longer being updated as of around April 2014, but I found it useful as a starting point to get the program up and running while I develop a scraper for more recent data.

## Future Improvements/Refinements

* Improve plotting - right now I have a basic plot, but it can be a little messy with many teams. I'd like to allow the user to hover over a point in time and see the standings at that point, along with clearing up the real estate of the graph.
* Goal distribution - I'd like to graph at which points goals are scored. Do teams tend to score a lot at the beginning of the halves when they're rested, or at the end of halves when they're tired and lacking on defense? Or is there some other pattern entirely (even none at all)?
* More scrapers - I'd like to develop different scrapers for different websites, including different leagues and more recent data.
* More sports - why stop at football? In theory, my system should work for virtually any sport (although with some additional wrinkles - for instance, basketball typically doesn't allow draws, instead using overtime to determine a winner for every game).
