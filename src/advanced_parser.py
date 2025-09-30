import spacy
import re

# Load spaCy model
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    print("Please download the spaCy model first: python -m spacy download en_core_web_sm")
    nlp = None

def extract_advanced_fields(text):
    """Extract advanced fields using spaCy NER"""
    if nlp is None:
        return extract_basic_fields(text)
    
    doc = nlp(text)
    
    entities = {
        'PERSON': [],
        'ORG': [],  # Companies, universities
        'GPE': [],  # Locations
        'DATE': [],
        'EMAIL': [],
        'PHONE': []
    }
    
    # Extract named entities
    for ent in doc.ents:
        if ent.label_ in entities:
            entities[ent.label_].append(ent.text)
    
    # Extract email and phone with regex (more reliable)
    entities['EMAIL'] = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
    entities['PHONE'] = re.findall(r'[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]', text)
    
    # Try to extract education
    education = extract_education(text)
    
    return {
        'name': entities['PERSON'][0] if entities['PERSON'] else '',
        'email': entities['EMAIL'][0] if entities['EMAIL'] else '',
        'phone': entities['PHONE'][0] if entities['PHONE'] else '',
        'organizations': list(set(entities['ORG'])),
        'locations': list(set(entities['GPE'])),
        'education': education,
        'entities': entities
    }

def extract_education(text):
    """Extract education information using patterns"""
    education_keywords = ['bachelor', 'master', 'phd', 'degree', 'university', 'college', 'institute']
    education = []
    
    lines = text.split('\n')
    for line in lines:
        line_lower = line.lower()
        if any(keyword in line_lower for keyword in education_keywords):
            education.append(line.strip())
    
    return education

if __name__ == "__main__":
    # Test advanced parser
    test_text = """
    John Doe
    Email: john.doe@email.com  
    Phone: +1-555-123-4567
    
    EDUCATION:
    Bachelor of Science in Computer Science from MIT University
    Master of Technology from Stanford
    
    EXPERIENCE:
    Software Engineer at Google in California
    Senior Developer at Microsoft
    """
    
    result = extract_advanced_fields(test_text)
    print("Advanced Fields Extraction:")
    for key, value in result.items():
        if key != 'entities':
            print(f"{key}: {value}")
