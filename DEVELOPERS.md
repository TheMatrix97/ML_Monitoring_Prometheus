# Monitoring ML Model Performance with Prometheus & Grafana - Developers**

In this tutorial, we'll walk you through deploying a simple **sentiment analysis app** using **Streamlit** and setting up **Prometheus** and **Grafana** to monitor the model's performance in real time. By the end, you'll be able to track key metrics like **model accuracy**, **number of requests** and **model confidence**.
Use the following guide to prepare the development environment and run the 

---

## **Prerequisites**

1. **Python 3.7+** installed
2. **Docker** installed (for running Prometheus and Grafana)
   - Install Docker by following the official guide: [https://www.docker.com/get-started/](https://www.docker.com/get-started/)
3. Basic understanding of Python and machine learning Basic understanding of Python and machine learning

---

## **Step 1: Install Dependencies**
Let’s start by cloning the repository and setting up your environment.

2. **Set Up a Virtual Environment and Install Dependencies:**

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install torch~=2.9.1 --index-url https://download.pytorch.org/whl/cpu
   pip install -r requirements.txt
   ```
   > Note we are installing Torch only for CPU in an effort to reduce space. But you could go with the full package :) (Optional)

---

## **Step 2: Run the Streamlit App**
Let’s launch the Streamlit app and verify that it’s exposing the necessary metrics.

### **Option 1: Run Locally**

1. **Start the Streamlit app:**

   ```bash
   streamlit run app/app.py
   ```

2. **Check if the app is running:**

   Open your browser and go to **`http://localhost:8501`**.

3. **Verify Prometheus metrics are exposed:**

   Visit **`http://localhost:8001/metrics`** to see the metrics exposed by the app

### **Option 2: Run the App Using Docker**

1. **Build the Docker image for the Streamlit app:**

   ```bash
   docker build -t streamlit-sentiment-app -f ./Dockerfile.app .
   ```

2. **Run the Streamlit app in a Docker container:**

   ```bash
   docker run -d -p 8501:8501 streamlit-sentiment-app
   ```

3. **Access the app in your browser:**

   Go to **`http://localhost:8501`** to interact with the sentiment analysis app.

4. **Verify Prometheus metrics are exposed:**

   Visit **`http://localhost:8001/metrics`** to ensure metrics are being tracked.
---

##  **Step 3: Understand Key Parts of the App (Prometheus Integration)**

Here’s a quick overview of how Prometheus metrics are integrated into the Streamlit app.

### **1. Starting Prometheus Metrics Server:**
This exposes an HTTP endpoint for Prometheus to scrape metrics from.
```python
from prometheus_client import start_http_server
start_http_server(8001)  # Metrics available at http://localhost:8001/metrics
```

### **2. Defining Metrics:**

We define counters and gauges to track the number of requests and model accuracy.

```python
from prometheus_client import Gauge, Counter

# Tracks the total number of prediction requests
request_count_metric = Counter("ml_model_requests_total", "Total number of prediction requests")

# Tracks user-reported model accuracy
accuracy_metric = Gauge("ml_model_accuracy", "User-reported model accuracy")
```

### **3. Updating Metrics in the App:**

Metrics are updated based on user interactions in the Streamlit app.

```python
if st.button("Analyze Sentiment"):
    request_count_metric.inc()  # Increment request count
    label, confidence = predict_sentiment(user_input)

# Update accuracy based on user feedback
if feedback == "Yes":
    accuracy_metric.set(new_accuracy_value)
```

---

## **Step 4: Start the enviroment**

1. **Deploy the stack with docker compose**

   ```bash
   docker compose up -d
   ```

---

## **Step 5: Configure Grafana**

Grafana helps visualize the metrics collected by Prometheus.

1. **Access Grafana:**
   Open **`http://localhost:3000`**.

3. **Login to Grafana:**

   - **Username:** `admin`
   - **Password:** `admin`

4. **Add Prometheus as a Data Source:**

   - Go to **Connections → Data Sources → Add Data Source**
   - Choose **Prometheus**
   - Set URL to **`http://prometheus:9090`**
   - Click **Save & Test**
---