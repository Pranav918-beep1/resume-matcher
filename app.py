import streamlit as st
import pandas as pd
import os
import tempfile
from src.simple_parser import extract_text_from_pdf, extract_text_from_docx, extract_basic_fields
from src.matcher import match_resume_to_jd

# Page configuration
st.set_page_config(
    page_title="Resume-JD Matcher",
    page_icon="í³„",
    layout="wide"
)

# Custom CSS for better appearance
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .match-score {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .excellent { background-color: #d4edda; color: #155724; }
    .good { background-color: #fff3cd; color: #856404; }
    .poor { background-color: #f8d7da; color: #721c24; }
    .reason-box {
        padding: 1rem;
        border-left: 4px solid #1f77b4;
        background-color: #f8f9fa;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Header
    st.markdown('<div class="main-header">í³„ Resume-JD Matching Tool</div>', unsafe_allow_html=True)
    
    # Sidebar for instructions
    with st.sidebar:
        st.header("Instructions")
        st.markdown("""
        1. **Upload Job Description** - Paste or upload JD text
        2. **Upload Resumes** - Upload one or multiple resumes (PDF/DOCX/TXT)
        3. **View Results** - See match scores and analysis
        4. **Download Rankings** - Export results as CSV
        """)
        
        st.header("About")
        st.markdown("""
        This tool analyzes resumes against job descriptions using:
        - **Keyword Matching** - Skills and technologies
        - **Smart Scoring** - Percentage-based matching
        - **Explainable Results** - Clear reasons for scores
        """)
    
    # Main content area
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("í³‹ Job Description")
        jd_input_method = st.radio("JD Input Method:", ["Paste Text", "Upload File"])
        
        jd_text = ""
        if jd_input_method == "Paste Text":
            jd_text = st.text_area("Paste Job Description:", height=300, 
                                 placeholder="Paste the job description here...\n\nRequired Skills:\n- Python\n- SQL\n- AWS\n\nNice to have:\n- Docker\n- JavaScript")
        else:
            jd_file = st.file_uploader("Upload JD File", type=['txt'])
            if jd_file:
                jd_text = jd_file.read().decode("utf-8")
                st.text_area("JD Content:", jd_text, height=300)
    
    with col2:
        st.subheader("í³„ Resumes")
        resume_files = st.file_uploader("Upload Resume Files", 
                                      type=['pdf', 'docx', 'txt'], 
                                      accept_multiple_files=True,
                                      help="You can upload multiple resumes")
    
    # Process when both JD and resumes are provided
    if jd_text and resume_files:
        st.subheader("í¾¯ Matching Results")
        
        results = []
        progress_bar = st.progress(0)
        
        for i, resume_file in enumerate(resume_files):
            # Update progress
            progress_bar.progress((i + 1) / len(resume_files))
            
            # Extract text from resume based on file type
            with tempfile.NamedTemporaryFile(delete=False, suffix=resume_file.name) as tmp_file:
                tmp_file.write(resume_file.getvalue())
                tmp_path = tmp_file.name
            
            try:
                if resume_file.name.endswith('.pdf'):
                    resume_text = extract_text_from_pdf(tmp_path)
                elif resume_file.name.endswith('.docx'):
                    resume_text = extract_text_from_docx(tmp_path)
                else:  # txt file
                    resume_text = resume_file.read().decode("utf-8")
                
                # Extract basic fields
                basic_fields = extract_basic_fields(resume_text)
                
                # Match with JD
                match_result = match_resume_to_jd(resume_text, jd_text)
                
                # Store results
                results.append({
                    'Resume': resume_file.name,
                    'Candidate': basic_fields.get('email', 'Unknown').split('@')[0] if basic_fields.get('email') else resume_file.name,
                    'Email': basic_fields.get('email', ''),
                    'Phone': basic_fields.get('phone', ''),
                    'Match Score': match_result['match_score'],
                    'Resume Skills': len(match_result['resume_skills']),
                    'JD Skills': len(match_result['jd_skills']),
                    'Matched Skills': len(match_result['matched_skills']),
                    'Reasons': ' | '.join(match_result['reasons'])
                })
                
                # Display individual result
                with st.expander(f"{resume_file.name} - Score: {match_result['match_score']}%"):
                    # Score with color coding
                    score_class = "excellent" if match_result['match_score'] >= 70 else "good" if match_result['match_score'] >= 50 else "poor"
                    st.markdown(f'<div class="match-score {score_class}">{match_result["match_score"]}% Match</div>', unsafe_allow_html=True)
                    
                    # Reasons
                    for reason in match_result['reasons']:
                        st.markdown(f'<div class="reason-box">{reason}</div>', unsafe_allow_html=True)
                    
                    # Skills details
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Resume Skills", len(match_result['resume_skills']))
                    with col2:
                        st.metric("JD Skills", len(match_result['jd_skills']))
                    with col3:
                        st.metric("Matched", len(match_result['matched_skills']))
                    
                    # Skills lists
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write("**Resume Skills:**", ", ".join(match_result['resume_skills'][:10]))
                    with col2:
                        st.write("**Missing Skills:**", ", ".join(match_result['missing_skills'][:10]))
            
            except Exception as e:
                st.error(f"Error processing {resume_file.name}: {str(e)}")
            finally:
                # Clean up temp file
                if os.path.exists(tmp_path):
                    os.unlink(tmp_path)
        
        # Display summary table
        if results:
            st.subheader("í³Š Summary Rankings")
            df = pd.DataFrame(results)
            df = df.sort_values('Match Score', ascending=False)
            
            # Display table
            st.dataframe(df, use_container_width=True)
            
            # Download button
            csv = df.to_csv(index=False)
            st.download_button(
                label="í³¥ Download Rankings as CSV",
                data=csv,
                file_name="resume_rankings.csv",
                mime="text/csv"
            )
    
    elif jd_text or resume_files:
        st.info("í±† Please provide both a Job Description and at least one Resume to start matching.")
    
    else:
        st.info("í±ˆ Upload a Job Description and Resumes to get started!")

if __name__ == "__main__":
    main()
