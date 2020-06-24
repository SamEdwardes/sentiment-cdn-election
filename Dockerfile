# to build:
# docker image build -t cdn_election:latest .
# to run:
# docker run -d --rm -p 5000:5000 cdn_election
# to run interactively:
# docker run -it --rm -p 5000:5000 cdn_election bash
# to run interactivly and attach local volcume:
# docker run -it --rm -p 5000:5000 -v $(pwd):/home/ cdn_election bash

FROM python:3.7

COPY requirements.txt /
RUN pip install -r /requirements.txt

# get NLTK data
RUN mkdir /usr/local/nltk_data
RUN python -m nltk.downloader -d /usr/local/nltk_data stopwords
RUN python -m textblob.download_corpora

RUN apt-get update
RUN apt-get install tree
RUN apt-get -y install vim

# RUN mkdir /cdn-election
# WORKDIR /cdn-election
# COPY ./ ./

CMD ["python", "app.py"]