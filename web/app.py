import streamlit as st
import requests
import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Page config
st.set_page_config(
    page_title="Solar System Calculator",
    page_icon="☀️",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
.main-header {
    text-align: center;
    padding: 2rem 0;
    background: linear-gradient(90deg, #f39c12, #e74c3c);
    color: white;
    border-radius: 10px;
    margin-bottom: 2rem;
}

.metric-card {
    background: white;
    padding: 1rem;
    border-radius: 10px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    border-left: 4px solid #3498db;
}

.component-card {
    background: #f8f9fa;
    padding: 1rem;
    border-radius: 8px;
    border: 1px solid #dee2e6;
    margin-bottom: 1rem;
}
</style>
""", unsafe_allow_html=True)

def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>☀️ Solar System Calculator</h1>
        <p>Design your optimal solar power system for Nigeria</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar for inputs
    with st.sidebar:
        st.header("🔧 System Requirements")
        
        # Location input
        location = st.text_input("Location", placeholder="e.g., Lagos, Nigeria")
        
        # Coordinates (optional)
        col1, col2 = st.columns(2)
        with col1:
            latitude = st.number_input("Latitude", value=None, format="%.4f")
        with col2:
            longitude = st.number_input("Longitude", value=None, format="%.4f")
        
        # Budget
        budget = st.number_input("Budget (₦)", min_value=0, value=500000, step=50000)
        
        # Backup hours
        backup_hours = st.slider("Backup Hours Required", 1, 72, 24)
        
        # Priority
        priority = st.selectbox(
            "Optimization Priority",
            ["cost", "reliability", "efficiency", "balanced"]
        )
        
        # System expansion
        expansion_planned = st.checkbox("Plan for future expansion")
    
    # Main content area
    st.header("⚡ Appliance Selection")
    
    # **LOAD YOUR APPLIANCE DATA HERE**
    # Placeholder appliance data - replace with your actual data loading
    sample_appliances = [
        {"appliance": "LED Light", "power_rating": 20},
        {"appliance": "Ceiling Fan", "power_rating": 75},
        {"appliance": "Refrigerator", "power_rating": 150},
        {"appliance": "TV (32 inch)", "power_rating": 100},
        {"appliance": "Laptop", "power_rating": 65},
        {"appliance": "Air Conditioner", "power_rating": 1500},
        {"appliance": "Washing Machine", "power_rating": 500},
        {"appliance": "Microwave", "power_rating": 1000}
    ]
    
    # Dynamic appliance input
    if 'appliances' not in st.session_state:
        st.session_state.appliances = []
    
    # Add appliance form
    with st.expander("➕ Add Appliances", expanded=True):
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            selected_appliance = st.selectbox(
                "Select Appliance",
                [app["appliance"] for app in sample_appliances]
            )
        
        # Get power rating for selected appliance
        power_rating = next(
            (app["power_rating"] for app in sample_appliances 
             if app["appliance"] == selected_appliance), 100
        )
        
        with col2:
            power_input = st.number_input("Power (W)", value=power_rating, min_value=1)
        
        with col3:
            hours_input = st.number_input("Hours/Day", value=8.0, min_value=0.1, step=0.5)
        
        with col4:
            quantity_input = st.number_input("Quantity", value=1, min_value=1)
        
        if st.button("Add Appliance"):
            st.session_state.appliances.append({
                "appliance": selected_appliance,
                "power_rating": power_input,
                "hours_per_day": hours_input,
                "quantity": quantity_input
            })
    
    # Display added appliances
    if st.session_state.appliances:
        st.subheader("📋 Selected Appliances")
        
        appliance_df = pd.DataFrame(st.session_state.appliances)
        appliance_df['Daily Energy (kWh)'] = (
            appliance_df['power_rating'] * 
            appliance_df['hours_per_day'] * 
            appliance_df['quantity']
        ) / 1000
        
        st.dataframe(appliance_df, use_container_width=True)
        
        # Summary metrics
        col1, col2, col3 = st.columns(3)
        
        total_power = appliance_df['power_rating'].sum()
        total_daily_energy = appliance_df['Daily Energy (kWh)'].sum()
        estimated_cost = total_daily_energy * 45 * 30  # ₦45/kWh * 30 days
        
        with col1:
            st.metric("Total Power", f"{total_power:,.0f} W")
        with col2:
            st.metric("Daily Energy", f"{total_daily_energy:.2f} kWh")
        with col3:
            st.metric("Monthly Cost", f"₦{estimated_cost:,.0f}")
        
        # Clear appliances button
        if st.button("Clear All Appliances"):
            st.session_state.appliances = []
            st.rerun()
    
    # Calculate button
    if st.button("🔍 Calculate Solar System", type="primary", use_container_width=True):
        if not location or not st.session_state.appliances:
            st.error("Please provide location and select at least one appliance")
        else:
            with st.spinner("Calculating optimal solar system..."):
                # Prepare input data
                input_data = {
                    "location": location,
                    "latitude": latitude,
                    "longitude": longitude,
                    "budget": budget,
                    "appliances": st.session_state.appliances,
                    "backup_hours": backup_hours,
                    "system_expansion": expansion_planned,
                    "priority": priority
                }
                
                # **REPLACE WITH YOUR API CALL OR ORCHESTRATOR**
                # For demo purposes, we'll simulate the calculation
                result = simulate_calculation(input_data)
                
                if result.get('status') == 'success':
                    display_results(result)
                else:
                    st.error(f"Calculation failed: {result.get('error', 'Unknown error')}")

def simulate_calculation(input_data):
    """Simulate calculation results - REPLACE WITH ACTUAL API CALL"""
    # This is a placeholder - replace with actual orchestrator call
    # or API request to your FastAPI backend
    
    total_daily_energy = sum(
        (app['power_rating'] * app['hours_per_day'] * app['quantity']) / 1000 
        for app in input_data['appliances']
    )
    
    # Simulated results
    return {
        'status': 'success',
        'executive_summary': {
            'recommended_system_cost': input_data['budget'] * 0.8,
            'daily_energy_needs': total_daily_energy,
            'projected_annual_savings': 240000,
            'payback_period': 6.5,
            'key_benefits': [
                'Reduce electricity costs by ₦240,000 annually',
                f'Meet {total_daily_energy:.1f} kWh daily energy needs',
                'Reduce carbon footprint by 2.1 tons CO2/year',
                'Energy independence from grid instability'
            ]
        },
        'technical_details': {
            'solar_panels': {
                'model': 'Sample 400W Panel',
                'total_capacity': 2400,
                'number_needed': 6
            },
            'battery_system': {
                'model': 'Sample 200Ah Battery',
                'total_capacity_ah': 400,
                'number_needed': 2
            },
            'inverter': {
                'model': 'Sample 3000W Inverter',
                'power_rating': 3000
            }
        },
        'financial_analysis': {
            'initial_investment': input_data['budget'] * 0.8,
            'annual_savings_year_1': 240000,
            'payback_period_years': 6.5,
            'roi_percentage': 15.4,
            'net_savings_25_years': 4800000
        }
    }

def display_results(result):
    """Display calculation results"""
    
    st.success("✅ Solar system calculation completed!")
    
    # Executive Summary
    st.header("📊 Executive Summary")
    
    summary = result.get('executive_summary', {})
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "System Cost",
            f"₦{summary.get('recommended_system_cost', 0):,.0f}"
        )
    
    with col2:
        st.metric(
            "Daily Energy",
            f"{summary.get('daily_energy_needs', 0):.1f} kWh"
        )
    
    with col3:
        st.metric(
            "Annual Savings",
            f"₦{summary.get('projected_annual_savings', 0):,.0f}"
        )
    
    with col4:
        st.metric(
            "Payback Period",
            f"{summary.get('payback_period', 0):.1f} years"
        )
    
    # Key Benefits
    st.subheader("🎯 Key Benefits")
    benefits = summary.get('key_benefits', [])
    for benefit in benefits:
        st.write(f"✓ {benefit}")
    
    # Technical Details
    st.header("🔧 Technical Specifications")
    
    technical = result.get('technical_details', {})
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Solar Panels")
        panel_info = technical.get('solar_panels', {})
        st.write(f"**Model:** {panel_info.get('model', 'N/A')}")
        st.write(f"**Total Capacity:** {panel_info.get('total_capacity', 0):,} W")
        st.write(f"**Number Needed:** {panel_info.get('number_needed', 0)}")
        
        st.subheader("Inverter")
        inverter_info = technical.get('inverter', {})
        st.write(f"**Model:** {inverter_info.get('model', 'N/A')}")
        st.write(f"**Power Rating:** {inverter_info.get('power_rating', 0):,} W")
    
    with col2:
        st.subheader("Battery System")
        battery_info = technical.get('battery_system', {})
        st.write(f"**Model:** {battery_info.get('model', 'N/A')}")
        st.write(f"**Total Capacity:** {battery_info.get('total_capacity_ah', 0)} Ah")
        st.write(f"**Number Needed:** {battery_info.get('number_needed', 0)}")
    
    # Financial Analysis
    st.header("💰 Financial Analysis")
    
    financial = result.get('financial_analysis', {})
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Initial Investment", f"₦{financial.get('initial_investment', 0):,.0f}")
        st.metric("Annual Savings (Year 1)", f"₦{financial.get('annual_savings_year_1', 0):,.0f}")
        st.metric("ROI Percentage", f"{financial.get('roi_percentage', 0):.1f}%")
    
    with col2:
        st.metric("Payback Period", f"{financial.get('payback_period_years', 0):.1f} years")
        st.metric("Net Savings (25 years)", f"₦{financial.get('net_savings_25_years', 0):,.0f}")
    
    # Savings Chart
    st.subheader("📈 Cumulative Savings Projection")
    
    # Generate 25-year projection
    years = list(range(1, 26))
    annual_savings = financial.get('annual_savings_year_1', 240000)
    initial_cost = financial.get('initial_investment', 400000)
    
    cumulative_savings = []
    for year in years:
        inflation_factor = 1.05 ** year  # 5% annual inflation
        yearly_savings = annual_savings * inflation_factor
        
        if year == 1:
            cumulative = yearly_savings - initial_cost
        else:
            cumulative = cumulative_savings[-1] + yearly_savings
        
        cumulative_savings.append(cumulative)
    
    # Create chart
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=years,
        y=cumulative_savings,
        mode='lines+markers',
        name='Cumulative Savings',
        line=dict(color='#2ecc71', width=3)
    ))
    
    fig.add_hline(y=0, line_dash="dash", line_color="red", 
                  annotation_text="Break-even point")
    
    fig.update_layout(
        title="25-Year Cumulative Savings Projection",
        xaxis_title="Year",
        yaxis_title="Cumulative Savings (₦)",
        hovermode='x unified'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Download report button
    if st.button("📥 Download Detailed Report"):
        report_json = json.dumps(result, indent=2)
        st.download_button(
            label="Download Report (JSON)",
            data=report_json,
            file_name=f"solar_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )

if __name__ == "__main__":
    main()