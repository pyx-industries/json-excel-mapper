import json
import openpyxl

def resolve_ref(ref, root_schema):
    """Resolve local $ref within the schema"""
    if not ref.startswith("#/"):
        raise ValueError(f"Only local refs are supported: {ref}")
    parts = ref.lstrip("#/").split("/")
    node = root_schema
    for p in parts:
        node = node[p]
    return node

def is_writable(schema):
    schema_type = schema.get("type")
    if schema_type in ["string", "number", "boolean", "integer"]:
        return True
    if schema_type == "array":
        item_type = schema.get("items", {}).get("type")
        return item_type in ["string", "number", "boolean", "integer"]
    return False

def extract_fields(schema, root_schema=None, path="", visited_refs=None, array_level=0):
    if root_schema is None:
        root_schema = schema
    if visited_refs is None:
        visited_refs = set()

    fields = []

    # Handle $ref first
    if "$ref" in schema:
        ref_path = schema["$ref"]
        if ref_path in visited_refs:
            fields.append({
                "Path": path,
                "Type": "ref",
                "Required": "Yes" if schema.get("minItems", 0) > 0 else "No",
                "Description": f"Reference to {ref_path}",
                "Ref": ref_path,
                "Writable": "No",
                "Data": schema.get("default", "")
            })
            return fields
        visited_refs.add(ref_path)
        ref_schema = resolve_ref(ref_path, root_schema)
        fields.extend(extract_fields(ref_schema, root_schema, path, visited_refs, array_level))
        return fields

    schema_type = schema.get("type")

    if schema_type == "object" and "properties" in schema:
        required = schema.get("required", [])
        for prop, subschema in schema["properties"].items():
            prop_path = f"{path}.{prop}" if path else prop
            field = {
                "Path": prop_path,
                "Type": subschema.get("type", "object") if "$ref" not in subschema else "ref",
                "Required": "Yes" if prop in required else "No",
                "Description": subschema.get("description", ""),
                "Ref": subschema.get("$ref", ""),
                "Writable": "Yes" if is_writable(subschema) else "No",
                "Data": subschema.get("default", "")
            }
            fields.append(field)
            fields.extend(extract_fields(subschema, root_schema, prop_path, visited_refs, array_level))

    elif schema_type == "array" and "items" in schema:
        # Display array at current path
        item_schema = schema["items"]
        field = {
            "Path": path if path else "root",
            "Type": "array",
            "Required": "Yes" if schema.get("minItems", 0) > 0 else "No",
            "Description": schema.get("description", ""),
            "Ref": item_schema.get("$ref", ""),
            "Writable": "No",  # array structure itself is not directly writable
            "Data": schema.get("default", "")
        }
        # fields.append(field)
        # Recurse into items using [0] notation for this level
        item_path = f"{path}[0]" if path else "[0]"
        fields.extend(extract_fields(item_schema, root_schema, item_path, visited_refs, array_level + 1))

    return fields

def schema_to_excel(schema_file, excel_file):
    with open(schema_file, "r", encoding="utf-8") as f:
        schema = json.load(f)

    fields = extract_fields(schema)

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Schema Mapping"
    headers = ["Path", "Type", "Required", "Description", "Ref", "Writable", "Data", "Data 2", "Data 3"]
    ws.append(headers)

    for field in fields:
        row = []
        for h in headers[:-2] + ["", ""]:
            val = field.get(h, "")
            if isinstance(val, (dict, list)):  
                val = json.dumps(val)   # stringify complex defaults
            row.append(val)
        ws.append(row)

    wb.save(excel_file)
    print(f"Excel saved to {excel_file}")

