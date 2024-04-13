# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework.parsers import MultiPartParser, FormParser
# import pytesseract
# import cv2
# import numpy as np
# import re
# import io

# class OCRAPIView(APIView):
#     parser_classes = (MultiPartParser, FormParser)
#     def post(self, request, *args, **kwargs):
#         uploaded_image = request.FILES.get('image')
#         if uploaded_image:
#             image_data = uploaded_image.read() 
#             img_np_array = np.frombuffer(image_data, np.uint8) 
#             img = cv2.imdecode(img_np_array, cv2.IMREAD_COLOR)  
#             extracted_text = pytesseract.image_to_string(img)
#             extracted_details = preprocess_details(extracted_text)
#             return Response({'status_patient': extracted_details['status_patient'], 'hemoglobin': extracted_details['details_OCR_CBC']['Hemoglobin']})
#         else:
#             return Response({'error': 'No Image Find.'}, status=400)

# def preprocess_details(text):
#     ranges = {
#         'WBC': (4.12, 11.12),
#         'RBC': (4.40, 6.12),
#         'Platelet Count': (150, 400),
#         'Hemoglobin': (13.12, 18.12),
#     }
#     patterns = {
#         'WBC': r'WBC\s*Count\s*([\d.]+)',
#         'RBC': r'RBC\s*Count\s*([\d.]+)',
#         'Platelet Count': r'Platelet\s*Count\s*([\d.]+)',
#         'Hemoglobin': r'Hemoglobin\s*([\d.]+)',
#     }
#     extracted_details = {}
#     status_patient = "Good"
#     for key, pattern in patterns.items():
#         match = re.search(pattern, text, re.IGNORECASE)
#         if match:
#             value = float(match.group(1))
#             extracted_details[key] = value
#             if key in ranges:
#                 if value < ranges[key][0] or value > ranges[key][1]:
#                     status_patient = "Not Good"
#         else:
#             extracted_details[key] = None
#             status_patient = "Not Good"

#     return {'status_patient': status_patient, 'details_OCR_CBC': extracted_details}

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
import easyocr
import cv2
import numpy as np
import re
import io

class OCRAPIView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        uploaded_image = request.FILES.get('image')
        if uploaded_image:
            image_data = uploaded_image.read()
            img_np_array = np.frombuffer(image_data, np.uint8)
            img = cv2.imdecode(img_np_array, cv2.IMREAD_COLOR)

            # Initialize easyocr reader
            reader = easyocr.Reader(['en'])

            # Perform OCR on the image
            result = reader.readtext(img)

            # Extract text from the result
            extracted_text = ' '.join([item[1] for item in result])

            extracted_details = preprocess_details(extracted_text)
            return Response({'status_patient': extracted_details['status_patient'], 'hemoglobin': extracted_details['details_OCR_CBC']['Hemoglobin']})
        else:
            return Response({'error': 'No Image Find.'}, status=400)

def preprocess_details(text):
    ranges = {
        'WBC': (4.12, 11.12),
        'RBC': (4.40, 6.12),
        'Platelet Count': (150, 400),
        'Hemoglobin': (13.12, 18.12),
    }
    patterns = {
        'WBC': r'WBC\s*Count\s*([\d.]+)',
        'RBC': r'RBC\s*Count\s*([\d.]+)',
        'Platelet Count': r'Platelet\s*Count\s*([\d.]+)',
        'Hemoglobin': r'Hemoglobin\s*([\d.]+)',
    }
    extracted_details = {}
    status_patient = "Good"
    for key, pattern in patterns.items():
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            value = float(match.group(1))
            extracted_details[key] = value
            if key in ranges:
                if value < ranges[key][0] or value > ranges[key][1]:
                    status_patient = "Not Good"
        else:
            extracted_details[key] = None
            status_patient = "Not Good"

    return {'status_patient': status_patient, 'details_OCR_CBC': extracted_details}
