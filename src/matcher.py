import re
from jd_parser import extract_skills_from_jd

def extract_skills_from_resume(resume_text):
    """Extract skills from resume text using keyword matching"""
    # Expanded tech skills dictionary
    tech_skills = [
        'python', 'java', 'javascript', 'sql', 'aws', 'docker', 'kubernetes',
        'react', 'node.js', 'django', 'flask', 'mongodb', 'mysql', 'postgresql',
        'git', 'jenkins', 'linux', 'html', 'css', 'typescript', 'angular', 'vue',
        'c++', 'c#', 'php', 'ruby', 'go', 'rust', 'swift', 'kotlin',
        'azure', 'gcp', 'cloud', 'machine learning', 'ml', 'ai', 'tensorflow',
        'pytorch', 'pandas', 'numpy', 'scikit-learn', 'data analysis',
        'rest api', 'graphql', 'microservices', 'ci/cd', 'devops'
    ]
    
    found_skills = []
    resume_lower = resume_text.lower()
    
    for skill in tech_skills:
        # Use word boundaries to avoid partial matches
        if re.search(r'\b' + re.escape(skill) + r'\b', resume_lower):
            found_skills.append(skill)
    
    return found_skills

def calculate_match_score(resume_skills, jd_skills):
    """Calculate match score between resume and JD skills"""
    if not jd_skills:
        return 0, [], []
    
    # Find matching skills
    matched_skills = [skill for skill in jd_skills if skill in resume_skills]
    missing_skills = [skill for skill in jd_skills if skill not in resume_skills]
    
    # Calculate score (percentage of JD skills found in resume)
    match_score = (len(matched_skills) / len(jd_skills)) * 100
    
    return match_score, matched_skills, missing_skills

def generate_match_reasons(matched_skills, missing_skills, score):
    """Generate human-readable reasons for the match score"""
    reasons = []
    
    if matched_skills:
        reasons.append(f"Found: {', '.join(matched_skills[:5])}" + 
                      ("..." if len(matched_skills) > 5 else ""))
    
    if missing_skills:
        reasons.append(f"Missing: {', '.join(missing_skills[:5])}" + 
                      ("..." if len(missing_skills) > 5 else ""))
    
    # Add qualitative assessment
    if score >= 80:
        assessment = "Excellent match!"
    elif score >= 60:
        assessment = "Good match"
    elif score >= 40:
        assessment = "Moderate match"
    elif score >= 20:
        assessment = "Poor match"
    else:
        assessment = "Very poor match"
    
    reasons.append(assessment)
    
    return reasons

def match_resume_to_jd(resume_text, jd_text):
    """Main function to match a resume against a job description"""
    # Extract skills from both
    resume_skills = extract_skills_from_resume(resume_text)
    jd_skills = extract_skills_from_jd(jd_text)
    
    # Calculate match score
    score, matched, missing = calculate_match_score(resume_skills, jd_skills)
    
    # Generate reasons
    reasons = generate_match_reasons(matched, missing, score)
    
    return {
        'match_score': round(score, 2),
        'resume_skills': resume_skills,
        'jd_skills': jd_skills,
        'matched_skills': matched,
        'missing_skills': missing,
        'reasons': reasons,
        'resume_skills_count': len(resume_skills),
        'jd_skills_count': len(jd_skills),
        'matched_count': len(matched)
    }

if __name__ == "__main__":
    # Test the matcher
    test_resume = """
    Python developer with 3 years experience.
    Skills: Python, Django, SQL, AWS, Docker, JavaScript, React
    Experience with MySQL and PostgreSQL databases.
    Deployed applications on AWS EC2 and used Docker for containerization.
    """
    
    test_jd = """
    Looking for Python Developer with:
    - Python programming
    - Django framework
    - SQL databases
    - AWS cloud services
    - Docker containerization
    - Kubernetes experience
    - MongoDB knowledge
    """
    
    result = match_resume_to_jd(test_resume, test_jd)
    
    print("=== MATCHER TEST RESULTS ===")
    print(f"Match Score: {result['match_score']}%")
    print(f"Resume Skills: {result['resume_skills']}")
    print(f"JD Skills: {result['jd_skills']}")
    print(f"Matched Skills: {result['matched_skills']}")
    print(f"Missing Skills: {result['missing_skills']}")
    print("Reasons:")
    for reason in result['reasons']:
        print(f"  - {reason}")
