Sentiment Analysis Project

This project performs sentiment analysis on comments scraped from LinkedIn posts. It consists of a frontend built using Nuxt.js and a Django backend.

Frontend
The frontend is located in the pages directory. It has:

An index.vue file which contains templates for:
Displaying username, email and password from the database
Displaying comments for a specific URL
Displaying mined comments for a specific URL
A getCommentByUrl.vue file which contains:
A script to call the backend API to get comments for a URL
A template to display the received comments
Styling for the template
Styling handled by Tailwind CSS
Backend
The backend is a Django project located in the backend directory. It has:

A crawler app which contains:
linkedin_scraper.py to scrape comments from Linkedin using Selenium and BeautifulSoup
mining.py to apply two text mining models on comments and save the mined data to the database
A config folder with Django settings
models.py which contains database models
serializers.py to convert model data to formats suitable for the API
urls.py to setup URLs for the API views
views.py which contains API views to:
Add a new post and associated comments to the database (addPostView)
Get all comments for a URL (GetCommmentsView)
Get mined comments for a URL (GetCommmentsMindedView)
Get mined comments for a URL and perform mining on comments (GetCommmentsDataminedView)
Delete all comments for a URL (deleteCommmentsView)
Get a list of usernames and passwords (post_list)
A db.sqlite3 database
The project can scrape LinkedIn comments, apply text mining models on the comments and provide an API to access the data. Please let me know if you have any other questions!