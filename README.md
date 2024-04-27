# OCR API using Django REST Framework

This Django REST Framework API provides functionality for Optical Character Recognition (OCR) on medical Complete Blood Count (CBC) reports. It extracts details such as White Blood Cell (WBC) count, Red Blood Cell (RBC) count, Platelet Count, and Hemoglobin levels from uploaded images of CBC reports.

## Installation

To set up this API locally, follow these steps:

1. Clone this repository to your local machine:

```bash
git clone <repository-url>
```

2. Navigate to the project directory:

```bash
cd <project-directory>
```

3. Create a virtual environment (optional but recommended):

```bash
python -m venv venv
```

4. Activate the virtual environment:

   - On Windows:

```bash
venv\Scripts\activate
```

   - On macOS and Linux:

```bash
source venv/bin/activate
```

5. Install the required dependencies:

```bash
pip install -r requirements.txt
```

6. Run migrations to set up the database (assuming you have Django models):

```bash
python manage.py migrate
```

7. Start the Django development server:

```bash
python manage.py runserver
```

## Usage

### Uploading an Image for OCR

Send a POST request to the endpoint `/ocr/` with a multipart form containing an image file named `image`. The API will perform OCR on the uploaded image and extract details from the CBC report.

### Response Format

The API returns a JSON response with the extracted details and patient status:

```json
{
  "status_patient": "Good",
  "details_OCR_CBC": {
    "WBC": 7.2,
    "RBC": 5.5,
    "Platelet Count": 280,
    "Hemoglobin": 15.6
  }
}
```

The `status_patient` field indicates whether the patient's CBC report falls within acceptable ranges. If any detail is outside the acceptable range, `status_patient` will be set to "Not Good".


## Host Link
https://radwan-ocr-api.onrender.com/

## Requirements

- Python (3.x recommended)
- Django (3.x)
- Django REST Framework (3.x)
- OpenCV (for image processing)
- Pytesseract (for OCR)
- numpy
- re


