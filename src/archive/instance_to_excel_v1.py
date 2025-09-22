import json
import openpyxl

def is_primitive(value):
    return isinstance(value, (str, int, float, bool))

def extract_instance_fields(data, path=""):
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
            elif isinstance(value, list) and all(is_primitive(i) for i in value):
                fields.append({
                    "Path": prop_path,
                    "Type": "array",
                    "Value": value,
                })
            else:
                # Recurse into objects or non-primitive arrays
                fields.extend(extract_instance_fields(value, prop_path))
    elif isinstance(data, list):
        for i, item in enumerate(data):
            item_path = f"{path}[{i}]"
            if is_primitive(item):
                fields.append({
                    "Path": item_path,
                    "Type": type(item).__name__,
                    "Value": item,
                })
            else:
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
instance_to_excel("../files/input/0.6.0/sample_instance/FacilityRecord_instance.json", "../files/output/0.6.0/sample_instance/FacilityRecord_instance_mapping.xlsx")
