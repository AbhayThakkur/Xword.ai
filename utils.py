import easyocr
from deep_translator import GoogleTranslator
import re
from nltk.corpus import stopwords
from PIL import Image

# Preprocess extracted text
def preprocess_text(text):
    """Clean up extracted text by removing unwanted characters and normalizing spaces."""
    return re.sub(r'\s+', ' ', re.sub(r'[^\w\s]', '', text)).strip()

# Remove stop words
def filter_stop_words(words):
    """Remove common English stop words."""
    stop_words = set(stopwords.words('english'))
    return [word for word in words if word.lower() not in stop_words]

# Resize image if too large
def resize_image(image_path, base_width=800):
    """Resize the image while maintaining aspect ratio."""
    image = Image.open(image_path)
    if image.size[0] > base_width:
        width_percent = (base_width / float(image.size[0]))
        height_size = int((float(image.size[1]) * float(width_percent)))
        image = image.resize((base_width, height_size), Image.LANCZOS)
    return image

# Translate words in bulk with fallback to word-by-word
def batch_translate(words):
    """Translate a list of words from English to Hindi."""
    translator = GoogleTranslator(source='en', target='hi')
    text_to_translate = ' '.join(words)
    translated_text = translator.translate(text_to_translate)
    translated_words = translated_text.split()

    return dict(zip(words, translated_words)) if len(words) == len(translated_words) else {word: translator.translate(word) for word in words}

# Function to process image and return translations
def process_image(image_path):
    try:
        # Resize the image if necessary
        resized_image = resize_image(image_path)
        resized_image.save("media/resized_temp.png")  # Save resized image for easyocr processing
        
        # Extract text using EasyOCR
        reader = easyocr.Reader(['en'])  # Specify language
        result = reader.readtext("media/resized_temp.png")

        # Extract detected text
        extracted_text = ' '.join([detection[1] for detection in result])
        processed_text = preprocess_text(extracted_text)

        # Process and translate words
        words = processed_text.split()
        filtered_words = filter_stop_words(words)
        translations = batch_translate(filtered_words)

        return translations
    except Exception as e:
        return {"error": str(e)}
