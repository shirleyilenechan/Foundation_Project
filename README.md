# <img src="https://sassytownhouseliving.com/wp-content/uploads/2016/04/foundationShades2.png">

## www.throwingshade.net

## About

Throwing Shade is a foundation matching application that allows users to upload a photo and then recommends foundation products for the user's skin tone. Users are able to leave reviews for each brand, see each brand's latest media posts from Twitter, as well as favorite their preferred products.

I implemented k-means clustering in order to find the dominant color for each foundation product and the dominant color for the user's face. Foundation recommendations are based on the closest color distance between the user's skin color and each foundation shade. In the future, I hope to incorporate white balance and exposure adjustment--as well as convert the hex codes to lab space-- for more accurate recommendations.

## <a name="tech-stack"></a>Tech Stack
Scikit Image, Flask, Python, PostgreSQL, SqlAlchemy, PIL(Python Image Library), Ajax, Jinja , Bootstrap, HTML, CSS, unittest, SciPy

APIs Used:
Twitter, Sephora XHR

## <a name="features"></a>Features
![gif website walkthrough](/static/uploads/recording_take_3.gif)

## <a name="installation"></a>Setup/Installation 

Clone repository:
```
$ git clone https://github.com/shirleyilenechan/Foundation_Project
```
Create a virtual environment:
```
$ virtualenv env
```
Activate the virtual environment:
```
$ source env/bin/activate
```
Install dependencies:
```
$ pip install -r requirements.txt
```
Get your own secret keys for [Twitter](https://developer.twitter.com/en/apply-for-access). Save them to a file `secrets.py`. Your file should look something like this:
```
export TWITTER_CONSUMER_KEY="abc123"
export TWITTER_CONSUMER_SECRET="abc123"
export TWITTER_ACCESS_TOKEN_KEY="abc123"
export TWITTER_ACCESS_TOKEN_SECRET="abc123"
```
Run Model.py
```
$ python3 model.py
```
Run Seed.py to create the tables
```
$ python3 seed.py
```
Seed the tables with Foundation information 
```
$ psql foundation_project < foundation_project.sql
```
Source Secrets File
```
$ source secrets.sh
```
Run server.py
```
$ python3 server.py
```


