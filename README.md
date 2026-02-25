🚀 OptiWin Pro: Next-Generation Windows Optimizer
OptiWin Pro is a high-performance, modern, and deep system optimization tool developed by ByAlonexTM. It bridges the gap between complex power-user tools like SophiApp and WinUtil by providing a clean, animated, and user-friendly experience.

✨ Key Features
100+ Advanced Tweaks: Deep registry and service optimizations for maximum system efficiency.

Smart Profiles: One-click setups for Gaming (Max FPS), Work/Office, and Essential usage.

Modern UI/UX: Built with a smooth "Waterfall" animation and high-fidelity "Soft" & "Dark" themes.

Safety First: Optional automatic System Restore Point creation before any changes.

Deep Clean Engine: Removes Windows Update residue, temp files, and system junk.

Developer Tools: Toggle WSL, Sandbox, and Hyper-V with a single click.

🛠 Technical Specifications
Language: Python 3.13+

Hardware Detection: Automatically detects and displays your CPU, GPU, and RAM for tailored tweaks.

Multi-Language: Full support for English and Turkish with dynamic switching.

📥 Installation
1. Portable Version (Recommended)
Go to the Releases page.

Download the latest OptiWin.exe.

Run as Administrator and enjoy the performance boost!

2. For Developers
   
   # Clone the repository
git clone https://github.com/byalonex01/OptiWin.git

# Install dependencies
pip install customtkinter psutil darkdetect packaging

# Run the app
python main.py




📦 Building from Source
To create your own standalone executable:

pip install pyinstaller
python -m PyInstaller --noconfirm --onefile --windowed --add-data "lang_pack.py;." --add-data "ui_engine.py;." --add-data "core_optimizer.py;." --collect-all customtkinter --name "OptiWin" main.py


⚠️ Disclaimer
This tool modifies deep system settings. While safety features are included, please create a restore point in the settings menu before use. Use at your own risk.

Developed with precision by ByAlonexTM
