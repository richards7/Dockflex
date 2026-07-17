# The app already targets Python 3.14; use the matching slim runtime image.
FROM python:3.14-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# Writer and Calc provide DOCX/XLSX-to-PDF conversion. DejaVu provides a
# dependable baseline font set for documents converted in the container.
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        libreoffice-writer \
        libreoffice-calc \
        fonts-dejavu-core \
    && rm -rf /var/lib/apt/lists/*

COPY backend/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ ./

RUN addgroup --system docflex \
    && adduser --system --ingroup docflex --home /app docflex \
    && mkdir -p uploads converted \
    && chown -R docflex:docflex /app

USER docflex

EXPOSE 7000

CMD ["gunicorn", "--bind", "0.0.0.0:7000", "--workers", "2", "--threads", "4", "--timeout", "120", "app:app"]
