FROM python:3.8.12-slim-buster
RUN pip --no-cache-dir install pipenv
COPY ["Pipfile", "Pipfile.lock", "./"]
RUN pipenv install --deploy --system && rm -rf /root/.cache
COPY ["*.py", "model.pkl","./"]
EXPOSE 9696
ENTRYPOINT ["gunicorn", "--bind", "0.0.0.0:9696", "predict_loan_status:app"]