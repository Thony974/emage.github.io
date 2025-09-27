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
    Recursively copy all .php files from the source folder (and subfolders) to the destination folder,
    changing their extension to .html. All files are placed directly in the destination folder,
    without preserving the original directory structure.
    """
    for root, _, files in os.walk(source_folder):
        for filename in files:
            if filename.endswith(".php") and filename not in [
                "form_controller.php", 
                "contact_controller.php", 
                "home_controller.php", 
                "services_controller.php", 
                "who_controller.php"]:
                source_file = os.path.join(root, filename)
                new_filename = os.path.splitext(filename)[0] + ".html"
                destination_file = os.path.join(destination_folder, new_filename)
                os.makedirs(destination_folder, exist_ok=True)
                shutil.copy(source_file, destination_file)
                print(f"Copied and converted: {source_file} -> {destination_file}")

def replace_php_include_with_html_content(html_file_path):
    """
    Replace occurrences of specific PHP include patterns in the given HTML file
    with the content of the specified component HTML files.
    :param html_file_path: Path to the .html file to process
    """
    # Read the content of the HTML file
    with open(html_file_path, "r", encoding="utf-8") as f:
        html_content = f.read()

    # Replace the PHP include with the content of the component HTML file
    for pattern, component_path in {
        "<?php include 'components/head.php'; ?>": os.path.join(static_site_dir, "head.html"),
        "<?php include 'components/footer.php'; ?>": os.path.join(static_site_dir, "footer.html")
    }.items():
        if not os.path.exists(component_path):
            print(f"{component_path} not found.")
            continue
        with open(component_path, "r", encoding="utf-8") as f:
            component_content = f.read()
        new_content = html_content.replace(pattern, component_content)
        html_content = new_content

    # Write the new content back to the HTML file
    with open(html_file_path, "w", encoding="utf-8") as f:
        f.write(new_content)
    print(f"Processed: {html_file_path}")

def replace_file_content(html_file_path, component_path):
    """
    Replace the entire content of the given HTML file with the content of the specified component HTML file.
    :param html_file_path: Path to the .html file to process
    :param component_path: The full path to the component HTML file to insert (e.g., "./views/home.html")
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
    Rewrite any relative paths in the given HTML file to ensure they point correctly
    to the static assets and HTML files.
    :param html_file_path: Path to the .html file to process
    """
    with open(html_file_path, "r", encoding="utf-8") as f:
        html_content = f.read()

    # Pattern: match href or src with any path ending with assets/
    pattern = re.compile(r'((href|src)=["\'])[^"\']*assets/', re.IGNORECASE)
    html_content = pattern.sub(r'\1assets/', html_content)

    for php_file, html_file in {
        "index.php": "index.html",
        "controllers/contact_controller.php": "contact.html",
        "controllers/form_controller.php": "form.html",
        "controllers/home_controller.php": "home.html",
        "controllers/services_controller.php": "services.html",
        "controllers/who_controller.php": "who.html",
        "assets": "assets"
    }.items():
        pattern = re.compile(r'((href|src)=["\'])[^"\']*' + re.escape(php_file) + r'(["\'])', re.IGNORECASE)
        new_content = pattern.sub(r'\1' + html_file + r'\3', html_content)
        html_content = new_content

    with open(html_file_path, "w", encoding="utf-8") as f:
        f.write(new_content)
    print(f"Processed: {html_file_path}")

"""
This script generates a static version of a PHP-based website
"""
if __name__ == "__main__":
    # Output directory for the static site
    static_site_dir = "./docs"

    # Copy assets directory to static site directory
    copy_directory("assets", os.path.join(static_site_dir, "assets"))

    # Copy and convert specific PHP files to HTML to the static_site directory
    copy_and_convert_php_files_to_html("./", static_site_dir)

    # Replace the content of index.html with home.html content to set home as the landing page
    replace_file_content(os.path.join(static_site_dir, "index.html"), os.path.join(static_site_dir, "home.html"))

    # Process each .html file in the static_site directory
    for filename in os.listdir(static_site_dir):
        if filename.endswith(".html"):
            html_file_path = os.path.join(static_site_dir, filename)
            replace_php_include_with_html_content(html_file_path)
            rewrite_any_relative_paths(html_file_path)
