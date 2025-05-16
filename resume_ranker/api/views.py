import os
import re
import fitz  # PyMuPDF
from django.http import JsonResponse
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Function to extract text from different types of files (PDF, TXT)
def extract_text_from_file(file):
    file_name = file.name.lower()
    if file_name.endswith('.pdf'):
        return extract_text_from_pdf(file)
    elif file_name.endswith('.txt'):
        return file.read().decode('utf-8')
    else:
        return ""

# Extract text from PDF using PyMuPDF
def extract_text_from_pdf(pdf_file):
    text = ""
    try:
        temp_path = f"temp_{pdf_file.name}"
        with open(temp_path, 'wb') as f:
            for chunk in pdf_file.chunks():
                f.write(chunk)
        doc = fitz.open(temp_path)
        for page in doc:
            text += page.get_text()
        doc.close()
        os.remove(temp_path)
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
    return text

# Enhanced preprocessing
def preprocess_text(text):
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^\w\s]', ' ', text)
    text = re.sub(r'\d+', '', text)
    return text.lower().strip()

# TF-IDF based resume ranking
def rank_resumes_by_similarity(job_description, resumes_data):
    job_description = preprocess_text(job_description)
    
    resume_texts = []
    resume_names = []
    
    for resume in resumes_data:
        processed_text = preprocess_text(resume['text'])
        resume_texts.append(processed_text)
        resume_names.append(resume['name'])

    corpus = [job_description] + resume_texts

    vectorizer = TfidfVectorizer(
        stop_words='english',
        ngram_range=(1, 2),
        max_features=5000
    )
    tfidf_matrix = vectorizer.fit_transform(corpus)
    
    job_vector = tfidf_matrix[0:1]
    resume_vectors = tfidf_matrix[1:]
    
    similarities = cosine_similarity(job_vector, resume_vectors)

    rankings = []
    for i, similarity in enumerate(similarities[0]):
        match_percentage = round(similarity * 100, 2)
        rankings.append({
            'name': resume_names[i],
            'match_percentage': match_percentage
        })
    
    rankings = sorted(rankings, key=lambda x: x['match_percentage'], reverse=True)
    return rankings

# API: Rank Resumes
@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def rank_resumes(request):
    try:
        job_description = request.data.get('jobDescription', '')
        if not job_description:
            return JsonResponse({'error': 'Job description is required'}, status=400)
        
        resume_files = request.FILES.getlist('resumes')
        if not resume_files:
            return JsonResponse({'error': 'Resume files are required'}, status=400)
        
        resumes_data = []
        for resume_file in resume_files:
            resume_text = extract_text_from_file(resume_file)
            resumes_data.append({
                'name': resume_file.name,
                'text': resume_text
            })
        
        ranked_resumes = rank_resumes_by_similarity(job_description, resumes_data)
        return JsonResponse({'rankings': ranked_resumes})
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

# API: Extract Resume Text
@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def upload_resume(request):
    try:
        resume_file = request.FILES.get('resume')
        if not resume_file:
            return JsonResponse({'error': 'Resume file is required'}, status=400)
        
        resume_text = extract_text_from_file(resume_file)
        return JsonResponse({'resume_text': resume_text})
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
