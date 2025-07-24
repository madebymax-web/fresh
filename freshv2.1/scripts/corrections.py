import json

def load_corrections(correction_file):
    with open(correction_file, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_corrections(correction_file, corrections):
    with open(correction_file, 'w', encoding='utf-8') as f:
        json.dump(corrections, f, indent=4)

def apply_corrections(text, corrections):
    for wrong, right in corrections.items():
        text = text.replace(wrong, right)
    return text

def fuzzy_suggest_corrections(lines_dict, fuzzy_dict):
    from difflib import get_close_matches
    suggestions = []
    for idx, line in lines_dict.items():
        words = line.split()
        for word in words:
            matches = get_close_matches(word, fuzzy_dict.keys(), n=3, cutoff=0.75)
            for match in matches:
                suggestions.append((idx, match, fuzzy_dict[match], line))
    return suggestions
