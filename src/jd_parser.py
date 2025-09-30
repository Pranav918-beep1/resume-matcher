import re
import json

def extract_skills_from_jd(jd_text):
    """Extract skills from job description using simple keyword matching"""
    # Common tech skills dictionary
    tech_skills = [
        'python', 'java', 'javascript', 'sql', 'aws', 'docker', 'kubernetes',
        'react', 'node.js', 'django', 'flask', 'mongodb', 'mysql', 'postgresql',
        'git', 'jenkins', 'linux', 'html', 'css', 'typescript', 'angular', 'vue'
    ]
    
    found_skills = []
    jd_lower = jd_text.lower()
    
    for skill in tech_skills:
        if skill in jd_lower:
            found_skills.append(skill)
    
    return found_skills

def parse_jd_file(jd_path):
    """Parse a job description file and extract requirements"""
    try:
        with open(jd_path, 'r', encoding='utf-8') as f:
            jd_text = f.read()
        
        skills = extract_skills_from_jd(jd_text)
        
        return {
            'skills_required': skills,
            'text': jd_text,
            'total_skills': len(skills)
        }
    except Exception as e:
        print(f"Error reading JD file {jd_path}: {e}")
        return None

if __name__ == "__main__":
    # Test the JD parser
    test_jd = """
    We are looking for a Python Developer with experience in:
    - Python programming
    - Django framework
    - SQL databases
    - AWS cloud services
    - Docker containerization
    
    Nice to have: JavaScript, React, MongoDB
    """
    
    skills = extract_skills_from_jd(test_jd)
    print("Extracted skills:", skills)
