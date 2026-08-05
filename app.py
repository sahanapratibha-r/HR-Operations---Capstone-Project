import streamlit as st
import pandas as pd

# Page Configuration
app_title = "Smart HR Operations & Onboarding Hub"
st.set_page_config(page_title=app_title, layout="wide")

st.title(f"🏢 {app_title}")
st.markdown("### AI-Powered Multi-Policy Q&A, Expertise Directory & Onboarding Assistant")

# Sidebar Navigation
app_mode = st.sidebar.selectbox(
    "Select Portal Mode",
    ["Employee Self-Service (Policy & Experts)", "HRSS Operations (Onboarding & KYC)"]
)

# Load real datasets robustly with path fallback
@st.cache_data
def load_all_data():
    df_hr, df_emp = pd.DataFrame(), pd.DataFrame()
    
    # Try different possible paths for Streamlit Cloud deployment
    paths_hr = ['HR Team Information.xlsx', './HR Team Information.xlsx', 'data/HR Team Information.xlsx']
    for p in paths_hr:
        try:
            df_hr = pd.read_excel(p)
            if not df_hr.empty:
                break
        except:
            continue
            
    paths_emp = ['Employee Information.xlsx', './Employee Information.xlsx', 'data/Employee Information.xlsx']
    for p in paths_emp:
        try:
            df_emp = pd.read_excel(p)
            if not df_emp.empty:
                break
        except:
            continue
            
    return df_hr, df_emp

df_hr, df_emp = load_all_data()
if app_mode == "Employee Self-Service (Policy & Experts)":
    st.subheader("💬 Employee Self-Service Portal")
    
    tab1, tab2 = st.tabs(["Multi-Policy & HR Q&A", "Search Expertise Directory"])
    
    with tab1:
        st.markdown("Ask instant questions regarding company policies: **Leave, Payroll/TDS, LTA, Ethics & Compliance, and POSH**.")
        user_query = st.text_input("Enter your HR policy or payroll query:", placeholder="e.g., What is the carry forward rule for Earned Leave? Or how to file a POSH complaint?")
        if user_query:
            st.info("💡 **AI Policy Assistant Response:**")
            q_lower = user_query.lower()
            if "leave" in q_lower or "el" in q_lower or "casual leave" in q_lower or "sick leave" in q_lower:
                st.write("Based on **Policy 1 (Comprehensive Leave Policy)**: Earned Leave (EL) can accumulate up to 45 days. Casual Leaves (12 days/year) cannot be carried forward. Sick Leaves (10 days/year) require a medical certificate for consecutive absences exceeding 3 working days.")
            elif "payroll" in q_lower or "salary" in q_lower or "tds" in q_lower or "tax" in q_lower:
                st.write("Based on **Policy 2 (Payroll and Compensation Policy)**: Salaries are disbursed on or before the last working day of the month. TDS is computed based on annual declarations; failure to submit proofs within the tax-proof window results in higher automatic tax deductions.")
            elif "lta" in q_lower or "travel" in q_lower:
                st.write("Based on **Policy 3 (Leave Travel Allowance Policy)**: LTA covers economy airfare, AC first-class rail, or public bus fares for the employee and immediate family within a 4-year block period (e.g., 2026–2029), limited to two journeys.")
            elif "ethics" in q_lower or "conflict" in q_lower or "moonlighting" in q_lower or "whistleblower" in q_lower:
                st.write("Based on **Policy 4 (Ethics and Compliance Policy)**: Secondary employment or moonlighting without written executive authorization is strictly prohibited. Suspected misconduct can be reported via the Whistleblower Hotline with guaranteed anti-retaliation protection.")
            elif "posh" in q_lower or "harassment" in q_lower or "icc" in q_lower:
                st.write("Based on **Policy 5 (POSH Policy)**: The organization maintains zero tolerance for sexual harassment. Aggrieved employees can submit a formal written complaint to the Internal Complaints Committee (ICC) within 3 months of the incident.")
            else:
                st.write("Based on Company HR Policy Manuals: For specific inquiries outside these parameters, please contact your designated HR Operations partner or submit a ticket through the HR Helpdesk.")
                
   with tab2:
        st.markdown(f"Search across your entire company directory (**{len(df_hr) + len(df_emp)} total profiles loaded**).")
        search_term = st.text_input("Search by skill, name, department, or designation:", placeholder="Type a keyword to search...")
        
        if search_term:
            combined_records = []
            
            # Load HR Team records
            if not df_hr.empty:
                for _, row in df_hr.iterrows():
                    combined_records.append({
                        "id": str(row.get('Employee ID', '')),
                        "name": str(row.get('Employee Name', '')),
                        "designation": str(row.get('Designation', '')),
                        "department": "Human Resources",
                        "skills": str(row.get('Core Skills', '')) + " " + str(row.get('Bio', '')),
                        "location": str(row.get('Location', '')),
                        "email": str(row.get('Email', ''))
                    })
            
            # Load General Employee records
            if not df_emp.empty:
                for _, row in df_emp.iterrows():
                    combined_records.append({
                        "id": str(row.get('Employee ID', '')),
                        "name": str(row.get('Employee Name', '')),
                        "designation": str(row.get('Designation', '')),
                        "department": "General Employee",
                        "skills": str(row.get('Bio', '')),
                        "location": str(row.get('Location', '')),
                        "email": str(row.get('Email', ''))
                    })
            
            # Flexible case-insensitive search across all fields
            results = []
            for emp in combined_records:
                searchable_text = f"{emp['id']} {emp['name']} {emp['designation']} {emp['department']} {emp['skills']} {emp['location']} {emp['email']}".lower()
                if search_term.lower() in searchable_text:
                    results.append(emp)
            
            st.write(f"### Found {len(results)} Matching Expert(s):")
            if len(results) > 0:
                for emp in results[:15]:
                    with st.expander(f"👤 {emp['name']} — {emp['designation']} ({emp['department']})"):
                        st.markdown(f"**Employee ID:** {emp['id']} | **Location:** {emp['location']}")
                        st.markdown(f"**Skills / Bio:** {emp['skills']}")
                        st.markdown(f"**Email:** {emp['email']}")
            else:
                st.warning("No matching profiles found. Try a different keyword or skill.")

elif app_mode == "HRSS Operations (Onboarding & KYC)":
    st.subheader("🛠️ HRSS Operations & Onboarding Hub")
    
    st.markdown("### 1. New-Joiner KYC Document Verification (Simulation)")
    uploaded_file = st.file_uploader("Upload New Joiner ID Proof (Aadhar / PAN / Passport PDF or Image)", type=["pdf", "png", "jpg"])
    if uploaded_file:
        st.success("📄 Document successfully uploaded and parsed via OCR!")
        st.json({
            "Extracted_Name": "Aarav Sharma",
            "Document_Type": "Government ID Proof (Simulated)",
            "ID_Number": "XXXX-XXXX-9876",
            "Match_Status": "Verified against Offer Letter (100% Match)"
        })
        if st.button("Sync Data to HRIS (Workday / GreytHR)"):
            st.balloons()
            st.success("Successfully pushed verified profile data into HRIS database with Human-in-the-Loop approval!")

    st.markdown("---")
    st.markdown("### 2. Project Onboarding Pack Generator")
    new_project = st.text_input("Enter New Project / Department Name:", placeholder="e.g., Enterprise Operations Rollout")
    if st.button("Generate Onboarding Pack"):
        st.write(f"### 📦 Custom Onboarding Pack for: {new_project}")
        st.markdown("- **Assigned HR Operations Partner:** Sahana Pratubha R (Assistant Manager - People Operations & POSH Lead)")
        st.markdown("- **Required Compliance Modules:** Comprehensive Leave Policy, Ethics & Code of Conduct, POSH Awareness Training, TDS/Payroll Onboarding")
        st.markdown("- **Day 1 Action Items:** System provisioning, HRIS profile mapping, corporate policy sign-off, and team introduction call setup.")
