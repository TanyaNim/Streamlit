import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import plotly.express as px

# Set dark theme styling
st.set_page_config(page_title="Ibogaine Effectiveness Dashboard", layout="wide")
st.markdown("""
    <style>
    body {
        background-color: #000000;
        color: white;
    }
    .block-container {
        padding: 2rem 2rem 2rem;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center;'>🌿 The Healing Power of Ibogaine</h1>", unsafe_allow_html=True)
st.markdown("<div style='height: 30px;'></div>", unsafe_allow_html=True)

# Define the 2-column layout: 2/3 (left) and 1/3 (right)
left_col, right_col = st.columns([2, 1])

with left_col:
    # ----- Donut Charts -----
    st.markdown("## Clinical Effectiveness of Ibogaine")
    treatments = {
        "Opioid Use Disorder (OUD)": {"value": 97, "description": "3x more effective than traditional treatments"},
        "PTSD": {"value": 100, "description": "Full remission after Ibogaine treatment"},
        "Depression": {"value": 78, "description": "Full symptom resolution in most patients"},
        "Anxiety": {"value": 90, "description": "Long-term relief observed"}
    }

    colors = {
        "Opioid Use Disorder (OUD)": "#9f7aea",
        "PTSD": "#6b46c1",
        "Depression": "#a569bd",
        "Anxiety": "#bb8fce"
    }

    donut_cols = st.columns(4)
    for idx, (label, data) in enumerate(treatments.items()):
        with donut_cols[idx]:
            st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
            st.markdown(f"<div style='text-align: center; font-weight: bold; font-size: 13px'>{label}</div>", unsafe_allow_html=True)
            st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

            fig = go.Figure(data=[
                go.Pie(
                    labels=["Effectiveness", "Remaining"],
                    values=[data["value"], 100 - data["value"]],
                    hole=0.6,
                    marker_colors=[colors.get(label, "#999999"), "#2c3e50"],
                    textinfo='none',
                    hoverinfo='label+percent'
                )
            ])
            fig.update_layout(
                annotations=[dict(text=f"{data['value']}%", x=0.5, y=0.5, font_size=18, font_color="white", showarrow=False)],
                showlegend=False,
                margin=dict(t=20, b=20, l=20, r=20),
                height=160,
                paper_bgcolor='#000000',
                plot_bgcolor='#000000'
            )
            st.plotly_chart(fig, use_container_width=True)

            st.markdown(f"""
                <div style='text-align: center;
                            font-size: 15px;
                            font-weight: 500;
                            background-color: white;
                            color: black;
                            padding: 0px 2px;
                            border-radius: 2px;
                            margin-top: 0px'>
                    {data['description']}
                </div>
            """, unsafe_allow_html=True)

    # Spacer
    st.markdown("<div style='height: 40px;'></div>", unsafe_allow_html=True)

    # ----- Bar Chart -----
    data = {
        "Condition": ["OUD", "OUD", "PTSD", "PTSD", "Depression", "Depression", "Anxiety", "Anxiety"],
        "Treatment": ["Ibogaine", "Traditional", "Ibogaine", "Traditional", "Ibogaine", "Traditional", "Ibogaine", "Traditional"],
        "Effectiveness": [97, 26, 100, 60, 78, 60, 90, 60]
    }
    df = pd.DataFrame(data)

    fig = px.bar(
        df,
        x="Condition",
        y="Effectiveness",
        color="Treatment",
        barmode="group",
        text="Effectiveness",
        title="  Ibogaine vs Traditional Treatment",
        color_discrete_map={
            "Ibogaine": "#9F7AEA",
            "Traditional": "#CBD5E0"
        }
    )

    fig.update_traces(texttemplate='%{text}%', textposition='outside')
    fig.update_layout(
        title_font=dict(size=24, color='white', family="Arial"),
        yaxis=dict(range=[0, 110], title="Effectiveness (%)", title_font=dict(color="white"), tickfont=dict(color="white")),
        xaxis=dict(title=None, tickfont=dict(color="white")),
        legend=dict(
            title=dict(text="Treatment", font=dict(color="white")),
            font=dict(color="white")
        ),
        plot_bgcolor="#000000",
        paper_bgcolor="#000000",
        font_color="white",
        margin=dict(l=40, r=40, t=60, b=40)
    )

    st.plotly_chart(fig, use_container_width=True)

with right_col:
    # ----- Expandable Sections -----
    with st.expander("🧬 Scientific Context & Notes"):
        st.markdown("""
Ibogaine is a naturally occurring, non-classical psychedelic alkaloid derived from West African plants. It has demonstrated remarkable potential in treating trauma-related and substance use disorders by resetting neurochemical pathways linked to addiction and psychological distress—often after just a **single session**. 

---

### 🤔 If Ibogaine is so powerful, why haven’t you heard of it?
- **Natural compounds like Ibogaine can't be patented**, so pharmaceutical companies can’t claim exclusive profits.  
- It often works in just **1–2 doses**, unlike conventional treatments requiring **lifelong use** — making it less profitable for industries built on recurring prescriptions.

---                
⚠️ **Ibogaine’s potency comes with real risks if used irresponsibly.**  
Ibogaine should only be administered in **clinical settings**, with **ECG screening** and
 **professional supervision** as it can cause **cardiotoxicity, arrhythmias**, and in rare cases, **death**.
        """)

    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

    with st.expander("📈 Ibogaine Treatment Outcomes"):
        st.markdown("""
- **OUD (Opioid Use Disorder)**:  
  ▸ 80% success after 1 dose  
  ▸ 97% success with a supportive second dose  

- **PTSD**:  
  ▸ 100% showed *no disability diagnosis* 1 month post-treatment  

- **Depression**:  
  ▸ 78% showed *no diagnosis* after 12 months  

- **Anxiety**:  
  ▸ 90% long-term reduction after 12 months  

✨ Ibogaine offers **long-lasting effects** unlike conventional treatments requiring continuous use.
        """)

    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

    with st.expander("🌍 Global Legal Status of Ibogaine"):
        st.markdown("""
- **U.S.**: Schedule I drug (*illegal since 1970*)  
- **Globally**: Legal or unregulated in many countries  
- **Clinically used in**: Brazil, New Zealand, South Africa, Mexico, Canada, Netherlands, Spain, and more

💡 Despite its legal status, **Ibogaine has not shown abuse potential**.
        """)

    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

    with st.expander("💊 Existing Treatments: Effectiveness & Limitations"):
        st.markdown("""
##### OUD (Opioid Use Disorder)
- Treatments like **Methadone**, **Suboxone**, or **Abstinence**:
  ▸ 7%–26% effectiveness  
  ▸ Sustain dependency rather than heal it  
  ▸ Do **not** reverse neurochemical brain injury

##### PTSD / Depression / Anxiety
- Treated with **SSRIs** and **Therapy**:
  ▸ 20%–60% symptom relief  
  ▸ No curative effect  
  ▸ Delayed onset (up to 6 weeks)  
  ▸ Come with **many side effects**

🧪 **Common side effects**:  
Nausea, dizziness, restlessness, sexual dysfunction, appetite changes, flu-like symptoms, anxiety

⚠️ May **increase suicidal thoughts** in people under 25
        """)


    st.markdown("<div style='height: 80px;'></div>", unsafe_allow_html=True)
# Resources part
    with st.expander ("📚 **Resources**"):
        st.markdown("""
    ▸ Madison Carlino. Geoffrey Lawrence. IBOGAINE TREATMENT FOR OPIOID USE DISORDER. March 2024
                
    ▸ Mandy Oaklander, “Inside Ibogaine, One of the Most Promising and Perilous Psychedelics for Addiction,” time.com, Time, 5 April 2021. time.com/5951772/ibogaine-drug-treatment-addiction/ (accessed 25 Sep. 2023).
                
    ▸ Jessica Meisner, Susan Wilcox, & Jeremy Richards, “Ibogaine-associated cardiac arrest and death: case report and review of the literature,” Therapeutic Advances in Psychopharmacology, 6 (2016). 95–98
    
    ▸ Thomas Brown & Kenneth Alper, “Treatment of opioid use disorder with ibogaine: Detoxification and drug use outcomes,” The American Journal of Drug and Alcohol Abuse 44 (2018). 24–36.         
                """)
