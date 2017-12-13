# our base image
FROM python:3-onbuild

# specify the port number the container should expose
EXPOSE 5000

# run the application
CMD ["python", "./manage_server.py","runserver","-h","0.0.0.0"]

# Run the app.  CMD is required to run on Heroku            
#CMD gunicorn gettingstarted.wsgi --log-file -
