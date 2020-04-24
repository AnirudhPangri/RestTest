FROM python:3
COPY . .
CMD [ "python", "resttest.py" ]
