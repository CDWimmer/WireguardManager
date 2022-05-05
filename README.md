# WireguardManager
A webpanel for generating wirguard configurations


### Development
To set up a development environment do the following:
1. Clone the repo
2. Create a virtual environment in the root of the repo `python -m venv venv`
3. Activate the virtual environment `source venv/bin/activate`
4. Install the python dependencies `pip install -r requirements.txt`
5. Migrate your database `python webpanel/manage.py migrate`
6. Create a file called "debug.txt" in the webpanel directory `touch webpanel/debug.txt`
7. Run the test server `python webpanel/manage.py runserver`