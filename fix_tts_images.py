from PIL import Image
import os

def optimize_image_for_tts(input_path, output_path):
    """Optimize image for TTS compatibility"""
    try:
        # Open image
        img = Image.open(input_path)
        
        # Convert to RGB (no transparency/alpha channel)
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Ensure dimensions are correct (TTS expects exact sizes)
        # Standard TTS grid: 10 cards × 7 cards
        # Card size: 183 × 265 pixels
        expected_width = 10 * 183  # 1830
        expected_height = 7 * 265  # 1855
        
        if img.size != (expected_width, expected_height):
            img = img.resize((expected_width, expected_height), Image.LANCZOS)
        
        # Save with TTS-optimized settings
        img.save(output_path, 'JPEG', 
                quality=95,           # High quality for TTS
                optimize=True,        # Optimize file size
                progressive=False,    # TTS prefers baseline JPEG
                subsampling=0)        # No chroma subsampling
        
        print(f"Optimized: {os.path.basename(output_path)}")
        return True
        
    except Exception as e:
        print(f"Error optimizing {input_path}: {e}")
        return False

def optimize_all_grids():
    """Optimize all image grids for TTS"""
    grids_dir = "C:\\GitHub\\YGO-TTS-Assets\\grids"
    
    categories = ['classic_commons', 'classic_rares', 'classic_super_rares', 
                 'classic_ultra_rares', 'classic_spells', 'classic_traps']
    
    for category in categories:
        category_dir = os.path.join(grids_dir, category)
        if os.path.exists(category_dir):
            print(f"\nOptimizing {category}...")
            
            for filename in os.listdir(category_dir):
                if filename.endswith('.jpg'):
                    input_path = os.path.join(category_dir, filename)
                    output_path = input_path  # Overwrite original
                    
                    optimize_image_for_tts(input_path, output_path)
    
    # Also optimize card back
    card_back_path = "C:\\GitHub\\YGO-TTS-Assets\\card-backs\\yugioh_card_back_grid.jpg"
    if os.path.exists(card_back_path):
        print(f"\nOptimizing card back...")
        optimize_image_for_tts(card_back_path, card_back_path)

if __name__ == "__main__":
    print("Optimizing images for TTS compatibility...")
    optimize_all_grids()
    print("\nOptimization complete!")