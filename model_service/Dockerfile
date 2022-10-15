FROM python:3.9-slim

COPY . .
RUN pip install -r requirements.txt


# create registry with feature views
CMD ["feast", "apply"]
# start feature server
CMD ["feast", "serve"]
