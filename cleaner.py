import os
import shutil
import argparse
import sys
from pathlib import Path


CATEGORIES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".svg", ".bmp"],
    "Documents": [".pdf", ".docx", ".txt", ".xlsx", ".pptx", ".csv", ".doc"],
    "Installers": [".exe", ".msi", ".iso"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
    "Scripts": [".py", ".sh", ".bat", ".js"]
}


def get_default_desktop_path():

    home = Path.home()
    possible_paths = [
        home / "OneDrive" / "Desktop",
        home / "OneDrive" / "Pulpit",
        home / "Desktop",
        home / "Pulpit"
    ]
    for path in possible_paths:
        if path.exists():
            return path
    return None


def organize_directory(target_path):
    path = Path(target_path)

    if not path.exists():
        print(f"Error: Path '{target_path}' does not exist.")
        return

    print(f"--> Scanning directory: {path}")

    files_moved = 0

    try:
        for item in path.iterdir():

            if item.is_dir() or item.name.startswith('.'):
                continue


            if item.suffix.lower() == ".lnk":
                continue

            file_ext = item.suffix.lower()
            moved = False

            for category, extensions in CATEGORIES.items():
                if file_ext in extensions:

                    dest_dir = path / category
                    dest_dir.mkdir(exist_ok=True)

                    try:
                        destination = dest_dir / item.name

                        if destination.exists():
                            print(f"Skipped (duplicate): {item.name}")
                        else:
                            shutil.move(str(item), str(destination))
                            print(f"Moved: {item.name} -> {category}/")
                            files_moved += 1
                        moved = True
                    except Exception as e:
                        print(f"Error moving {item.name}: {e}")
                    break
    except Exception as e:
        print(f"Critical error: {e}")

    print(f"\nDone! Total files organized: {files_moved}")


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Desktop/Folder Cleaner Automation Tool")
    parser.add_argument("--path", type=str, help="Path to the folder you want to clean")

    args = parser.parse_args()


    if args.path:
        target_dir = args.path
    else:

        print("No path provided. Trying to detect Desktop...")
        target_dir = get_default_desktop_path()
        if not target_dir:
            print("Could not detect Desktop. Please use --path argument.")
            sys.exit(1)

    organize_directory(target_dir)