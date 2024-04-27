from django.shortcuts import render

# Create your views here.
import cv2
import numpy as np
import pytesseract
import re
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

def extract_values_from_text(text):
    values = {}
    lines = text.split('\n')
    for line in lines:
        if 'Platelet' in line:
            platelet_value = re.search(r"\d+\.\d+", line)
            values['Platelet'] = platelet_value.group() if platelet_value else None
        elif 'RBC' in line:
            rbc_value = re.search(r"\d+\.\d+", line)
            values['RBC'] = rbc_value.group() if rbc_value else None
        elif 'WBC' in line:
            wbc_value = re.search(r"\d+\.\d+", line)
            values['WBC'] = wbc_value.group() if wbc_value else None
        elif 'Hemoglobin' in line:
            hemoglobin_value = re.search(r"\d+\.\d+", line)
            values['Hemoglobin'] = hemoglobin_value.group() if hemoglobin_value else None
    return values

def build_model_and_predict(values):
    platelet_min = 150
    platelet_max = 400
    rbc_min = 4.40
    rbc_max = 6.00
    wbc_min = 4.00
    wbc_max = 11.00
    hemoglobin_min = 13.5
    hemoglobin_max = 18.0

    platelet = float(values.get('Platelet', 0)) if values.get('Platelet') is not None else 0
    rbc = float(values.get('RBC', 0)) if values.get('RBC') is not None else 0
    wbc = float(values.get('WBC', 0)) if values.get('WBC') is not None else 0
    hemoglobin = float(values.get('Hemoglobin', 0)) if values.get('Hemoglobin') is not None else 0

    result = "NORMAL" if (platelet_min <= platelet <= platelet_max and
                           rbc_min <= rbc <= rbc_max and
                           wbc_min <= wbc <= wbc_max and
                           hemoglobin_min <= hemoglobin <= hemoglobin_max) else "ABNORMAL"

    if result == "NORMAL":
        return "NORMAL", hemoglobin

    return result, None

@csrf_exempt
def upload_image(request):
    if request.method == 'POST' and request.FILES.get('image'):
        image_file = request.FILES['image']
        result, hemoglobin_value = process_image(image_file)
        if hemoglobin_value is not None:
            return JsonResponse({'result': result, 'Hemoglobin': hemoglobin_value})
        else:
            return JsonResponse({'result': result})
    else:
        return JsonResponse({'error': 'An error occurred while processing the image'}, status=500)

def process_image(image_data):
    try:
        nparr = np.frombuffer(image_data.read(), np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = cv2.resize(image, None, fx=1.5, fy=1.5, interpolation=cv2.INTER_CUBIC)

        custom_config = r'--oem 3 --psm 6'
        text = pytesseract.image_to_string(image, config=custom_config)

        values = extract_values_from_text(text)

        result, hemoglobin_value = build_model_and_predict(values)
        return result, hemoglobin_value
    except pytesseract.TesseractError as e:
        return "Tesseract Error: " + str(e), None
    except Exception as e:
        return "An error occurred: " + str(e), None
