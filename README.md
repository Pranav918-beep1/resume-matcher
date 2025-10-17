#  Resume Matcher
An AI-powered Resume Screening and Ranking System built with **Python + NLP + Streamlit**.  
This project matches candidate resumes against a given job description and ranks them based on relevance — helping recruiters shortlist top candidates faster.

---

## Features

 Extracts and parses text from resumes (PDF/DOCX).  
 Parses and understands job descriptions.  
 Calculates similarity between resumes and job description using NLP.  
 Displays ranked results in an interactive **Streamlit** dashboard.  
 Supports export of ranked results to CSV.  

---

## 🧩 Project Structure

resume-matcher/
├── app.py # Main Streamlit app
├── matcher.py # Matching logic (TF-IDF / similarity)
├── advanced_parser.py # Advanced resume parser
├── simple_parser.py # Simple text parser
├── jd_parser.py # Job description parser
├── requirements.txt # Dependencies
├── ranking_results.csv # Sample output
└── README.md # Project documentation
