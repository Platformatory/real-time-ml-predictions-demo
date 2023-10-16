FROM python:3.8-slim

# Copy app handler code
COPY . .

# Install dependencies
RUN pip3 install -r requirements.txt

CMD [ "python3", "-u", "kafka_demo.py", "--mode", "setup", "--bootstrap_servers", "kafka:9071"]
