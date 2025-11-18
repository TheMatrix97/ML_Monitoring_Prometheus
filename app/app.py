import streamlit as st
import pandas as pd
import time
from prometheus_client import start_http_server, Gauge, Counter, Histogram, REGISTRY

from model import predict_sentiment


# --- Callback Functions for Feedback ---
def handle_feedback(feedback_type):
    """
    Updates session state based on user feedback.
    """
    if feedback_type == "yes":
        st.session_state.accuracy_history.append((time.time(), 1)) # Correct
        st.session_state.feedback_given = "yes"
        st.session_state.yes_count += 1
        st.session_state.accuracy_feedback_metric.observe(1.0)
    elif feedback_type == "no":
        st.session_state.accuracy_history.append((time.time(), 0)) # Incorrect
        st.session_state.feedback_given = "no"
        st.session_state.no_count += 1
        st.session_state.accuracy_feedback_metric.observe(0.0)

# --- Reset Feedback for New Prediction ---
def reset_feedback():
    """
    Resets feedback state when a new prediction is made.
    """
    st.session_state.prediction_result = None
    st.session_state.feedback_given = None

# Start Prometheus metrics server only once
if "server_started" not in st.session_state:
    try:
        start_http_server(8001)  # Metrics available at port 8001
    except OSError:
        pass  # Avoid "Address already in use" error on reruns
    st.session_state.server_started = True

# Define a request counter
if "request_count_metric" not in st.session_state:
    try:
        print("Initialize request count Prometheus metric")
        st.session_state.request_count_metric = Counter("ml_model_requests_total", "Total number of prediction requests", registry=REGISTRY)
    except ValueError:
        # Metric already exists, retrieve it instead
        st.session_state.request_count_metric = REGISTRY._names_to_collectors["ml_model_requests_total"]

# Define the Prometheus Gauge only once
if "accuracy_feedback_metric" not in st.session_state:
    try:
        print("Initialize accuracy metric Prometheus metric")
        confidence_buckets = [0.5, 0.6, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 1.0]
        st.session_state.accuracy_feedback_metric = Histogram(
            "ml_model_accuracy_feedback", 
            "Distribution of user accuracy feedback (1.0=Correct, 0.0=Incorrect)",
            buckets=confidence_buckets,
            registry=REGISTRY
        )
    except ValueError:
        # Metric already exists, retrieve it instead
        st.session_state.accuracy_feedback_metric = REGISTRY._names_to_collectors["ml_model_accuracy_feedback"]

# Define the Prometheus Confidence histogram only once
if "confidence_metric" not in st.session_state:
    try:
        print("Initialize confidence metric Prometheus metric")
        confidence_buckets = [0.5, 0.6, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 1.0]
        st.session_state.confidence_metric = Histogram(
            "ml_model_confidence", "Library report confidence on results",['label'], registry=REGISTRY, 
            buckets=confidence_buckets)
    except ValueError:
        # Metric already exists, retrieve it instead
        st.session_state.confidence_metric = REGISTRY._names_to_collectors["ml_model_confidence"]

# Initialize session state variables
if "accuracy_history" not in st.session_state:
    st.session_state.accuracy_history = []
if "feedback_given" not in st.session_state:
    st.session_state.feedback_given = None
if "prediction_result" not in st.session_state:
    st.session_state.prediction_result = None
if "yes_count" not in st.session_state:
    st.session_state.yes_count = 0
if "no_count" not in st.session_state:
    st.session_state.no_count = 0

st.title("Sentiment Analysis & Model Monitoring")

# --- Section 1: Sentiment Prediction ---
st.header("💬 Try It Out!")

user_input = st.text_area("Enter a sentence:", "I love this!")

if st.button("Analyze Sentiment"):
    # Increment the request count each time a prediction is made
    st.session_state.request_count_metric.inc()
    label, confidence = predict_sentiment(user_input)
    st.session_state.confidence_metric.labels(label=label).observe(confidence) # Record confidence in Prometheus histogram
    emoji = "😊" if label == "POSITIVE" else "😡" if label == "NEGATIVE" else "😐"

    st.session_state.prediction_result = {
        "label": label,
        "confidence": confidence,
        "emoji": emoji
    }
    st.session_state.feedback_given = None  # Reset feedback state after new prediction

# Show prediction result if available
if st.session_state.prediction_result:
    label = st.session_state.prediction_result["label"]
    confidence = st.session_state.prediction_result["confidence"]
    emoji = st.session_state.prediction_result["emoji"]

    st.success(f"Predicted Sentiment: {label} {emoji}")
    st.info(f"Confidence: {confidence:.2f}")

    # Show buttons only if no feedback has been given yet
    if st.session_state.feedback_given is None:
        st.write("### Was this prediction correct?")
        col1, col2 = st.columns(2)

        with col1:
            st.button("✅ Yes", key="yes_button",
                on_click=handle_feedback,
                args=("yes",))            

        with col2:
            st.button("❌ No", key="no_button",
                on_click=handle_feedback,
                args=("no",))    

# Show feedback message if feedback was given
if st.session_state.feedback_given == "yes":
    st.success("🙂 Yeah!")
elif st.session_state.feedback_given == "no":
    st.error("😞 We are sorry")