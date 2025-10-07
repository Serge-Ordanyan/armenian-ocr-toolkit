
#!/usr/bin/env python3
"""
Advanced Armenian OCR with multiple processing attempts
Saves multiple versions for comparison
"""
import pytesseract
from pdf2image import convert_from_path
from PIL import Image, ImageEnhance, ImageFilter, ImageOps
import os

pdf_path = "/Users/seryozhaordanyan/Desktop/PDFConverter/Anania_Shirakatsi_1979.pdf"
output_dir = "/Users/seryozhaordanyan/Desktop/PDFConverter/ocr_outputs"
pytesseract.pytesseract.tesseract_cmd = "/opt/homebrew/bin/tesseract"
# ---------------------------------------------

os.makedirs(output_dir, exist_ok=True)

def preprocess_aggressive(img):
    """Aggressive preprocessing - high contrast and hard threshold to pure black/white"""
    img = img.convert('L')
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(3.0)
    enhancer = ImageEnhance.Sharpness(img)
    img = enhancer.enhance(2.5)
    img = img.point(lambda x: 0 if x < 128 else 255, '1')
    return img

def preprocess_gentle(img):
    """Gentle preprocessing - preserve detail with moderate contrast and denoising"""
    img = img.convert('L')
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(1.5)
    img = img.filter(ImageFilter.MedianFilter(size=3))
    return img

def preprocess_inverted(img):
    """Try inverted colors (for dark backgrounds)"""
    img = img.convert('L')
    img = ImageOps.invert(img)
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(2.0)
    return img

def ocr_with_config(img, lang, psm):
    """OCR with specific configuration"""
    custom_config = f'--oem 3 --psm {psm} -c preserve_interword_spaces=1'
    try:
        text = pytesseract.image_to_string(img, lang=lang, config=custom_config)
        return text
    except Exception as e:
        return f"Error: {str(e)}"

def process_with_multiple_methods(images):
    """Try multiple OCR methods and save all results"""
    
    methods = [
        {
            'name': 'Method_1_HYE+ARM_Aggressive',
            'lang': 'hye+arm',
            'preprocess': preprocess_aggressive,
            'psm': 6
        },
        {
            'name': 'Method_2_HYE+ARM_Gentle',
            'lang': 'hye+arm',
            'preprocess': preprocess_gentle,
            'psm': 6
        },
        {
            'name': 'Method_3_Original_HYE+ARM',
            'lang': 'hye+arm',
            'preprocess': lambda x: x.convert('L'),
            'psm': 6
        },
        {
            'name': 'Method_4_HYE_Aggressive',
            'lang': 'hye',
            'preprocess': preprocess_aggressive,
            'psm': 6
        },
        {
            'name': 'Method_5_HYE+ARM_AutoDetect_PSM3',
            'lang': 'hye+arm',
            'preprocess': preprocess_gentle,
            'psm': 3 
        }
    ]

    for method in methods:
        print(f"\n📝 Processing: {method['name']} (Lang: {method['lang']}, PSM: {method['psm']})")
        print("=" * 60)
        text = ""
        for i, img in enumerate(images, 1):
            print(f" Page {i}/{len(images)}...", end=" ")
            processed = method['preprocess'](img)
            page_text = ocr_with_config(
                processed, 
                method['lang'], 
                method['psm']
            )
            
            text += f"\n{'='*50}\nԷջ {i}\n{'='*50}\n\n"
            text += page_text + "\n"
            print("✓")

        output_file = os.path.join(output_dir, f"{method['name']}.txt")
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(text)
        print(f" ✅ Saved: {output_file}")

def main():
    print("🔄 Converting PDF to images (DPI=600 for maximum quality)...")
    print("⚠️ This may take several minutes...\n")
    
    try:
        # Very high DPI for best quality
        images = convert_from_path(pdf_path, dpi=600)
    except Exception as e:
        print(f"🔴 ERROR converting PDF: {e}")
        print("Ensure 'poppler' is installed and accessible if this error persists.")
        return

    print(f"📄 Found {len(images)} pages\n")
    print("🔬 Will try 5 different OCR methods (prioritizing 'hye+arm')...")
    print(f"📁 Results will be saved to: {output_dir}\n")
    
    process_with_multiple_methods(images)
    
    print("\n" + "="*60)
    print("✅ ALL METHODS COMPLETED!")
    print("="*60)
    print(f"\n📂 Check folder: {output_dir}")
    print("\n💡 Compare all 5 files and use the one with best accuracy")
    print(" Then you can manually fix remaining errors\n")

if __name__ == "__main__":
    main()
