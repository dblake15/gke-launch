FROM python:3.7-slim AS compile-image
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
  build-essential \
  gcc 
  #python3 python3-dev 
  #libc-dev musl-dev linux-headers
RUN python -m venv /app/env
ENV PATH="/app/env/bin:$PATH"
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

FROM docker:git
COPY --from=compile-image /app/env /app/env
ENV PATH="/app/env/bin:$PATH"
#RUN apk add --no-cache gcc g++ python3 python3-dev libc-dev linux-headers musl-dev
COPY . /app
WORKDIR /app
# RUN pip3 install --upgrade pip
# RUN pip3 install -r requirements.txt
EXPOSE 5001
CMD ["python3", "./app.py"]

# /Library/Frameworks/Python.framework/Versions/3.6/bin:/Library/Frameworks/Python.framework/Versions/3.7/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:/Library/Frameworks/Mono.framework/Versions/Current/Commands:/Users/dylanblake/google-cloud-sdk/bin:/usr/local/ImageMagick-7.0.8/bin:/Library/Frameworks/Python.framework/Versions/3.6/bin:/Library/Frameworks/Python.framework/Versions/3.7/bin