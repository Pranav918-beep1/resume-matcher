import streamlit as st
import pandas as pd
import os
import tempfile
import chardet  # We'll install this if needed

st.set_page_config(page_title="Resume Matcher", layout="wide")

st.title("í³„ Resume-JD Matcher")

# Simple version that avoids encoding issues
jd_text = st.text_area("Paste Job Description here:", height=200)
resume_files = st.file_uploader("Upload Resumes", type=['txt'], accept_multiple_files=True)

if jd_text and resume_files:
    results = []
    
    for resume_file in resume_files:
        try:
            # Super simple text reading
            content = resume_file.getvalue()
            
            # Try to detect encoding
            try:
                text = content.decode('utf-8')
            except:
                try:
                    text = content.decode('latin-1')
                except:
                    text = str(content)  # Last resort
            
            # Simple matching (import your functions)
            from src.matcher import match_resume_to_jd
            match_result = match_resume_to_jd(text, jd_text)
            
            results.append({
                'File': resume_file.name,
                'Score': match_result['match_score'],
                'Matched': len(match_result['matched_skills']),
                'Missing': len(match_result['missing_skills'])
            })
            
            st.write(f"**{resume_file.name}**: {match_result['match_score']}%")
            
        except Exception as e:
            st.error(f"Error with {resume_file.name}: {e}")
    
    if results:
        df = pd.DataFrame(results)
        st.dataframe(df)
