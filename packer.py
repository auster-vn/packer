import os
import streamlit as st
from tkinter import Tk
from tkinter.filedialog import askdirectory

def select_folder():
    """
    Opens a folder selection dialog using tkinter.
    Returns the selected folder path or an empty string if canceled.
    """
    root = Tk()
    root.withdraw()  # Hide the root window
    folder_path = askdirectory(title="Select a Repository Folder")
    root.destroy()
    return folder_path

def pack_repository(repo_path, output_file, ignore_extensions=None, ignore_dirs=None):
    """
    Packs the contents of a repository into a single AI-friendly text file.

    Args:
        repo_path (str): Path to the repository root.
        output_file (str): Path to the output text file.
        ignore_extensions (list): List of file extensions to ignore (e.g., ['.exe', '.png']).
        ignore_dirs (list): List of directory names to ignore (e.g., ['.git', 'node_modules']).

    Returns:
        str: Path to the packed repository file.
    """
    if not os.path.exists(repo_path):
        raise FileNotFoundError(f"Repository not found: {repo_path}")

    ignore_extensions = ignore_extensions or []
    ignore_dirs = ignore_dirs or []

    with open(output_file, 'w', encoding='utf-8') as out_file:
        for root, dirs, files in os.walk(repo_path):
            # Skip ignored directories
            dirs[:] = [d for d in dirs if d not in ignore_dirs]

            for file in files:
                file_path = os.path.join(root, file)

                # Skip files based on extension
                if any(file.endswith(ext) for ext in ignore_extensions):
                    continue

                # Read and write file content
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()

                    relative_path = os.path.relpath(file_path, repo_path)
                    out_file.write(f"\n--- FILE: {relative_path} ---\n")
                    out_file.write(content)
                    out_file.write("\n")
                except Exception as e:
                    st.warning(f"Skipped {file_path}: {e}")
    
    return output_file

# Streamlit App Interface
st.title("Repository Packer for AI-friendly Text Files")

# Initialize session state for repository path
if "repo_path" not in st.session_state:
    st.session_state.repo_path = ""

# Folder Browser Button
if st.button("Browse for Repository Folder"):
    repo_path = select_folder()
    if repo_path:
        st.session_state.repo_path = repo_path
        st.success(f"Selected Repository: {repo_path}")
    else:
        st.warning("No folder selected.")

# Display the selected path
st.write(f"Selected folder: {st.session_state.repo_path}")

# Fallback Manual Input
repo_path = st.text_input("Or enter the repository path manually:", st.session_state.repo_path)

# Output File Path Input
output_file = st.text_input("Enter the path for the output file (default: packed_repo.txt):", "packed_repo.txt")

# Ignore Extensions and Directories
ignore_extensions = st.text_area(
    "Enter file extensions to ignore (comma-separated, e.g., .exe, .png):",
    value=".exe, .png, .jpg, .pdf, .zip, .tar"
)
ignore_dirs = st.text_area(
    "Enter directories to ignore (comma-separated, e.g., .git, node_modules):",
    value=".git, node_modules, __pycache__"
)

# Parse Inputs
ignore_extensions = [ext.strip() for ext in ignore_extensions.split(",")]
ignore_dirs = [d.strip() for d in ignore_dirs.split(",")]

# Run Packer
if st.button("Pack Repository"):
    if os.path.isdir(repo_path):
        try:
            packed_file = pack_repository(repo_path, output_file, ignore_extensions, ignore_dirs)
            st.success(f"Repository packed successfully into: {packed_file}")
        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.error("Please select a valid repository folder or enter a valid path.")

