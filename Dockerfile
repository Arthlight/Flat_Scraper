FROM python:3.7-slim AS compile-image
RUN apt-get update
RUN apt-get install -y --no-install-recommends build-essential gcc

COPY requirements.txt .
RUN pip install --user -r requirements.txt

COPY /Flat_Scraper_Scrapy .

FROM python:3.7-slim AS build-image
ARG VERSION=V1.0
LABEL com.HotspotHousing.version=$VERSION
ENV STATUS="production"
COPY --from=compile-image /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH
EXPOSE 3000
ENTRYPOINT ['Flat_Scraper_Scrapy']
