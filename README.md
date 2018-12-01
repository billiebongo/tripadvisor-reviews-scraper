
Documents:
-Crawled text data: /sgfood_app/data/. Folders TA and burpple contain text files of the crawled text.
-The above data is also available in db.sqlite which can be accessed from the admin page for easy viewing. username: lek, password: no89757no89757


How to run:

1. Run solr. Put solr-7.2.1 in home directory of (preferably linux) machine. cd into solr-7.2.1 and run $bin/solr start. check if documents is indexed in solr by going to http://127.0.0.1:8983/solr/admin and see the number of documents in core "food"

2. cd into /sgfood (directory should have a requirements.txt file). $pip3 install -r requirements.txt 
Do ensure correct version of Django is used

3. $python manage.py runserver
in your browser, go to http://127.0.0.1:8000/home/


youtube link:
https://youtu.be/ARZhbKJCMIo


if solr index folder does not work:
-install solr 7.2.1.
-create core named "food"
-start solr $bin/solr start
-cd into /sgfood/ directory, and run $python manage.py shell
In the python shell, run the following 2 lines.
$from sgfood_app.index_solr import run_script as r
$r()

-Restart solr core $bin/solr stop and then $bin/solr start

-check http://127.0.0.1:8983/solr/admin and see the "food" core has documents indexed

Data from db.sqlite3 will be posted to "food" core




