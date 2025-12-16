import streamlit as st
import pandas as pd
import numpy as np
import math
from datetime import datetime, timedelta
import plotly.graph_objects as go


# ============================================
# PAGE CONFIG
# ============================================
st.set_page_config(
    page_title="AeroVoyage - Premium Flight Booking",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ============================================
# CUSTOM CSS
# ============================================
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    .stApp {
        background: linear-gradient(to bottom right, #f0f4ff, #e0e7ff, #fce7f3);
    }
    
    .flight-card {
        background: white;
        border-radius: 20px;
        padding: 25px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        margin: 15px 0;
        border: 1px solid #e5e7eb;
        transition: all 0.3s ease;
    }
    
    .flight-card:hover {
        box-shadow: 0 20px 40px rgba(0,0,0,0.15);
        transform: translateY(-5px);
    }
    
    .best-badge {
        display: inline-block;
        padding: 8px 20px;
        border-radius: 25px;
        font-weight: bold;
        font-size: 12px;
        margin-bottom: 10px;
        letter-spacing: 1px;
    }
    
    .cheapest-badge {
        background: linear-gradient(135deg, #10b981, #059669);
        color: white;
    }
    
    .fastest-badge {
        background: linear-gradient(135deg, #f59e0b, #ef4444);
        color: white;
    }
    
    .price-tag {
        font-size: 36px;
        font-weight: 900;
        background: linear-gradient(135deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .hero-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 60px 20px;
        border-radius: 30px;
        text-align: center;
        margin-bottom: 30px;
    }
    
    .search-box {
        background: white;
        padding: 30px;
        border-radius: 20px;
        box-shadow: 0 20px 60px rgba(0,0,0,0.2);
        margin-top: 30px;
    }
    
    .comparison-table {
        background: white;
        border-radius: 20px;
        padding: 25px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        margin: 20px 0;
    }
    
    .feature-box {
        background: linear-gradient(135deg, #e0e7ff, #fce7f3);
        padding: 25px;
        border-radius: 15px;
        text-align: center;
        margin: 10px 0;
        border: 2px solid #c7d2fe;
    }
    
    .section-header {
        font-size: 32px;
        font-weight: 900;
        color: #1f2937;
        margin: 30px 0 20px 0;
    }
    
    .flight-route {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin: 20px 0;
    }
    
    .flight-time {
        font-size: 28px;
        font-weight: 700;
        color: #1f2937;
    }
    
    .flight-city {
        font-size: 14px;
        color: #6b7280;
        font-weight: 500;
    }
    
    .stat-card {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        margin: 10px 0;
    }
    
    .stat-number {
        font-size: 42px;
        font-weight: 900;
        margin: 10px 0;
    }
    
    div[data-testid="stMetricValue"] {
        font-size: 32px;
        font-weight: 900;
    }
</style>
""", unsafe_allow_html=True)


# ============================================
# DATA & HELPERS
# ============================================
CITIES = {
    "Mumbai": {"lat": 19.0896, "lon": 72.8656, "code": "BOM"},
    "Delhi": {"lat": 28.5562, "lon": 77.1000, "code": "DEL"},
    "Bangalore": {"lat": 12.9716, "lon": 77.5946, "code": "BLR"},
    "Chennai": {"lat": 13.0827, "lon": 80.2707, "code": "MAA"},
    "Kolkata": {"lat": 22.5726, "lon": 88.3639, "code": "CCU"},
    "Hyderabad": {"lat": 17.3850, "lon": 78.4867, "code": "HYD"},
}


AIRLINES = [
    {"name": "IndiGo", "logo": "🔵", "multiplier": 1.0, "rating": 4.2},
    {"name": "Air India", "logo": "🔴", "multiplier": 1.2, "rating": 4.0},
    {"name": "Vistara", "logo": "🟣", "multiplier": 1.4, "rating": 4.5},
    {"name": "SpiceJet", "logo": "🟡", "multiplier": 0.9, "rating": 3.8},
    {"name": "GoAir", "logo": "🟢", "multiplier": 0.85, "rating": 3.9},
    {"name": "AirAsia", "logo": "🔴", "multiplier": 0.88, "rating": 4.1},
]


def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    p1 = math.radians(lat1)
    p2 = math.radians(lat2)
    dp = math.radians(lat2 - lat1)
    dl = math.radians(lon2 - lon1)
    a = math.sin(dp/2)**2 + math.cos(p1) * math.cos(p2) * math.sin(dl/2)**2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))


def generate_flights(source, dest, class_type, passengers):
    if source == dest:
        return []
    
    coord1 = CITIES[source]
    coord2 = CITIES[dest]
    distance = haversine(coord1["lat"], coord1["lon"], coord2["lat"], coord2["lon"])
    
    flights = []
    for idx, airline in enumerate(AIRLINES):
        base_price = distance * 2.5
        class_mult = {"Economy": 1, "Premium Economy": 1.5, "Business": 2.5}[class_type]
        price = int(base_price * airline["multiplier"] * class_mult * passengers)
        
        base_duration = int((distance / 770) * 60 + 30)
        duration = base_duration + np.random.randint(0, 20)
        
        dep_hour = 6 + idx * 2
        dep_min = [0, 15, 30, 45][idx % 4]
        dep_time = f"{dep_hour:02d}:{dep_min:02d}"
        
        arr_mins = (dep_hour * 60 + dep_min + duration) % 1440
        arr_time = f"{(arr_mins // 60):02d}:{(arr_mins % 60):02d}"
        
        flights.append({
            **airline,
            "price": price,
            "duration": duration,
            "departure": dep_time,
            "arrival": arr_time,
            "stops": 0 if idx % 3 == 0 else idx % 3,
            "seats": int(np.random.randint(5, 25)),
            "flight_no": f"{airline['name'][:2].upper()}{np.random.randint(1000, 9999)}"
        })
    
    return flights


# ============================================
# HEADER
# ============================================
st.markdown("""
<div style='text-align: center; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border-radius: 20px; margin-bottom: 30px;'>
    <h1 style='font-size: 56px; font-weight: 900; margin: 0; letter-spacing: -1px;'>✈️ AeroVoyage</h1>
    <p style='font-size: 20px; margin: 10px 0 0 0; opacity: 0.9;'>Your Journey, Our Priority</p>
</div>
""", unsafe_allow_html=True)


# ============================================
# SEARCH SECTION
# ============================================
st.markdown("<div class='search-box'>", unsafe_allow_html=True)
st.markdown("### 🔍 Find Your Perfect Flight")


col1, col2, col3, col4, col5 = st.columns(5)


with col1:
    source = st.selectbox("📍 From", list(CITIES.keys()), index=0)


with col2:
    dest = st.selectbox("📍 To", list(CITIES.keys()), index=1)


with col3:
    travel_date = st.date_input("📅 Date", datetime.now() + timedelta(days=7))


with col4:
    class_type = st.selectbox("💺 Class", ["Economy", "Premium Economy", "Business"])


with col5:
    passengers = st.number_input("👥 Passengers", min_value=1, max_value=9, value=1)


st.markdown("</div>", unsafe_allow_html=True)


# ============================================
# GENERATE FLIGHTS
# ============================================
flights = generate_flights(source, dest, class_type, passengers)


if flights:
    # Create DataFrame and derived fields immediately so all sections use enriched data
    df = pd.DataFrame(flights)
    max_price = df['price'].max()
    df['savings'] = max_price - df['price']
    df['duration_str'] = df.apply(lambda x: f"{int(x['duration'])//60}h {int(x['duration'])%60}m", axis=1)
    df['stops_str'] = df.apply(lambda x: '✈️ Non-stop' if int(x['stops']) == 0 else f"{int(x['stops'])} stop(s)", axis=1)
    df['route'] = df.apply(lambda x: f"{x['departure']} → {x['arrival']}", axis=1)

    # Update flights to include derived columns (use this list everywhere below)
    flights = df.to_dict(orient='records')

    # Find best options (from enriched list)
    cheapest = min(flights, key=lambda x: x["price"])
    fastest = min(flights, key=lambda x: x["duration"])
    
    # ============================================
    # STATISTICS
    # ============================================
    st.markdown("<div class='section-header'>📊 Quick Stats</div>", unsafe_allow_html=True)
    
    stat1, stat2, stat3, stat4 = st.columns(4)
    
    with stat1:
        st.markdown(f"""
        <div class='stat-card'>
            <div style='font-size: 18px;'>💰 Lowest Price</div>
            <div class='stat-number'>₹{cheapest['price']:,}</div>
            <div>{cheapest['name']}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with stat2:
        st.markdown(f"""
        <div class='stat-card'>
            <div style='font-size: 18px;'>⚡ Fastest Flight</div>
            <div class='stat-number'>{fastest['duration'] // 60}h {fastest['duration'] % 60}m</div>
            <div>{fastest['name']}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with stat3:
        avg_price = int(np.mean([f['price'] for f in flights]))
        st.markdown(f"""
        <div class='stat-card'>
            <div style='font-size: 18px;'>📈 Avg Price</div>
            <div class='stat-number'>₹{avg_price:,}</div>
            <div>{len(flights)} options</div>
        </div>
        """, unsafe_allow_html=True)
    
    with stat4:
        distance = haversine(CITIES[source]["lat"], CITIES[source]["lon"], 
                           CITIES[dest]["lat"], CITIES[dest]["lon"])
        st.markdown(f"""
        <div class='stat-card'>
            <div style='font-size: 18px;'>🛫 Distance</div>
            <div class='stat-number'>{int(distance)}</div>
            <div>kilometers</div>
        </div>
        """, unsafe_allow_html=True)
    
    # ============================================
    # BEST OPTIONS
    # ============================================
    st.markdown("<div class='section-header'>✨ Best Options for You</div>", unsafe_allow_html=True)
    
    best_col1, best_col2 = st.columns(2)
    
    with best_col1:
        st.markdown(f"""
        <div class='flight-card'>
            <div class='best-badge cheapest-badge'>💰 CHEAPEST FLIGHT</div>
            <div style='display: flex; justify-content: space-between; align-items: center; margin: 15px 0;'>
                <div style='display: flex; align-items: center; gap: 15px;'>
                    <span style='font-size: 40px;'>{cheapest['logo']}</span>
                    <div>
                        <div style='font-size: 22px; font-weight: 700;'>{cheapest['name']}</div>
                        <div style='color: #6b7280;'>{cheapest['flight_no']}</div>
                    </div>
                </div>
                <div class='price-tag'>₹{cheapest['price']:,}</div>
            </div>
            <div class='flight-route'>
                <div style='text-align: center;'>
                    <div class='flight-time'>{cheapest['departure']}</div>
                    <div class='flight-city'>{source}</div>
                </div>
                <div style='flex: 1; text-align: center; margin: 0 20px;'>
                    <div style='border-top: 2px dashed #cbd5e1; position: relative;'>
                        <div style='position: absolute; top: -12px; left: 50%; transform: translateX(-50%); background: white; padding: 0 10px;'>
                            ✈️
                        </div>
                    </div>
                    <div style='margin-top: 15px; font-weight: 600;'>{cheapest['duration_str']}</div>
                    <div style='font-size: 12px; color: #6b7280;'>{cheapest['stops_str']}</div>
                </div>
                <div style='text-align: center;'>
                    <div class='flight-time'>{cheapest['arrival']}</div>
                    <div class='flight-city'>{dest}</div>
                </div>
            </div>
            <div style='display: flex; justify-content: space-between; align-items: center; margin-top: 20px; padding-top: 20px; border-top: 1px solid #e5e7eb;'>
                <div style='color: #6b7280;'>⭐ {cheapest['rating']} • {cheapest['seats']} seats left</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with best_col2:
        st.markdown(f"""
        <div class='flight-card'>
            <div class='best-badge fastest-badge'>⚡ FASTEST FLIGHT</div>
            <div style='display: flex; justify-content: space-between; align-items: center; margin: 15px 0;'>
                <div style='display: flex; align-items: center; gap: 15px;'>
                    <span style='font-size: 40px;'>{fastest['logo']}</span>
                    <div>
                        <div style='font-size: 22px; font-weight: 700;'>{fastest['name']}</div>
                        <div style='color: #6b7280;'>{fastest['flight_no']}</div>
                    </div>
                </div>
                <div class='price-tag'>₹{fastest['price']:,}</div>
            </div>
            <div class='flight-route'>
                <div style='text-align: center;'>
                    <div class='flight-time'>{fastest['departure']}</div>
                    <div class='flight-city'>{source}</div>
                </div>
                <div style='flex: 1; text-align: center; margin: 0 20px;'>
                    <div style='border-top: 2px dashed #cbd5e1; position: relative;'>
                        <div style='position: absolute; top: -12px; left: 50%; transform: translateX(-50%); background: white; padding: 0 10px;'>
                            ✈️
                        </div>
                    </div>
                    <div style='margin-top: 15px; font-weight: 600;'>{fastest['duration_str']}</div>
                    <div style='font-size: 12px; color: #6b7280;'>{fastest['stops_str']}</div>
                </div>
                <div style='text-align: center;'>
                    <div class='flight-time'>{fastest['arrival']}</div>
                    <div class='flight-city'>{dest}</div>
                </div>
            </div>
            <div style='display: flex; justify-content: space-between; align-items: center; margin-top: 20px; padding-top: 20px; border-top: 1px solid #e5e7eb;'>
                <div style='color: #6b7280;'>⭐ {fastest['rating']} • {fastest['seats']} seats left</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # ============================================
    # COMPARISON CHARTS
    # ============================================
    st.markdown("<div class='section-header'>📊 Flight Comparison</div>", unsafe_allow_html=True)
    
    chart_col1, chart_col2 = st.columns(2)
    
    with chart_col1:
        # Price comparison
        fig_price = go.Figure()
        colors_price = ['#10b981' if f['price'] == cheapest['price'] else '#667eea' for f in flights]
        fig_price.add_trace(go.Bar(
            x=[f['name'] for f in flights],
            y=[f['price'] for f in flights],
            marker_color=colors_price,
            text=[f"₹{f['price']:,}" for f in flights],
            textposition='outside',
        ))
        fig_price.update_layout(
            title="💰 Price Comparison",
            yaxis_title="Price (₹)",
            height=400,
            showlegend=False,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
        )
        st.plotly_chart(fig_price, use_container_width=True)
    
    with chart_col2:
        # Duration comparison
        fig_duration = go.Figure()
        colors_dur = ['#f59e0b' if f['duration'] == fastest['duration'] else '#764ba2' for f in flights]
        fig_duration.add_trace(go.Bar(
            x=[f['name'] for f in flights],
            y=[f['duration'] for f in flights],
            marker_color=colors_dur,
            text=[f"{int(f['duration'])//60}h {int(f['duration'])%60}m" for f in flights],
            textposition='outside',
        ))
        fig_duration.update_layout(
            title="⏱️ Duration Comparison",
            yaxis_title="Duration (minutes)",
            height=400,
            showlegend=False,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
        )
        st.plotly_chart(fig_duration, use_container_width=True)
    
    # ============================================
    # DETAILED COMPARISON TABLE
    # ============================================
    
    # ============================================
    # ROUTE MAP
    # ============================================
    st.markdown("<div class='section-header'>🗺️ Route Map</div>", unsafe_allow_html=True)
    
    coord1 = CITIES[source]
    coord2 = CITIES[dest]
    
    # Create curved flight path
    n = 50
    lats = np.linspace(coord1["lat"], coord2["lat"], n)
    lons = np.linspace(coord1["lon"], coord2["lon"], n)
    for i in range(n):
        lats[i] += 2 * math.sin(math.pi * i / n)
    
    fig_map = go.Figure()
    
    # Flight path
    fig_map.add_trace(go.Scattermapbox(
        lat=lats,
        lon=lons,
        mode='lines',
        line=dict(width=4, color='#667eea'),
        hoverinfo='skip'
    ))
    
    # Cities
    fig_map.add_trace(go.Scattermapbox(
        lat=[coord1["lat"], coord2["lat"]],
        lon=[coord1["lon"], coord2["lon"]],
        mode='markers+text',
        marker=dict(size=20, color=['#10b981', '#ef4444']),
        text=[f"🛫 {source}", f"🛬 {dest}"],
        textposition="top center",
        textfont=dict(size=14, color='black', family='Arial Black')
    ))
    
    fig_map.update_layout(
        mapbox=dict(
            style="open-street-map",
            center=dict(lat=(coord1["lat"] + coord2["lat"]) / 2, lon=(coord1["lon"] + coord2["lon"]) / 2),
            zoom=4.5
        ),
        height=500,
        margin=dict(l=0, r=0, t=0, b=0),
        showlegend=False
    )
    
    st.plotly_chart(fig_map, use_container_width=True)

else:
    st.markdown("""
    <div style='text-align: center; padding: 100px 20px; background: white; border-radius: 20px; margin: 40px 0;'>
        <div style='font-size: 80px; margin-bottom: 20px;'>✈️</div>
        <h2 style='color: #1f2937; font-weight: 800;'>Select Different Cities</h2>
        <p style='color: #6b7280; font-size: 18px;'>Choose your departure and destination to see available flights</p>
    </div>
    """, unsafe_allow_html=True)


# ============================================
# FEATURES SECTION
# ============================================
st.markdown("<div class='section-header'>⚡ Why Choose AeroVoyage?</div>", unsafe_allow_html=True)

feat1, feat2, feat3, feat4 = st.columns(4)

with feat1:
    st.markdown("""
    <div class='feature-box'>
        <div style='font-size: 48px; margin-bottom: 15px;'>💰</div>
        <h3 style='font-weight: 800; margin: 10px 0;'>Best Prices</h3>
        <p style='color: #6b7280;'>Save up to 40% on every booking</p>
    </div>
    """, unsafe_allow_html=True)

with feat2:
    st.markdown("""
    <div class='feature-box'>
        <div style='font-size: 48px; margin-bottom: 15px;'>🔒</div>
        <h3 style='font-weight: 800; margin: 10px 0;'>Secure Booking</h3>
        <p style='color: #6b7280;'>100% payment protection</p>
    </div>
    """, unsafe_allow_html=True)

with feat3:
    st.markdown("""
    <div class='feature-box'>
        <div style='font-size: 48px; margin-bottom: 15px;'>🏆</div>
        <h3 style='font-weight: 800; margin: 10px 0;'>Top Airlines</h3>
        <p style='color: #6b7280;'>Premium airline partners</p>
    </div>
    """, unsafe_allow_html=True)

with feat4:
    st.markdown("""
    <div class='feature-box'>
        <div style='font-size: 48px; margin-bottom: 15px;'>⏰</div>
        <h3 style='font-weight: 800; margin: 10px 0;'>24/7 Support</h3>
        <p style='color: #6b7280;'>Always here to help</p>
    </div>
    """, unsafe_allow_html=True)


# ============================================
# FOOTER
# ============================================
st.markdown("""
<div style='text-align: center; padding: 40px 20px; margin-top: 60px; 
            background: linear-gradient(135deg, #1f2937, #111827); 
            color: white; border-radius: 20px;'>
    <div style='font-size: 48px; margin-bottom: 15px;'>✈️</div>
    <h2 style='font-weight: 900; margin: 10px 0;'>AeroVoyage</h2>
    <p style='opacity: 0.8; margin: 5px 0;'>Your Journey, Our Priority</p>
    <p style='font-size: 14px; opacity: 0.7; margin-top: 20px;'>© 2024 AeroVoyage. All rights reserved.</p>
</div>
""", unsafe_allow_html=True)
