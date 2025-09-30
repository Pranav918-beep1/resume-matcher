
import os
import pandas as pd
from simple_parser import extract_text_from_pdf, extract_text_from_docx
from advanced_parser import extract_advanced_fields
from matcher import match_resume_to_jd

def main():
    print("=== ENHANCED Resume Parser with spaCy NER ===")
    
    # Ensure directories exist
    os.makedirs("data/resumes", exist_ok=True)
    os.makedirs("data/jds", exist_ok=True)
    os.makedirs("output", exist_ok=True)
    
    # Check for files
    resume_files = [f for f in os.listdir("data/resumes") if f.endswith(('.pdf', '.docx', '.txt'))]
    jd_files = [f for f in os.listdir("data/jds") if f.endswith('.txt')]
    
    if not resume_files or not jd_files:
        print("Please add some resume and JD files to the data directories")
        return
    
    print(f"Processing {len(resume_files)} resumes against {len(jd_files)} JDs")
    
    results = []
    
    for jd_file in jd_files:
        jd_path = os.path.join("data/jds", jd_file)
        with open(jd_path, 'r', encoding='utf-8') as f:
            jd_text = f.read()
        
        for resume_file in resume_files:
            print(f"\n--- Analyzing {resume_file} ---")
            resume_path = os.path.join("data/resumes", resume_file)
            
            # Extract text
            text = extract_resume_text(resume_path)
            if not text:
                continue
            
            # Extract ADVANCED fields with spaCy
            advanced_fields = extract_advanced_fields(text)
            
            # Match with JD
            match_result = match_resume_to_jd(text, jd_text)
            
            # Store enhanced results
            result = {
                'resume_file': resume_file,
                'jd_file': jd_file,
                'candidate_name': advanced_fields.get('name', os.path.splitext(resume_file)[0]),
                'email': advanced_fields.get('email', ''),
                'phone': advanced_fields.get('phone', ''),
                'organizations': ', '.join(advanced_fields.get('organizations', [])[:3]),
                'education': ', '.join(advanced_fields.get('education', [])[:2]),
                'match_score': match_result['match_score'],
                'resume_skills_count': match_result['resume_skills_count'],
                'jd_skills_count': match_result['jd_skills_count'],
                'matched_skills_count': match_result['matched_count'],
                'reasons': ' | '.join(match_result['reasons'])
            }
            results.append(result)
            
            # Print detailed analysis
            print(f" Name: {result['candidate_name']}")
            print(f" Email: {result['email']}")
            print(f" Phone: {result['phone']}")
            print(f" Education: {result['education']}")
            print(f" Organizations: {result['organizations']}")
            print(f" Match Score: {match_result['match_score']}%")
            for reason in match_result['reasons']:
                print(f"   - {reason}")
    
    # Save enhanced results
    if results:
        df = pd.DataFrame(results)
        df = df.sort_values('match_score', ascending=False)
        df.to_csv('output/enhanced_ranking_results.csv', index=False)
        print(f"\n=== Enhanced results saved to output/enhanced_ranking_results.csv ===")
        
        # Show top candidates
        print("\n��� TOP CANDIDATES:")
        print(df[['candidate_name', 'match_score', 'education', 'organizations']].head().to_string(index=False))

def extract_resume_text(file_path):
    """Extract text from resume file based on type"""
    if file_path.endswith('.pdf'):
        return extract_text_from_pdf(file_path)
    elif file_path.endswith('.docx'):
        return extract_text_from_docx(file_path)
    else:  # txt file
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except UnicodeDecodeError:
            with open(file_path, 'r', encoding='latin-1') as f:
                return f.read()

if __name__ == "__main__":
    main()
