FROM python:3.7 

WORKDIR /heroku_app

COPY requirements.txt ./requirements.txt 

RUN pip3 install -r requirements.txt

EXPOSE 8501

COPY . /heroku_app

ENTRYPOINT ["streamlit","run"]

CMD ["structure_singapore_1.py"]