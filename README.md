





What this does:

Overview of project:
Scraped food Reviews from 8000+ Singapore Restaurants in [Tripadvisor](https://www.tripadvisor.com.sg/Restaurants-g294265-Singapore.html)
Scraped food reviews from  1700+ Singapore Restaurants in [Burpple](https://www.burpple.com)


Store original review in Database, sqlite.
Indexes cleaned review with Solr
Simple search engine frontend to query indexed data. Server is meant to be run locally.

Note: Data scraped is not uploaded or shared

***
How to run:

1. Set up Solr-7.2.1. The solr syntax used here only works for Solr 7. Create solr core named "food" and run solr locally by running `$bin/solr start`. 

2. `cd sgfood` (directory should have a requirements.txt file). Create a virtualenv and `pip3 install -r requirements.txt` 
Do ensure that correct version of Django is used.

3. `python manage.py runserver`. In your browser, go to http://127.0.0.1:8000/home/


One way to index the scraped data stored in database is to `run python manage.py shell`
In shell, run the following 2 lines:
`from sgfood_app.index_solr import run_script as r`
`r()`

After indexing is done, restart Solr core by `bin/solr stop` and then `bin/solr start`

You check http://127.0.0.1:8983/solr/admin and see the "food" core has documents indexed





