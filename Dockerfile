FROM python:3.7 

WORKDIR /structure_singapore_1

COPY requirements.txt ./requirements.txt 

RUN pip3 install -r requirements.txt

EXPOSE 8501

COPY . /structure_singapore_1

ENTRYPOINT ["streamlit","run"]

CMD ["structure_singapore_1.py"]