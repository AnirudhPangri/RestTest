FROM python:3
ADD config.py .
ADD resttest.py .
CMD [ "python", "./resttest.py" ]
