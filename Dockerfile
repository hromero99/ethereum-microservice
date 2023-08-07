FROM --platform=linux/amd64 ethereum/solc:0.8.0 as solc
FROM --platform=linux/amd64 python:3.8
COPY --from=solc /usr/bin/solc /usr/bin/solc
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt
CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "80","--reload-include","*.py"]