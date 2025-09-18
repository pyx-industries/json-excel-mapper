# JSON Schema to Excel Mapper

This tool converts a **JSON Schema** into an **Excel mapping sheet** that you can fill in with values and later convert back to a JSON instance.

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

3. Place your schema in `files/input/`, e.g.:
   ```
   files/input/FacilityRecord.json
   or
   files/input/0.6.0/FacilityRecord.json
   files/input/0.6.0/ProductPassport.json
   ```

4. Update `INPUT_DIR` and `OUTPUT_DIR` in `run.py` accordingly

5. Run the tool:
   ```bash
   python run.py
   ```

6. The Excel mapping will appear in `files/output/` or any `OUTPUT_DIR` you specified, e.g.:
   ```
   files/output/FacilityRecord_mapping.xlsx
   ```

## 📝 Excel Columns
- **Path** → JSON path to the field  
- **Type** → field type (string, number, object, array, ref)  
- **Required** → whether the field is mandatory  
- **Description** → schema description  
- **Ref** → `$ref` target if applicable  
- **Writable** → whether you can directly enter a value  
- **Value** → pre-filled with schema defaults if provided  
