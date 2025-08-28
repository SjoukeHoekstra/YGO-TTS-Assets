import json
import os

def fix_tts_deck_urls(deck_file):
    """Fix GitHub URLs in TTS deck JSON files"""
    with open(deck_file, 'r', encoding='utf-8') as f:
        deck_data = json.load(f)
    
    # Determine category from filename
    filename = os.path.basename(deck_file)
    if 'commons' in filename:
        category = 'classic_commons'
    elif 'rares' in filename and 'super' not in filename and 'ultra' not in filename:
        category = 'classic_rares'  
    elif 'super_rares' in filename:
        category = 'classic_super_rares'
    elif 'ultra_rares' in filename:
        category = 'classic_ultra_rares'
    elif 'spells' in filename:
        category = 'classic_spells'
    elif 'traps' in filename:
        category = 'classic_traps'
    else:
        print(f"Unknown category for {filename}")
        return
    
    # Update CustomDeck URLs
    if 'ObjectStates' in deck_data:
        for obj in deck_data['ObjectStates']:
            if 'CustomDeck' in obj:
                for deck_id, deck_info in obj['CustomDeck'].items():
                    # Update FaceURL to correct subdirectory path
                    if 'FaceURL' in deck_info:
                        old_url = deck_info['FaceURL']
                        # Extract grid number from the old URL
                        if 'grid_' in old_url:
                            grid_part = old_url.split('grid_')[-1]  # Gets "1.jpg", "2.jpg", etc.
                            grid_num = grid_part.split('.')[0]  # Gets "1", "2", etc.
                            
                            # Create correct URL with subdirectory
                            new_url = f"https://raw.githubusercontent.com/SjoukeHoekstra/YGO-TTS-Assets/main/grids/{category}/{category}_grid_{grid_num}.jpg"
                            deck_info['FaceURL'] = new_url
                            print(f"Fixed URL: {category}_grid_{grid_num}.jpg")
    
    # Save updated file
    with open(deck_file, 'w', encoding='utf-8') as f:
        json.dump(deck_data, f, indent=2, ensure_ascii=False)
    
    print(f"Fixed URLs in {os.path.basename(deck_file)}")

def main():
    # Fix all deck files
    decks_dir = "C:\\GitHub\\YGO-TTS-Assets\\decks"
    for filename in os.listdir(decks_dir):
        if filename.endswith('.json'):
            deck_file = os.path.join(decks_dir, filename)
            fix_tts_deck_urls(deck_file)
    
    print(f"\nAll deck files fixed with correct subdirectory paths!")

if __name__ == "__main__":
    main()