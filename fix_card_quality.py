from PIL import Image
import os

def create_single_card_back():
    """Create a single card back image (not grid)"""
    # Open the official card back
    back_img = Image.open("C:\\GitHub\\YGO-TTS-Assets\\card-backs\\official_yugioh_back.png")
    
    # Convert to RGB and resize to match front card dimensions
    back_img = back_img.convert('RGB')
    back_img = back_img.resize((813, 1185), Image.LANCZOS)  # Match full-size card dimensions
    
    # Save as JPEG for TTS with maximum quality
    back_img.save("C:\\GitHub\\YGO-TTS-Assets\\card-backs\\yugioh_card_back_single.jpg", 
                  'JPEG', quality=100, optimize=False, subsampling=0)
    
    print("Created single card back: yugioh_card_back_single.jpg (813x1185)")

def increase_card_quality():
    """Recreate grids with full-size cards in 5x3 layout"""
    print("Creating 5x3 grids with full-size 813x1185 cards...")
    
    # Use actual full-size card dimensions from downloads
    CARD_WIDTH = 813   # Full resolution card width
    CARD_HEIGHT = 1185 # Full resolution card height
    CARDS_PER_ROW = 5
    CARDS_PER_COL = 3
    
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
        cards_per_grid = CARDS_PER_ROW * CARDS_PER_COL  # 15 cards per grid
        num_grids = math.ceil(len(available_images) / cards_per_grid)
        
        # Create output directory
        grids_dir = f"C:\\GitHub\\YGO-TTS-Assets\\grids\\{category_name}"
        os.makedirs(grids_dir, exist_ok=True)
        
        # Create each grid
        for grid_num in range(num_grids):
            start_idx = grid_num * cards_per_grid
            end_idx = min(start_idx + cards_per_grid, len(available_images))
            grid_images = available_images[start_idx:end_idx]
            
            # Create initial grid at full card size (5x3 * 813x1185 = 4065x3555)
            initial_width = CARDS_PER_ROW * CARD_WIDTH   # 4065 pixels
            initial_height = CARDS_PER_COL * CARD_HEIGHT # 3555 pixels
            grid_image = Image.new('RGB', (initial_width, initial_height), 'white')
            
            cards_placed = 0
            for i, image_path in enumerate(grid_images):
                try:
                    # Open card image at full resolution
                    card_image = Image.open(image_path)
                    # Ensure card is exactly 813x1185 (should already be this size)
                    if card_image.size != (CARD_WIDTH, CARD_HEIGHT):
                        card_image = card_image.resize((CARD_WIDTH, CARD_HEIGHT), Image.LANCZOS)
                    
                    # Calculate position in 5x3 grid
                    row = i // CARDS_PER_ROW
                    col = i % CARDS_PER_ROW
                    x = col * CARD_WIDTH
                    y = row * CARD_HEIGHT
                    
                    # Paste card into grid
                    grid_image.paste(card_image, (x, y))
                    cards_placed += 1
                    
                except Exception as e:
                    print(f"Error processing {image_path}: {e}")
            
            # Scale the grid to maximum size within 4096x4096 while preserving aspect ratio
            original_width = initial_width   # 4065
            original_height = initial_height # 3555
            
            # Calculate scale factor to fit within 4096x4096
            scale_x = 4096 / original_width
            scale_y = 4096 / original_height
            scale_factor = min(scale_x, scale_y)  # Use smaller scale to maintain aspect ratio
            
            # Calculate new dimensions
            new_width = int(original_width * scale_factor)
            new_height = int(original_height * scale_factor)
            
            # Resize grid maintaining aspect ratio
            final_grid = grid_image.resize((new_width, new_height), Image.LANCZOS)
            
            # Save grid with maximum quality
            output_path = os.path.join(grids_dir, f"{category_name}_grid_{grid_num + 1}.jpg")
            final_grid.save(output_path, 'JPEG', quality=100, optimize=False, subsampling=0)
            print(f"Created {new_width}x{new_height} grid: {category_name}_grid_{grid_num + 1}.jpg ({cards_placed} cards)")

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
                            # Update dimensions for 5x3 grid layout
                            deck_info['NumWidth'] = 5
                            deck_info['NumHeight'] = 3
            
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
    print("- Single card back created (813x1185)")
    print("- 5x3 grids with full-size cards scaled to maximum size within 4096x4096")  
    print("- TTS JSON files updated for 5x3 layout")

if __name__ == "__main__":
    main()