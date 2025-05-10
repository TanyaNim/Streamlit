import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import base64
from PIL import Image
import base64
from io import BytesIO


# ------------------ Load data for MAP ------------------
# Set up updated region coordinates
region_coords = {
    "North America": (50, -100),
    "Western Europe": (54, 6),
    "Oceania": (-25, 135),
    "Southeast and East Asia": (20, 110),
    "Central and eastern Europe": (48, 30),
    "High-income Asia Pacific": (35, 135),
    "Latin America and Caribbean": (-15, -60),
    "North Africa and Middle East": (30, 25),
    "South Asia": (25, 80),
    "Sub-Saharan Africa": (0, 20),
}

# Region data including obesity rate and top 5 countries
region_data = {
    "North America": {
        "ObesityRate": 36.7,
        "TopCountries": ["United States (42.9%)", "Canada (30.4%)"]
    },
    "Western Europe": {
        "ObesityRate": 25.6,
        "TopCountries": ["United Kingdom (30.7%)", "Ireland (28.0%)", "Germany (25.0%)", "Belgium (24.5%)", "France (23.9%)"]
    },
    "Oceania": {
        "ObesityRate": 34.2,
        "TopCountries": ["New Zealand (34.8%)", "Australia (33.5%)"]
    },
    "Southeast and East Asia": {
        "ObesityRate": 7.5,
        "TopCountries": ["Malaysia (19.5%)", "Vietnam (18.3%)", "Thailand (15.0%)", "China (7.3%)", "South Korea (6.7%)"]
    },
    "Central and eastern Europe": {
        "ObesityRate": 33.1,
        "TopCountries": ["Romania (38.2%)", "Hungary (36.4%)", "Croatia (35.7%)", "Poland (31.4%)", "Czech Republic (31.3%)"]
    },
    "High-income Asia Pacific": {
        "ObesityRate": 6.2,
        "TopCountries": ["Singapore (9.0%)", "South Korea (6.7%)", "Japan (4.9%)"]
    },
    "Latin America and Caribbean": {
        "ObesityRate": 33.0,
        "TopCountries": ["Chile (39.5%)", "Barbados (38.2%)", "Mexico (36.1%)", "Argentina (36.0%)", "Jamaica (34.2%)"]
    },
    "North Africa and Middle East": {
        "ObesityRate": 33.5,
        "TopCountries": ["Kuwait (45.4%)", "Qatar (43.8%)", "Egypt (43.0%)", "Saudi Arabia (41.1%)", "Iraq (37.4%)"]
    },
    "South Asia": {
        "ObesityRate": 10.0,
        "TopCountries": ["Pakistan (21.9%)", "Sri Lanka (10.6%)", "India (7.2%)", "Nepal (6.6%)", "Bangladesh (5.3%)"]
    },
    "Sub-Saharan Africa": {
        "ObesityRate": 10.2,
        "TopCountries": ["South Africa (30.0%)", "Kenya (11.0%)", "Tanzania (11.4%)", "Zambia (9.4%)", "Mozambique (8.8%)"]
    }
}

# Build DataFrame for plotting
data = []
for region, coords in region_coords.items():
    obesity = region_data[region]["ObesityRate"]
    top = "<br>".join([f"&nbsp;&nbsp;&nbsp;&nbsp;• {c}" for c in region_data[region]["TopCountries"]])
    hover = f"<b>{region}</b><br>Top Countries:<br>{top}"
    data.append({
        "Region": region,
        "lat": coords[0],
        "lon": coords[1],
        "ObesityRate": obesity,
        "hover_label": hover
    })

filtered_df = pd.DataFrame(data)

# Calculate global average
world_rate = filtered_df['ObesityRate'].mean()

# ------------------ Layout section ------------------
# Outer circle markers
outer_circles = go.Scattergeo(
    lat=filtered_df['lat'],
    lon=filtered_df['lon'],
    mode='markers',
    marker=dict(
        size=filtered_df['ObesityRate'],
        color=filtered_df['ObesityRate'],
        colorscale='Plasma',
        opacity=0.35,
        sizemode='area',
        sizeref=2. * max(filtered_df['ObesityRate']) / (55.**2),
        sizemin=10,
        line=dict(width=0),
        
    ),
    customdata=filtered_df[['hover_label']],
    hovertemplate='%{customdata[0]}<extra></extra>',
    name=''
)

# Inner white labels
inner_circles = go.Scattergeo(
    lat=filtered_df['lat'],
    lon=filtered_df['lon'],
    mode='markers+text',
    marker=dict(
        size=filtered_df['ObesityRate'] * 0.7,
        color='white',
        sizemode='area',
        sizeref=2. * max(filtered_df['ObesityRate']) / (45.**2),
        sizemin=2,
        line=dict(width=0)
    ),
    text=filtered_df['ObesityRate'].round(1).astype(str) + '%',
    textposition='middle center',
    textfont=dict(color='green', size=11, family='Arial Black'),
    hoverinfo='skip',
    showlegend=False
)

# Layout config
layout = go.Layout(
    annotations=[
        dict(
            text=f"<span style='font-size:16px; color:green;'><b>Global average: {world_rate:.1f}%</b></span>",
            showarrow=False, x=0.5, y=-0.009, xref='paper', yref='paper', xanchor='center', yanchor='top'
        )
    ],
    geo=dict(
        showland=True,
        landcolor='rgb(243, 243, 243)',
        countrycolor='rgba(0,0,0,0.1)',
        showcountries=True,
        showframe=False,
        showcoastlines=False,
        projection_type='aitoff',
        projection_rotation=dict(lon=-0, lat=0),
        projection_scale=1.2,
        bgcolor='rgba(0,0,0,0)'
    ),
    margin=dict(l=0, r=0, t=0, b=0),
    height=300,
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
)


# ---------- 1st Row: Full-width Map ----------
# Title and expander side by side
title_col, expander_col = st.columns([3, 2])  # Adjust ratio as needed

with title_col:
    st.markdown("### Global Obesity Rates in 2024")

with expander_col:
    with st.expander("Learn More", expanded=False):
        st.markdown("""
            <div style='font-size: 12px; color: #555; line-height: 1.2; margin: 0; padding: 0;'>
                <ul style="margin: 0; padding-left: 1em;">
                    <li><b>WHO</b> declared obesity a global epidemic in <b>1997</b>.</li>
                    <li>Now over <b>1 billion</b> people—around <b>1 in 8</b>— live with obesity.</li>
                    <li>Adult obesity has more than <b>doubled</b> since 1990.</li>
                </ul>
                <p style="margin: 0.5em 0 0.2em 0;"><b>About the map:</b></p>
                <ul style="margin: 0; padding-left: 1em;">
                    Circle <b>size and color</b> reflect regional obesity rates.<br>
                    <b>Hover</b> to see the top 5 most obese countries per region.<br>
                    *Data from WHO and national health reports (2024).
                </ul>
            </div>
        """, unsafe_allow_html=True)

# Display the map
fig_map = go.Figure(data=[outer_circles, inner_circles], layout=layout)
st.plotly_chart(fig_map, use_container_width=True, config={'displayModeBar': False})

# ---------- 2nd ROW: Graph left, Donut charts right ----------------------------------------------------------------
left_col, right_col = st.columns([2, 3])



# ---------------Obesity donuts---------------
# Load images
def get_image_base64(img_path):
    with open(img_path, "rb") as img_file:
        img_bytes = img_file.read()
        encoded = base64.b64encode(img_bytes).decode()
    return f"data:image/png;base64,{encoded}"

img_female = get_image_base64("/Users/dr.t/Desktop/streamlit_trials/venv/assets/pics/female_transparent.png")
img_male = get_image_base64("/Users/dr.t/Desktop/streamlit_trials/venv/assets/pics/male_transparent.png")

# Colors for slices
colors = [
    "rgba(185, 128, 237, 1)",  # Normal weight (violet)
    "rgba(239, 135, 192, 1)",  # Overweight (pink)
    "rgba(255, 195, 113, 1)"   # Obese (soft yellow-orange)
]
# Chart data
charts = [
    {
        "title": "USA in 1960s",
        "values": [55, 32, 13],
        "labels": ["Normal weight", "Overweight", "Obese"]
    },
    {
        "title": "Global in 1960s",
        "values": [80, 15, 5],
        "labels": ["Normal weight", "Overweight", "Obese"]
    },
    {
        "title": "USA in 2023",
        "values": [26, 31, 43],
        "labels": ["Normal weight", "Overweight", "Obese"]
    },
    {
        "title": "Global in 2022",
        "values": [57, 26, 17],
        "labels": ["Normal weight", "Overweight", "Obese"]
    },
    {
        "title": "Global Projection (2050)",
        "values": [40, 35, 25],
        "labels": ["Normal weight", "Overweight", "Obese"]
    }
]
# Layout rows
rows = [
    charts[0:2],
    charts[2:4],
  
]
with left_col:
    st.markdown("### Obesity Progression From 1960 to 2022")
    for row in rows:
        cols = st.columns(len(row))
        for i, chart in enumerate(row):
            with cols[i]:
                st.markdown(
                f"<div style='text-align: center; font-weight: bold; font-size: 12px; margin-bottom: 0px;'>{chart['title']}</div>",
                unsafe_allow_html=True)

                hover_texts = chart["labels"]
                percent_labels = [f"{value}%" for value in chart["values"]]

                fig = go.Figure(data=[go.Pie(
                    labels=percent_labels,  # Just show percent on chart
                    values=chart["values"],
                    hole=0.4,
                    marker=dict(colors=colors),
                    sort=False,
                    direction='clockwise',
                    textinfo='percent',  # Only show % on the chart itself
                    textposition='inside',
                    hoverinfo='text',  # Use custom hover text
                    hovertext=hover_texts,  # Weight category names
                    textfont=dict(color='black', size=10),
                    domain=dict(x=[0, 1], y=[0.2, 0.8])
                )])

                fig.add_layout_image(
                    dict(
                        source=img_male,
                        xref="paper", yref="paper",
                        x=0.45, y=0.5,
                        sizex=0.12, sizey=0.12,
                        xanchor="center", yanchor="middle",
                        layer="above"
                    )
                )
                fig.add_layout_image(
                    dict(
                        source=img_female,
                        xref="paper", yref="paper",
                        x=0.55, y=0.5,
                        sizex=0.12, sizey=0.12,
                        xanchor="center", yanchor="middle",
                        layer="above"
                    )
                )

                fig.update_layout(
                    showlegend=False,
                    margin=dict(t=2, b=2, l=0, r=0),
                    paper_bgcolor="white",
                    plot_bgcolor="white",
                    height=175
                )

                st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    with st.expander("More Information"):
        st.markdown("""
        <div style='font-size: 11px; line-height: 1.5; color: #444; margin-top: 0.5rem;'>
            <b>Definitions:</b><br>
            • <b>Overweight</b> is defined as a Body Mass Index (BMI) of <b>25 or higher</b>.<br>
            • <b>Obesity</b> is defined as a BMI of <b>30 or higher</b>.<br><br>
        </div>
        <div style='font-size: 13px; line-height: 1.5; color: #444;'>
            The charts above highlight a concerning global trend: nearly <b>half of the world’s adult population</b> is now either overweight or obese. What began in the United States has become a <b>global health crisis</b>, as more people worldwide are becoming <b>overweight, obese, and increasingly unwell</b>.
        </div>
        """, unsafe_allow_html=True)


#----------Disease increase----------------
# Diabetes Data
diabetes_years = [1890, 1935, 1961, 2000, 2016, 2024]
diabetes_prevalence = [0.0028, 0.37, 1.8, 5.8, 13.0, 16.0]  # In percent

# CHD Data
chd_years = [1800, 1912, 1930, 2010]
chd_prevalence = [0.0001, 0.01, 10, 32]

# Cancer Mortality Data
cancer_years = [1811, 1900, 2010]
cancer_mortality = [1/188*100, 1/17*100, 1/3*100]  # ≈ 0.53%, 5.88%, 33.33%

with right_col:
    # Title
    st.markdown("### The Steep Rise of Chronic Diseases in the U.S.")


    # Create the figure
    fig = go.Figure()

    # Diabetes
    fig.add_trace(go.Scatter(
        x=diabetes_years,
        y=diabetes_prevalence,
        mode='lines+markers',
        name='Type 2 Diabetes',
        line=dict(color='rgba(185, 128, 237, 1)', width=3),
        fill='tozeroy',
        fillcolor='rgba(185, 128, 237, 0.5)',
        marker=dict(size=8),
        hovertemplate='Diabetes: %{y:.2f}% in %{x}<extra></extra>'
    ))

    # CHD
    fig.add_trace(go.Scatter(
        x=chd_years,
        y=chd_prevalence,
        mode='lines+markers',
        name='Coronary Heart Disease (CHD)',
        line=dict(color='rgba(239, 135, 192, 1)', width=3, dash='dash'),
        fill='tozeroy',
        fillcolor='rgba(239, 135, 192, 0.2)',
        marker=dict(size=8),
        hovertemplate='CHD: %{y:.2f}% in %{x}<extra></extra>'
    ))

    # Cancer
    fig.add_trace(go.Scatter(
        x=cancer_years,
        y=cancer_mortality,
        mode='lines+markers',
        name='Cancer Mortality',
        line=dict(color='rgba(255, 195, 113, 1)', width=3, dash='dot'),
        fill='tozeroy',
        fillcolor='rgba(255, 195, 113, 0.2)',
        marker=dict(size=8),
        hovertemplate='Cancer: %{y:.2f}% in %{x}<extra></extra>'
    ))

    # Layout
    fig.update_layout(
        xaxis_title="Year",
        yaxis_title="Prevalence / Mortality (%)",
        yaxis=dict(range=[0, 35]),
        template="simple_white",
        height=415,
        legend=dict(x=0.01, y=0.99, bgcolor="rgba(255,255,255,0.5)"),
        margin=dict(t=10, b=10, l=40, r=40)
    )

    # Display
    st.plotly_chart(fig, use_container_width=True)
    with st.expander("About this graph"):
        st.markdown("""
        <span style="font-size:14px; color:gray;">
        Since the mid-20th century, the prevalence of chronic diseases such as coronary heart disease, stroke, cancer, type 2 diabetes, Alzheimer's disease, age-related macular degeneration, and various autoimmune conditions has risen sharply in the United States—a trend that is increasingly mirrored globally. This rise in chronic illness, often referred to as <em>“diseases of civilization”</em>, has closely paralleled increasing rates of obesity and overweight. Despite medical advances, developed societies face a growing crisis of metabolic and degenerative conditions.
        </span>
        """, unsafe_allow_html=True)
# ------------------------DISEASE PREVALENCE IN OBESE PEOPLE----------------------
# === File paths ===
female_path = "/Users/dr.t/Desktop/streamlit_trials/venv/assets/pics/female_violet.png"
male_path = "/Users/dr.t/Desktop/streamlit_trials/venv/assets/pics/male_violet.png"
female_yellow_path = "/Users/dr.t/Desktop/streamlit_trials/venv/assets/pics/female_yellow.png"  
male_yellow_path = "/Users/dr.t/Desktop/streamlit_trials/venv/assets/pics/male_yellow.png"  

# === Load and resize ===
female_icon = Image.open(female_path).resize((30, 60))
male_icon = Image.open(male_path).resize((30, 60))
female_yellow_icon = Image.open(female_yellow_path).resize((30, 60))
male_yellow_icon = Image.open(male_yellow_path).resize((30, 60))

# === Convert to base64 ===

st.markdown("### Disease Prevalence in Obese People(US population data)")
def image_to_base64(img):
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        return base64.b64encode(buffer.getvalue()).decode()

female_b64 = image_to_base64(female_icon)
male_b64 = image_to_base64(male_icon)
female_red_b64 = image_to_base64(female_yellow_icon)
male_red_b64 = image_to_base64(male_yellow_icon)

    # === Function to generate grid ===

    
def display_grid(title, red_count, total_icons, description):
        col1, col2 = st.columns([1, 3])

        # Generate icon images
        icons = []
        for i in range(total_icons):
            b64 = (
                female_red_b64 if i % 2 == 0 and i < red_count else
                male_red_b64 if i % 2 == 1 and i < red_count else
                female_b64 if i % 2 == 0 else
                male_b64
            )
            icons.append(Image.open(BytesIO(base64.b64decode(b64))))

        group_size = 6
        groups = [icons[i:i + group_size] for i in range(0, len(icons), group_size)]

        with col2:
            st.markdown(f"""
            <div style="line-height:1.1;">
                <strong style="font-size:16px;">{title}</strong><br>
                <span style="font-size:12px; color:gray;">{description}</span>
            </div>
            """, unsafe_allow_html=True)

        with col1:
            for group in groups:
                st.image(group, width=20)
                st.markdown(" ", unsafe_allow_html=True)  # vertical space between rows



    # === Display 3 updated grids with descriptions ===
display_grid("Hypertension", red_count=3, total_icons=6, description="1 in 2 adults with obesity develop Hypertension")
display_grid("Type 2 Diabetes", red_count=2, total_icons=6, description="1 in 3 adults with obesity develop type 2 diabetes.")
display_grid("Myocardial Infarction", red_count=1, total_icons=6, description="1 in 6 obese individuals are likely to develop myocardial infarction.")
    
