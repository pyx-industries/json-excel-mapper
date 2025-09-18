import os
from src.schema_to_excel import schema_to_excel

INPUT_DIR = "files/input/0.6.0"
OUTPUT_DIR = "files/output/0.6.0"

def main():
    for filename in os.listdir(INPUT_DIR):
        if filename.endswith(".json"):
            input_path = os.path.join(INPUT_DIR, filename)
            output_name = filename.replace(".json", "_mapping.xlsx")
            output_path = os.path.join(OUTPUT_DIR, output_name)
            schema_to_excel(input_path, output_path)

if __name__ == "__main__":
    main()
