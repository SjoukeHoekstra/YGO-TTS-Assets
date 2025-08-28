from PIL import Image
import os

def create_single_card_back():
    """Create a single card back image (not grid)"""
    # Open the official card back
    back_img = Image.open("C:\\GitHub\\YGO-TTS-Assets\\card-backs\\official_yugioh_back.png")
    
    # Convert to RGB and resize to match front card dimensions
    back_img = back_img.convert('RGB')
    back_img = back_img.resize((421, 614), Image.LANCZOS)  # Match front card size
    
    # Save as JPEG for TTS with maximum quality
    back_img.save("C:\\GitHub\\YGO-TTS-Assets\\card-backs\\yugioh_card_back_single.jpg", 
                  'JPEG', quality=100, optimize=False, subsampling=0)
    
    print("Created single card back: yugioh_card_back_single.jpg (421x614)")

def increase_card_quality():
    """Recreate grids with higher quality and larger card sizes"""
    print("Recreating grids with original card dimensions for maximum quality...")
    
    # Use original card dimensions for maximum quality
    CARD_WIDTH = 421   # Original card width from YGOPRODeck
    CARD_HEIGHT = 614  # Original card height from YGOPRODeck
    CARDS_PER_ROW = 10
    CARDS_PER_COL = 7
    
    categories = {
        'classic_commons': 'C:\\GitHub\\YGO-TTS\\images\\classic_commons',
        'classic_rares': 'C:\\GitHub\\YGO-TTS\\images\\classic_rares',
        'classic_super_rares': 'C:\\GitHub\\YGO-TTS\\images\\classic_super_rares',
        'classic_ultra_rares': 'C:\\GitHub\\YGO-TTS\\images\\classic_ultra_rares',
        'classic_spells': 'C:\\GitHub\\YGO-TTS\\images\\classic_spells',
        'classic_traps': 'C:\\GitHub\\YGO-TTS\\images\\classic_traps'
    }
    
    for category_name, images_dir in categories.items():
        if not os.path.exists(images_dir):
            print(f"Skipping {category_name} - images directory not found")
            continue
            
        print(f"Processing {category_name}...")
        
        # Get CSV file to maintain card order
        csv_file = f"C:\\GitHub\\YGO-TTS\\data\\{category_name}.csv"
        if not os.path.exists(csv_file):
            continue
            
        import pandas as pd
        df = pd.read_csv(csv_file)
        
        # Get available images in correct order
        available_images = []
        for index, row in df.iterrows():
            card_id = row['ID']
            image_path = os.path.join(images_dir, f"{card_id}.jpg")
            if os.path.exists(image_path):
                available_images.append(image_path)
        
        if not available_images:
            continue
            
        # Calculate grids needed
        import math
        cards_per_grid = CARDS_PER_ROW * CARDS_PER_COL
        num_grids = math.ceil(len(available_images) / cards_per_grid)
        
        # Create output directory
        grids_dir = f"C:\\GitHub\\YGO-TTS-Assets\\grids\\{category_name}"
        os.makedirs(grids_dir, exist_ok=True)
        
        # Create each grid
        for grid_num in range(num_grids):
            start_idx = grid_num * cards_per_grid
            end_idx = min(start_idx + cards_per_grid, len(available_images))
            grid_images = available_images[start_idx:end_idx]
            
            # Create grid
            grid_width = CARDS_PER_ROW * CARD_WIDTH
            grid_height = CARDS_PER_COL * CARD_HEIGHT
            grid_image = Image.new('RGB', (grid_width, grid_height), 'white')
            
            cards_placed = 0
            for i, image_path in enumerate(grid_images):
                try:
                    # Open card image - keep original size for maximum quality
                    card_image = Image.open(image_path)
                    # Only resize if not already the target size
                    if card_image.size != (CARD_WIDTH, CARD_HEIGHT):
                        card_image = card_image.resize((CARD_WIDTH, CARD_HEIGHT), Image.LANCZOS)
                    
                    # Calculate position in grid
                    row = i // CARDS_PER_ROW
                    col = i % CARDS_PER_ROW
                    x = col * CARD_WIDTH
                    y = row * CARD_HEIGHT
                    
                    # Paste card into grid
                    grid_image.paste(card_image, (x, y))
                    cards_placed += 1
                    
                except Exception as e:
                    print(f"Error processing {image_path}: {e}")
            
            # Save grid with maximum quality
            output_path = os.path.join(grids_dir, f"{category_name}_grid_{grid_num + 1}.jpg")
            grid_image.save(output_path, 'JPEG', quality=100, optimize=False, subsampling=0)
            print(f"Created high-quality grid: {category_name}_grid_{grid_num + 1}.jpg ({cards_placed} cards)")

def update_tts_json_files():
    """Update TTS JSON files with new card back URL and dimensions"""
    decks_dir = "C:\\GitHub\\YGO-TTS-Assets\\decks"
    
    for filename in os.listdir(decks_dir):
        if filename.endswith('.json') and filename != 'test_deck_minimal.json':
            deck_file = os.path.join(decks_dir, filename)
            
            with open(deck_file, 'r', encoding='utf-8') as f:
                import json
                deck_data = json.load(f)
            
            # Update CustomDeck settings
            if 'ObjectStates' in deck_data:
                for obj in deck_data['ObjectStates']:
                    if 'CustomDeck' in obj:
                        for deck_id, deck_info in obj['CustomDeck'].items():
                            # Update BackURL to single card back
                            deck_info['BackURL'] = "https://raw.githubusercontent.com/SjoukeHoekstra/YGO-TTS-Assets/main/card-backs/yugioh_card_back_single.jpg"
                            # Update dimensions for higher quality
                            deck_info['NumWidth'] = 10
                            deck_info['NumHeight'] = 7
            
            # Save updated file
            with open(deck_file, 'w', encoding='utf-8') as f:
                json.dump(deck_data, f, indent=2, ensure_ascii=False)
            
            print(f"Updated {filename}")

def main():
    print("Fixing card back and quality issues...")
    
    # Step 1: Create single card back
    create_single_card_back()
    
    # Step 2: Recreate grids with higher quality
    increase_card_quality()
    
    # Step 3: Update JSON files
    update_tts_json_files()
    
    print("\nAll fixes complete!")
    print("- Single card back created (not grid)")
    print("- Maximum quality: original size (421x614 per card, 4210x4298 grids)")  
    print("- TTS JSON files updated")

if __name__ == "__main__":
    main()