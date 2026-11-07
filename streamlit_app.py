
import streamlit as st
import requests
import json

st.set_page_config(
    page_title="LLMOps Quality & Observability",
    page_icon="📊",
    layout="wide"
)

st.sidebar.title("API Configuration")

api = st.sidebar.text_input(
    "FastAPI URL",
    value="http://127.0.0.1:8003"
).rstrip("/")


def get(path):
    response = requests.get(api + path, timeout=10)
    response.raise_for_status()
    return response.json()


def post(path, payload):
    response = requests.post(
        api + path,
        json=payload,
        timeout=20
    )
    response.raise_for_status()
    return response.json()


try:
    health = get("/health")
    st.sidebar.success("Backend online")
except requests.exceptions.RequestException:
    health = None
    st.sidebar.warning("Start FastAPI first")


st.title("📊 LLMOps Quality & Observability Dashboard")
st.caption("FastAPI backend • LLM quality monitoring • Demo data")

tab1, tab2, tab3 = st.tabs([
    "📊 Overview",
    "🧪 Run Evaluation",
    "📁 Sample Data"
])


with tab1:
    st.header("LLMOps Monitoring Overview")

    if health:
        try:
            metrics = get("/metrics")

            st.subheader("Quality Metrics")

            numeric_metrics = {
                key: value
                for key, value in metrics.items()
                if isinstance(value, (int, float))
                and not isinstance(value, bool)
            }

            if numeric_metrics:
                columns = st.columns(
                    min(len(numeric_metrics), 4)
                )

                for i, (key, value) in enumerate(
                    numeric_metrics.items()
                ):
                    columns[i % len(columns)].metric(
                        key.replace("_", " ").title(),
                        value
                    )

            st.subheader("Complete Monitoring Results")
            st.json(metrics)

        except Exception as e:
            st.error(f"Unable to load metrics: {e}")
    else:
        st.warning("FastAPI backend is offline.")


with tab2:
    st.header("Run LLMOps Evaluation")

    if health:
        try:
            sample = get("/sample")
            default_json = json.dumps(sample, indent=2)
        except Exception:
            default_json = "[]"
    else:
        default_json = "[]"

    payload_text = st.text_area(
        "Evaluation JSON",
        value=default_json,
        height=300
    )

    if st.button("Run Evaluation", type="primary"):
        if not health:
            st.error("Start FastAPI first.")
        else:
            try:
                payload = json.loads(payload_text)

                with st.spinner("Running evaluation..."):
                    result = post("/evaluate", payload)

                st.success("Evaluation completed!")
                st.json(result)

            except json.JSONDecodeError as e:
                st.error(f"Invalid JSON: {e}")
            except requests.exceptions.RequestException as e:
                st.error(f"API request failed: {e}")
            except Exception as e:
                st.error(f"Evaluation failed: {e}")


with tab3:
    st.header("Sample Monitoring Data")

    if health:
        try:
            sample = get("/sample")

            st.json(sample)

            st.download_button(
                "Download Sample JSON",
                data=json.dumps(sample, indent=2),
                file_name="llmops_sample.json",
                mime="application/json"
            )

        except Exception as e:
            st.error(f"Unable to load sample data: {e}")
    else:
        st.warning("Backend unavailable.")


st.divider()
st.caption(
    "LLMOps Quality & Observability | "
    "Quality • Latency • Cost • Monitoring"
)
