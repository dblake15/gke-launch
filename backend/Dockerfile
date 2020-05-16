FROM docker:git
COPY . /app
WORKDIR /app
RUN apk add --no-cache gcc g++ python3 python3-dev libc-dev linux-headers musl-dev
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
EXPOSE 5001
CMD ["python3", "./app.py"]