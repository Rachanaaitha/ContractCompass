import streamlit as st
import os
import json
import requests
from app.utils import extract_text_from_pdf, extract_text_from_docx
from app.llm_processor import analyzer

st.set_page_config(page_title="ContractCompass", page_icon="📄")

st.title("📄 ContractCompass")
st.write("AI-Powered Legal Contract Analysis")

uploaded_file = st.file_uploader("Upload Contract (PDF or DOCX)", type=['pdf', 'docx'])

if uploaded_file is not None:
    file_path = f"temp_{uploaded_file.name}"
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    st.success(f"✅ Uploaded: {uploaded_file.name}")
    
    # Extract text
    if uploaded_file.name.endswith('.pdf'):
        text = extract_text_from_pdf(file_path)
    else:
        text = extract_text_from_docx(file_path)
    
    with st.expander("View Extracted Text"):
        st.text_area("Raw Text", text, height=200, label_visibility="collapsed")
    
    # AI Analysis
    if st.button("🔍 Analyze Contract", type="primary"):
        with st.spinner("🤖 Analyzing contract..."):
            analysis = analyzer.analyze_contract(text)
        
        st.subheader("📊 AI Analysis Results")
        
        # Display in columns
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**📅 Dates & Deadlines**")
            if analysis['dates_deadlines']:
                for date in analysis['dates_deadlines']:
                    st.write(f"- {date}")
            else:
                st.info("No specific dates found")
                
            st.write("**💰 Financial Terms**")
            if analysis['financials']:
                for financial in analysis['financials']:
                    st.write(f"- {financial}")
            else:
                st.info("No financial terms extracted")
        
        with col2:
            st.write("**⚖️ Key Obligations**")
            if analysis['obligations']:
                for obligation in analysis['obligations'][:4]:
                    st.write(f"- {obligation[:120]}...")
            else:
                st.info("No clear obligations identified")
        
        st.write("**🚨 Risk Assessment**")
        high_risk_count = sum(1 for risk in analysis['risks'] if 'High Risk' in risk['level'])
        medium_risk_count = sum(1 for risk in analysis['risks'] if 'Medium Risk' in risk['level'])
        
        if analysis['risks']:
            for risk in analysis['risks']:
                if 'High Risk' in risk['level']:
                    st.error(f"{risk['level']}: {risk['description']}")
                elif 'Medium Risk' in risk['level']:
                    st.warning(f"{risk['level']}: {risk['description']}")
                else:
                    st.info(f"{risk['level']}: {risk['description']}")
        else:
            st.success("No major risks detected")
        
        st.write("**📝 Contract Summary**")
        st.info(analysis['summary'])
        
        st.success(analysis['status'])
        
        # n8n Workflow Integration
        if high_risk_count > 0:
            st.markdown("---")
            st.subheader("🔔 n8n Workflow Automation")
            
            # Prepare n8n payload
            n8n_payload = {
                "contract_name": uploaded_file.name,
                "risk_level": "high",
                "risk_count": high_risk_count,
                "risk_details": ", ".join([risk['description'] for risk in analysis['risks'] if 'High Risk' in risk['level']]),
                "analysis_summary": analysis['summary'],
                "priority": "URGENT"
            }
            
            st.write("**High-risk contract detected! n8n workflow would trigger:**")
            st.json(n8n_payload)
            
            col1, col2 = st.columns(2)
            with col1:
                st.success("📧 Email alert to legal team")
            with col2:
                st.success("💬 Slack notification to compliance channel")
            
            st.info("In production, this would automatically trigger n8n workflows for alerts, task creation, and compliance tracking.")
        
        elif medium_risk_count > 0:
            st.markdown("---")
            st.subheader("🔔 n8n Workflow Automation")
            st.warning("Medium risk contract - n8n workflow would create review task in legal team's project management system")
    
    # Clean up
    os.remove(file_path)

# n8n Workflow Documentation
with st.expander("📋 n8n Workflow Design"):
    st.write("""
    **Automated Contract Review Workflow:**
    
    1. **Webhook Trigger** → Contract analysis complete
    2. **Condition Check** → Risk level evaluation
    3. **High Risk Path**:
       - Send email alert to legal team
       - Post to Slack compliance channel
       - Create urgent task in project management
    4. **Medium Risk Path**:
       - Create standard review task
       - Schedule follow-up reminder
    5. **Low Risk Path**:
       - Log to audit trail
       - Archive for records
    """)
    
    st.image("https://n8n.io/_next/static/media/workflow-example.12345678.png", 
             caption="Sample n8n Workflow for Contract Alerts", use_column_width=True)