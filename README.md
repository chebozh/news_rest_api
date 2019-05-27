
news-rest-api

News article REST API. Deployed the project on Heroku (free tier). Available at - https://news-rest-api.herokuapp.com/
# API endpoints:
#### Retrieve the news article with the specified title

```/news?title=<article title> (GET)```

#### Retrieve a news article or list of articles with the specified date

```/news?date=<dd-mm-yyy> (GET)```

#### Add a news article to the database

```/news (POST)```

Required request data params: 
`date=[string]` (format: dd-mm-yyyy) `title=[string]` `description=[string]` `text=[string]`

As JSON in the request's body.

#### Create a new item, or update an existing one

```/news (PUT)```

Optional request data params: 
`date=[string]` (format: dd-mm-yyyy) `title=[string]` `description=[string]` `text=[string]`

#### Update an existing article, filtered by title

```/news?title=<title of article to be modified> (PUT)```

#### Update an existing article, filtered by id

```/news?title=<id of article to be modified> (PUT)```

In the body of the PUT request add in JSON format the fields from the list above, which are to be changed.

#### Delete one ore more news articles by date

```/news?date=<dd-mm-yyyy> (DELETE)```

#### Delete a news article by title

```/news?title=<title of article to be deleted> (DELETE)```

#### Delete a news article by id

```/news?id=<id of article to be deleted> (DELETE)```

#### Retrieve all news articles sorted by date

```/news/sorted_by_date (GET)```

#### Retrieve all news articles sorted by title

```/news/sorted_by_title (GET)```
#### Retrieve all news articles sorted by date and title

```/news/sorted_by_date_title (GET)```
