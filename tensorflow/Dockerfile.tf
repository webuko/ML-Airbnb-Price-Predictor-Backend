FROM tensorflow/serving
COPY ./models/airbnb_price_net/ /models/airbnb_price_net/
COPY ./model.config /models/