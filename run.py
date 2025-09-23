import os
from src import schema_to_excel
from src import instance_to_excel
from src import excel_to_instance

# Default directories
INPUT_DIR = "files/input"
OUTPUT_DIR = "files/output"

def process_schema(input_path, output_path):
    print(f"Processed schema: {os.path.basename(input_path)}")
    schema_to_excel.json_schema_to_excel(input_path, output_path)

def process_instance(input_path, output_path):
    print(f"Processed instance: {os.path.basename(input_path)}")
    instance_to_excel.instance_to_excel(input_path, output_path)

def process_excel(input_path, output_path):
    print(f"Processed Excel: {os.path.basename(input_path)}")
    excel_to_instance.excel_to_instance(input_path, output_path)

def process_folder(input_dir, output_dir, file_ext, processor_func, suffix):
    for filename in os.listdir(input_dir):
        if filename.endswith(file_ext):
            input_path = os.path.join(input_dir, filename)
            output_name = filename.replace(file_ext, suffix)
            output_path = os.path.join(output_dir, output_name)
            processor_func(input_path, output_path)

def main():
    print("Choose an action:")
    print("1 - Convert JSON schema(s) to Excel")
    print("2 - Convert JSON instance(s) to Excel")
    print("3 - Convert Excel(s) to JSON instance(s)")
    choice = input("Enter 1, 2, or 3: ").strip()

    input_path = input(f"Enter input file or folder path [{INPUT_DIR}]: ").strip() or INPUT_DIR
    output_dir = input(f"Enter output folder path [{OUTPUT_DIR}]: ").strip() or OUTPUT_DIR
    os.makedirs(output_dir, exist_ok=True)

    # Determine if input is a file or folder
    if os.path.isfile(input_path):
        filename = os.path.basename(input_path)
        if choice == "1":
            output_name = filename.replace(".json", "_mapping.xlsx")
            process_schema(input_path, os.path.join(output_dir, output_name))
        elif choice == "2":
            output_name = filename.replace(".json", "_mapping.xlsx")
            process_instance(input_path, os.path.join(output_dir, output_name))
        elif choice == "3":
            output_name = filename.replace(".xlsx", "_instance.json")
            process_excel(input_path, os.path.join(output_dir, output_name))
        else:
            print("Invalid choice!")

    elif os.path.isdir(input_path):
        if choice == "1":
            process_folder(input_path, output_dir, ".json", process_schema, "_mapping.xlsx")
        elif choice == "2":
            process_folder(input_path, output_dir, ".json", process_instance, "_mapping.xlsx")
        elif choice == "3":
            process_folder(input_path, output_dir, ".xlsx", process_excel, "_instance.json")
        else:
            print("Invalid choice!")
    else:
        print("Invalid input path!")

if __name__ == "__main__":
    main()
