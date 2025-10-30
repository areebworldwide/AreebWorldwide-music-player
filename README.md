# 🎵 AreebWorldwide Music Player - Ultimate Edition

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![CustomTkinter](https://img.shields.io/badge/CustomTkinter-5.0+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Status](https://img.shields.io/badge/Status-Production-brightgreen.svg)

**A feature-rich, modern music player built with Python and CustomTkinter**

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [Shortcuts](#-keyboard-shortcuts) • [Screenshots](#-screenshots)

</div>

---

## 📖 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Installation](#-installation)
- [Usage](#-usage)
- [Keyboard Shortcuts](#-keyboard-shortcuts)
- [File Formats](#-supported-file-formats)
- [Configuration](#-configuration)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [License](#-license)
- [Credits](#-credits)

---

## 🌟 Overview

**AreebWorldwide Music Player** is a sophisticated, feature-packed desktop music player with a beautiful modern UI. Built with Python, it combines powerful functionality with an intuitive interface, offering everything from basic playback to advanced features like equalizers, sleep timers, and lyrics display.

### Why Choose This Player?

✅ **Beautiful UI** - Modern dark theme with animated backgrounds  
✅ **Feature-Rich** - 20+ advanced features built-in  
✅ **Lightweight** - Fast and responsive  
✅ **Cross-Platform** - Works on Windows, macOS, and Linux  
✅ **Smart Playlists** - Advanced playlist management  
✅ **Customizable** - Multiple themes and settings  

---

## 🎯 Features

### 🎵 Core Playback Features

| Feature | Description |
|---------|-------------|
| **Multi-Format Support** | MP3, WAV, FLAC, OGG, M4A |
| **High-Quality Playback** | 44.1kHz stereo audio output |
| **Gapless Playback** | Seamless song transitions |
| **Volume Control** | Precise 0-100% volume adjustment |
| **Playback Speed** | Adjustable from 0.5x to 2.0x |
| **Crossfade** | Smooth transitions between tracks |

### 📋 Playlist Management

- ✅ **Smart Playlists** - Create, save, and manage playlists
- ✅ **Folder Browser** - Load entire music folders recursively
- ✅ **Recent Folders** - Quick access to recently loaded folders
- ✅ **Search & Filter** - Real-time playlist search
- ✅ **Drag & Drop** - Easy song organization
- ✅ **M3U Import/Export** - Standard playlist format support
- ✅ **Playlist History** - Track recently loaded playlists

### ⭐ Advanced Features

#### 1. **Favorites System**
- Mark songs as favorites with one click
- Quick access to all favorite songs
- Load favorites as instant playlist
- Visual star indicators

#### 2. **Play History**
- Automatic tracking of played songs
- Timestamp for each play session
- Quick replay from history
- Last 50 songs stored

#### 3. **Play Queue**
- "Play Next" functionality
- Visual queue manager
- Drag to reorder queue
- Queue persists across sessions

#### 4. **Sleep Timer**
- Auto-stop after set duration
- Quick presets: 15, 30, 45, 60 minutes
- Active timer display
- Notification on expiry

#### 5. **Audio Equalizer**
- Multiple presets (Rock, Pop, Jazz, Classical)
- Bass Boost & Treble Boost
- Custom EQ settings
- Per-playlist EQ memory

#### 6. **Lyrics Viewer**
- Display embedded lyrics (ID3 USLT tags)
- Support for companion .txt files
- Fullscreen lyrics mode
- Auto-scroll with playback

#### 7. **Mini Player Mode**
- Compact always-on-top window
- Essential controls only
- Quick toggle to full mode
- Perfect for multitasking

#### 8. **Audio Visualizer**
- Real-time frequency visualization
- 64-band spectrum analyzer
- Customizable colors
- Smooth animations

#### 9. **Album Art Display**
- Embedded album art extraction
- High-quality rendering
- Rounded corners design
- Default art for untagged files

#### 10. **Smart Features**
- **Shuffle Mode** - Randomized playback
- **Repeat Modes** - Off/One/All
- **Auto-Play Next** - Queue-aware playback
- **Crossfade** - Professional transitions

### 🎨 User Interface

- **3 Premium Themes** - Cyber Blue, Purple Haze, Emerald Night
- **Animated Background** - Dynamic particle effects
- **Responsive Design** - Scales to any window size
- **Dark Mode** - Easy on the eyes
- **Custom Widgets** - Polished controls

### 📊 Information Display

- Song title, artist, album
- Audio quality (bitrate, sample rate, format)
- Current time / Total duration
- Progress bar with seek
- Song count in playlist
- Queue status

---

## 💻 Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Operating System: Windows 10/11, macOS 10.14+, or Linux

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/areebworldwide-music-player.git
cd areebworldwide-music-player
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

**Required Libraries:**

```txt
customtkinter>=5.0.0
pygame>=2.5.0
Pillow>=10.0.0
mutagen>=1.47.0
tkinterdnd2>=0.3.0
```

**Manual Installation:**

```bash
pip install customtkinter pygame Pillow mutagen tkinterdnd2
```

### Step 3: Run the Application

```bash
python music_player.py
```

---

## 🚀 Usage

### Quick Start Guide

#### 1. **Loading Music**

**Method A: Load Folder**
1. Click `📁 Quick Load Folder` button
2. Select your music folder
3. All supported files will be loaded automatically

**Method B: Advanced Browser**
1. Click `📂 Browse` in menu bar
2. Browse recent folders or select new one
3. View song count before loading

**Method C: Add Individual Files**
1. Click `➕ Add Files` button
2. Select one or more music files
3. Files are added to current playlist

#### 2. **Basic Playback**

```
▶ Play/Pause  - Space bar or Play button
⏭ Next Song   - Right arrow or Next button
⏮ Previous    - Left arrow or Previous button
⏹ Stop        - Stop button
```

#### 3. **Creating Playlists**

1. Load your desired songs
2. Click `📋 Playlists` → `💾 Save Current`
3. Enter playlist name
4. Click Save

#### 4. **Using Favorites**

1. Play any song
2. Click the `⭐` button (top right)
3. Access favorites via `⚡ Features` → `⭐ Favorites`

#### 5. **Setting Sleep Timer**

1. Click `⚡ Features` → `⏰ Sleep Timer`
2. Select duration (or use quick presets)
3. Click `Start Timer`
4. Music will stop automatically

#### 6. **Viewing Lyrics**

1. Play a song with embedded lyrics
2. Click `⚡ Features` → `🎤 Show Lyrics`
3. Lyrics window opens automatically

**Note:** For songs without embedded lyrics, create a `.txt` file with the same name as your song in the same folder.

#### 7. **Mini Player Mode**

1. Click `🖼️ Mini Player` in menu bar
2. Main window minimizes
3. Mini player stays on top
4. Click `🔙` to restore full player

---

## ⌨️ Keyboard Shortcuts

### Global Shortcuts

| Shortcut | Action |
|----------|--------|
| `Space` | Play / Pause |
| `→` (Right Arrow) | Next Song |
| `←` (Left Arrow) | Previous Song |
| `Ctrl + O` | Open Folder Browser |
| `Ctrl + F` | Focus Search Box |
| `Ctrl + L` | Show Lyrics |
| `Ctrl + M` | Toggle Mini Player |

### Playlist Shortcuts

| Shortcut | Action |
|----------|--------|
| `Click Song` | Play Song |
| `Right Click` | Song Options (coming soon) |
| `📝 Icon` | Add to Queue |

---

## 📁 Supported File Formats

| Format | Extension | Quality | Notes |
|--------|-----------|---------|-------|
| **MP3** | `.mp3` | Lossy | Most common format |
| **WAV** | `.wav` | Lossless | Uncompressed audio |
| **FLAC** | `.flac` | Lossless | Best quality |
| **OGG** | `.ogg` | Lossy | Open-source format |
| **M4A** | `.m4a` | Lossy/Lossless | AAC format |

### Metadata Support

- **ID3 Tags** - Artist, Title, Album, Year
- **Album Art** - Embedded images (APIC)
- **Lyrics** - Embedded lyrics (USLT)
- **Audio Info** - Bitrate, Sample Rate, Duration

---

## ⚙️ Configuration

### Settings Files

The player creates several configuration files:

```
📁 Project Directory
├── music_player.py          # Main application
├── playlists.json          # Saved playlists
├── favorites.json          # Favorite songs
├── play_history.json       # Play history
├── folder_history.json     # Recent folders
└── player_settings.json    # User settings
```

### Settings File Structure

**player_settings.json:**
```json
{
    "volume": 70,
    "theme": "Cyber Blue",
    "crossfade": false,
    "playback_speed": 1.0
}
```

### Customization

#### Adding Custom Themes

Edit the `ColorTheme` class in `music_player.py`:

```python
"Your Theme Name": {
    "bg_primary": "#1a1a2e",
    "bg_secondary": "#16213e",
    "bg_tertiary": "#0f3460",
    "accent": "#00d9ff",
    "accent_hover": "#00a8cc",
    "text_primary": "#ffffff",
    "text_secondary": "#a0a0a0",
    "error": "#ff4757"
}
```

---

## 🛠️ Troubleshooting

### Common Issues

#### 1. **Application Won't Start**

**Error:** `ModuleNotFoundError: No module named 'customtkinter'`

**Solution:**
```bash
pip install --upgrade customtkinter pygame pillow mutagen
```

#### 2. **No Sound Playback**

**Possible Causes:**
- Audio drivers not installed
- Pygame mixer initialization failed
- File format not supported

**Solutions:**
```bash
# Reinstall pygame
pip uninstall pygame
pip install pygame

# Check audio system (Linux)
sudo apt-get install python3-pygame libsdl2-mixer-2.0-0
```

#### 3. **Album Art Not Showing**

**Causes:**
- No embedded album art in file
- Corrupted image data
- Pillow library issue

**Solutions:**
- Use MP3Tag or similar tool to embed album art
- Ensure image is JPG/PNG format
- Reinstall Pillow: `pip install --upgrade Pillow`

#### 4. **Slow Loading Large Playlists**

**Solutions:**
- Load folders in smaller batches
- Use SSD instead of HDD
- Disable real-time metadata scanning (edit code)

#### 5. **Theme Not Changing**

**Solution:**
- Restart the application after changing theme
- Delete `player_settings.json` to reset

#### 6. **M3U Import Fails**

**Causes:**
- Incorrect file paths in M3U
- Encoding issues

**Solutions:**
- Use absolute paths in M3U files
- Ensure M3U file is UTF-8 encoded

### Debug Mode

Enable debug output by adding this at the start of `music_player.py`:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

---

## 🗺️ Roadmap / Future Enhancements

### Planned Features

- [ ] **Cloud Integration** - Google Drive, Dropbox sync
- [ ] **Online Radio** - Stream internet radio stations
- [ ] **Podcast Support** - Subscribe and play podcasts
- [ ] **Scrobbling** - Last.fm integration
- [ ] **Lyrics Auto-Download** - Fetch lyrics from online databases
- [ ] **Spectrum Analyzer** - Advanced audio visualization
- [ ] **Audio Effects** - Echo, reverb, bass boost
- [ ] **Skin System** - Fully customizable UI skins
- [ ] **Mobile Remote** - Control from smartphone
- [ ] **Discord Rich Presence** - Show what you're listening to
- [ ] **Auto-Tagging** - Automatic metadata fetching
- [ ] **Gapless Playback** - Perfect for live albums
- [ ] **ReplayGain Support** - Volume normalization

### Version History

**v1.2.0** (Current) - Ultimate Edition
- ✅ Added 10 new advanced features
- ✅ Mini player mode
- ✅ Sleep timer
- ✅ Favorites system
- ✅ Play history
- ✅ Queue management
- ✅ Lyrics viewer
- ✅ M3U import/export
- ✅ Playback speed control
- ✅ Audio equalizer
- ✅ Crossfade

**v1.1.0** - Enhanced Edition
- ✅ Playlist management
- ✅ Advanced folder browser
- ✅ Audio visualizer
- ✅ Multiple themes
- ✅ Album art display

**v1.0.0** - Initial Release
- ✅ Basic playback functionality
- ✅ Playlist support
- ✅ Modern UI

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

### How to Contribute

1. **Fork the Repository**
```bash
git fork https://github.com/yourusername/areebworldwide-music-player.git
```

2. **Create a Feature Branch**
```bash
git checkout -b feature/AmazingFeature
```

3. **Commit Your Changes**
```bash
git commit -m 'Add some AmazingFeature'
```

4. **Push to Branch**
```bash
git push origin feature/AmazingFeature
```

5. **Open a Pull Request**

### Contribution Guidelines

- Follow PEP 8 style guide
- Add comments for complex logic
- Test on multiple platforms
- Update README if adding features
- Keep commits atomic and descriptive

### Bug Reports

Found a bug? Please open an issue with:
- Detailed description
- Steps to reproduce
- Expected vs actual behavior
- System information (OS, Python version)
- Error messages/logs

---

## 📜 License

This project is licensed under the **MIT License** - see below for details:

```
MIT License

Copyright (c) 2024 AreebWorldwide

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 👨‍💻 Credits

### Author

**AreebWorldwide**
- GitHub: [@AreebWorldwide](https://github.com/yourusername)
- Email: your.email@example.com

### Built With

- **[CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)** - Modern UI framework
- **[Pygame](https://www.pygame.org/)** - Audio playback engine
- **[Mutagen](https://mutagen.readthedocs.io/)** - Audio metadata handling
- **[Pillow](https://python-pillow.org/)** - Image processing
- **[TkinterDnD2](https://github.com/pmgagne/tkinterdnd2)** - Drag and drop support

### Special Thanks

- Tom Schimansky for CustomTkinter
- Pygame community for audio support
- All contributors and testers

---

## 📞 Support

### Get Help

- **Documentation:** [Wiki](https://github.com/yourusername/areebworldwide-music-player/wiki)
- **Issues:** [GitHub Issues](https://github.com/yourusername/areebworldwide-music-player/issues)
- **Discussions:** [GitHub Discussions](https://github.com/yourusername/areebworldwide-music-player/discussions)

### Community

- **Discord:** [Join our server](https://discord.gg/yourserver)
- **Reddit:** [r/AreebMusicPlayer](https://reddit.com/r/yoursubreddit)

---

## 📸 Screenshots

> **Note:** Add your screenshots here

### Main Interface
```
[Screenshot of main player interface]
```

### Mini Player
```
[Screenshot of mini player mode]
```

### Playlist Manager
```
[Screenshot of playlist manager]
```

### Advanced Features
```
[Screenshot of features menu]
```

---

## 🌟 Star History

If you like this project, please consider giving it a ⭐ on GitHub!

[![Star History Chart](https://api.star-history.com/svg?repos=yourusername/areebworldwide-music-player&type=Date)](https://star-history.com/#yourusername/areebworldwide-music-player&Date)

---

## 📊 Project Stats

![GitHub repo size](https://img.shields.io/github/repo-size/yourusername/areebworldwide-music-player)
![GitHub code size](https://img.shields.io/github/languages/code-size/yourusername/areebworldwide-music-player)
![Lines of code](https://img.shields.io/tokei/lines/github/yourusername/areebworldwide-music-player)
![GitHub last commit](https://img.shields.io/github/last-commit/yourusername/areebworldwide-music-player)

---

<div align="center">

**Made with ❤️ by AreebWorldwide**

*If you found this helpful, consider buying me a coffee!* ☕

[⬆ Back to Top](#-areebworldwide-music-player---ultimate-edition)

</div>
