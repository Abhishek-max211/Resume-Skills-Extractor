from flask import Flask, request, render_template
import fitz  # PyMuPDF
from docx import Document
import io
import re

app = Flask(__name__)

SKILLS = [
    'Python', 'Java', 'JavaScript', 'React', 'Angular', 'Vue', 'Django', 'Flask',
    'SQL', 'NoSQL', 'MongoDB', 'PostgreSQL', 'AWS', 'Azure', 'Docker', 'Kubernetes',
    'Git', 'Linux', 'C++', 'C#', 'Ruby', 'Go', 'HTML', 'CSS', 'TypeScript',
    'Node.js', 'Express', 'Machine Learning', 'Deep Learning', 'TensorFlow',
    'PyTorch', 'NLP', 'Computer Vision', 'REST', 'GraphQL', 'Agile', 'Scrum',
    'Data Analysis', 'Data Science', 'Tableau', 'PowerBI', 'Jenkins', 'CI/CD',
    'Swift', 'Objective-C', 'Android', 'iOS', 'SaaS', 'Microservices'
]

def extract_text_from_pdf(file_bytes):
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    return "\n".join([page.get_text() for page in doc])

def extract_text_from_docx(file_bytes):
    doc = Document(io.BytesIO(file_bytes))
    return "\n".join([para.text for para in doc.paragraphs])

def extract_text_from_txt(file_bytes):
    return file_bytes.decode('utf-8', errors='ignore')

def extract_skills(text):
    found = set()
    lower_text = text.lower()
    for skill in SKILLS:
        if re.search(r'\b' + re.escape(skill.lower()) + r'\b', lower_text):
            found.add(skill)
    return sorted(found)

@app.route('/', methods=['GET', 'POST'])
def index():
    skills = []
    error = None
    if request.method == 'POST':
        uploaded_file = request.files.get('resume')
        if not uploaded_file:
            error = "No file uploaded"
        else:
            filename = uploaded_file.filename.lower()
            file_bytes = uploaded_file.read()
            try:
                if filename.endswith('.pdf'):
                    text = extract_text_from_pdf(file_bytes)
                elif filename.endswith('.docx'):
                    text = extract_text_from_docx(file_bytes)
                elif filename.endswith('.txt'):
                    text = extract_text_from_txt(file_bytes)
                else:
                    error = "Unsupported file type"
                    text = ""
                if not error:
                    skills = extract_skills(text)
            except Exception as e:
                error = f"Error: {str(e)}"
    return render_template("index.html", skills=skills, error=error)

if __name__ == '__main__':
    app.run(debug=True)
