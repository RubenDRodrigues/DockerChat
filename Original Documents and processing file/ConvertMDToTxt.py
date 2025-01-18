import os
import markdown
import json
from bs4 import BeautifulSoup

def convert_md_to_text(md_content):
    html_content = markdown.markdown(md_content)
    soup = BeautifulSoup(html_content, "html.parser")
    return soup.get_text(separator="\n").strip()

def extract_metadata_and_content(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    file_name = os.path.basename(file_path)
    
    doc_id = file_name.replace('.', '_')  
    doc_id = doc_id.lstrip('_')  

    uri = f"gs://docu_storage/txt_files/{file_name.replace('.md', '')}.txt"  
    metadata = {
        "id": doc_id,
        "jsonData": json.dumps({
            "title": f"{file_name}",
            "description": f"Description for {file_name}",
            "keywords": "docker, tutorial, docker container, docker application"
        }),
        "content": {
            "mimeType": "text/plain",  
            "uri": uri  
        }
    }
    
    plain_text = convert_md_to_text(md_content)
    
    return metadata, plain_text

# Function to write metadata to a JSONL file
def write_metadata_to_jsonl(metadata_list, output_file):
    """Write metadata to a JSONL file."""
    with open(output_file, 'w', encoding='utf-8') as f:
        for metadata in metadata_list:
            f.write(json.dumps(metadata) + '\n')

# Function to write text content to a .txt file
def write_text_to_file(content, output_file):
    """Write content to a text file."""
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)

#  Function to process all Markdown files and generate JSONL and .txt files
def process_markdown_files(input_folder, output_jsonl, output_txt_folder):
    """Process all Markdown files, generate JSONL metadata and .txt files."""
    metadata_list = []
    
    os.makedirs(output_txt_folder, exist_ok=True)
    
    for root, _, files in os.walk(input_folder):
        for file in files:
            if file.endswith(".md"):
                file_path = os.path.join(root, file)
                
                metadata, plain_text = extract_metadata_and_content(file_path)
                
                metadata_list.append(metadata)
                
                txt_file_path = os.path.join(output_txt_folder, f"{file.replace('.md', '.txt')}")
                write_text_to_file(plain_text, txt_file_path)
    
    write_metadata_to_jsonl(metadata_list, output_jsonl)

input_folder = "docs-main"  # Path to the folder with .md files
output_jsonl = 'output/metadata.jsonl'       # Path to the output JSONL file
output_txt_folder = 'output/txt_files'  # Folder to save the .txt files

process_markdown_files(input_folder, output_jsonl, output_txt_folder)

print("Processing complete. Metadata saved to:", output_jsonl)
print("Text files saved to:", output_txt_folder)
