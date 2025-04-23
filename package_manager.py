import os
import zipfile

REPO_DIR = "repo"
INSTALL_DIR = "installed"
PACKAGE_DB = "packages.txt"

def ensure_dirs():
    os.makedirs(REPO_DIR, exist_ok=True)
    os.makedirs(INSTALL_DIR, exist_ok=True)
    if not os.path.exists(PACKAGE_DB):
        open(PACKAGE_DB, "w").close()

def list_repo_packages():
    return [f for f in os.listdir(REPO_DIR) if f.endswith(".hpkg")]

def list_installed_packages():
    with open(PACKAGE_DB, "r") as f:
        return [line.strip() for line in f.readlines()]

def install_package(package_name):
    package_path = os.path.join(REPO_DIR, package_name)
    if not os.path.exists(package_path):
        print(f"Package '{package_name}' not found in repo.")
        return

    try:
        with zipfile.ZipFile(package_path, "r") as zip_ref:
            folder_name = package_name.replace(".hpkg", "")
            target_dir = os.path.join(INSTALL_DIR, folder_name)
            zip_ref.extractall(target_dir)
        with open(PACKAGE_DB, "a") as f:
            f.write(f"{folder_name}\n")
        print(f"Installed package '{folder_name}' successfully.")
    except zipfile.BadZipFile:
        print("Invalid package file. Make sure it's a valid .hpkg (zip) file.")

def run_package(name):
    path = os.path.join(INSTALL_DIR, name, "main.py")
    if os.path.exists(path):
        os.system(f"python {path}")
    else:
        print(f"Package '{name}' not found or missing main.py")

def help_menu():
    print("Available commands:")
    print("  install <package.hpkg>   - Install a package from repo/")
    print("  list                     - List installed packages")
    print("  repo                     - List packages in repo")
    print("  run <package>            - Run an installed package")
    print("  help                     - Show this help")
    print("  exit                     - Exit the package manager")

def handle_pm_command(cmd):
    parts = cmd.strip().split()
    if not parts:
        return

    if parts[0] == "install":
        if len(parts) < 2:
            print("Usage: install <package.hpkg>")
        else:
            install_package(parts[1])
    elif parts[0] == "list":
        installed = list_installed_packages()
        print("Installed packages:")
        for pkg in installed:
            print("  -", pkg)
    elif parts[0] == "repo":
        repo_pkgs = list_repo_packages()
        print("Packages in repo:")
        for pkg in repo_pkgs:
            print("  -", pkg)
    elif parts[0] == "run":
        if len(parts) < 2:
            print("Usage: run <package>")
        else:
            run_package(parts[1])
    elif parts[0] == "help":
        help_menu()
    elif parts[0] == "exit":
        exit()
    else:
        print("Unknown command. Type 'help'.")

if __name__ == "__main__":
    ensure_dirs()
    print("Hexrail Package Manager (type 'help' for commands)")
    while True:
        try:
            cmd = input("hpm> ")
            handle_pm_command(cmd)
        except KeyboardInterrupt:
            print("\nExiting...")
            break
