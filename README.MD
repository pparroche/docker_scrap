# Malt scraper, mongoBD and mongo-express dockerised

## Prerequisite

Docker installed and running

## Installation

Set the folder with the dockercompose as working directory. In the terminal windows type the following commands

```bash


docker build -t [NAME] 'PATH to DOCKERFILE'
docker-compose up -d


```

## Usage

Scrap the website https://www.malt.fr/ and return the results as JSON files. The search criteria are :
- CSS
- JAVA
- JS
- python

The JSON files are stored in a malt database in 4 collections : Java, js, python and CSS.
Mongodb is monitored trought mongo-express :
    localhost:8081

