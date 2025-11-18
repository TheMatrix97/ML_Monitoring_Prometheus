# Monitoring ML Model Performance with Prometheus & Grafana

In this tutorial, we'll walk you through deploying a simple **sentiment analysis app** using **Streamlit** and setting up **Prometheus** and **Grafana** to monitor the model's performance in real time. By the end, you'll be able to track key metrics like **model accuracy**, **number of requests** and **model confidence**.

---

## **Prerequisites**

1. **Docker** installed (for running Prometheus and Grafana)
   - Install Docker by following the official guide: [https://www.docker.com/get-started/](https://www.docker.com/get-started/)
3. Basic understanding of Python and machine learning Basic understanding of Python and machine learning

---

### **Run the App Using Docker**

1. **Build the Docker image for the Streamlit app:**

   ```bash
   docker compose build
   ```

2. **Run the Streamlit app in a Docker container:**

   ```bash
   docker compose up -d
   ```

3. **Access the app in your browser:**

   Go to **`http://localhost:8501`** to interact with the sentiment analysis app.

4. **Verify Prometheus metrics are exposed:**

   Visit **`http://localhost:8001/metrics`** to ensure metrics are being tracked.
---

## **Step 2: Configure Grafana**

Grafana helps visualize the metrics collected by Prometheus.

1. **Access Grafana:**
   Open **`http://localhost:3000`**.

2. **Login to Grafana:**

   - **Username:** `admin`
   - **Password:** `admin`

3. **Add Prometheus as a Data Source:**

   - Go to **Connections → Data Sources → Add Data Source**
   - Choose **Prometheus**
   - Set URL to **`http://prometheus:9090`**
   - Click **Save & Test**

---

## **Step 3: Create Dashboards in Grafana**

### **1. Import the existing dashboard

   (Dashboard)[./monitoring/dashboard_ml.json]