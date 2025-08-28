import json
from datetime import datetime

def create_minimal_test_deck():
    """Create a minimal test deck with just a few cards"""
    
    test_deck = {
        "SaveName": "Yu-Gi-Oh Test Deck",
        "GameMode": "",
        "Date": datetime.now().strftime("%m/%d/%Y %I:%M:%S %p"),
        "Table": "",
        "Sky": "",
        "Note": "Minimal test deck for TTS compatibility",
        "Rules": "",
        "PlayerTurn": "",
        "ObjectStates": [
            {
                "Name": "DeckCustom",
                "Transform": {
                    "posX": 0.0,
                    "posY": 1.0,
                    "posZ": 0.0,
                    "rotX": 0.0,
                    "rotY": 180.0,
                    "rotZ": 180.0,
                    "scaleX": 1.0,
                    "scaleY": 1.0,
                    "scaleZ": 1.0
                },
                "Nickname": "Test Deck",
                "Description": "Test deck with 5 cards",
                "ColorDiffuse": {
                    "r": 0.713235259,
                    "g": 0.713235259,
                    "b": 0.713235259
                },
                "Locked": False,
                "Grid": True,
                "Snap": True,
                "Autoraise": True,
                "Sticky": True,
                "Tooltip": True,
                "GridProjection": False,
                "Hands": False,
                "SidewaysCard": False,
                "DeckIDs": [100, 101, 102, 103, 104],
                "CustomDeck": {
                    "1": {
                        "FaceURL": "https://raw.githubusercontent.com/SjoukeHoekstra/YGO-TTS-Assets/main/grids/classic_ultra_rares/classic_ultra_rares_grid_1.jpg",
                        "BackURL": "https://raw.githubusercontent.com/SjoukeHoekstra/YGO-TTS-Assets/main/card-backs/yugioh_card_back_grid.jpg",
                        "NumWidth": 10,
                        "NumHeight": 7,
                        "BackIsHidden": True,
                        "UniqueBack": False
                    }
                },
                "ContainedObjects": [
                    {
                        "Name": "Card",
                        "Transform": {
                            "posX": 0.0,
                            "posY": 0.0,
                            "posZ": 0.0,
                            "rotX": 0.0,
                            "rotY": 180.0,
                            "rotZ": 180.0,
                            "scaleX": 1.0,
                            "scaleY": 1.0,
                            "scaleZ": 1.0
                        },
                        "Nickname": "Test Card 1",
                        "Description": "First test card",
                        "ColorDiffuse": {
                            "r": 0.713235259,
                            "g": 0.713235259,
                            "b": 0.713235259
                        },
                        "Locked": False,
                        "Grid": True,
                        "Snap": True,
                        "Autoraise": True,
                        "Sticky": True,
                        "Tooltip": True,
                        "GridProjection": False,
                        "Hands": False,
                        "CardID": 100,
                        "SidewaysCard": False,
                        "LuaScript": "",
                        "LuaScriptState": "",
                        "GUID": "abc123"
                    },
                    {
                        "Name": "Card",
                        "Transform": {
                            "posX": 0.0,
                            "posY": 0.0,
                            "rotZ": 0.0,
                            "rotX": 0.0,
                            "rotY": 180.0,
                            "rotZ": 180.0,
                            "scaleX": 1.0,
                            "scaleY": 1.0,
                            "scaleZ": 1.0
                        },
                        "Nickname": "Test Card 2", 
                        "Description": "Second test card",
                        "ColorDiffuse": {
                            "r": 0.713235259,
                            "g": 0.713235259,
                            "b": 0.713235259
                        },
                        "Locked": False,
                        "Grid": True,
                        "Snap": True,
                        "Autoraise": True,
                        "Sticky": True,
                        "Tooltip": True,
                        "GridProjection": False,
                        "Hands": False,
                        "CardID": 101,
                        "SidewaysCard": False,
                        "LuaScript": "",
                        "LuaScriptState": "",
                        "GUID": "def456"
                    }
                ],
                "LuaScript": "",
                "LuaScriptState": "",
                "GUID": "test123"
            }
        ]
    }
    
    # Save test deck
    output_path = "C:\\GitHub\\YGO-TTS-Assets\\decks\\test_deck_minimal.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(test_deck, f, indent=2, ensure_ascii=False)
    
    print(f"Created minimal test deck: {output_path}")

if __name__ == "__main__":
    create_minimal_test_deck()