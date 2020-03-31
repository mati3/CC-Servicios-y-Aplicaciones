#docker build -f Dockerfile -t "mati331:ejer2_cc_v1" .
#docker run -p 8000:8000 --name ccmati -t mati331:ejer2_cc_v1

FROM python:3.6

EXPOSE 8000

COPY requirements.txt appv1.py ./
RUN python -m pip install -r requirements.txt

CMD gunicorn --bind 0.0.0.0:8000 appv1:app
