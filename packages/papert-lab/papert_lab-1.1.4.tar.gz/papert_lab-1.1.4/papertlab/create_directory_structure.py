import os
import re

def get_file_content(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        return content
    except Exception as e:
        return f"Error reading file: {str(e)}"

def get_language(file_extension):
    extension_to_language = {
        '.py': 'python',
        '.js': 'javascript',
        '.html': 'html',
        '.scm': 'scheme'
    }
    return extension_to_language.get(file_extension, 'plaintext')

def create_markdown(directory):
    markdown = ""
    
    for root, dirs, files in os.walk(directory):
        level = root.replace(directory, '').count(os.sep)
        indent = '  ' * level
        folder_name = os.path.basename(root)
        
        if level > 0:
            markdown += f"{indent}- {folder_name}\n"
        
        for file in files:
            file_extension = os.path.splitext(file)[1]
            if file_extension in ['.py', '.js', '.html', '.scm']:
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, directory)
                markdown += f"{indent}  - {file}\n"
                markdown += f"{indent}    ## Code\n"
                language = get_language(file_extension)
                markdown += f"{indent}    ```{language}\n"
                content = get_file_content(file_path)
                # Indent each line of the content
                indented_content = '\n'.join(f"{indent}    {line}" for line in content.splitlines())
                markdown += f"{indented_content}\n"
                markdown += f"{indent}    ```\n\n"
    
    return markdown

def main():
    directory = input("Enter the directory path: ")
    output_file = "directory_structure.md"
    
    markdown_content = create_markdown(directory)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(markdown_content)
    
    print(f"Markdown file '{output_file}' has been created successfully.")

if __name__ == "__main__":
    main()