import streamlit as st
import pandas as pd
from datetime import timedelta
import preprocessor
import plotly.express as px
import emoji
from collections import Counter

# ===============================
# Page Setup
# ===============================
st.set_page_config(page_title="💬 WhatsApp Chat Analyzer", page_icon="💬", layout="wide")

# ===============================
# Sidebar Profile
# ===============================
PROFILE_NAME = "Navin Raj"
PROFILE_TITLE = "Engineer | Data Science"
PROFILE_GITHUB = "https://github.com/mrnavinkr"
PROFILE_LINKEDIN = "https://www.linkedin.com/in/navin-kumar-744681264"
PROFILE_EMAIL = "mailto:kumarnavin9316@gmail.com"

profile_css = """<style>
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css');
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;800&display=swap');
.sidebar-id { background: linear-gradient(135deg, rgba(17,25,40,0.85), rgba(25,30,50,0.9)); backdrop-filter: blur(10px); border-radius: 14px; padding: 18px; text-align: center; margin-bottom: 18px; box-shadow: 0 4px 25px rgba(0,0,0,0.35); color: white; font-family: 'Poppins', sans-serif; animation: fadeIn 1.2s ease-in-out; }
.sidebar-id h2 { margin: 6px 0 4px 0; font-size: 22px; font-weight: 800; background: linear-gradient(90deg, #00f6ff, #ff00f2, #00ff95); background-clip: text; -webkit-background-clip: text; -webkit-text-fill-color: transparent; animation: pulse 3s infinite linear; transition: all 0.3s ease-in-out; }
.sidebar-id h2:hover { transform: scale(1.08); filter: drop-shadow(0 0 10px rgba(255,255,255,0.6)); }
.sidebar-id p { margin: 0 0 10px 0; font-size: 13px; color: rgba(255,255,255,0.75); }
.sidebar-links { display: flex; justify-content: center; align-items: center; gap: 18px; }
.sidebar-links a { color: #c7d2fe; font-size: 20px; transition: 0.3s ease; }
.sidebar-links a:hover { color: #ffffff; transform: scale(1.2); filter: drop-shadow(0 0 8px rgba(255,255,255,0.5)); }
[data-testid="stSidebar"] section { animation: fadeSlide 1.2s ease-in-out; }
div.stFileUploader:hover { filter: drop-shadow(0 0 10px rgba(99,102,241,0.5)); transition: all 0.3s ease; }
div[data-baseweb="select"]:hover { filter: drop-shadow(0 0 10px rgba(139,92,246,0.5)); transition: 0.3s ease; }
div.stNumberInput input:hover { box-shadow: 0 0 10px rgba(99,102,241,0.4); transition: 0.3s; }
div.stCheckbox > label:hover { color: #a5b4fc; transition: 0.3s; }
div.stButton > button { background: linear-gradient(90deg, #6366f1, #8b5cf6); color: white; border-radius: 10px; border: none; padding: 0.5em 1.2em; font-weight: 600; transition: all 0.3s ease; }
div.stButton > button:hover { transform: scale(1.05); box-shadow: 0 0 12px rgba(139,92,246,0.6); letter-spacing: 0.3px; }
@keyframes fadeIn { from {opacity: 0; transform: translateY(-10px);} to {opacity: 1; transform: translateY(0);} }
@keyframes pulse { 0% {filter: hue-rotate(0deg);} 50% {filter: hue-rotate(180deg);} 100% {filter: hue-rotate(360deg);} }
@keyframes fadeSlide { from {opacity: 0; transform: translateY(10px);} to {opacity: 1; transform: translateY(0);} }
</style>
"""

profile_html = f"""
{profile_css}
<div class="sidebar-id">
    <h2>{PROFILE_NAME}</h2>
    <p>{PROFILE_TITLE}</p>
    <div class="sidebar-links">
        <a href="{PROFILE_GITHUB}" target="_blank"><i class="fab fa-github"></i></a>
        <a href="{PROFILE_LINKEDIN}" target="_blank"><i class="fab fa-linkedin"></i></a>
        <a href="{PROFILE_EMAIL}" target="_blank"><i class="fas fa-envelope"></i></a>
    </div>
</div>
"""

st.sidebar.markdown(profile_html, unsafe_allow_html=True)
st.sidebar.markdown("---")

# ===============================
# Upload & Analysis Controls
# ===============================
st.sidebar.subheader("📂 Upload & Analysis Controls")
uploaded_file = st.sidebar.file_uploader("Upload WhatsApp chat (.txt)", type=["txt"], key="chat_upload")

if uploaded_file:
    bytes_data = uploaded_file.getvalue()
    string_data = bytes_data.decode("utf-8")

    preview_lines = st.sidebar.number_input("Preview lines", min_value=1, max_value=5000, value=20, step=1)
    show_preview = st.sidebar.checkbox("Show raw preview", value=True)
    if show_preview:
        st.subheader("📝 Raw Chat Preview")
        st.text("\n".join(string_data.splitlines()[:preview_lines]))

    # Preprocess
    df = preprocessor.preprocessor(string_data)

    # ===============================
    # User & View Options
    # ===============================
    st.sidebar.subheader("👥 User & View Options")
    users = sorted(df["user"].dropna().unique().tolist())
    users = [u for u in users if "group" not in u.lower()]
    users.insert(0, "Overall")
    selected_user = st.sidebar.selectbox("Select user", users)
    both_side = st.sidebar.checkbox("Show both-side conversation", value=False)
    show_replies = st.sidebar.checkbox("Show messages replied by this user", value=False)

    # ===============================
    # Manual Interactive Analytics
    # ===============================
    st.sidebar.markdown("---")
    st.sidebar.subheader("📊 Manual Interactive Analytics")
    metrics = ['Messages', 'Media', 'Links', 'Emojis']
    chart_options = ['2D Bar','3D Bar','Pie','Sunburst','Line','Area','Scatter','Heatmap','Polar','Bubble']
    selected_metrics = st.sidebar.multiselect("Select Metrics", metrics, default=['Messages'])
    selected_chart_types = st.sidebar.multiselect("Select Chart Types", chart_options, default=['2D Bar'])

# ===============================
# Run Analysis
# ===============================
if uploaded_file and st.sidebar.button("🔍 Run Analysis"):
    st.header("📊 Processed Chat Data")

    if selected_user == "Overall":
        target_df = df
    elif both_side:
        target_df = df
    else:
        target_df = df[df["user"] == selected_user]

    st.dataframe(target_df, use_container_width=True)

    # Replies Detection
    if show_replies and selected_user != "Overall":
        st.subheader("🧠 Detected replies by selected user (within 10-min window)")
        reply_pairs = []
        user_df = df.reset_index()
        for i in range(1, len(user_df)):
            current = user_df.iloc[i]
            prev = user_df.iloc[i - 1]
            if current["user"] == selected_user and prev["user"] != selected_user:
                if (current["date"] - prev["date"]) <= timedelta(minutes=10):
                    reply_pairs.append({
                        "original_user": prev["user"],
                        "original_message": prev["message"],
                        "reply_message": current["message"],
                        "reply_gap_min": (current["date"] - prev["date"]).seconds // 60
                    })
        if reply_pairs:
            st.dataframe(pd.DataFrame(reply_pairs), use_container_width=True)
        else:
            st.info("No replies detected for this user within the 10-minute window.")

    # Summary Metrics
    st.header("📈 Summary")
    total_messages = target_df.shape[0]
    total_media = target_df[target_df["message"] == "<Media omitted>"].shape[0]
    total_links = target_df[target_df["message"].str.contains("http", na=False)].shape[0]

    c1, c2, c3 = st.columns(3)
    c1.metric("Total Messages", total_messages)
    c2.metric("Media Shared", total_media)
    c3.metric("Links Shared", total_links)

    # Automatic Graphs
    st.header("📊 Graphical Analysis")
    def safe_plot(fig, metric):
        if fig is None:
            st.info(f"{metric} chart cannot be generated for selected data.")
        else:
            st.plotly_chart(fig, use_container_width=True)

    # Messages per user
    user_counts = df['user'].value_counts().reset_index()
    user_counts.columns = ['User','Messages']
    safe_plot(px.bar(user_counts, x='User', y='Messages', color='User', text='Messages', title="Messages per User"), "Messages per User")

    # Media per user
    media_df = df[df['message'] == '<Media omitted>']
    media_counts = media_df['user'].value_counts().reset_index()
    media_counts.columns = ['User','Media Shared']
    if not media_counts.empty:
        safe_plot(px.bar(media_counts, x='User', y='Media Shared', color='User', text='Media Shared', title="Media Shared per User"), "Media Shared per User")

    # Links per user
    link_df = df[df['message'].str.contains('http', na=False)]
    link_counts = link_df['user'].value_counts().reset_index()
    link_counts.columns = ['User','Links Shared']
    if not link_counts.empty:
        safe_plot(px.bar(link_counts, x='User', y='Links Shared', color='User', text='Links Shared', title="Links Shared per User"), "Links Shared per User")

    # Emoji usage
    def extract_emojis(s):
        return [c for c in s if c in emoji.EMOJI_DATA]
    all_emojis = sum(df['message'].dropna().apply(extract_emojis), [])
    emoji_count = Counter(all_emojis).most_common(10)
    if emoji_count:
        emoji_df = pd.DataFrame(emoji_count, columns=['Emoji','Count'])
        safe_plot(px.bar(emoji_df, x='Emoji', y='Count', text='Count', title="Top 10 Emojis Used"), "Emojis")
    else:
        st.info("No emojis found in chat.")

    # Manual Interactive Analytics
    st.subheader("🛠 Manual Interactive Analytics (Selected Metrics & Charts)")
    for metric in selected_metrics:
        if metric == 'Messages':
            chart_df = df['user'].value_counts().reset_index()
            chart_df.columns = ['User','Count']
        elif metric == 'Media':
            chart_df = df[df['message']=='<Media omitted>']['user'].value_counts().reset_index()
            chart_df.columns = ['User','Count']
        elif metric == 'Links':
            chart_df = df[df['message'].str.contains('http', na=False)]['user'].value_counts().reset_index()
            chart_df.columns = ['User','Count']
        elif metric == 'Emojis':
            chart_df = pd.DataFrame(Counter(all_emojis).most_common(10), columns=['Emoji','Count'])

        # Display data table beside graph
        st.markdown(f"**Data for {metric}:**")
        st.dataframe(chart_df, use_container_width=True)

        for chart_type in selected_chart_types:
            fig = None
            try:
                if chart_type == '2D Bar':
                    fig = px.bar(chart_df, x=chart_df.columns[0], y='Count', color=chart_df.columns[0], text='Count', title=f"{metric} - 2D Bar Chart")
                elif chart_type == '3D Bar':
                    fig = px.bar_3d(chart_df, x=chart_df.columns[0], y='Count', z='Count', color=chart_df.columns[0], title=f"{metric} - 3D Bar Chart")
                elif chart_type == 'Pie':
                    fig = px.pie(chart_df, names=chart_df.columns[0], values='Count', title=f"{metric} - Pie Chart")
                elif chart_type == 'Sunburst':
                    fig = px.sunburst(chart_df, path=[chart_df.columns[0]], values='Count', title=f"{metric} - Sunburst Chart")
                elif chart_type == 'Line':
                    fig = px.line(chart_df, x=chart_df.columns[0], y='Count', title=f"{metric} - Line Chart")
                elif chart_type == 'Area':
                    fig = px.area(chart_df, x=chart_df.columns[0], y='Count', title=f"{metric} - Area Chart")
                elif chart_type == 'Scatter':
                    fig = px.scatter(chart_df, x=chart_df.columns[0], y='Count', color=chart_df.columns[0], size='Count', title=f"{metric} - Scatter Chart")
                elif chart_type == 'Heatmap':
                    if metric != 'Emojis':
                        chart_df['index'] = range(len(chart_df))
                        fig = px.density_heatmap(chart_df, x=chart_df.columns[0], y='index', z='Count', color_continuous_scale='Turbo', title=f"{metric} - Heatmap")
                    else:
                        st.info(f"Heatmap not suitable for {metric}.")
                elif chart_type == 'Polar':
                    fig = px.line_polar(chart_df, r='Count', theta=chart_df.columns[0], line_close=True, title=f"{metric} - Polar Chart")
                elif chart_type == 'Bubble':
                    fig = px.scatter(chart_df, x=chart_df.columns[0], y='Count', size='Count', color=chart_df.columns[0], title=f"{metric} - Bubble Chart")
                safe_plot(fig, f"{metric} - {chart_type}")
            except Exception as e:
                st.info(f"{chart_type} chart cannot be generated for {metric}.")
else:
    st.info("📥 Upload a WhatsApp chat (.txt) in the sidebar to start.")
