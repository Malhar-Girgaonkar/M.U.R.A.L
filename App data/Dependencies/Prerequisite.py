import subprocess

modules_to_install = [
    "turtle",
    "CTkMessagebox",
    "customtkinter",
    "tkinter",
    "PIL",
    "time",
    "tqdm",
    "os",
    "shutil",
    "tensorflow",
    "numpy"
]

# Function to check and install missing modules
def install_missing_modules(module_name):
    try:
        __import__(module_name)
    except ImportError:
        print(f"Module {module_name} not found. Installing...")
        subprocess.run(["pip", "install", module_name])

# Install each module
for module_name in modules_to_install:
    print(f"Inatalling {module_name}")
    install_missing_modules(module_name)
    print(f"Module :{module_name}: Installed ")
    print()

print(f"Inatallation complete")
