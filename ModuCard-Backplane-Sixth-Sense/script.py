import csv
import re

def update_kicad_pinout(csv_file, sch_file, output_file):
    mapping = {}
    
    # 1. Parse the CSV file manually using the csv module
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            if not row:
                continue
            
            row_label = row[0].strip()
            
            # Identify rows containing 'ROW A', 'ROW B', 'ROW C'
            if row_label.startswith('ROW'):
                # Extract the row letter (e.g., 'a', 'b', 'c')
                row_letter = row_label.split(' ')[-1].lower()
                
                # Iterate through signals (columns 1 to 32)
                # The CSV indices 1-32 correspond to pin 1-32
                for i in range(1, 33):
                    if i < len(row):
                        signal = row[i].strip()
                        # Only map if signal is not empty and not 'nan'
                        if signal and signal.lower() != 'nan':
                            mapping[f"{row_letter}{i}"] = signal

    # 2. Read the schematic file
    with open(sch_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # 3. Regex to replace labels
    def replacer(match):
        label_text = match.group(1) # e.g., 'a1'
        key = label_text.lower()
        if key in mapping:
            return f'(label "{mapping[key]}")'
        return match.group(0) # Keep original if no mapping found

    # Regex matches (label "X#") where X is [a-c] and # is number
    new_content = re.sub(r'\(label\s+"([a-cA-C][0-9]+)"\)', replacer, content)

    # 4. Save the updated file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    return f"Successfully updated pinout. Saved to: {output_file}"

# Run the update
result = update_kicad_pinout(
    'ModuCardPinoutCreator(5).xlsx - Sheet1.csv', 
    'Connector.kicad_sch', 
    'Connector_updated.kicad_sch'
)
print(result)
