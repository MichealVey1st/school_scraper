# school_scraper

-----

Being a highschool student I have lots of assignments spread across multiple different Canvas's. I kept feeling like I was missing something somewhere so I decided to build a automated program that can do all the hard work of finding every assignment. So initally I was going to use beautiful soup, but when I configured it to log into my canvas it blocked that type of request. So because it would block a static scraper, I needed to find a scraper that acted like a user typing in the keys and so forth. That's when I came across Selenium. It perfectly fit my needs to login like a user so I got to work building a progam with selenium. This resulted in what we have today. So for the sanity of you, I can tell you which parts to copy and which ones to not.

----
## Functions

### detect_date_format(date_str):

This function is used to determine what format of date it found when looking up the assignments. There are 4 possible different date formats that I have found and 
