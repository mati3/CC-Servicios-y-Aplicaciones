#docker build -f Dockerfile -t "mati331:ejer2_cc_v2" .
#docker run -p 5000:5000 -t mati331:ejer2_cc_v2

FROM python:3.6

EXPOSE 5000

COPY requirements.txt appv2.py modelo.py ./
RUN python -m pip install -r requirements.txt

CMD gunicorn --bind 0.0.0.0:5000 appv2:app
