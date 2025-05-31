
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# --- تعریف لیست پروژه‌ها ---
projects = []

st.set_page_config(page_title="Engineering Economics App")

st.title("📊 Engineering Economics App")
st.write("Add projects, choose a method, and compare economic viability.")

# --- فرم ورود اطلاعات پروژه ---
st.sidebar.header("➕ Add a New Project")
name = st.sidebar.text_input("Project Name")
IC = st.sidebar.number_input("Initial Cost (IC)", value=0.0)
SV = st.sidebar.number_input("Salvage Value (SV)", value=0.0)
n = st.sidebar.number_input("Project Life (n in years)", step=1, value=1)
I = st.sidebar.number_input("Annual Income (I)", value=0.0)
M = st.sidebar.number_input("Annual Maintenance (M)", value=0.0)
T = st.sidebar.number_input("Tax Rate (%)", value=0.0)
i = st.sidebar.number_input("Interest Rate (%)", value=0.0)

if st.sidebar.button("Add Project"):
    projects.append({
        'name': name,
        'IC': IC,
        'SV': SV,
        'n': int(n),
        'I': I,
        'M': M,
        'T': T,
        'i': i
    })
    st.sidebar.success(f"Project '{name}' added.")

# --- انتخاب روش تحلیل ---
if projects:
    st.header("📌 Economic Analysis")

    method = st.selectbox("Choose Method", ["NPW", "B/C Ratio", "IRR"])

    def npw(p):
        rate = p['i'] / 100
        cashflow = (p['I'] - p['M']) * (1 - p['T']/100)
        npw_val = -p['IC']
        for t in range(1, p['n']+1):
            npw_val += cashflow / ((1 + rate) ** t)
        npw_val += p['SV'] / ((1 + rate) ** p['n'])
        return round(npw_val, 2)

    def bc_ratio(p):
        rate = p['i'] / 100
        benefits = sum([(p['I'] * (1 - p['T']/100)) / ((1 + rate) ** t) for t in range(1, p['n']+1)])
        costs = p['IC'] + sum([(p['M']) / ((1 + rate) ** t) for t in range(1, p['n']+1)])
        return round(benefits / costs, 2)

    def irr(p):
        cashflows = [-p['IC']]
        for _ in range(p['n']):
            net = (p['I'] - p['M']) * (1 - p['T']/100)
            cashflows.append(net)
        cashflows[-1] += p['SV']
        return round(np.irr(cashflows) * 100, 2)

    # --- محاسبه ---
    result_data = []
    for p in projects:
        if method == "NPW":
            val = npw(p)
        elif method == "B/C Ratio":
            val = bc_ratio(p)
        elif method == "IRR":
            val = irr(p)
        result_data.append({"Project": p['name'], method: val})

    df_result = pd.DataFrame(result_data)
    st.subheader("📋 Results")
    st.dataframe(df_result)

    # --- نمودار ---
    st.subheader("📈 Comparison Chart")
    fig, ax = plt.subplots()
    ax.bar(df_result["Project"], df_result[method])
    ax.set_ylabel(method)
    ax.set_title(f"Comparison by {method}")
    st.pyplot(fig)
else:
    st.info("Please add at least one project to begin analysis.")
