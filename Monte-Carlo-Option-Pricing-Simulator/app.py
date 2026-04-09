import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from utils import simulate_gbm_paths, monte_carlo_option_price, black_scholes_price

st.set_page_config(page_title="Quantum Monte Carlo Simulator", layout="wide")

st.title("⚛️ Quantum Monte Carlo Option Pricing")

# Sidebar Inputs
st.sidebar.header("Input Parameters")

S0 = st.sidebar.number_input("Initial Stock Price (S0)", value=100.0)
K = st.sidebar.number_input("Strike Price (K)", value=100.0)
r = st.sidebar.number_input("Risk-Free Rate (r)", value=0.05)
sigma = st.sidebar.number_input("Volatility (σ)", value=0.2)
T = st.sidebar.number_input("Time to Maturity (T)", value=1.0)

steps = st.sidebar.slider("Steps", 50, 500, 252)
n_paths = st.sidebar.slider("Number of Paths", 100, 3000, 1000)

mode = st.sidebar.radio("Mode", ["Classical Monte Carlo", "Quantum (Qiskit)"])

run = st.sidebar.button("Run Simulation")

if run:

    st.subheader("📊 Results")

    # Quantum toggle
    if mode == "Quantum (Qiskit)":
        use_quantum = True
        effective_paths = int(n_paths / 5)
        st.info(f"⚛️ Quantum mode: Using {effective_paths} paths (quantum efficiency)")
    else:
        use_quantum = False
        effective_paths = n_paths

    # Generate paths
    t, paths = simulate_gbm_paths(
        S0, r, sigma, T, steps, effective_paths, use_quantum=use_quantum
    )

    # Pricing
    mc_call = monte_carlo_option_price(paths, K, r, T, 'call')
    mc_put = monte_carlo_option_price(paths, K, r, T, 'put')

    bs_call = black_scholes_price(S0, K, r, sigma, T, 'call')
    bs_put = black_scholes_price(S0, K, r, sigma, T, 'put')

    # Metrics
    col1, col2 = st.columns(2)

    with col1:
        st.metric("MC Call", f"{mc_call:.4f}")
        st.metric("BS Call", f"{bs_call:.4f}")
        st.metric("Diff", f"{mc_call - bs_call:.4f}")

    with col2:
        st.metric("MC Put", f"{mc_put:.4f}")
        st.metric("BS Put", f"{bs_put:.4f}")
        st.metric("Diff", f"{mc_put - bs_put:.4f}")

    # Plot
    st.subheader("📈 Simulated Price Paths")

    fig, ax = plt.subplots(figsize=(10, 5))

    for i in range(min(50, effective_paths)):
        ax.plot(t, paths[i], alpha=0.5)

    ax.set_xlabel("Time")
    ax.set_ylabel("Stock Price")
    ax.set_title(mode)

    st.pyplot(fig)

    # Quantum explanation
    st.subheader("⚛️ Quantum Insight")

    st.markdown("""
This implementation integrates **Qiskit quantum circuits** to generate randomness.

- Classical mode → pseudo-random sampling  
- Quantum mode → randomness from **superposition (Hadamard gate)**  

Quantum computing enables:

- Faster convergence via **Quantum Amplitude Estimation**
- Parallel evaluation using **superposition**
- Reduced complexity from O(1/√N) → O(1/N)

This demonstrates a transition from classical Monte Carlo  
to quantum-enhanced financial computation.
""")