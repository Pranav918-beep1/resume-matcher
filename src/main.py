import os
import sys
from simple_parser import extract_text_from_pdf, extract_text_from_docx, extract_basic_fields
from matcher import match_resume_to_jd
import pandas as pd

def main():
    print("=== Resume Parser & Matcher Pipeline ===")
    
    # Check if data directories exist
    if not os.path.exists("data/resumes"):
        print("Creating data directories...")
        os.makedirs("data/resumes", exist_ok=True)
        os.makedirs("data/jds", exist_ok=True)
        create_test_files()
        return
    
    # List available files
    resume_files = [f for f in os.listdir("data/resumes") if f.endswith(('.pdf', '.docx', '.txt'))]
    jd_files = [f for f in os.listdir("data/jds") if f.endswith('.txt')]
    
    if not resume_files:
        print("No resume files found. Creating test files...")
        create_test_files()
        resume_files = ["test_resume.txt"]
        jd_files = ["test_jd.txt"]
    
    if not jd_files:
        print("No JD files found. Creating test JD...")
        create_test_jd()
        jd_files = ["test_jd.txt"]
    
    print(f"Found {len(resume_files)} resume files and {len(jd_files)} JD files")
    
    # Process all combinations
    results = []
    
    for jd_file in jd_files:
        jd_path = os.path.join("data/jds", jd_file)
        with open(jd_path, 'r', encoding='utf-8') as f:
            jd_text = f.read()
        
        for resume_file in resume_files:
            print(f"\n--- Matching {resume_file} with {jd_file} ---")
            resume_path = os.path.join("data/resumes", resume_file)
            
            # Extract resume text
            text = extract_resume_text(resume_path)
            if not text:
                continue
            
            # Extract basic fields
            fields = extract_basic_fields(text)
            
            # Match with JD
            match_result = match_resume_to_jd(text, jd_text)
            
            # Store results
            result = {
                'resume_file': resume_file,
                'jd_file': jd_file,
                'candidate_name': os.path.splitext(resume_file)[0],
                'email': fields['email'],
                'phone': fields['phone'],
                'match_score': match_result['match_score'],
                'resume_skills_count': match_result['resume_skills_count'],
                'jd_skills_count': match_result['jd_skills_count'],
                'matched_skills_count': match_result['matched_count'],
                'reasons': ' | '.join(match_result['reasons'])
            }
            results.append(result)
            
            # Print immediate results
            print(f"Match Score: {match_result['match_score']}%")
            for reason in match_result['reasons']:
                print(f"  - {reason}")
    
    # Save results to CSV
    if results:
        df = pd.DataFrame(results)
        df = df.sort_values('match_score', ascending=False)
        df.to_csv('output/ranking_results.csv', index=False)
        print(f"\n=== Results saved to output/ranking_results.csv ===")
        print(df[['candidate_name', 'match_score', 'reasons']].head())

def extract_resume_text(file_path):
    """Extract text from resume file based on type"""
    if file_path.endswith('.pdf'):
        return extract_text_from_pdf(file_path)
    elif file_path.endswith('.docx'):
        return extract_text_from_docx(file_path)
    else:  # txt file
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()

def create_test_files():
    """Create test resume and JD files"""
    os.makedirs("data/resumes", exist_ok=True)
    os.makedirs("data/jds", exist_ok=True)
    os.makedirs("output", exist_ok=True)
    
    # Test Resume
    resume_content = """John Doe
Software Developer
Email: john.doe@email.com
Phone: +91-9876543210

SKILLS:
Python, Java, SQL, AWS, Docker, JavaScript, React, MySQL, PostgreSQL

EDUCATION:
Bachelor of Technology in Computer Science
XYZ University, 2020-2024

EXPERIENCE:
Software Developer at ABC Company
- Developed web applications using Python and Django
- Managed MySQL databases with SQL
- Deployed applications on AWS EC2
- Used Docker for containerization

PROJECTS:
E-commerce Website - Built with React and Node.js
Machine Learning Model - Python, scikit-learn"""
    
    with open("data/resumes/test_resume.txt", 'w') as f:
        f.write(resume_content)
    
    # Test JD
    jd_content = """Python Developer Job Description

We are looking for a skilled Python Developer with experience in:

REQUIRED SKILLS:
- Python programming
- Django framework
- SQL databases
- AWS cloud services
- Docker containerization

NICE TO HAVE:
- Kubernetes
- MongoDB
- JavaScript
- React
- Machine Learning

RESPONSIBILITIES:
- Develop and maintain web applications
- Design and optimize databases
- Deploy and manage cloud infrastructure"""
    
    with open("data/jds/test_jd.txt", 'w') as f:
        f.write(jd_content)
    
    print("Created test_resume.txt and test_jd.txt in data directories")

def create_test_jd():
    """Create test JD if none exists"""
    jd_content = """Senior Python Developer

Required Skills:
Python, Django, AWS, Docker, SQL, Kubernetes, MongoDB

Qualifications:
- 3+ years Python experience
- Cloud deployment experience
- Database design skills"""
    
    os.makedirs("data/jds", exist_ok=True)
    with open("data/jds/test_jd.txt", 'w') as f:
        f.write(jd_content)

if __name__ == "__main__":
    main()
