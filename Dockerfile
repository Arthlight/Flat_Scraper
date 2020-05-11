FROM python:3.7
ARG VERSION=1.0.0
LABEL com.FlatScraper.version=$VERSION
ENV PYTHONUNBUFFERED 1
ENV STATUS="Development"

WORKDIR usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY Flat_Scraper_Scrapy/ .

EXPOSE 8080
# Test if you really need to specify IP Address or if Port is enough
ENTRYPOINT ["python", "Flat_Scraper_Scrapy/main.py"]