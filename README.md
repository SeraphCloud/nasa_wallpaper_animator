[Versão em Português](README-pt.md)

# NASA Wallpaper Animator

A Python script that fetches NASA's EPIC (Earth Polychromatic Imaging Camera) images for a specific date and animates them as a dynamic desktop wallpaper on Windows.

## Features

- Fetches high-quality Earth images from NASA's EPIC API
- Downloads and caches images locally for smooth animation
- Animates wallpaper at customizable FPS (default 2 FPS)
- Simple command-line interface
- Educational tool for visualizing Earth's rotation

## Requirements

- Python 3.x
- `requests` library (`pip install requests`)
- Windows OS (uses Windows API for wallpaper setting)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/nasa-wallpaper-animator.git
   cd nasa-wallpaper-animator
   ```

2. Install dependencies:
   ```bash
   pip install requests
   ```

## Usage

Run the script with optional arguments:
```bash
python epic_wallpaper.py [--date YYYY-MM-DD] [--fps FPS] [--cache-dir DIR]
```

Options:
- `--date`: Date in YYYY-MM-DD format (default: 2024-12-07)
- `--fps`: Frames per second (default: 0.5)
- `--cache-dir`: Cache directory (default: cache_nasa)

Examples:
```bash
# Use default date with default settings
python epic_wallpaper.py

# Use a specific date
python epic_wallpaper.py --date 2024-12-08

# Custom FPS and cache directory
python epic_wallpaper.py --date 2024-12-07 --fps 1.0 --cache-dir my_cache
```

The script will:
1. Fetch available images for the specified date
2. Download them to the cache directory
3. Start animating the wallpaper in a loop

Press Ctrl+C to stop the animation.

## Configuration

- Edit `api_test.py` to change the date or FPS variable.
- Images are cached in `cache_nasa/` and cleared on each run.

## API Information

Uses NASA's EPIC API: https://epic.gsfc.nasa.gov/api/natural

- No API key required
- Images are public domain
- Rate limits may apply for frequent requests

## Contributing

Feel free to submit issues or pull requests for improvements.

## License

This project is open source. NASA's EPIC images are in the public domain.