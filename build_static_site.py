import os
import shutil
import re

def copy_directory(source_dir, destination_dir):
    """
    Copy the entire contents of source_dir to destination_dir.
    If destination_dir exists, its contents will be overwritten.
    """
    if not os.path.exists(source_dir):
        print(f"Source directory '{source_dir}' does not exist.")
        return
    if os.path.exists(destination_dir):
        shutil.rmtree(destination_dir)
    shutil.copytree(source_dir, destination_dir)
    print(f"Copied directory: {source_dir} -> {destination_dir}")

def copy_and_convert_php_files_to_html(source_folder, destination_folder):
    """
    Copy all .php files from the source folder to the destination folder,
    changing their extension to .html.
    
    :param source_folder: Path to the source folder (e.g., 'views/')
    :param destination_folder: Path to the destination folder (e.g., root folder './')
    """
    if not os.path.exists(source_folder):
        print(f"Source folder '{source_folder}' does not exist.")
        return

    # Ensure the destination folder exists
    os.makedirs(destination_folder, exist_ok=True)

    # Iterate through all files in the source folder
    for filename in os.listdir(source_folder):
        if filename.endswith(".php"):
            # Construct full file paths
            source_file = os.path.join(source_folder, filename)
            new_filename = os.path.splitext(filename)[0] + ".html"
            destination_file = os.path.join(destination_folder, new_filename)

            # Copy and rename the file
            shutil.copy(source_file, destination_file)
            print(f"Copied and converted: {source_file} -> {destination_file}")

def replace_php_include_with_html_content(html_file_path, include_pattern, component_path):
    """
    Replace occurrences of a PHP include pattern in the given HTML file
    with the content of the specified component HTML file.

    :param html_file_path: Path to the .html file to process
    :param include_pattern: The PHP include string to search for (e.g., "<?php include 'components/head.php'; ?>")
    :param component_path: The full path to the component HTML file to insert (e.g., "./views/components/head.html")
    """
    # Read the content of the component HTML file
    if not os.path.exists(component_path):
        print(f"{component_path} not found.")
        return

    with open(component_path, "r", encoding="utf-8") as f:
        component_content = f.read()

    # Read the content of the HTML file
    with open(html_file_path, "r", encoding="utf-8") as f:
        html_content = f.read()

    # Replace the PHP include with the content of the component HTML file
    new_content = html_content.replace(include_pattern, component_content)

    # Write the new content back to the HTML file
    with open(html_file_path, "w", encoding="utf-8") as f:
        f.write(new_content)
    print(f"Processed: {html_file_path}")

def replace_file_content(html_file_path, component_path):
    """
    Replace all content in the given HTML file with the content of the specified component HTML file.

    :param html_file_path: Path to the .html file to overwrite
    :param component_path: The full path to the component HTML file to use as replacement
    """
    if not os.path.exists(component_path):
        print(f"{component_path} not found.")
        return

    with open(component_path, "r", encoding="utf-8") as f:
        component_content = f.read()

    with open(html_file_path, "w", encoding="utf-8") as f:
        f.write(component_content)
    print(f"Replaced all content in {html_file_path} with {component_path}")

def rewrite_any_relative_paths(html_file_path):
    """
    Rewrite any relative paths in href or src attributes to be fit html files.
    :param html_file_path: Path to the .html file to process
    """
    with open(html_file_path, "r", encoding="utf-8") as f:
        html_content = f.read()

    # Pattern: match href or src with any path ending with assets/
    pattern = re.compile(r'((href|src)=["\'])[^"\']*assets/', re.IGNORECASE)
    new_content = pattern.sub(r'\1assets/', html_content)

    # Additionally, replace specific PHP file references with their HTML counterparts
    pattern = re.compile(r'((href|src)=["\'])[^"\']*' + re.escape("index.php") + r'(["\'])', re.IGNORECASE)
    new_content = pattern.sub(r'\1' + "index.html" + r'\3', new_content)
    pattern = re.compile(r'((href|src)=["\'])[^"\']*' + re.escape("controllers/contact_controller.php") + r'(["\'])', re.IGNORECASE)
    new_content = pattern.sub(r'\1' + "contact.html" + r'\3', new_content)
    pattern = re.compile(r'((href|src)=["\'])[^"\']*' + re.escape("controllers/form_controller.php") + r'(["\'])', re.IGNORECASE)
    new_content = pattern.sub(r'\1' + "form.html" + r'\3', new_content)
    pattern = re.compile(r'((href|src)=["\'])[^"\']*' + re.escape("controllers/home_controller.php") + r'(["\'])', re.IGNORECASE)
    new_content = pattern.sub(r'\1' + "home.html" + r'\3', new_content)
    pattern = re.compile(r'((href|src)=["\'])[^"\']*' + re.escape("controllers/services_controller.php") + r'(["\'])', re.IGNORECASE)
    new_content = pattern.sub(r'\1' + "services.html" + r'\3', new_content)
    pattern = re.compile(r'((href|src)=["\'])[^"\']*' + re.escape("controllers/who_controller.php") + r'(["\'])', re.IGNORECASE)
    new_content = pattern.sub(r'\1' + "who.html" + r'\3', new_content)

    with open(html_file_path, "w", encoding="utf-8") as f:
        f.write(new_content)
    print(f"Processed: {html_file_path}")

"""
This script generates a static version of a PHP-based website by:
1. Copying all .php files to static site directory and converting them to .html files.
2. Copying the assets directory to the static site directory.
3. Adjusting relative paths in href and src attributes to ensure they work in the static context.
4. Replacing PHP include statements with the actual content of the included files.
"""
if __name__ == "__main__":
    static_site_dir = "./docs"

    # Copy and convert .php files to .html in the static_site directory
    copy_and_convert_php_files_to_html("./", static_site_dir)
    copy_and_convert_php_files_to_html("views", static_site_dir)
    copy_and_convert_php_files_to_html("views/components", static_site_dir)
    copy_directory("assets", os.path.join(static_site_dir, "assets"))

    # Replace the content of index.html with home.html content to set home as the landing page
    replace_file_content(os.path.join(static_site_dir, "index.html"), os.path.join(static_site_dir, "home.html"))

    # Process each .html file in the static_site directory
    for filename in os.listdir(static_site_dir):
        if filename.endswith(".html"):
            html_file_path = os.path.join(static_site_dir, filename)
            replace_php_include_with_html_content(html_file_path, "<?php include 'components/head.php'; ?>", os.path.join(static_site_dir, "head.html"))
            replace_php_include_with_html_content(html_file_path, "<?php include 'components/footer.php'; ?>", os.path.join(static_site_dir, "footer.html"))
            rewrite_any_relative_paths(html_file_path)
