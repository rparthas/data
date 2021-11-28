FROM agrigorev/zoomcamp-cats-dogs-lambda:v2
RUN pip install keras_image_helper
RUN pip install --extra-index-url https://google-coral.github.io/py-repo/ tflite_runtime
COPY lambda_function.py .
CMD [ "lambda_function.lambda_handler" ]