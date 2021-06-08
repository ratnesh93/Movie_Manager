# Movie_Manager
Adding, Deleting, Updating, Searching Movie using flask in python

Running application via docker container :
    1. Pull the docker image from https://hub.docker.com/layers/ratnesh93/movie_manager/test/images/sha256-9d5e3cdb864569273c844aa2c40a363365de52f4036c34ac85c381e2a3f928e7?context=repo
    2. run in docker cli: docker run -d -p 5000:5000 imageId



Steps for running the application in local system:
    1. See requirement.txt and download libraries
    2. Run app.py: it will start the server
    3. Now Run test.py to test if it is working fine
    4. Now go to http://127.0.0.1:5000/ and navigate to Home page from there,
        Home page url : http://127.0.0.1:5000/movie/all
