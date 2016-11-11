# Lidia Dokuchaeva - 21331893

## Accessing the Project
# End User

A running version of the app is available at http://21331893.au-syd.mybluemix.net/.

A user can:
- Search by a specific news article URL to see the analytics
- Search by a keyword or a keyphrase
- See some charts outlining overall statistics
- Do an advanced Cloudant Query, using JSON

# Admin
This project can also be accessed (in the au-syd region) through the Bluemix Dashboard-->Apps-->21331893. This should
 be visible to everyone in the organization. In order to run it, start the app.

 If a fresh copy is needed, clone the repository given below, and deploy it as a Bluemix App.

 The original git repository is available at https://hub.jazz.net/git/tenkeyangle/21331893 - it can be accessed
 through the app, and is part of the official Bluemix DevOps pipeline - pushing changes to it will update the app
 code, and as such is the quickest way to deploy changes to the app.

 A GitHub clone is available at .

Note: this project also uses a Cloudant database, which is bound to the app. If access is needed, or a copy of the database is required, the credentials are:

* Username: 1a818337-f029-449a-8a03-d34f30877d1d-bluemix
* Password: b20bcbf26bac5fa4ed56df09b07755ac1d8ccf6e3d3ad1177902957c1ca192c0
* URL: https://1a818337-f029-449a-8a03-d34f30877d1d-bluemix:b20bcbf26bac5fa4ed56df09b07755ac1d8ccf6e3d3ad1177902957c1ca192c0@1a818337-f029-449a-8a03-d34f30877d1d-bluemix.cloudant.com
* Database name: uwanews
* AlchemyAPI key: 6026adae6314a2a74df3c7a23a8e99d7f6e20c28

An API key for AlchemyAPI is also needed. The free key currently used is given above. However, if another key is
needed, going to the Bluemix Dashboard-->21331893-->Runtime-->Environment Variables will let you see the environment
variables used, and change the alchemyKey one to the key you have. In that view, you can also see the details of the
services currently bound to the app in VCAP_SERVICES, and potentially bind an AlchemyAPI service as well.

Additionaly, an IBM Workload Scheduler is bound to the service. Currently, it is set to send a GET request to
http://21331893.au-syd.mybluemix.net/scrape, which adds data to the database. In order to fill up the Cloudant
database, either schedule a similar call or go manually to the page. (Note: if the allocated amount of calls per day
is hit, an error is thrown. That is expected behavior, and should not be cause for alarm).

The workflow for this project goes like this:
* Data is scraped from news.uwa.edu.au: links and article titles are put into items/news.csv
* When http://21331893.au-syd.mybluemix.net/scrape is accessed, usually by an automated process, data from the CSV is
 read, and the program calls AlchemyLanguage to analyze each article and put the document into the database.
* The users can then data from the user interface, which queries the database, or by accessing the database directly

## Requirements
### Functional Requirements
 - 
### Non-Functional Requirements
 - Scalability: the database must be able to handle a large amount of data
 - Availability: the database must retrieve data quickly, to reduce user wait
 - Flexibility: the database should be able to accomodate a large variety of queries
 - Usability: the website must be user-friendly and easy to navigate
 - Room for Growth: the project should provide a framework that can be modified and extended by other developers

## Resources Used
- [Pygal and Flask Integration](https://www.google.com.au/url?sa=t&rct=j&q=&esrc=s&source=web&cd=1&cad=rja&uact=8&ved=0ahUKEwjymPrbxp3QAhXNNpQKHRLqDScQFggcMAA&url=http%3A%2F%2Fwww.blog.pythonlibrary.org%2F2015%2F04%2F16%2Fusing-pygal-graphs-in-flask%2F&usg=AFQjCNFKWy6PF9MOshjGlIs8BugYV8RIxQ)
- [Cloudant Query Tutorial](https://cloudant.com/using-cloudant-query-tutorial/)
- [Flask Tutorial](http://flask.pocoo.org/docs/0.11/tutorial/)
- [Pygal Tutorial](http://www.pygal.org/en/stable/documentation/first_steps.html)
- [Scrapy Tutorial](https://doc.scrapy.org/en/latest/intro/tutorial.html)
- CloudFoundry Sample Python/Flask app
- [Flask Bluemix HelloWorld App](https://www.ibm.com/blogs/bluemix/2015/03/simple-hello-world-python-app-using-flask/)
