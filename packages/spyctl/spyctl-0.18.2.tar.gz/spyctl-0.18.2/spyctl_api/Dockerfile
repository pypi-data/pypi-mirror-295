#
FROM python:3.11

#
WORKDIR /code

#
COPY ./requirements.txt /code/requirements.txt
ADD ./build/spyctl /spyctl

# Get Rust
RUN curl https://sh.rustup.rs -sSf | sh -s -- -y
# Add .cargo/bin to PATH
ENV PATH="/root/.cargo/bin:${PATH}"

RUN apt-get update && apt-get upgrade -y
RUN apt-get install cmake -y

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

#
COPY ./app /code/app

#
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]