import os
from src import schema_to_excel
from src import instance_to_excel
from src import excel_to_instance

# Default directories
INPUT_DIR = "files/input"
OUTPUT_DIR = "files/output"

def process_schema_folder(input_dir, output_dir):
    for filename in os.listdir(input_dir):
        if filename.endswith(".json"):
            input_path = os.path.join(input_dir, filename)
            output_name = filename.replace(".json", "_mapping.xlsx")
            output_path = os.path.join(output_dir, output_name)
            schema_to_excel.json_schema_to_excel(input_path, output_path)
            print(f"Processed schema: {filename}")

def process_instance_folder(input_dir, output_dir):
    for filename in os.listdir(input_dir):
        if filename.endswith(".json"):
            input_path = os.path.join(input_dir, filename)
            output_name = filename.replace(".json", "_mapping.xlsx")
            output_path = os.path.join(output_dir, output_name)
            instance_to_excel.instance_to_excel(input_path, output_path)
            print(f"Processed instance: {filename}")

def process_excel_folder(input_dir, output_dir):
    for filename in os.listdir(input_dir):
        if filename.endswith(".xlsx"):
            input_path = os.path.join(input_dir, filename)
            output_name = filename.replace(".xlsx", "_instance.json")
            output_path = os.path.join(output_dir, output_name)
            excel_to_instance.excel_to_instance(input_path, output_path)
            print(f"Processed Excel: {filename}")

def main():
    print("Choose an action:")
    print("1 - Convert JSON schema(s) to Excel")
    print("2 - Convert JSON instance(s) to Excel")
    print("3 - Convert Excel(s) to JSON instance(s)")
    choice = input("Enter 1, 2, or 3: ").strip()

    input_dir = input(f"Enter input folder path [{INPUT_DIR}]: ").strip() or INPUT_DIR
    output_dir = input(f"Enter output folder path [{OUTPUT_DIR}]: ").strip() or OUTPUT_DIR
    os.makedirs(output_dir, exist_ok=True)

    if choice == "1":
        process_schema_folder(input_dir, output_dir)
    elif choice == "2":
        process_instance_folder(input_dir, output_dir)
    elif choice == "3":
        process_excel_folder(input_dir, output_dir)
    else:
        print("Invalid choice!")

if __name__ == "__main__":
    main()
