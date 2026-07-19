# Dockflex

Dockflex is a powerful, containerized web application that provides lightning-fast document and image conversions to PDF. It supports converting DOCX, XLSX, PDF, JPG, JPEG, and PNG files into standardized PDFs securely and reliably.

## 🚀 Features
- **Multi-format Support**: Convert Word documents, Excel spreadsheets, PDFs, and images into a standardized PDF format.
- **Blazing Fast Image Conversion**: Uses `img2pdf` for lossless and instantaneous image-to-PDF generation.
- **LibreOffice Integration**: High-quality document conversions (DOCX/XLSX) running headless in the background.
- **Cloud-Ready**: Fully Dockerized and ready to deploy to Amazon EKS (Kubernetes) or ECS.
- **Responsive UI**: A clean, drag-and-drop web frontend for easy user interactions.

## 🏗️ Architecture
- **Backend**: Python/Flask application served by Gunicorn.
- **Converters**: LibreOffice (for documents) and `img2pdf` / `Pillow` (for images).
- **Frontend**: Vanilla HTML/JS with Service Worker for caching and offline capabilities.
- **Deployment**: Kubernetes manifests configured with AWS Network Load Balancer integration for high availability.

## 📦 Kubernetes Deployment (AWS EKS)

You can deploy Dockflex to an Amazon EKS cluster effortlessly.

1. **Build and push the Docker image to AWS ECR:**
   ```bash
   docker build -t dockflex:latest .
   docker tag dockflex:latest <your-account-id>.dkr.ecr.<region>.amazonaws.com/dockflex:latest
   docker push <your-account-id>.dkr.ecr.<region>.amazonaws.com/dockflex:latest
   ```

2. **Deploy to EKS:**
   Ensure your `kubectl` context is set to your EKS cluster, then apply the manifests located in the `k8s/` folder:
   ```bash
   kubectl apply -f k8s/deployment.yml
   kubectl apply -f k8s/service.yml
   ```

3. **Access the App:**
   The service automatically provisions an AWS internet-facing Load Balancer. Retrieve the URL using:
   ```bash
   kubectl get svc dockflex-service
   ```
   Copy the `EXTERNAL-IP` and open it in your browser!
