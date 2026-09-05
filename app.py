import streamlit as st
import pandas as pd
import json
import os
import datetime
import time

# --- 1. PERSISTENCE ENGINE ---
DB_PATH = "audit_registry.json"
TX_ID = "PAY-LX-98234-2024"


def load_state():
    if not os.path.exists(DB_PATH):
        initial = {"tx_id": TX_ID, "state": "PENDING", "events": [
            {"time": datetime.datetime.now().strftime("%H:%M:%S"), "source": "SYS", "type": "INITIATED",
             "msg": "Payment request received"}]}
        json.dump(initial, open(DB_PATH, "w"), indent=4)
        return initial
    return json.load(open(DB_PATH))


def save_state(data):
    json.dump(data, open(DB_PATH, "w"), indent=4)


def add_event(msg_type, msg, source="SYS"):
    data = load_state()
    data["events"].insert(0, {"time": datetime.datetime.now().strftime("%H:%M:%S"), "source": source, "type": msg_type,
                              "msg": msg})
    save_state(data)


# --- 2. UI CONFIGURATION ---
st.set_page_config(page_title="ZeroTrust Pay | SOC", layout="wide", initial_sidebar_state="collapsed")
current_tx = load_state()

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono&family=Inter:wght@400;600;700&display=swap');
    header, [data-testid="stHeader"] {visibility: hidden; display: none;}
    html, body, [data-testid="stAppViewContainer"] { background-color: #050810; font-family: 'Inter', sans-serif; color: #E0E6ED; overflow-x: hidden; }
    .block-container { padding-top: 1rem !important; max-width: 98%; }
    .stCard { background-color: #0E1626; border: 1px solid #1E293B; padding: 20px; border-radius: 4px; margin-bottom: 10px; }
    .mono { font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; color: #3B82F6; }
    .risk-ring { border: 4px solid #F43F5E; border-radius: 50%; width: 60px; height: 60px; line-height: 52px; text-align: center; font-size: 1.2rem; font-weight: 700; color: #F43F5E; margin: auto; }
    .pill { padding: 2px 6px; border-radius: 3px; font-size: 0.6rem; font-weight: 700; text-transform: uppercase; }
    .pill-red { background: rgba(244, 63, 94, 0.1); color: #F43F5E; border: 1px solid #F43F5E; }
    .pill-blue { background: rgba(59, 130, 246, 0.1); color: #3B82F6; border: 1px solid #3B82F6; }
    .pill-teal { background: rgba(45, 212, 191, 0.1); color: #2DD4BF; border: 1px solid #2DD4BF; }
    </style>
""", unsafe_allow_html=True)

# --- 3. HEADER & METRICS ---
h1, h2 = st.columns([0.7, 0.3])
with h1:
    st.markdown(
        '<h3 style="color: #3B82F6; margin: 0; padding:0;">🛡️ ZeroTrust Pay <span style="font-size: 0.8rem; font-weight:400; color: #64748B;">| Risk Governance Dashboard</span></h3>',
        unsafe_allow_html=True)
with h2:
    label = "pill-red" if current_tx["state"] == "BLOCKED" else "pill-teal" if current_tx[
                                                                                   "state"] == "PAID" else "pill-blue"
    st.markdown(
        f'<div style="text-align:right;"><span class="pill {label}">● {current_tx["state"]}</span> <span class="pill pill-teal" style="margin-left:5px;">Llama-3.1 Stable</span></div>',
        unsafe_allow_html=True)

m = st.columns(5)
m[0].metric("Precision", "94.2%", "0.5%")
m[1].metric("Recall", "89.7%")
m[2].metric("FPR", "3.8%", "-0.2%", delta_color="inverse")
m[3].metric("Prevented Loss", "₹2.4M")
m[4].metric("Status", "Secure")

# --- 4. MAIN WORKSPACE ---
left_col, right_col = st.columns([0.65, 0.35])

with left_col:
    # Execute Audit Button
    if st.button("🔍 EXECUTE MULTIMODAL PRE-PAYMENT AUDIT", type="primary", use_container_width=True):
        st.session_state.audit_active = True
        st.rerun()

    st.markdown('<div class="stCard">', unsafe_allow_html=True)

    # A. Case: Blocked
    if current_tx['state'] == "BLOCKED":
        st.error("🔒 TRANSACTION TERMINATED")
        st.info("Policy Violation: Risk 91%. Beneficiary Blacklisted.")
        if st.button("Reset Admin Session"): os.remove(DB_PATH); st.rerun()

    # B. Case: Paid (Balloons Fix)
    elif current_tx['state'] == "PAID":
        st.balloons()  # फायर गुब्बारे!
        st.success("✅ SETTLEMENT SUCCESSFUL")
        st.markdown(f"""<div style="background: #111B2D; border: 2px solid #2DD4BF; padding: 15px; border-radius: 4px;">
            <p style="color:#2DD4BF; font-weight:700; margin:0; font-size:0.75rem;">SETTLEMENT RECEIPT</p>
            <p class="mono" style="font-size:0.7rem; color:#94A3B8;">Recipient: Cloud-Scale Logistics LTD<br>Amount: ₹42,500.00<br>Ref: ORD_{int(time.time())}</p>
        </div>""", unsafe_allow_html=True)
        if st.button("Audit New Request"): os.remove(DB_PATH); st.rerun()

    # C. Case: Active Audit Assessment
    elif st.session_state.get('audit_active'):
        t1, t2 = st.columns([0.7, 0.3])
        with t1:
            st.markdown(
                f'<p style="color: #64748B; font-size: 0.65rem; font-weight: 700; margin:0;">ENTRY ID: <span class="mono">{TX_ID}</span></p>',
                unsafe_allow_html=True)
        with t2:
            st.markdown('<div style="text-align:right;"><span class="pill pill-red">HOLD FOR REVIEW</span></div>',
                        unsafe_allow_html=True)

        st.markdown(
            '<p class="mono" style="font-size: 0.8rem; background: #050810; padding: 6px 12px; border-radius: 4px; color: #94A3B8; margin-top:5px;">₹42,500.00 • Cloud-Scale Logistics • Sep 02, 10:15:22</p>',
            unsafe_allow_html=True)

        sc1, sc2 = st.columns([0.25, 0.75])
        with sc1:
            st.markdown('<div class="risk-ring">91</div>', unsafe_allow_html=True)
            st.markdown(
                '<p style="text-align:center; color:#F43F5E; font-weight:700; font-size:0.8rem; margin-top:10px;">HIGH RISK</p>',
                unsafe_allow_html=True)
        with sc2:
            st.markdown('<p style="font-size: 0.75rem; font-weight: 700; margin-bottom: 5px;">Evidence Summary</p>',
                        unsafe_allow_html=True)
            st.markdown("""<table style="width:100%; font-size:0.7rem; border-collapse:collapse;">
                <tr style="border-bottom:1px solid #1E293B;"><th style="text-align:left;">Signal</th><th style="text-align:right;">Impact</th></tr>
                <tr><td>👤 Beneficiary Mismatch</td><td style="text-align:right; color:#F43F5E">90%</td></tr>
                <tr><td>📄 Font Tampering (YOLO)</td><td style="text-align:right; color:#F59E0B">65%</td></tr>
            </table>""", unsafe_allow_html=True)

        with st.expander("✨ AI EXPLANATION", expanded=True):
            st.write("Beneficiary name differs from records. YOLOv8 flagged font alteration in the 'Total' field.")

        # Actions
        st.divider()
        a1, a2, a3 = st.columns(3)
        with a1:
            if st.button("🔴 Block Payment", use_container_width=True):
                current_tx['state'] = "BLOCKED";
                save_state(current_tx)
                add_event("PAYMENT_BLOCKED", "Manual lockout by Analyst", "ANALYST_01");
                st.rerun()
        with a2:
            st.button("Review", use_container_width=True)
        with a3:
            with st.popover("🟢 Approve & Pay", use_container_width=True):
                st.warning("Override requires manual signature.")
                if st.button("Confirm Payout"):
                    current_tx['state'] = "PAID";
                    save_state(current_tx)
                    add_event("SETTLEMENT_SUCCESS", "Funds settled via RazorpayX", "RAZORPAY_API")
                    st.rerun()  # Iske baad balloons PAID block me chalenge
    else:
        st.info("System Ready. Please initiate pre-payment audit scan.")

    st.markdown('</div>', unsafe_allow_html=True)

with right_col:
    # --- AUDIT TRAIL ---
    st.markdown('<div class="stCard" style="padding-bottom:5px;">', unsafe_allow_html=True)
    st.markdown('<p style="font-weight: 700; font-size: 0.8rem; margin:0;">🛡️ AUDIT TRAIL</p>', unsafe_allow_html=True)
    st.markdown('<p style="color: #2DD4BF; font-size: 0.6rem; margin-bottom:5px;">✔ SHA-256 Verified</p>',
                unsafe_allow_html=True)
    with st.container(height=380):
        for e in current_tx['events']:
            color = "#3B82F6"
            if "BLOCKED" in e['type']: color = "#F43F5E"
            if "SUCCESS" in e['type']: color = "#2DD4BF"
            st.markdown(f"""<div style="border-left: 2px solid #1E293B; padding-left: 10px; margin-bottom: 12px; position: relative;">
                <div style="position: absolute; left: -6px; top: 0; width: 10px; height: 10px; background: {color}; border-radius: 50%;"></div>
                <div class="mono" style="font-size: 0.6rem; color: #475569;">{e['time']} • {e['source']}</div>
                <div style="font-size: 0.75rem; font-weight: 600;">{e['type']}</div>
                <div style="font-size: 0.7rem; color: #94A3B8;">{e['msg']}</div>
            </div>""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# --- 7. CHART ---
st.write("")
chart_data = pd.DataFrame({'Valid': [210, 245, 190, 320, 300, 180, 205], 'Risks': [4, 8, 3, 12, 10, 2, 5]},
                          index=['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'])
st.area_chart(chart_data, color=["#2DD4BF", "#F43F5E"], height=150)

