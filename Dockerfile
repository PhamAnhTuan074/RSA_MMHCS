FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DEFAULT_TIMEOUT=120 \
    PIP_RETRIES=10

WORKDIR /app

RUN groupadd --system rsa && useradd --system --gid rsa --create-home rsa

COPY requirements.txt .
RUN python -m pip install -r requirements.txt

COPY --chown=rsa:rsa app.py ./
COPY --chown=rsa:rsa core ./core
COPY --chown=rsa:rsa ui ./ui
COPY --chown=rsa:rsa .streamlit ./.streamlit

USER rsa

EXPOSE 8501

HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8501/_stcore/health', timeout=3)"

CMD ["python", "-m", "streamlit", "run", "app.py", \
    "--server.address=0.0.0.0", \
    "--server.port=8501", \
    "--server.headless=true", \
    "--server.runOnSave=false", \
    "--browser.gatherUsageStats=false"]
