# our base image
FROM python:3-onbuild

# specify the port number the container should expose
EXPOSE 5000

# run the application
CMD ["python", "public/app.py"]

# Run the app.  CMD is required to run on Heroku      
#CMD gunicorn public/app.wsgi --log-file -  
#CMD gunicorn gettingstarted.wsgi --log-file -
#CMD gunicorn -bind 0.0.0.0:5000 wsgi
