import streamlit as st

st.set_page_config(
    page_title="Emosic AI",
    page_icon="🎵",
    layout="wide"
)

st.markdown("""
<style>

[data-testid="stAppViewContainer"]{
    background: linear-gradient(
        135deg,
        #0F172A,
        #111827,
        #1E293B
    );
}

.hero {
    text-align:center;
    padding-top:60px;
    padding-bottom:40px;
}

.hero-title{
    font-size:72px;
    font-weight:700;
    color:white;
}

.hero-subtitle{
    font-size:20px;
    color:#CBD5E1;
}

.stButton > button{
    width:100%;
    height:55px;
    border-radius:15px;
    border:none;
    font-size:18px;
    font-weight:bold;
}

</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">

<div class="hero-title">
🎵 Emosic AI
</div>

<div class="hero-subtitle">
Music that understands how you feel
</div>

</div>
""", unsafe_allow_html=True)

st.markdown("### Tell us how you're feeling")

user_text = st.text_area(
    "",
    height=180,
    placeholder="Example: I feel stressed about my exams and need to relax..."
)

generate = st.button("Generate Playlist")

if generate:

    st.success("Emotion analysis coming soon 🚀")

    col1,col2,col3 = st.columns(3)

    with col1:
        st.metric(
            "Emotion",
            "Fear"
        )

    with col2:
        st.metric(
            "Confidence",
            "92%"
        )

    with col3:
        st.metric(
            "Songs",
            "10"
        )

    st.markdown("## 🎧 Recommended Songs")

    for i in range(5):

        st.markdown(f"""
        <div style="
        background:#1E293B;
        padding:20px;
        border-radius:15px;
        margin-bottom:10px;
        ">
        
        <h4>Song {i+1}</h4>
        <p>Artist Name</p>

        </div>
        """, unsafe_allow_html=True)