[![Backend Actions Status](https://github.com/webuko/backend/workflows/ci-cd/badge.svg)](https://github.com/webuko/backend/actions)
[![Codecov](https://codecov.io/gh/webuko/backend/branch/main/graph/badge.svg?token=JU4PD2E8MU)](https://codecov.io/gh/webuko/backend)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/06921c99537e4a6ba307389b28f8e11d)](https://www.codacy.com/gh/webuko/backend/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=webuko/backend&amp;utm_campaign=Badge_Grade)

# Backend

This repository serves the purpose of building an API for retrieving data related to Airbnb listings. In the following,
the data source, the involved frameworks and the API are presented (for a detailed API description, please have a look
at this repository's wiki, or the included Swagger documentation). Importantly, the goal is to provide the application
as a Docker application.

## Data

The data used in this project comes from Airbnb. For the purpose of this project, listings data for Berlin is used.
Basically, the listing dataset contains information about each listing. This includes, for instance, the listing's name,
description, price, number of bathrooms and bedrooms. The dataset contains over 100 attributes. For a more detailed
overview of the data, have a look at this [website](http://insideairbnb.com/get-the-data.html).

## Frameworks

The following two frameworks are used in this project:

- [Flask](https://flask.palletsprojects.com/en/2.0.x/)

  Flask is used as Web API.

- [Tensorflow](https://www.tensorflow.org)

  Tensorflow is used for the machine learning components in this project.

## API

The API aims to deliver the following functionalities:

- Retrieve data for Airbnb listings in Berlin
- Filter data (e.g. for price ranges or a specific neighbourhood)
- Provide polygon geoJson data for neighbourhoods and their respective average Airbnb prices
- Get price predictions for a not yet published Airbnb listings

As stated above, please consult the **[wiki](https://github.com/webuko/backend/wiki/API-Documentation)** for a more
detailed explanation. For an overview of the ongoing efforts to improve the functionalities, have a look at
the **[issues](https://github.com/webuko/backend/issues)** section in this repository.

## How to run the API

### Development environment

If you want to use this API in a development environment, you can clone this repository and use it with `docker-compose`
. For this purpose, use the `docker-compose.yaml` in the root directory. This will start all microservices and set the
flask application to development mode. Additionally, a volume is shared with the host system so that code changes can be
applied immediately.

```shell
git clone https://github.com/webuko/backend.git
cd backend
docker-compose up
```

### Production environment

If you want to use this API in a production environment, you can use the file `dc-production.yaml` with
`docker-compose`. You can pull the images and then start the containers with the following commands:

```shell
docker-compose -f dc-production.yaml pull
docker-compose -f dc-production.yaml up
```
