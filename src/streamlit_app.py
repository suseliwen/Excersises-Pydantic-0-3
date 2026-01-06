import requests
import streamlit as st

st.set_page_config(page_title="Restaurant Generator", page_icon="🍽️", layout="wide")

API_BASE = "http://127.0.0.1:8000"

st.sidebar.header("Settings")

api_base = st.sidebar.text_input("API base URL", value=API_BASE)


if "latest" not in st.session_state:
    st.session_state["latest"] = {}


@st.cache_data(ttl=30)
def fetch_restaurants(api_base: str):
    res = requests.get(f"{api_base}/restaurants", timeout=30)
    res.raise_for_status()
    return res.json()


def create_restaurant_ui():
    st.subheader("Generate restaurant")

    with st.form("create_restaurant_form"):
        location = st.text_input("Location", value="Göteborg")
        cuisine = st.text_input("Cuisine", value="Italienskt")
        submitted = st.form_submit_button("Get restaurant")

    if submitted:
        payload = {"location": location, "cuisine": cuisine}
        with st.spinner("Getting restaurant..."):
            try:
                res = requests.post(f"{API_BASE}/restaurant", json=payload, timeout=60)
                res.raise_for_status()
                st.session_state["latest"] = res.json()
                st.success("Restaurant fetched!")
            except requests.RequestException as e:
                st.error("Something went wrong when calling the API")
                st.exception(e)


def latest_ui():
    st.subheader("Latest created")

    latest = st.session_state.get("latest") or {}
    if not latest:
        st.info("No restaurant created yet.")
        return

    st.markdown(f"### {latest.get('name', '-')}")
    st.write(f"**Cuisine:** {latest.get('cuisine', '-')}")
    st.write(f"**Location:** {latest.get('location', '-')}")
    st.write(f"**Rating:** {latest.get('rating', '-')}")
    st.write(f"**Price level:** {latest.get('price_level', '-')}")
    st.write(f"**Opening hours:** {latest.get('opening_hours', '-')}")
    st.caption(latest.get("description", ""))

    with st.expander("Show raw JSON"):
        st.json(latest)



def restaurants_list_ui():
    st.subheader("All restaurants")

    c1, c2 = st.columns([1, 1])
    with c1:
        if st.button("Refresh list"):
            st.cache_data.clear()
            st.rerun()

    try:
        data = fetch_restaurants(API_BASE)

        total = len(data) if isinstance(data, list) else 0
        latest = st.session_state.get("latest") or {}

        m1, m2 = st.columns(2)
        m1.metric("Total restaurants", total)

        latest_label = "-"
        if latest:
            latest_label = f'{latest.get("name", "-")} ({latest.get("location", "-")})'
        m2.metric("Latest created", latest_label)

        preferred_cols = ["name", "cuisine", "price_level", "rating", "location", "opening_hours"]
        rows = []
        if isinstance(data, list):
            for item in data:
                rows.append({k: item.get(k) for k in preferred_cols})

        st.dataframe(rows, use_container_width=True)

    except requests.RequestException as e:
        st.error("Could not fetch restaurants")
        st.exception(e)


def main():
    st.title("Restaurant Generator")

    tab_create, tab_latest, tab_all = st.tabs(["➕ Create", "🕒 Latest", "📋 All restaurants"])

    with tab_create:
        create_restaurant_ui()

    with tab_latest:
        latest_ui()

    with tab_all:
        restaurants_list_ui()


main()



