from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import *
from .serializers import *

import datetime

import pickle
import re
import docx
import fitz  # PyMuPDF

import os
import pickle
from django.conf import settings




@api_view(['GET'])
def getRoutes(request):
    return Response('recrutment')


@api_view(['GET'])
def getCandidates (resquest):
    candidates = Candidate.objects.all()
    serializer = CandiateSerializer(candidates, many=True)
    return Response(serializer.data)



@api_view(['GET'])
def getCandidate (resquest, pk):
    candidates = Candidate.objects.get(id=pk)
    serializer = CandiateSerializer(candidates, many=False)
    return Response(serializer.data)








# Load model & preprocessing
model_path = os.path.join(settings.BASE_DIR, 'recrutement', 'MLModels')

tfidf = pickle.load(open(os.path.join(model_path, 'tfidf.pkl'), 'rb'))
rf_model = pickle.load(open(os.path.join(model_path, 'clf_rf.pkl'), 'rb'))
label_encoder = pickle.load(open(os.path.join(model_path, 'label_encoder.pkl'), 'rb'))

def cleanResume(txt):
    txt = re.sub(r'http\S+\s', ' ', txt)
    txt = re.sub('RT|cc', ' ', txt)
    txt = re.sub(r'@\S+', ' ', txt)
    txt = re.sub(r'#\S+\s', ' ', txt)
    txt = re.sub(r'[%s]' % re.escape(r"""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""), ' ', txt)
    txt = re.sub(r'[^\x00-\x7f]', ' ', txt)
    txt = re.sub(r'\s+', ' ', txt)
    return txt.strip()

def extract_text_from_pdf(file):
    pdf_document = fitz.open(stream=file.read(), filetype="pdf")
    text = ""
    for page in pdf_document:
        text += page.get_text()
    return text

def extract_text_from_docx(file):
    doc = docx.Document(file)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text






def extract_email(text):
    match = re.search(r'[\w\.-]+@[\w\.-]+', text)
    return match.group(0) if match else None



def extract_phone(text):
    # Cherche un numéro tunisien (8 chiffres consécutifs)
    match = re.search(r'\b\d{8}\b', text)
    return match.group() if match else None

def extract_name(text):
    # Very simple: first line with two words capitalized or near start of document
    lines = text.strip().split('\n')
    for line in lines[:5]:  # only first 5 lines
        if len(line.split()) >= 2 and all(word[0].isupper() for word in line.split()[:2]):
            return line.strip()
    return None

def extract_birthdate(text):
    # Format AAAA/MM/JJ ou AAAA-MM-JJ
    match = re.search(r'\b\d{4}[-/]\d{2}[-/]\d{2}\b', text)
    return match.group() if match else None

def extract_universities(cv_text):
    # Nettoyage du texte
    lines = [line.strip() for line in cv_text.split("\n") if line.strip()]

    universities = []
    keywords = r"(université|university|institut|école|school|faculty)"
    
    for i, line in enumerate(lines):
        if re.search(keywords, line, re.IGNORECASE):
            # On prend la ligne actuelle
            uni_name = line

            # Si la ligne suivante contient des mots complémentaires (ville, pays, sigle)
            if i + 1 < len(lines) and len(lines[i+1].split()) < 6:
                uni_name += " " + lines[i+1]

            universities.append(uni_name)

    return universities






def extract_skills(text):
    # Very simple: extract after 'COMPETENCES' or 'Skills' section header until next empty line
    skills_section = re.search(r'(COMPETENCES|Skills|Compétences)(.*?)(\n\n|\Z)', text, flags=re.DOTALL|re.IGNORECASE)
    if skills_section:
        skills_text = skills_section.group(2).strip()
        # split by commas, bullets, newlines
        skills = re.split(r'[\n,•]+', skills_text)
        skills = [s.strip() for s in skills if s.strip()]
        return ', '.join(skills)
    return None



def extract_languages(text):
    # Liste élargie de langues possibles
    languages_list = [
        "Arabic", "Français", "French", "English", "Anglais", "Spanish", "Espagnol",
        "German", "Deutsch", "Italien", "Italian", "Chinese", "Mandarin", "Russian",
        "Portuguese", "Turkish", "Dutch", "Hindi", "Japanese", "Korean", "Polish",
        "Swedish", "Norwegian", "Danish", "Finnish", "Greek"
    ]
    
    # Regex pour niveaux possibles
    level_pattern = r"(A1|A2|B1|B2|C1|C2|Native|Fluent|Courant|Intermédiaire|Débutant|Avancé)"
    
    found_languages = []
    for lang in languages_list:
        # Recherche avec niveau possible juste après ou sur la même ligne
        pattern = rf"({lang})\s*(?:{level_pattern})?"
        matches = re.findall(pattern, text, flags=re.IGNORECASE)
        
        for match in matches:
            language = match[0]
            level = match[1] if len(match) > 1 else ""
            found_languages.append({
                "langue": language,
                "niveau": level if level else "Non précisé"
            })
    
    return found_languages





def extract_address(text):
    # Try to find lines with typical address elements (e.g. city names, postal codes, street names)
    # This is tricky and depends on your CV format; here just grab line containing keywords like 'Ariana' or postal codes digits
    matches = re.findall(r'.*(Ariana|Tunisie|Tunisia|City|Street|Berges|kef|Tunis|Rue|address|adresse).*', text, flags=re.IGNORECASE)
    return matches[0].strip() if matches else None



def parse_date(date_str):
    if not date_str:
        return None  # No date found
    date_str = date_str.replace('/', '-')
    try:
        return datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        return None









def compute_fit_score(cv_skills_text, job_description):
    """
    Compute a CV-to-job-description fit score.
    Returns: score (0-100), matched skills, missing skills
    """
    # Extract skills from job description (simple regex or predefined list)
    job_skills = re.findall(r'\b\w+\b', job_description.lower())
    job_skills = set([s for s in job_skills if len(s) > 2])  # remove very small words

    # Extract skills from CV (from extract_skills function)
    if not cv_skills_text:
        cv_skills_text = ""
    cv_skills = cv_skills_text.lower().split(',')  # your extract_skills returns comma-separated
    cv_skills = set([s.strip() for s in cv_skills if s.strip()])

    # Match
    matched = cv_skills.intersection(job_skills)
    missing = job_skills - cv_skills

    # Base scoring: ratio of matched skills
    score = len(matched) / len(job_skills) * 100 if job_skills else 0

    # Intelligent criteria: bonus points for repetition or keyword density
    repetition_weight = 0
    for skill in matched:
        # Count how many times each matched skill appears in the CV text
        repetition_count = cv_skills_text.lower().count(skill)
        repetition_weight += repetition_count - 1  # first occurrence already counted in base score

    # Adjust score with repetition weight, max 100
    score = min(score + repetition_weight, 100)

    return round(score, 2), ', '.join(matched), ', '.join(missing)



@api_view(['POST'])
def predictJob(request):
    print("📥 Incoming predictJob request")

    job_description = request.data.get('job_description', '').strip()
    files = request.FILES.getlist('cvs')  # multiple CVs from Angular

    print(f"📝 Job description: {job_description}")
    print(f"📂 Number of files received: {len(files)}")

    if not files:
        print(" No CVs uploaded")
        return Response({"error": "No CVs uploaded"}, status=400)
    
    if not job_description:
        print(" No job description provided")
        return Response({"error": "Job description is required"}, status=400)

    results = []

    try:
        for idx, file in enumerate(files, start=1):
            try:
                print(f"\n--- Processing file {idx}/{len(files)}: {file.name} ---")
                filename = file.name.lower()

                # Extract raw text
                if filename.endswith(".pdf"):
                    print(" Extracting text from PDF...")
                    raw_text = extract_text_from_pdf(file)
                elif filename.endswith(".docx"):
                    print(" Extracting text from DOCX...")
                    raw_text = extract_text_from_docx(file)
                elif filename.endswith(".txt"):
                    print(" Reading text file...")
                    raw_text = file.read().decode('utf-8', errors='ignore')
                else:
                    print(f" Unsupported format for file: {filename}")
                    results.append({"file": filename, "error": "Unsupported format"})
                    continue

                print("🧹 Cleaning resume text...")
                cleaned = cleanResume(raw_text)

                print("Running prediction model...")
                features = tfidf.transform([cleaned])
                pred_id = rf_model.predict(features)[0]
                pred_label = label_encoder.inverse_transform([pred_id])[0]
                print(f" Predicted role: {pred_label}")

                print("Extracting candidate details...")
                name = extract_name(raw_text)
                email = extract_email(raw_text)
                phone = extract_phone(raw_text)
                date_naissance_str = extract_birthdate(raw_text)
                date_naissance = parse_date(date_naissance_str)
                university = extract_universities(raw_text)
                skills = extract_skills(raw_text)
                langues = extract_languages(raw_text)
                adresse = extract_address(raw_text)

                print("Computing fit score...")
                fit_score, matched_skills, missing_skills = compute_fit_score(skills, job_description)

                print(" Saving prediction to database...")
                prediction = JobPrediction.objects.create(
                    cv_file=file,
                    predicted_role=pred_label,
                    name=name,
                    email=email,
                    phone=phone,
                    date_naissance=date_naissance,
                    university=university,
                    skills=skills,
                    langues=langues,
                    adresse=adresse,
                    job_description=job_description,
                    fit_score=fit_score,
                    matched_skills=matched_skills,
                    missing_skills=missing_skills
                )

                results.append({
                    "file": filename,
                    "predicted_role": pred_label,
                    "id": prediction.id,
                    "name": name,
                    "email": email,
                    "phone": phone,
                    "date_naissance": date_naissance,
                    "university": university,
                    "skills": skills,
                    "langues": langues,
                    "adresse": adresse,
                    "job_description": job_description,
                    "fit_score": fit_score,
                    "matched_skills": matched_skills,
                    "missing_skills": missing_skills,
                })

                print(f" Finished processing {filename}")

            except Exception as file_error:
                print(f" Error processing file {file.name}: {file_error}")
                results.append({"file": file.name, "error": str(file_error)})

        print("\nReturning all results")
        return Response({"results": results})

    except Exception as e:
        print(f" Fatal server error: {e}")
        return Response({"error": str(e)}, status=500)









# @api_view(['POST'])
# def predictJob(request):
#     job_description = request.data.get('job_description', '').strip()
#     files = request.FILES.getlist('cvs')  # multiple CVs from Angular

#     if not files:
#         return Response({"error": "No CVs uploaded"}, status=400)
    
#     if not job_description:
#         return Response({"error": "Job description is required"}, status=400)

#     results = []

#     try:
#         for file in files:
#             filename = file.name.lower()

#             # Extract raw text from file
#             if filename.endswith(".pdf"):
#                 raw_text = extract_text_from_pdf(file)
#             elif filename.endswith(".docx"):
#                 raw_text = extract_text_from_docx(file)
#             elif filename.endswith(".txt"):
#                 raw_text = file.read().decode('utf-8', errors='ignore')
#             else:
#                 results.append({"file": filename, "error": "Unsupported format"})
#                 continue

#             # Predict job role
#             cleaned = cleanResume(raw_text)
#             features = tfidf.transform([cleaned])
#             pred_id = rf_model.predict(features)[0]
#             pred_label = label_encoder.inverse_transform([pred_id])[0]

#             # Extract details
#             name = extract_name(raw_text)
#             email = extract_email(raw_text)
#             phone = extract_phone(raw_text)
#             date_naissance_str = extract_birthdate(raw_text)
#             date_naissance = parse_date(date_naissance_str)
#             university = extract_universities(raw_text)
#             skills = extract_skills(raw_text)
#             langues = extract_languages(raw_text)
#             adresse = extract_address(raw_text)

#             # Compute fit score
#             fit_score, matched_skills, missing_skills = compute_fit_score(skills, job_description)

#             # Save to DB
#             prediction = JobPrediction.objects.create(
#                 cv_file=file,
#                 predicted_role=pred_label,
#                 name=name,
#                 email=email,
#                 phone=phone,
#                 date_naissance=date_naissance,
#                 university=university,
#                 skills=skills,
#                 langues=langues,
#                 adresse=adresse,
#                 job_description=job_description,
#                 fit_score=fit_score,
#                 matched_skills=matched_skills,
#                 missing_skills=missing_skills
#             )

#             results.append({
#                 "file": filename,
#                 "predicted_role": pred_label,
#                 "id": prediction.id,
#                 "name": name,
#                 "email": email,
#                 "phone": phone,
#                 "date_naissance": date_naissance,
#                 "university": university,
#                 "skills": skills,
#                 "langues": langues,
#                 "adresse": adresse,
#                 "job_description":job_description,
#                 "fit_score": fit_score,
#                 "matched_skills": matched_skills,
#                 "missing_skills": missing_skills,
#             })

#         return Response({"results": results})

#     except Exception as e:
#         return Response({"error": str(e)}, status=500)




@api_view(['GET'])
def getPredictions(request):
    try:
       
        prediction = JobPrediction.objects.all()
        serializer = JobPredictionSerializer(prediction , many=True)
        return Response(serializer.data)
    except JobPrediction.DoesNotExist:
        return Response({"error": "Prediction not found"}, status=404)
    




@api_view(['GET'])
def getPrediction(request, prediction_id):
    try:
        prediction = JobPrediction.objects.get(id=prediction_id)
        serializer = JobPredictionSerializer(prediction)
        return Response(serializer.data)
    except JobPrediction.DoesNotExist:
        return Response({"error": "Prediction not found"}, status=404)