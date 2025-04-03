import re
import pandas as pd
from io import BytesIO

def parse_text_from_string(text):
    """Parse text into structured dialogue data."""
    lines = text.strip().split('\n')
    parsed_data = []
    
    for line in lines:
        if not line.strip():
            continue
            
        # Check if line follows the format "Character (emotion): Dialogue"
        match = re.match(r"(.*?)(?:\s*\((.*?)\))?\s*:\s*(.*)", line)
        
        if match:
            character = match.group(1).strip()
            emotion = match.group(2).strip() if match.group(2) else None
            dialogue = match.group(3).strip()
            
            parsed_data.append({
                "character": character,
                "emotion": emotion,
                "dialogue": dialogue
            })
        else:
            # If line doesn't match the format, treat it as narration
            parsed_data.append({
                "character": "Narrator",
                "emotion": None,
                "dialogue": line.strip()
            })
    
    return parsed_data

def parse_text_from_file(file):
    """Parse text from uploaded file."""
    text = file.getvalue().decode('utf-8')
    return parse_text_from_string(text)

def export_dialogue_to_csv(parsed_data):
    """Export parsed dialogue data to CSV."""
    if not parsed_data:
        return None
    
    df = pd.DataFrame(parsed_data)
    csv_buffer = BytesIO()
    df.to_csv(csv_buffer, index=False)
    csv_buffer.seek(0)
    
    return csv_buffer

def import_dialogue_from_csv(csv_file):
    """Import dialogue data from CSV file."""
    try:
        df = pd.read_csv(csv_file)
        return df.to_dict('records')
    except Exception as e:
        raise ValueError(f"Error importing CSV: {str(e)}")

def extract_unique_characters(parsed_data):
    """Extract unique character names from parsed data."""
    return list(set([item.get("character", "Narrator") for item in parsed_data]))

def validate_dialogue_format(parsed_data):
    """Validate the format of parsed dialogue data."""
    if not parsed_data or not isinstance(parsed_data, list):
        return False, "No dialogue data found."
    
    for idx, item in enumerate(parsed_data):
        if not isinstance(item, dict):
            return False, f"Item at index {idx} is not a dictionary."
        
        if "character" not in item or "dialogue" not in item:
            return False, f"Item at index {idx} is missing required fields."
    
    return True, "Validation successful."
