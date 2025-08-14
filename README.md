# DOW2: Retribution - GOG Launcher

A modern Python Flet application for launching Warhammer 40k: Dawn of War 2 - Retribution with GOG DLL injection capabilities.
![Preview](asset/preview.jpg)
## Features

- **Modern Warhammer 40k Theme**: Dark aesthetic with gold and red accents
- **Game Cover Art**: Includes official DOW2: Retribution cover image
- **Fixed Window Size**: Optimized 400x300 window for consistent UI scaling
- **Game Path Management**: Save and validate your DOW2 installation directory
- **DLL Injection**: Switch between offline skirmish and GOG version modes
- **Auto-launch**: Automatically launches the game after DLL injection

## Installation

1. **Install Python 3.8+** if you haven't already
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Run the launcher**:
   ```bash
   python main.py
   ```

2. **Set Game Path**: 
   - Enter the directory path where `DOW2.exe` is located
   - Click "Save Path" to store the location

3. **Choose Mode**:
   - **Play Offline Skirmish**: Injects DLLs from `GOGEmuDLL/` folder and launches the game
   - **Switch to GOG Version**: Injects DLLs from `OriginalGOGDLL/` folder

## File Structure

```
RETLauncher/
├── main.py                 # Main application file
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── GOGEmuDLL/            # DLLs for offline skirmish mode
│   └── Galaxy.dll
└── OriginalGOGDLL/       # Original GOG DLLs
    └── Galaxy.dll
```

## DLL Injection System

The launcher automatically handles DLL injection by copying the appropriate files from the source folders to your game directory. This allows you to:

- **Offline Mode**: Use modified DLLs for offline skirmish gameplay
- **GOG Mode**: Restore original GOG DLLs for online functionality

### How It Works

1. **Smart DLL Management**: Automatically detects and removes existing DLLs before injection
2. **Clean Injection**: Copies new DLLs from source folders to your game directory
3. **Source Preservation**: Original DLL files remain in source folders for future use
4. **Mode Switching**: Switch between offline and GOG modes as needed

## Notes

- The launcher saves your game path in `launcher_config.txt`
- DLL injection requires write permissions to your game directory
- Make sure the `GOGEmuDLL` and `OriginalGOGDLL` folders contain the correct DLL files
- The application window is fixed at 400x300 pixels for optimal UI scaling

## Troubleshooting

- **"Invalid game path"**: Ensure the path contains `DOW2.exe`
- **"DLL not found"**: Verify that DLL files exist in the respective folders
- **Permission errors**: Run as administrator if needed for DLL injection

