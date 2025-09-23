# 📘 JSON ↔ Excel Mapping Tool

This project converts between **JSON Schema**, **JSON Instances**, and **Excel mappings**.  
It supports three modes:

1. **Schema → Excel**: Generate an Excel mapping from a JSON Schema.  
2. **Instance → Excel**: Flatten a JSON instance into an Excel mapping.  
3. **Excel → Instance**: Reconstruct a JSON instance from an Excel mapping. 

## 📂 Folder Structure
```
json-schema-mapper/
├── files/input/   # put your JSON Schemas here
├── files/output/  # Excel mapping will be saved here
├── src/           # main Python code
└── run.py         # entrypoint
```

## 🚀 Setup & Usage

1. Create and activate a Python virtual environment (recommended):
   ```bash
   python -m venv .venv
   source .venv/bin/activate   # Linux / macOS
   .venv\Scripts\activate      # Windows
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Place your files in `files/input/`, e.g.:
   ```
   files/input/0.6.0/FacilityRecord.json                # schema
   files/input/0.6.0/sample_instance/FacilityRecord_instance.json   # instance
   files/input/0.6.0/sample_instance_excel/FacilityRecord_instance_mapping.xlsx  # excel
   ```

4. Run the tool:
   ```bash
   python run.py
   ```

5. Choose a mode when prompted:
   ```
   Choose an action:
   1 - Convert JSON schema(s) to Excel
   2 - Convert JSON instance(s) to Excel
   3 - Convert Excel(s) to JSON instance(s)
   ```

6. Enter the **input** file or folder path and the **output** folder path (defaults are provided):
   ```
   Enter input file or folder path [files/input]:
   Enter output folder path [files/output]:
   ```

---

## 📂 Input & Output Examples

- **Schema → Excel**  
  ```
  files/input/0.6.0/FacilityRecord.json
  → files/output/0.6.0/FacilityRecord_mapping.xlsx
  ```

- **Instance → Excel**  
  ```
  files/input/0.6.0/sample_instance/FacilityRecord_instance.json
  → files/output/0.6.0/sample_instance/FacilityRecord_instance_mapping.xlsx
  ```

- **Excel → Instance**  
  ```
  files/output/0.6.0/sample_instance/FacilityRecord_instance_mapping.xlsx
  → files/output/0.6.0/sample_instance_json/FacilityRecord_instance_mapping_instance.json
  ```

---

## ✅ Notes

### 📝 Excel Columns for JSON Instance
- `Path` → flattened JSON path (e.g., `root.child[0].name`)  
- `Type` → data type (`string`, `int`, `float`, `bool`, `array`, `dict`)  
- `Value` → actual value or JSON-encoded list/dict  

### 📝 Excel Columns for JSON Schema
- **Path** → JSON path to the field  
- **Type** → field type (string, number, object, array, ref)  
- **Required** → whether the field is mandatory  
- **Description** → schema description  
- **Ref** → `$ref` target if applicable  
- **Writable** → whether you can directly enter a value  
- **Value** → pre-filled with schema defaults if provided  
