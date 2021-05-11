FROM tensorflow/serving
COPY ./models/ /models/airbnb_price_net/
COPY ./model.config /models/