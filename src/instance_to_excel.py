import json
import openpyxl

def is_primitive(value):
    return isinstance(value, (str, int, float, bool))

def extract_instance_fields(data, path=""):
    """
    Flatten JSON for Excel:
    - Keep primitive arrays (including multi-dimensional) intact
    - Recurse into dicts
    - Recurse into arrays only if they contain objects
    """
    fields = []

    if isinstance(data, dict):
        for key, value in data.items():
            prop_path = f"{path}.{key}" if path else key
            if is_primitive(value):
                fields.append({
                    "Path": prop_path,
                    "Type": type(value).__name__,
                    "Value": value,
                })
            elif isinstance(value, list):
                # Check if list contains objects
                if all(is_primitive(i) or isinstance(i, list) for i in value):
                    # Primitive or nested array → keep as-is
                    fields.append({
                        "Path": prop_path,
                        "Type": "array",
                        "Value": value,
                    })
                else:
                    # Contains objects → recurse into each object
                    for i, item in enumerate(value):
                        item_path = f"{prop_path}[{i}]"
                        fields.extend(extract_instance_fields(item, item_path))
            else:
                # Recurse into dict
                fields.extend(extract_instance_fields(value, prop_path))

    elif isinstance(data, list):
        # Handle top-level list
        if all(is_primitive(i) or isinstance(i, list) for i in data):
            fields.append({
                "Path": path,
                "Type": "array",
                "Value": data,
            })
        else:
            for i, item in enumerate(data):
                item_path = f"{path}[{i}]"
                fields.extend(extract_instance_fields(item, item_path))

    return fields

def instance_to_excel(instance_file, excel_file):
    with open(instance_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    fields = extract_instance_fields(data)

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Instance Mapping"
    headers = ["Path", "Type", "Value"]
    ws.append(headers)

    for field in fields:
        row = []
        for h in headers:
            val = field.get(h, "")
            if isinstance(val, (dict, list)):  
                val = json.dumps(val)   # stringify complex defaults
            row.append(val)
        ws.append(row)

    wb.save(excel_file)
    print(f"Excel saved to {excel_file}")

# Example usage
# instance_to_excel("../files/input/0.6.1/sample_instance/DigitalFacilityRecord_instance.json", "../files/output/0.6.1/sample_instance/DigitalFacilityRecord_instance_mapping.xlsx")
