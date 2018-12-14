# Tripadvisor web scraper
- Scrapes food Reviews from 9 000+ Singapore Restaurants in [Tripadvisor](https://www.tripadvisor.com.sg/Restaurants-g294265-Singapore.html)
- Scrapes food reviews from  1700+ Singapore Restaurants in [Burpple](https://www.burpple.com)
- Indexes preprocessed data with Solr and lucene.
- Provides a simple server with Home and Results Page. Server processes query to better find suitable results (eg identifying if query is a question or looking for food/restaurant related data) and processes resulting query with similar precedure as the data before indexing to ensure consistency
- original data stored in sqlite3.
 
 
***
# Requirements
- Start virtualenv and run `pip install -r requirements.txt`
- Set up Solr-7.2.1. The solr syntax used here only works for Solr 7. Create solr core named "food" and run solr locally by running `$bin/solr start`. 
-`cd sgfood` (directory should have a requirements.txt file). Create a virtualenv and `pip3 install -r requirements.txt` 
Do ensure that correct version of Django is used.

- `python manage.py runserver`. In your browser, go to http://127.0.0.1:8000/home/

# Notes: 
Data scraped is not uploaded or shared

- Current implementation to index the scraped data stored in database is to `run python manage.py shell`
In shell, run the following 2 lines:
`from sgfood_app.index_solr import run_script as r`
`r()`

After indexing is done, restart Solr core by `bin/solr stop` and then `bin/solr start`

You check http://127.0.0.1:8983/solr/admin and see the "food" core has documents indexed





