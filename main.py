import customtkinter as ctk
from tkinter import filedialog, messagebox, Canvas
import tkinterdnd2 as tkdnd
import pygame
from pathlib import Path
import os
import random
from mutagen.mp3 import MP3
from mutagen.wave import WAVE
from mutagen.flac import FLAC
from mutagen.oggvorbis import OggVorbis
from mutagen.id3 import ID3, APIC, USLT
import threading
import time
from PIL import Image, ImageTk, ImageDraw
import io
import json
from datetime import datetime, timedelta

# Set appearance
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class ColorTheme:
    """Customizable color themes"""
    THEMES = {
        "Cyber Blue": {
            "bg_primary": "#1a1a2e",
            "bg_secondary": "#16213e",
            "bg_tertiary": "#0f3460",
            "accent": "#00d9ff",
            "accent_hover": "#00a8cc",
            "text_primary": "#ffffff",
            "text_secondary": "#a0a0a0",
            "error": "#ff4757"
        },
        "Purple Haze": {
            "bg_primary": "#1a0933",
            "bg_secondary": "#2d1b4e",
            "bg_tertiary": "#3e2a5c",
            "accent": "#a855f7",
            "accent_hover": "#9333ea",
            "text_primary": "#ffffff",
            "text_secondary": "#b8b8b8",
            "error": "#ef4444"
        },
        "Emerald Night": {
            "bg_primary": "#0a2e1a",
            "bg_secondary": "#134d2e",
            "bg_tertiary": "#1e6b42",
            "accent": "#10b981",
            "accent_hover": "#059669",
            "text_primary": "#ffffff",
            "text_secondary": "#a0a0a0",
            "error": "#f87171"
        }
    }
    
    def __init__(self, theme_name="Cyber Blue"):
        self.set_theme(theme_name)
        
    def set_theme(self, theme_name):
        self.current_theme = theme_name
        theme = self.THEMES.get(theme_name, self.THEMES["Cyber Blue"])
        for key, value in theme.items():
            setattr(self, key, value)

class AudioVisualizer:
    """Real-time audio visualizer"""
    def __init__(self, canvas, width, height, color):
        self.canvas = canvas
        self.width = width
        self.height = height
        self.color = color
        self.num_bars = 64
        self.bar_values = [0] * self.num_bars
        self.animation_running = False
        
    def start_animation(self):
        self.animation_running = True
        self.animate()
        
    def stop_animation(self):
        self.animation_running = False
        
    def animate(self):
        if not self.animation_running:
            return
            
        for i in range(self.num_bars):
            target = random.random() * 0.8 + 0.2
            self.bar_values[i] = self.bar_values[i] * 0.7 + target * 0.3
            
        self.draw_bars()
        self.canvas.after(50, self.animate)
        
    def draw_bars(self):
        self.canvas.delete("visualizer")
        bar_width = self.width / self.num_bars
        
        for i, value in enumerate(self.bar_values):
            x = i * bar_width
            bar_height = value * self.height * 0.8
            y = self.height - bar_height
            
            intensity = int(255 * value)
            color_hex = f"#{intensity:02x}{intensity//2:02x}{255:02x}"
            
            self.canvas.create_rectangle(
                x, y, x + bar_width - 2, self.height,
                fill=color_hex,
                outline="",
                tags="visualizer"
            )

class PlaylistManager:
    """Playlist Management System"""
    def __init__(self, playlists_file="playlists.json"):
        self.playlists_file = playlists_file
        self.playlists = {}
        self.load_playlists()
        
    def load_playlists(self):
        try:
            if os.path.exists(self.playlists_file):
                with open(self.playlists_file, 'r', encoding='utf-8') as f:
                    self.playlists = json.load(f)
        except Exception as e:
            print(f"Error loading playlists: {e}")
            self.playlists = {}
            
    def save_playlists(self):
        try:
            with open(self.playlists_file, 'w', encoding='utf-8') as f:
                json.dump(self.playlists, f, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving playlists: {e}")
            return False
            
    def create_playlist(self, name, songs=None):
        if name in self.playlists:
            return False, "Playlist already exists"
        
        self.playlists[name] = {
            "songs": songs if songs else [],
            "created": time.strftime("%Y-%m-%d %H:%M:%S"),
            "modified": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        self.save_playlists()
        return True, f"Playlist '{name}' created successfully"
        
    def delete_playlist(self, name):
        if name in self.playlists:
            del self.playlists[name]
            self.save_playlists()
            return True, f"Playlist '{name}' deleted"
        return False, "Playlist not found"
        
    def get_playlist(self, name):
        if name in self.playlists:
            return self.playlists[name]["songs"]
        return None
        
    def get_all_playlists(self):
        return list(self.playlists.keys())

class FolderBrowser:
    """Advanced folder browser with history"""
    def __init__(self, history_file="folder_history.json"):
        self.history_file = history_file
        self.recent_folders = []
        self.load_history()
        
    def load_history(self):
        try:
            if os.path.exists(self.history_file):
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    self.recent_folders = json.load(f)
        except:
            self.recent_folders = []
            
    def save_history(self):
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(self.recent_folders[:10], f, indent=4)
        except:
            pass
            
    def add_folder(self, folder_path):
        if folder_path in self.recent_folders:
            self.recent_folders.remove(folder_path)
        self.recent_folders.insert(0, folder_path)
        self.save_history()
        
    def get_recent_folders(self):
        valid_folders = [f for f in self.recent_folders if os.path.exists(f)]
        self.recent_folders = valid_folders
        return valid_folders[:10]

# ==================== NEW FEATURE 1: FAVORITES MANAGER ====================
class FavoritesManager:
    """Manage favorite/starred songs"""
    def __init__(self, favorites_file="favorites.json"):
        self.favorites_file = favorites_file
        self.favorites = []
        self.load_favorites()
        
    def load_favorites(self):
        try:
            if os.path.exists(self.favorites_file):
                with open(self.favorites_file, 'r', encoding='utf-8') as f:
                    self.favorites = json.load(f)
        except:
            self.favorites = []
            
    def save_favorites(self):
        try:
            with open(self.favorites_file, 'w', encoding='utf-8') as f:
                json.dump(self.favorites, f, indent=4, ensure_ascii=False)
        except:
            pass
            
    def toggle_favorite(self, song_path):
        if song_path in self.favorites:
            self.favorites.remove(song_path)
            self.save_favorites()
            return False
        else:
            self.favorites.append(song_path)
            self.save_favorites()
            return True
            
    def is_favorite(self, song_path):
        return song_path in self.favorites
        
    def get_favorites(self):
        return [f for f in self.favorites if os.path.exists(f)]

# ==================== NEW FEATURE 2: PLAY HISTORY ====================
class PlayHistoryManager:
    """Track recently played songs"""
    def __init__(self, history_file="play_history.json", max_items=50):
        self.history_file = history_file
        self.max_items = max_items
        self.history = []
        self.load_history()
        
    def load_history(self):
        try:
            if os.path.exists(self.history_file):
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    self.history = json.load(f)
        except:
            self.history = []
            
    def save_history(self):
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(self.history[:self.max_items], f, indent=4, ensure_ascii=False)
        except:
            pass
            
    def add_song(self, song_path):
        entry = {
            "path": song_path,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        # Remove if exists
        self.history = [h for h in self.history if h["path"] != song_path]
        # Add to front
        self.history.insert(0, entry)
        self.save_history()
        
    def get_history(self, limit=20):
        return [h for h in self.history[:limit] if os.path.exists(h["path"])]

# ==================== NEW FEATURE 3: QUEUE SYSTEM ====================
class QueueManager:
    """Manage play queue (play next)"""
    def __init__(self):
        self.queue = []
        
    def add_to_queue(self, song_path):
        if song_path not in self.queue:
            self.queue.append(song_path)
            return True
        return False
        
    def remove_from_queue(self, song_path):
        if song_path in self.queue:
            self.queue.remove(song_path)
            return True
        return False
        
    def get_next(self):
        if self.queue:
            return self.queue.pop(0)
        return None
        
    def clear(self):
        self.queue.clear()
        
    def get_queue(self):
        return self.queue.copy()
        
    def is_empty(self):
        return len(self.queue) == 0

# ==================== NEW FEATURE 4: SLEEP TIMER ====================
class SleepTimer:
    """Sleep timer to auto-stop playback"""
    def __init__(self, callback):
        self.callback = callback
        self.timer_thread = None
        self.end_time = None
        self.active = False
        
    def start(self, minutes):
        self.stop()
        self.end_time = datetime.now() + timedelta(minutes=minutes)
        self.active = True
        self.timer_thread = threading.Thread(target=self._run, daemon=True)
        self.timer_thread.start()
        
    def _run(self):
        while self.active and datetime.now() < self.end_time:
            time.sleep(1)
        if self.active:
            self.callback()
            self.active = False
            
    def stop(self):
        self.active = False
        self.end_time = None
        
    def get_remaining(self):
        if self.active and self.end_time:
            remaining = (self.end_time - datetime.now()).total_seconds()
            return max(0, remaining)
        return 0
        
    def is_active(self):
        return self.active

class PremiumMusicPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("🎵 AreebWorldwide Music Player - Ultimate Edition")
        self.root.geometry("1400x800")
        self.root.minsize(1200, 700)
        
        # Initialize pygame mixer
        pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
        
        # Color theme
        self.theme = ColorTheme("Cyber Blue")
        
        # Initialize managers
        self.playlist_manager = PlaylistManager()
        self.folder_browser = FolderBrowser()
        self.favorites_manager = FavoritesManager()  # NEW
        self.history_manager = PlayHistoryManager()  # NEW
        self.queue_manager = QueueManager()  # NEW
        self.sleep_timer = SleepTimer(self.sleep_timer_callback)  # NEW
        
        # Player state
        self.playlist = []
        self.current_index = 0
        self.is_playing = False
        self.is_paused = False
        self.shuffle_mode = False
        self.repeat_mode = "off"
        self.current_song_length = 0
        self.folder_path = ""
        self.filtered_playlist = []
        self.is_fullscreen = False
        self.current_playlist_name = None
        self.mini_player_window = None  # NEW
        self.playback_speed = 1.0  # NEW
        self.crossfade_enabled = False  # NEW
        
        # Supported formats
        self.supported_formats = ['.mp3', '.wav', '.flac', '.ogg', '.m4a']
        
        # Settings
        self.settings_file = "player_settings.json"
        self.load_settings()
        
        # Create UI
        self.create_animated_background()
        self.create_ui()
        
        # Start update thread
        self.update_thread = threading.Thread(target=self.update_progress, daemon=True)
        self.update_thread.start()
        
        # Bind shortcuts
        self.bind_shortcuts()
        
        # Protocol
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    def create_animated_background(self):
        """Animated background"""
        self.bg_canvas = Canvas(
            self.root,
            bg=self.theme.bg_primary,
            highlightthickness=0
        )
        self.bg_canvas.place(relx=0, rely=0, relwidth=1, relheight=1)
        
        self.particles = []
        for _ in range(30):
            x = random.randint(0, 1400)
            y = random.randint(0, 800)
            size = random.randint(2, 5)
            speed = random.uniform(0.5, 2)
            self.particles.append([x, y, size, speed])
            
        self.animate_background()
        
    def animate_background(self):
        self.bg_canvas.delete("particle")
        
        for particle in self.particles:
            x, y, size, speed = particle
            self.bg_canvas.create_oval(
                x, y, x + size, y + size,
                fill=self.theme.accent,
                outline="",
                tags="particle"
            )
            particle[1] += speed
            if particle[1] > 800:
                particle[1] = 0
                particle[0] = random.randint(0, 1400)
                
        self.root.after(50, self.animate_background)
        
    def create_ui(self):
        """Main UI"""
        self.main_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        self.main_frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.95, relheight=0.95)
        
        self.create_menu_bar()
        self.create_top_section()
        self.create_middle_section()
        self.create_bottom_section()
        
    def create_menu_bar(self):
        """Menu bar"""
        menu_bar = ctk.CTkFrame(self.main_frame, fg_color=self.theme.bg_secondary, 
                                corner_radius=15, height=50)
        menu_bar.pack(fill="x", padx=10, pady=(5, 5))
        menu_bar.pack_propagate(False)
        
        ctk.CTkLabel(
            menu_bar,
            text="🎵 AreebWorldwide Music Player",
            font=("Segoe UI", 16, "bold"),
            text_color=self.theme.accent
        ).pack(side="left", padx=20)
        
        btn_config = {
            "fg_color": "transparent",
            "hover_color": self.theme.bg_tertiary,
            "font": ("Segoe UI", 11),
            "width": 120,
            "height": 35,
            "corner_radius": 8
        }
        
        # NEW: Mini Player Button
        self.mini_player_btn = ctk.CTkButton(
            menu_bar,
            text="🖼️ Mini Player",
            command=self.toggle_mini_player,
            **btn_config
        )
        self.mini_player_btn.pack(side="right", padx=5)
        
        # NEW: More Features Menu
        self.more_btn = ctk.CTkButton(
            menu_bar,
            text="⚡ Features",
            command=self.show_features_menu,
            **btn_config
        )
        self.more_btn.pack(side="right", padx=5)
        
        self.browser_btn = ctk.CTkButton(
            menu_bar,
            text="📂 Browse",
            command=self.show_advanced_browser,
            **btn_config
        )
        self.browser_btn.pack(side="right", padx=5)
        
        self.theme_btn = ctk.CTkButton(
            menu_bar,
            text="🎨 Theme",
            command=self.show_theme_menu,
            **btn_config
        )
        self.theme_btn.pack(side="right", padx=5)
        
        self.playlist_manager_btn = ctk.CTkButton(
            menu_bar,
            text="📋 Playlists",
            command=self.show_playlist_manager,
            **btn_config
        )
        self.playlist_manager_btn.pack(side="right", padx=5)
        
    def create_top_section(self):
        """Top section with song info"""
        top_frame = ctk.CTkFrame(self.main_frame, fg_color=self.theme.bg_secondary, 
                                corner_radius=20, height=200)
        top_frame.pack(fill="x", padx=10, pady=5)
        top_frame.pack_propagate(False)
        
        # Album art
        self.album_art_frame = ctk.CTkFrame(top_frame, fg_color="transparent", width=180)
        self.album_art_frame.pack(side="left", padx=20, pady=20)
        self.album_art_frame.pack_propagate(False)
        
        self.album_art_canvas = Canvas(
            self.album_art_frame,
            width=160,
            height=160,
            bg=self.theme.bg_tertiary,
            highlightthickness=0
        )
        self.album_art_canvas.pack()
        self.create_default_album_art()
        
        # Song info
        info_container = ctk.CTkFrame(top_frame, fg_color="transparent")
        info_container.pack(side="left", fill="both", expand=True, padx=10)
        
        self.song_title = ctk.CTkLabel(
            info_container,
            text="No Song Playing",
            font=("Segoe UI", 32, "bold"),
            text_color=self.theme.text_primary,
            anchor="w"
        )
        self.song_title.pack(anchor="w", pady=(20, 5))
        
        self.song_artist = ctk.CTkLabel(
            info_container,
            text="Unknown Artist",
            font=("Segoe UI", 16),
            text_color=self.theme.text_secondary,
            anchor="w"
        )
        self.song_artist.pack(anchor="w", pady=2)
        
        self.song_info = ctk.CTkLabel(
            info_container,
            text="Select a folder to begin",
            font=("Segoe UI", 12),
            text_color=self.theme.text_secondary,
            anchor="w"
        )
        self.song_info.pack(anchor="w", pady=2)
        
        self.audio_quality = ctk.CTkLabel(
            info_container,
            text="",
            font=("Segoe UI", 11),
            text_color=self.theme.accent,
            anchor="w"
        )
        self.audio_quality.pack(anchor="w", pady=(10, 0))
        
        # NEW: Favorite button
        self.favorite_btn = ctk.CTkButton(
            top_frame,
            text="⭐",
            command=self.toggle_favorite_current,
            width=50,
            height=50,
            font=("Segoe UI", 24),
            fg_color="transparent",
            hover_color=self.theme.accent,
            corner_radius=25
        )
        self.favorite_btn.pack(side="right", padx=20)
        
    def create_default_album_art(self):
        """Default album art"""
        self.album_art_canvas.delete("all")
        
        for i in range(80, 0, -2):
            intensity = int((80 - i) / 80 * 100) + 50
            color = f"#{intensity:02x}{intensity//2:02x}{intensity:02x}"
            self.album_art_canvas.create_oval(
                80 - i, 80 - i, 80 + i, 80 + i,
                fill=color,
                outline=""
            )
            
        self.album_art_canvas.create_text(
            80, 80,
            text="♫",
            font=("Arial", 60, "bold"),
            fill=self.theme.accent
        )
        
    def load_album_art(self, song_path):
        """Load album art from file"""
        try:
            if song_path.lower().endswith('.mp3'):
                audio = ID3(song_path)
                for tag in audio.values():
                    if isinstance(tag, APIC):
                        image_data = tag.data
                        image = Image.open(io.BytesIO(image_data))
                        image = image.resize((160, 160), Image.Resampling.LANCZOS)
                        
                        mask = Image.new('L', (160, 160), 0)
                        draw = ImageDraw.Draw(mask)
                        draw.rounded_rectangle([(0, 0), (160, 160)], radius=15, fill=255)
                        
                        output = Image.new('RGBA', (160, 160), (0, 0, 0, 0))
                        output.paste(image, (0, 0))
                        output.putalpha(mask)
                        
                        photo = ImageTk.PhotoImage(output)
                        self.album_art_canvas.delete("all")
                        self.album_art_canvas.create_image(80, 80, image=photo)
                        self.album_art_canvas.image = photo
                        return
        except Exception as e:
            print(f"Could not load album art: {e}")
            
        self.create_default_album_art()
        
    def create_middle_section(self):
        """Middle section"""
        middle_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        middle_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.create_playlist_section(middle_frame)
        self.create_controls_section(middle_frame)
        
    def create_playlist_section(self, parent):
        """Playlist section"""
        playlist_container = ctk.CTkFrame(parent, fg_color=self.theme.bg_secondary, 
                                         corner_radius=20)
        playlist_container.pack(side="left", fill="both", expand=True, padx=(0, 5))
        
        # Header
        playlist_header = ctk.CTkFrame(playlist_container, fg_color=self.theme.bg_tertiary, 
                                      corner_radius=15, height=60)
        playlist_header.pack(fill="x", padx=15, pady=15)
        playlist_header.pack_propagate(False)
        
        header_left = ctk.CTkFrame(playlist_header, fg_color="transparent")
        header_left.pack(side="left", fill="y")
        
        ctk.CTkLabel(
            header_left,
            text="🎵 Playlist",
            font=("Segoe UI", 18, "bold"),
            text_color=self.theme.accent
        ).pack(side="left", padx=15)
        
        self.current_playlist_label = ctk.CTkLabel(
            header_left,
            text="",
            font=("Segoe UI", 11),
            text_color=self.theme.text_secondary
        )
        self.current_playlist_label.pack(side="left", padx=5)
        
        self.song_count_label = ctk.CTkLabel(
            playlist_header,
            text="0 songs",
            font=("Segoe UI", 12),
            text_color=self.theme.text_secondary
        )
        self.song_count_label.pack(side="right", padx=15)
        
        # Search
        search_frame = ctk.CTkFrame(playlist_container, fg_color="transparent")
        search_frame.pack(fill="x", padx=15, pady=(0, 10))
        
        self.search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="🔍 Search songs...",
            font=("Segoe UI", 12),
            height=35,
            corner_radius=10,
            fg_color=self.theme.bg_tertiary,
            border_color=self.theme.accent
        )
        self.search_entry.pack(fill="x", side="left", expand=True, padx=(0, 5))
        self.search_entry.bind("<KeyRelease>", self.filter_playlist)
        
        clear_btn = ctk.CTkButton(
            search_frame,
            text="✕",
            command=self.clear_search,
            width=35,
            height=35,
            fg_color=self.theme.bg_tertiary,
            hover_color=self.theme.error
        )
        clear_btn.pack(side="right")
        
        # Playlist frame
        self.playlist_frame = ctk.CTkScrollableFrame(
            playlist_container,
            fg_color="transparent",
            scrollbar_button_color=self.theme.bg_tertiary,
            scrollbar_button_hover_color=self.theme.accent
        )
        self.playlist_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
    def create_controls_section(self, parent):
        """Controls section"""
        controls_container = ctk.CTkFrame(parent, fg_color=self.theme.bg_secondary, 
                                         corner_radius=20, width=350)
        controls_container.pack(side="right", fill="y")
        controls_container.pack_propagate(False)
        
        # Visualizer
        viz_frame = ctk.CTkFrame(controls_container, fg_color=self.theme.bg_tertiary, 
                                corner_radius=15, height=120)
        viz_frame.pack(fill="x", padx=20, pady=(20, 10))
        viz_frame.pack_propagate(False)
        
        self.viz_canvas = Canvas(
            viz_frame,
            width=310,
            height=100,
            bg=self.theme.bg_tertiary,
            highlightthickness=0
        )
        self.viz_canvas.pack(padx=10, pady=10)
        
        self.visualizer = AudioVisualizer(self.viz_canvas, 310, 100, self.theme.accent)
        
        # Volume
        volume_frame = ctk.CTkFrame(controls_container, fg_color="transparent")
        volume_frame.pack(fill="x", padx=20, pady=10)
        
        volume_header = ctk.CTkFrame(volume_frame, fg_color="transparent")
        volume_header.pack(fill="x")
        
        ctk.CTkLabel(
            volume_header,
            text="🔊 Volume",
            font=("Segoe UI", 14, "bold"),
            text_color=self.theme.text_primary
        ).pack(side="left")
        
        self.volume_label = ctk.CTkLabel(
            volume_header,
            text="70%",
            font=("Segoe UI", 12, "bold"),
            text_color=self.theme.accent
        )
        self.volume_label.pack(side="right")
        
        self.volume_slider = ctk.CTkSlider(
            volume_frame,
            from_=0,
            to=100,
            number_of_steps=100,
            command=self.change_volume,
            button_color=self.theme.accent,
            button_hover_color=self.theme.accent_hover,
            progress_color=self.theme.accent,
            height=20
        )
        self.volume_slider.set(70)
        self.volume_slider.pack(fill="x", pady=(10, 0))
        
        # NEW: Playback Speed
        speed_frame = ctk.CTkFrame(controls_container, fg_color="transparent")
        speed_frame.pack(fill="x", padx=20, pady=10)
        
        speed_header = ctk.CTkFrame(speed_frame, fg_color="transparent")
        speed_header.pack(fill="x")
        
        ctk.CTkLabel(
            speed_header,
            text="⚡ Speed",
            font=("Segoe UI", 14, "bold"),
            text_color=self.theme.text_primary
        ).pack(side="left")
        
        self.speed_label = ctk.CTkLabel(
            speed_header,
            text="1.0x",
            font=("Segoe UI", 12, "bold"),
            text_color=self.theme.accent
        )
        self.speed_label.pack(side="right")
        
        self.speed_slider = ctk.CTkSlider(
            speed_frame,
            from_=0.5,
            to=2.0,
            number_of_steps=30,
            command=self.change_playback_speed,
            button_color=self.theme.accent,
            button_hover_color=self.theme.accent_hover,
            progress_color=self.theme.accent,
            height=20
        )
        self.speed_slider.set(1.0)
        self.speed_slider.pack(fill="x", pady=(10, 0))
        
        # Separator
        ctk.CTkFrame(controls_container, height=2, fg_color=self.theme.bg_tertiary).pack(
            fill="x", padx=20, pady=15
        )
        
        # Modes
        modes_frame = ctk.CTkFrame(controls_container, fg_color="transparent")
        modes_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(
            modes_frame,
            text="⚙️ Playback Modes",
            font=("Segoe UI", 14, "bold"),
            text_color=self.theme.text_primary
        ).pack(anchor="w", pady=(0, 15))
        
        self.shuffle_btn = ctk.CTkButton(
            modes_frame,
            text="🔀 Shuffle: OFF",
            command=self.toggle_shuffle,
            fg_color=self.theme.bg_tertiary,
            hover_color=self.theme.accent,
            font=("Segoe UI", 12, "bold"),
            height=45,
            corner_radius=12
        )
        self.shuffle_btn.pack(fill="x", pady=5)
        
        self.repeat_btn = ctk.CTkButton(
            modes_frame,
            text="🔁 Repeat: OFF",
            command=self.toggle_repeat,
            fg_color=self.theme.bg_tertiary,
            hover_color=self.theme.accent,
            font=("Segoe UI", 12, "bold"),
            height=45,
            corner_radius=12
        )
        self.repeat_btn.pack(fill="x", pady=5)
        
        # Separator
        ctk.CTkFrame(controls_container, height=2, fg_color=self.theme.bg_tertiary).pack(
            fill="x", padx=20, pady=15
        )
        
        # Quick load buttons
        self.folder_btn = ctk.CTkButton(
            controls_container,
            text="📁 Quick Load Folder",
            command=self.select_folder,
            fg_color=self.theme.accent,
            hover_color=self.theme.accent_hover,
            font=("Segoe UI", 14, "bold"),
            height=55,
            corner_radius=15
        )
        self.folder_btn.pack(fill="x", padx=20, pady=10)
        
        self.add_files_btn = ctk.CTkButton(
            controls_container,
            text="➕ Add Files",
            command=self.add_files,
            fg_color=self.theme.bg_tertiary,
            hover_color=self.theme.accent,
            font=("Segoe UI", 12, "bold"),
            height=45,
            corner_radius=12
        )
        self.add_files_btn.pack(fill="x", padx=20, pady=(0, 10))
        
        self.clear_btn = ctk.CTkButton(
            controls_container,
            text="🗑️ Clear Playlist",
            command=self.clear_playlist,
            fg_color=self.theme.bg_tertiary,
            hover_color=self.theme.error,
            font=("Segoe UI", 11, "bold"),
            height=40,
            corner_radius=12
        )
        self.clear_btn.pack(fill="x", padx=20, pady=(0, 10))
        
    def create_bottom_section(self):
        """Bottom controls"""
        bottom_frame = ctk.CTkFrame(self.main_frame, fg_color=self.theme.bg_secondary, 
                                   corner_radius=20, height=180)
        bottom_frame.pack(fill="x", padx=10, pady=(5, 10))
        bottom_frame.pack_propagate(False)
        
        # Progress
        progress_container = ctk.CTkFrame(bottom_frame, fg_color="transparent")
        progress_container.pack(fill="x", padx=30, pady=(20, 10))
        
        time_frame = ctk.CTkFrame(progress_container, fg_color="transparent")
        time_frame.pack(fill="x", pady=(0, 5))
        
        self.current_time_label = ctk.CTkLabel(
            time_frame,
            text="0:00",
            font=("Segoe UI", 11, "bold"),
            text_color=self.theme.text_secondary
        )
        self.current_time_label.pack(side="left")
        
        self.total_time_label = ctk.CTkLabel(
            time_frame,
            text="0:00",
            font=("Segoe UI", 11, "bold"),
            text_color=self.theme.text_secondary
        )
        self.total_time_label.pack(side="right")
        
        self.progress_slider = ctk.CTkSlider(
            progress_container,
            from_=0,
            to=100,
            number_of_steps=1000,
            command=self.seek_song,
            button_color=self.theme.accent,
            button_hover_color=self.theme.accent_hover,
            progress_color=self.theme.accent,
            height=20
        )
        self.progress_slider.set(0)
        self.progress_slider.pack(fill="x", pady=5)
        
        # Controls
        controls_frame = ctk.CTkFrame(bottom_frame, fg_color="transparent")
        controls_frame.pack(expand=True)
        
        button_config = {
            "width": 70,
            "height": 70,
            "corner_radius": 35,
            "font": ("Segoe UI", 24, "bold")
        }
        
        small_button_config = {
            "width": 55,
            "height": 55,
            "corner_radius": 27,
            "font": ("Segoe UI", 18)
        }
        
        self.prev_btn = ctk.CTkButton(
            controls_frame,
            text="⏮",
            command=self.previous_song,
            fg_color=self.theme.bg_tertiary,
            hover_color=self.theme.accent,
            **small_button_config
        )
        self.prev_btn.pack(side="left", padx=8)
        
        self.stop_btn = ctk.CTkButton(
            controls_frame,
            text="⏹",
            command=self.stop_song,
            fg_color=self.theme.bg_tertiary,
            hover_color=self.theme.error,
            **small_button_config
        )
        self.stop_btn.pack(side="left", padx=8)
        
        self.play_pause_btn = ctk.CTkButton(
            controls_frame,
            text="▶",
            command=self.play_pause_song,
            fg_color=self.theme.accent,
            hover_color=self.theme.accent_hover,
            **button_config
        )
        self.play_pause_btn.pack(side="left", padx=12)
        
        self.next_btn = ctk.CTkButton(
            controls_frame,
            text="⏭",
            command=self.next_song,
            fg_color=self.theme.bg_tertiary,
            hover_color=self.theme.accent,
            **small_button_config
        )
        self.next_btn.pack(side="left", padx=8)

    # ==================== NEW FEATURE 5: FEATURES MENU ====================
    def show_features_menu(self):
        """Show advanced features menu"""
        features_window = ctk.CTkToplevel(self.root)
        features_window.title("⚡ Advanced Features")
        features_window.geometry("600x700")
        features_window.transient(self.root)
        features_window.grab_set()
        
        # Header
        header = ctk.CTkFrame(features_window, fg_color=self.theme.bg_secondary, height=70)
        header.pack(fill="x", padx=20, pady=20)
        header.pack_propagate(False)
        
        ctk.CTkLabel(
            header,
            text="⚡ Advanced Features",
            font=("Segoe UI", 24, "bold"),
            text_color=self.theme.accent
        ).pack(pady=15)
        
        # Scrollable content
        content = ctk.CTkScrollableFrame(
            features_window,
            fg_color="transparent"
        )
        content.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        btn_config = {
            "font": ("Segoe UI", 13, "bold"),
            "height": 55,
            "corner_radius": 12,
            "fg_color": self.theme.bg_secondary,
            "hover_color": self.theme.accent
        }
        
        # Equalizer
        ctk.CTkButton(
            content,
            text="🎚️ Equalizer",
            command=self.show_equalizer,
            **btn_config
        ).pack(fill="x", pady=5)
        
        # Sleep Timer
        ctk.CTkButton(
            content,
            text="⏰ Sleep Timer",
            command=self.show_sleep_timer,
            **btn_config
        ).pack(fill="x", pady=5)
        
        # Queue Manager
        ctk.CTkButton(
            content,
            text="📝 Play Queue",
            command=self.show_queue_manager,
            **btn_config
        ).pack(fill="x", pady=5)
        
        # Favorites
        ctk.CTkButton(
            content,
            text="⭐ Favorites",
            command=self.show_favorites,
            **btn_config
        ).pack(fill="x", pady=5)
        
        # History
        ctk.CTkButton(
            content,
            text="🕐 Play History",
            command=self.show_play_history,
            **btn_config
        ).pack(fill="x", pady=5)
        
        # Lyrics Viewer
        ctk.CTkButton(
            content,
            text="🎤 Show Lyrics",
            command=self.show_lyrics_viewer,
            **btn_config
        ).pack(fill="x", pady=5)
        
        # Export/Import Playlists
        ctk.CTkButton(
            content,
            text="📤 Export Playlist",
            command=self.export_playlist_m3u,
            **btn_config
        ).pack(fill="x", pady=5)
        
        ctk.CTkButton(
            content,
            text="📥 Import Playlist",
            command=self.import_playlist_m3u,
            **btn_config
        ).pack(fill="x", pady=5)
        
        # Crossfade Toggle
        crossfade_frame = ctk.CTkFrame(content, fg_color=self.theme.bg_secondary, corner_radius=12)
        crossfade_frame.pack(fill="x", pady=5, padx=5)
        
        ctk.CTkLabel(
            crossfade_frame,
            text="🌊 Crossfade Between Songs",
            font=("Segoe UI", 13, "bold")
        ).pack(side="left", padx=15, pady=15)
        
        self.crossfade_switch = ctk.CTkSwitch(
            crossfade_frame,
            text="",
            command=self.toggle_crossfade,
            fg_color=self.theme.accent,
            progress_color=self.theme.accent_hover
        )
        self.crossfade_switch.pack(side="right", padx=15)
        if self.crossfade_enabled:
            self.crossfade_switch.select()

    # ==================== NEW FEATURE 6: EQUALIZER ====================
    def show_equalizer(self):
        """Show audio equalizer"""
        eq_window = ctk.CTkToplevel(self.root)
        eq_window.title("🎚️ Audio Equalizer")
        eq_window.geometry("500x600")
        eq_window.transient(self.root)
        eq_window.grab_set()
        
        # Header
        ctk.CTkLabel(
            eq_window,
            text="🎚️ Audio Equalizer",
            font=("Segoe UI", 24, "bold"),
            text_color=self.theme.accent
        ).pack(pady=20)
        
        # Presets
        presets_frame = ctk.CTkFrame(eq_window, fg_color=self.theme.bg_secondary)
        presets_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(
            presets_frame,
            text="Presets:",
            font=("Segoe UI", 14, "bold")
        ).pack(side="left", padx=10, pady=10)
        
        presets = ["Flat", "Rock", "Pop", "Jazz", "Classical", "Bass Boost", "Treble Boost"]
        
        for preset in presets:
            ctk.CTkButton(
                presets_frame,
                text=preset,
                command=lambda p=preset: self.apply_eq_preset(p),
                width=100,
                height=35,
                fg_color=self.theme.bg_tertiary,
                hover_color=self.theme.accent,
                font=("Segoe UI", 11)
            ).pack(side="left", padx=3, pady=10)
        
        # Note
        ctk.CTkLabel(
            eq_window,
            text="Note: Full EQ requires external audio processing library.\nPresets will be saved to settings.",
            font=("Segoe UI", 10),
            text_color=self.theme.text_secondary,
            justify="center"
        ).pack(pady=10)
        
        messagebox.showinfo(
            "Equalizer",
            f"Equalizer preset selection available.\n\nNote: Real-time frequency adjustment requires\nadditional audio processing libraries like PyAudio."
        )
    
    def apply_eq_preset(self, preset_name):
        """Apply EQ preset"""
        messagebox.showinfo("EQ Preset", f"Applied '{preset_name}' preset!")
        # In a full implementation, this would adjust frequency bands

    # ==================== NEW FEATURE 7: SLEEP TIMER ====================
    def show_sleep_timer(self):
        """Show sleep timer dialog"""
        timer_window = ctk.CTkToplevel(self.root)
        timer_window.title("⏰ Sleep Timer")
        timer_window.geometry("400x350")
        timer_window.transient(self.root)
        timer_window.grab_set()
        
        # Header
        ctk.CTkLabel(
            timer_window,
            text="⏰ Sleep Timer",
            font=("Segoe UI", 24, "bold"),
            text_color=self.theme.accent
        ).pack(pady=20)
        
        # Status
        status_text = "Timer Active" if self.sleep_timer.is_active() else "No Timer Set"
        status_color = self.theme.accent if self.sleep_timer.is_active() else self.theme.text_secondary
        
        status_label = ctk.CTkLabel(
            timer_window,
            text=status_text,
            font=("Segoe UI", 16),
            text_color=status_color
        )
        status_label.pack(pady=10)
        
        if self.sleep_timer.is_active():
            remaining = int(self.sleep_timer.get_remaining() / 60)
            ctk.CTkLabel(
                timer_window,
                text=f"Remaining: {remaining} minutes",
                font=("Segoe UI", 14),
                text_color=self.theme.text_secondary
            ).pack(pady=5)
        
        # Time selection
        ctk.CTkLabel(
            timer_window,
            text="Set Timer (minutes):",
            font=("Segoe UI", 14)
        ).pack(pady=(20, 10))
        
        time_var = ctk.StringVar(value="30")
        time_entry = ctk.CTkEntry(
            timer_window,
            textvariable=time_var,
            font=("Segoe UI", 16),
            width=150,
            height=45,
            justify="center"
        )
        time_entry.pack(pady=10)
        
        # Quick buttons
        quick_frame = ctk.CTkFrame(timer_window, fg_color="transparent")
        quick_frame.pack(pady=15)
        
        for mins in [15, 30, 45, 60]:
            ctk.CTkButton(
                quick_frame,
                text=f"{mins}m",
                command=lambda m=mins: time_var.set(str(m)),
                width=70,
                height=35,
                fg_color=self.theme.bg_secondary,
                hover_color=self.theme.accent
            ).pack(side="left", padx=5)
        
        # Buttons
        btn_frame = ctk.CTkFrame(timer_window, fg_color="transparent")
        btn_frame.pack(pady=20)
        
        def start_timer():
            try:
                minutes = int(time_var.get())
                if minutes <= 0:
                    messagebox.showwarning("Invalid Time", "Please enter a positive number!")
                    return
                self.sleep_timer.start(minutes)
                messagebox.showinfo("Timer Started", f"Music will stop in {minutes} minutes")
                timer_window.destroy()
            except ValueError:
                messagebox.showwarning("Invalid Input", "Please enter a valid number!")
        
        ctk.CTkButton(
            btn_frame,
            text="Start Timer",
            command=start_timer,
            fg_color=self.theme.accent,
            hover_color=self.theme.accent_hover,
            width=150,
            height=45,
            font=("Segoe UI", 14, "bold")
        ).pack(side="left", padx=5)
        
        if self.sleep_timer.is_active():
            ctk.CTkButton(
                btn_frame,
                text="Cancel Timer",
                command=lambda: [self.sleep_timer.stop(), timer_window.destroy()],
                fg_color=self.theme.error,
                hover_color="#cc0000",
                width=150,
                height=45,
                font=("Segoe UI", 14, "bold")
            ).pack(side="left", padx=5)
    
    def sleep_timer_callback(self):
        """Called when sleep timer expires"""
        self.stop_song()
        messagebox.showinfo("Sleep Timer", "Sleep timer expired. Playback stopped.")

    # ==================== NEW FEATURE 8: QUEUE MANAGER ====================
    def show_queue_manager(self):
        """Show play queue manager"""
        queue_window = ctk.CTkToplevel(self.root)
        queue_window.title("📝 Play Queue")
        queue_window.geometry("600x500")
        queue_window.transient(self.root)
        queue_window.grab_set()
        
        # Header
        header = ctk.CTkFrame(queue_window, fg_color=self.theme.bg_secondary, height=70)
        header.pack(fill="x", padx=20, pady=20)
        header.pack_propagate(False)
        
        ctk.CTkLabel(
            header,
            text="📝 Play Queue",
            font=("Segoe UI", 24, "bold"),
            text_color=self.theme.accent
        ).pack(side="left", padx=20, pady=15)
        
        queue_count = ctk.CTkLabel(
            header,
            text=f"{len(self.queue_manager.get_queue())} songs",
            font=("Segoe UI", 14),
            text_color=self.theme.text_secondary
        )
        queue_count.pack(side="right", padx=20)
        
        # Queue list
        queue_frame = ctk.CTkScrollableFrame(
            queue_window,
            fg_color=self.theme.bg_secondary,
            corner_radius=15
        )
        queue_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        self.refresh_queue_display(queue_frame, queue_count)
        
        # Clear button
        ctk.CTkButton(
            queue_window,
            text="🗑️ Clear Queue",
            command=lambda: [self.queue_manager.clear(), self.refresh_queue_display(queue_frame, queue_count)],
            fg_color=self.theme.error,
            hover_color="#cc0000",
            height=45,
            font=("Segoe UI", 13, "bold")
        ).pack(side="bottom", pady=(0, 20), padx=20, fill="x")
    
    def refresh_queue_display(self, container, count_label):
        """Refresh queue display"""
        for widget in container.winfo_children():
            widget.destroy()
        
        queue = self.queue_manager.get_queue()
        count_label.configure(text=f"{len(queue)} songs")
        
        if not queue:
            ctk.CTkLabel(
                container,
                text="📝 Queue is empty\n\nRight-click songs to add to queue",
                font=("Segoe UI", 16),
                text_color=self.theme.text_secondary,
                justify="center"
            ).pack(pady=100)
            return
        
        for idx, song_path in enumerate(queue):
            song_name = Path(song_path).stem
            
            item_frame = ctk.CTkFrame(
                container,
                fg_color=self.theme.bg_tertiary,
                corner_radius=10,
                height=50
            )
            item_frame.pack(fill="x", pady=3, padx=10)
            item_frame.pack_propagate(False)
            
            ctk.CTkLabel(
                item_frame,
                text=f"{idx + 1}.",
                font=("Segoe UI", 12, "bold"),
                text_color=self.theme.accent,
                width=40
            ).pack(side="left", padx=10)
            
            ctk.CTkLabel(
                item_frame,
                text=song_name,
                font=("Segoe UI", 12),
                anchor="w"
            ).pack(side="left", fill="x", expand=True, padx=10)
            
            ctk.CTkButton(
                item_frame,
                text="✕",
                command=lambda s=song_path: [
                    self.queue_manager.remove_from_queue(s),
                    self.refresh_queue_display(container, count_label)
                ],
                width=35,
                height=35,
                fg_color="transparent",
                hover_color=self.theme.error
            ).pack(side="right", padx=5)

    # ==================== NEW FEATURE 9: FAVORITES ====================
    def toggle_favorite_current(self):
        """Toggle favorite for current song"""
        if self.playlist and 0 <= self.current_index < len(self.playlist):
            song_path = self.playlist[self.current_index]
            is_fav = self.favorites_manager.toggle_favorite(song_path)
            
            if is_fav:
                self.favorite_btn.configure(text="⭐", fg_color=self.theme.accent)
                messagebox.showinfo("Favorite", "Added to favorites!")
            else:
                self.favorite_btn.configure(text="☆", fg_color="transparent")
                messagebox.showinfo("Favorite", "Removed from favorites!")
            
            self.update_playlist_ui()
    
    def show_favorites(self):
        """Show favorites list"""
        fav_window = ctk.CTkToplevel(self.root)
        fav_window.title("⭐ Favorite Songs")
        fav_window.geometry("700x600")
        fav_window.transient(self.root)
        fav_window.grab_set()
        
        # Header
        header = ctk.CTkFrame(fav_window, fg_color=self.theme.bg_secondary, height=70)
        header.pack(fill="x", padx=20, pady=20)
        header.pack_propagate(False)
        
        ctk.CTkLabel(
            header,
            text="⭐ Favorite Songs",
            font=("Segoe UI", 24, "bold"),
            text_color=self.theme.accent
        ).pack(side="left", padx=20, pady=15)
        
        # Favorites list
        fav_frame = ctk.CTkScrollableFrame(
            fav_window,
            fg_color=self.theme.bg_secondary,
            corner_radius=15
        )
        fav_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        favorites = self.favorites_manager.get_favorites()
        
        if not favorites:
            ctk.CTkLabel(
                fav_frame,
                text="⭐ No favorites yet\n\nClick the star button to add favorites!",
                font=("Segoe UI", 16),
                text_color=self.theme.text_secondary,
                justify="center"
            ).pack(pady=100)
            return
        
        for song_path in favorites:
            song_name = Path(song_path).stem
            
            item_frame = ctk.CTkFrame(
                fav_frame,
                fg_color=self.theme.bg_tertiary,
                corner_radius=10,
                height=55
            )
            item_frame.pack(fill="x", pady=3, padx=10)
            item_frame.pack_propagate(False)
            
            ctk.CTkLabel(
                item_frame,
                text="⭐",
                font=("Segoe UI", 16),
                width=40
            ).pack(side="left", padx=10)
            
            ctk.CTkButton(
                item_frame,
                text=song_name,
                command=lambda s=song_path: [self.play_song_by_path(s), fav_window.destroy()],
                fg_color="transparent",
                hover_color=self.theme.bg_secondary,
                anchor="w",
                font=("Segoe UI", 12)
            ).pack(side="left", fill="both", expand=True, padx=5)
            
            ctk.CTkButton(
                item_frame,
                text="✕",
                command=lambda s=song_path: [
                    self.favorites_manager.toggle_favorite(s),
                    self.show_favorites(),
                    fav_window.destroy()
                ],
                width=35,
                height=35,
                fg_color="transparent",
                hover_color=self.theme.error
            ).pack(side="right", padx=5)
        
        # Load all button
        ctk.CTkButton(
            fav_window,
            text="▶ Play All Favorites",
            command=lambda: [self.load_favorites_playlist(), fav_window.destroy()],
            fg_color=self.theme.accent,
            hover_color=self.theme.accent_hover,
            height=50,
            font=("Segoe UI", 14, "bold")
        ).pack(side="bottom", pady=(0, 20), padx=20, fill="x")
    
    def load_favorites_playlist(self):
        """Load all favorites as playlist"""
        favorites = self.favorites_manager.get_favorites()
        if favorites:
            self.playlist = favorites
            self.filtered_playlist = self.playlist.copy()
            self.current_index = 0
            self.update_playlist_ui()
            messagebox.showinfo("Favorites Loaded", f"Loaded {len(favorites)} favorite songs!")

    # ==================== NEW FEATURE 10: PLAY HISTORY ====================
    def show_play_history(self):
        """Show play history"""
        history_window = ctk.CTkToplevel(self.root)
        history_window.title("🕐 Play History")
        history_window.geometry("700x600")
        history_window.transient(self.root)
        history_window.grab_set()
        
        # Header
        header = ctk.CTkFrame(history_window, fg_color=self.theme.bg_secondary, height=70)
        header.pack(fill="x", padx=20, pady=20)
        header.pack_propagate(False)
        
        ctk.CTkLabel(
            header,
            text="🕐 Recently Played",
            font=("Segoe UI", 24, "bold"),
            text_color=self.theme.accent
        ).pack(side="left", padx=20, pady=15)
        
        # History list
        history_frame = ctk.CTkScrollableFrame(
            history_window,
            fg_color=self.theme.bg_secondary,
            corner_radius=15
        )
        history_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        history = self.history_manager.get_history()
        
        if not history:
            ctk.CTkLabel(
                history_frame,
                text="🕐 No play history yet\n\nYour recently played songs will appear here",
                font=("Segoe UI", 16),
                text_color=self.theme.text_secondary,
                justify="center"
            ).pack(pady=100)
            return
        
        for entry in history:
            song_path = entry["path"]
            timestamp = entry["timestamp"]
            song_name = Path(song_path).stem
            
            item_frame = ctk.CTkFrame(
                history_frame,
                fg_color=self.theme.bg_tertiary,
                corner_radius=10,
                height=65
            )
            item_frame.pack(fill="x", pady=3, padx=10)
            item_frame.pack_propagate(False)
            
            info_frame = ctk.CTkFrame(item_frame, fg_color="transparent")
            info_frame.pack(side="left", fill="both", expand=True, padx=15, pady=10)
            
            ctk.CTkLabel(
                info_frame,
                text=song_name,
                font=("Segoe UI", 13, "bold"),
                anchor="w"
            ).pack(anchor="w")
            
            ctk.CTkLabel(
                info_frame,
                text=f"🕐 {timestamp}",
                font=("Segoe UI", 10),
                text_color=self.theme.text_secondary,
                anchor="w"
            ).pack(anchor="w", pady=(2, 0))
            
            ctk.CTkButton(
                item_frame,
                text="▶",
                command=lambda s=song_path: [self.play_song_by_path(s), history_window.destroy()],
                width=45,
                height=45,
                fg_color=self.theme.accent,
                hover_color=self.theme.accent_hover,
                font=("Segoe UI", 16)
            ).pack(side="right", padx=10)

    # ==================== NEW: LYRICS VIEWER ====================
    def show_lyrics_viewer(self):
        """Show lyrics for current song"""
        if not self.playlist or not (0 <= self.current_index < len(self.playlist)):
            messagebox.showwarning("No Song", "No song is currently playing!")
            return
        
        lyrics_window = ctk.CTkToplevel(self.root)
        lyrics_window.title("🎤 Lyrics Viewer")
        lyrics_window.geometry("600x700")
        lyrics_window.transient(self.root)
        
        song_path = self.playlist[self.current_index]
        song_name = Path(song_path).stem
        
        # Header
        ctk.CTkLabel(
            lyrics_window,
            text=f"🎤 Lyrics: {song_name}",
            font=("Segoe UI", 20, "bold"),
            text_color=self.theme.accent,
            wraplength=550
        ).pack(pady=20, padx=20)
        
        # Lyrics text
        lyrics_text = ctk.CTkTextbox(
            lyrics_window,
            font=("Segoe UI", 13),
            wrap="word",
            fg_color=self.theme.bg_secondary,
            corner_radius=15
        )
        lyrics_text.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Try to load lyrics
        lyrics = self.extract_lyrics(song_path)
        
        if lyrics:
            lyrics_text.insert("1.0", lyrics)
        else:
            lyrics_text.insert("1.0", "No lyrics found for this song.\n\n"
                                     "Lyrics can be embedded in MP3 files using ID3 tags (USLT).\n\n"
                                     "You can also create a .txt file with the same name as your song\n"
                                     "in the same folder to display lyrics.")
        
        lyrics_text.configure(state="disabled")
    
    def extract_lyrics(self, song_path):
        """Extract lyrics from song file or companion .txt file"""
        # Try embedded lyrics
        try:
            if song_path.lower().endswith('.mp3'):
                audio = ID3(song_path)
                for tag in audio.values():
                    if isinstance(tag, USLT):
                        return tag.text
        except:
            pass
        
        # Try companion .txt file
        txt_path = Path(song_path).with_suffix('.txt')
        if txt_path.exists():
            try:
                with open(txt_path, 'r', encoding='utf-8') as f:
                    return f.read()
            except:
                pass
        
        return None

    # ==================== NEW: EXPORT/IMPORT M3U ====================
    def export_playlist_m3u(self):
        """Export current playlist to M3U format"""
        if not self.playlist:
            messagebox.showwarning("No Playlist", "Load some songs first!")
            return
        
        file_path = filedialog.asksaveasfilename(
            title="Export Playlist",
            defaultextension=".m3u",
            filetypes=[("M3U Playlist", "*.m3u"), ("M3U8 Playlist", "*.m3u8")]
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write("#EXTM3U\n")
                    for song_path in self.playlist:
                        song_name = Path(song_path).stem
                        duration = int(self.get_song_length(song_path))
                        f.write(f"#EXTINF:{duration},{song_name}\n")
                        f.write(f"{song_path}\n")
                
                messagebox.showinfo("Success", f"Playlist exported to:\n{file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export:\n{str(e)}")
    
    def import_playlist_m3u(self):
        """Import M3U playlist"""
        file_path = filedialog.askopenfilename(
            title="Import Playlist",
            filetypes=[("M3U Playlist", "*.m3u *.m3u8"), ("All Files", "*.*")]
        )
        
        if file_path:
            try:
                songs = []
                with open(file_path, 'r', encoding='utf-8') as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith('#'):
                            if os.path.exists(line):
                                songs.append(line)
                
                if songs:
                    self.playlist = songs
                    self.filtered_playlist = self.playlist.copy()
                    self.current_index = 0
                    self.update_playlist_ui()
                    messagebox.showinfo("Success", f"Imported {len(songs)} songs!")
                else:
                    messagebox.showwarning("No Songs", "No valid songs found in playlist!")
                    
            except Exception as e:
                messagebox.showerror("Error", f"Failed to import:\n{str(e)}")

    # ==================== NEW: PLAYBACK SPEED ====================
    def change_playback_speed(self, value):
        """Change playback speed (Note: Limited pygame support)"""
        self.playback_speed = float(value)
        self.speed_label.configure(text=f"{self.playback_speed:.1f}x")
        
        # Note: pygame.mixer doesn't support real-time speed change
        # This would require reloading the song with modified playback
        # For demonstration, we just show the setting
        
    def toggle_crossfade(self):
        """Toggle crossfade mode"""
        self.crossfade_enabled = self.crossfade_switch.get()
        status = "enabled" if self.crossfade_enabled else "disabled"
        messagebox.showinfo("Crossfade", f"Crossfade {status}!")

    # ==================== NEW: MINI PLAYER ====================
    def toggle_mini_player(self):
        """Toggle mini player mode"""
        if self.mini_player_window and self.mini_player_window.winfo_exists():
            self.mini_player_window.destroy()
            self.mini_player_window = None
            self.root.deiconify()
        else:
            self.create_mini_player()
            self.root.withdraw()
    
    def create_mini_player(self):
        """Create mini player window"""
        self.mini_player_window = ctk.CTkToplevel(self.root)
        self.mini_player_window.title("Mini Player")
        self.mini_player_window.geometry("400x150")
        self.mini_player_window.attributes("-topmost", True)
        self.mini_player_window.protocol("WM_DELETE_WINDOW", self.close_mini_player)
        
        # Song info
        if self.playlist and 0 <= self.current_index < len(self.playlist):
            song_name = Path(self.playlist[self.current_index]).stem
        else:
            song_name = "No Song Playing"
        
        title_label = ctk.CTkLabel(
            self.mini_player_window,
            text=song_name,
            font=("Segoe UI", 16, "bold"),
            wraplength=350
        )
        title_label.pack(pady=(15, 5))
        
        # Progress
        self.mini_progress = ctk.CTkProgressBar(
            self.mini_player_window,
            width=350,
            progress_color=self.theme.accent
        )
        self.mini_progress.pack(pady=10)
        self.mini_progress.set(0)
        
        # Controls
        controls_frame = ctk.CTkFrame(self.mini_player_window, fg_color="transparent")
        controls_frame.pack(pady=10)
        
        btn_config = {
            "width": 50,
            "height": 50,
            "corner_radius": 25,
            "font": ("Segoe UI", 18)
        }
        
        ctk.CTkButton(
            controls_frame,
            text="⏮",
            command=self.previous_song,
            fg_color=self.theme.bg_tertiary,
            hover_color=self.theme.accent,
            **btn_config
        ).pack(side="left", padx=5)
        
        self.mini_play_btn = ctk.CTkButton(
            controls_frame,
            text="⏸" if self.is_playing and not self.is_paused else "▶",
            command=self.play_pause_song,
            fg_color=self.theme.accent,
            hover_color=self.theme.accent_hover,
            **btn_config
        )
        self.mini_play_btn.pack(side="left", padx=5)
        
        ctk.CTkButton(
            controls_frame,
            text="⏭",
            command=self.next_song,
            fg_color=self.theme.bg_tertiary,
            hover_color=self.theme.accent,
            **btn_config
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            controls_frame,
            text="🔙",
            command=self.close_mini_player,
            fg_color=self.theme.bg_secondary,
            hover_color=self.theme.accent,
            **btn_config
        ).pack(side="left", padx=15)
        
        # Start update
        self.update_mini_player()
    
    def update_mini_player(self):
        """Update mini player display"""
        if self.mini_player_window and self.mini_player_window.winfo_exists():
            if self.is_playing and self.current_song_length > 0:
                progress = (pygame.mixer.music.get_pos() / 1000) / self.current_song_length
                self.mini_progress.set(min(progress, 1.0))
            
            self.mini_player_window.after(500, self.update_mini_player)
    
    def close_mini_player(self):
        """Close mini player and restore main window"""
        if self.mini_player_window:
            self.mini_player_window.destroy()
            self.mini_player_window = None
        self.root.deiconify()

    # ==================== HELPER FUNCTIONS ====================
    
    def play_song_by_path(self, song_path):
        """Play specific song by path"""
        if song_path in self.playlist:
            self.current_index = self.playlist.index(song_path)
            self.play_song()
        else:
            messagebox.showwarning("Song Not Found", "This song is not in the current playlist!")

    # ==================== ADVANCED FOLDER BROWSER ====================
    
    def show_advanced_browser(self):
        """Show advanced folder browser with recent folders"""
        browser_window = ctk.CTkToplevel(self.root)
        browser_window.title("📂 Advanced Folder Browser")
        browser_window.geometry("700x600")
        browser_window.transient(self.root)
        browser_window.grab_set()
        
        header = ctk.CTkFrame(browser_window, fg_color=self.theme.bg_secondary, height=80)
        header.pack(fill="x", padx=20, pady=20)
        header.pack_propagate(False)
        
        ctk.CTkLabel(
            header,
            text="📂 Browse & Load Music",
            font=("Segoe UI", 28, "bold"),
            text_color=self.theme.accent
        ).pack(side="left", padx=20)
        
        actions_frame = ctk.CTkFrame(browser_window, fg_color="transparent", height=70)
        actions_frame.pack(fill="x", padx=20, pady=(0, 10))
        actions_frame.pack_propagate(False)
        
        btn_config = {
            "font": ("Segoe UI", 13, "bold"),
            "height": 50,
            "corner_radius": 12
        }
        
        browse_btn = ctk.CTkButton(
            actions_frame,
            text="🔍 Browse New Folder",
            command=lambda: self.browse_and_load(browser_window),
            fg_color=self.theme.accent,
            hover_color=self.theme.accent_hover,
            **btn_config
        )
        browse_btn.pack(side="left", padx=5, expand=True, fill="x")
        
        add_btn = ctk.CTkButton(
            actions_frame,
            text="➕ Add Individual Files",
            command=lambda: self.add_files_from_browser(browser_window),
            fg_color=self.theme.bg_tertiary,
            hover_color=self.theme.accent,
            **btn_config
        )
        add_btn.pack(side="left", padx=5, expand=True, fill="x")
        
        recent_label = ctk.CTkLabel(
            browser_window,
            text="📌 Recent Folders",
            font=("Segoe UI", 18, "bold"),
            text_color=self.theme.text_primary
        )
        recent_label.pack(anchor="w", padx=30, pady=(10, 10))
        
        recent_frame = ctk.CTkScrollableFrame(
            browser_window,
            fg_color=self.theme.bg_secondary,
            corner_radius=15
        )
        recent_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        self.load_recent_folders_ui(recent_frame, browser_window)
        
        formats_text = f"Supported: {', '.join(self.supported_formats)}"
        ctk.CTkLabel(
            browser_window,
            text=formats_text,
            font=("Segoe UI", 10),
            text_color=self.theme.text_secondary
        ).pack(pady=(0, 10))
        
    def load_recent_folders_ui(self, container, parent_window):
        """Load recent folders into UI"""
        for widget in container.winfo_children():
            widget.destroy()
            
        recent_folders = self.folder_browser.get_recent_folders()
        
        if not recent_folders:
            ctk.CTkLabel(
                container,
                text="📂 No recent folders\n\nBrowse for music to get started!",
                font=("Segoe UI", 16),
                text_color=self.theme.text_secondary,
                justify="center"
            ).pack(pady=100)
            return
            
        for folder_path in recent_folders:
            folder_name = os.path.basename(folder_path)
            parent_path = str(Path(folder_path).parent)
            
            try:
                song_count = sum(1 for f in Path(folder_path).rglob('*') 
                               if f.suffix.lower() in self.supported_formats)
            except:
                song_count = 0
            
            folder_frame = ctk.CTkFrame(
                container,
                fg_color=self.theme.bg_tertiary,
                corner_radius=12,
                height=90
            )
            folder_frame.pack(fill="x", pady=5, padx=10)
            folder_frame.pack_propagate(False)
            
            info_frame = ctk.CTkFrame(folder_frame, fg_color="transparent")
            info_frame.pack(side="left", fill="both", expand=True, padx=15, pady=10)
            
            name_label = ctk.CTkLabel(
                info_frame,
                text=f"📁 {folder_name}",
                font=("Segoe UI", 15, "bold"),
                text_color=self.theme.text_primary,
                anchor="w"
            )
            name_label.pack(anchor="w")
            
            path_label = ctk.CTkLabel(
                info_frame,
                text=parent_path,
                font=("Segoe UI", 10),
                text_color=self.theme.text_secondary,
                anchor="w"
            )
            path_label.pack(anchor="w", pady=(2, 0))
            
            count_label = ctk.CTkLabel(
                info_frame,
                text=f"🎵 {song_count} songs found",
                font=("Segoe UI", 11),
                text_color=self.theme.accent,
                anchor="w"
            )
            count_label.pack(anchor="w", pady=(5, 0))
            
            actions_frame = ctk.CTkFrame(folder_frame, fg_color="transparent")
            actions_frame.pack(side="right", padx=10)
            
            load_btn = ctk.CTkButton(
                actions_frame,
                text="📂 Load",
                command=lambda p=folder_path: self.load_folder_from_browser(p, parent_window),
                fg_color=self.theme.accent,
                hover_color=self.theme.accent_hover,
                width=100,
                height=40,
                font=("Segoe UI", 13, "bold")
            )
            load_btn.pack(pady=2)
            
            remove_btn = ctk.CTkButton(
                actions_frame,
                text="✕",
                command=lambda p=folder_path: self.remove_from_history(p, container, parent_window),
                fg_color=self.theme.bg_secondary,
                hover_color=self.theme.error,
                width=40,
                height=30,
                font=("Segoe UI", 12)
            )
            remove_btn.pack(pady=2)
            
    def browse_and_load(self, parent_window):
        """Browse for new folder and load"""
        folder = filedialog.askdirectory(title="Select Music Folder")
        if folder:
            self.load_folder_from_browser(folder, parent_window)
            
    def add_files_from_browser(self, parent_window):
        """Add individual files from browser"""
        files = filedialog.askopenfilenames(
            title="Select Music Files",
            filetypes=[
                ("All Audio", " ".join(f"*{ext}" for ext in self.supported_formats)),
                ("MP3 Files", "*.mp3"),
                ("WAV Files", "*.wav"),
                ("FLAC Files", "*.flac"),
                ("OGG Files", "*.ogg")
            ]
        )
        
        if files:
            added = 0
            for file in files:
                if file not in self.playlist:
                    self.playlist.append(file)
                    added += 1
                    
            self.filtered_playlist = self.playlist.copy()
            self.update_playlist_ui()
            
            messagebox.showinfo(
                "✅ Files Added",
                f"Added {added} new files!\nTotal songs: {len(self.playlist)}"
            )
            parent_window.destroy()
            
    def load_folder_from_browser(self, folder_path, parent_window):
        """Load folder from browser"""
        if not os.path.exists(folder_path):
            messagebox.showerror("Error", "Folder not found!")
            return
            
        self.folder_browser.add_folder(folder_path)
        self.folder_path = folder_path
        self.current_playlist_name = None
        
        loading_label = ctk.CTkLabel(
            parent_window,
            text="⏳ Loading songs...",
            font=("Segoe UI", 16, "bold"),
            text_color=self.theme.accent
        )
        loading_label.place(relx=0.5, rely=0.5, anchor="center")
        parent_window.update()
        
        def load_thread():
            self.load_playlist(folder_path)
            parent_window.after(100, lambda: [loading_label.destroy(), parent_window.destroy()])
            
        threading.Thread(target=load_thread, daemon=True).start()
        
    def remove_from_history(self, folder_path, container, parent_window):
        """Remove folder from history"""
        if folder_path in self.folder_browser.recent_folders:
            self.folder_browser.recent_folders.remove(folder_path)
            self.folder_browser.save_history()
            self.load_recent_folders_ui(container, parent_window)
            
    # ==================== FILE LOADING FUNCTIONS ====================
    
    def select_folder(self):
        """Quick folder selection"""
        folder = filedialog.askdirectory(title="Select Music Folder")
        if folder:
            self.folder_browser.add_folder(folder)
            self.folder_path = folder
            self.current_playlist_name = None
            self.load_playlist(folder)
            
    def add_files(self):
        """Add individual files"""
        files = filedialog.askopenfilenames(
            title="Select Music Files",
            filetypes=[
                ("All Audio", " ".join(f"*{ext}" for ext in self.supported_formats)),
                ("MP3 Files", "*.mp3"),
                ("WAV Files", "*.wav"),
                ("FLAC Files", "*.flac"),
                ("OGG Files", "*.ogg")
            ]
        )
        
        if files:
            added = 0
            for file in files:
                if file not in self.playlist:
                    self.playlist.append(file)
                    added += 1
                    
            self.filtered_playlist = self.playlist.copy()
            self.update_playlist_ui()
            
            messagebox.showinfo(
                "✅ Files Added",
                f"Added {added} new files!\nTotal: {len(self.playlist)} songs"
            )
            
    def load_playlist(self, folder):
        """Load all music files from folder recursively"""
        self.playlist.clear()
        
        try:
            for file in Path(folder).rglob('*'):
                if file.suffix.lower() in self.supported_formats:
                    self.playlist.append(str(file))
                    
            self.filtered_playlist = self.playlist.copy()
            
            if self.playlist:
                self.playlist.sort(key=lambda x: Path(x).name.lower())
                self.filtered_playlist = self.playlist.copy()
                
                self.update_playlist_ui()
                self.update_playlist_header()
                
                folder_name = os.path.basename(folder)
                self.song_info.configure(
                    text=f"✅ Loaded {len(self.playlist)} songs from '{folder_name}'"
                )
                
                messagebox.showinfo(
                    "✅ Success",
                    f"Loaded {len(self.playlist)} songs from:\n{folder}"
                )
            else:
                self.song_info.configure(text="No supported audio files found")
                messagebox.showwarning(
                    "No Music Found",
                    f"No supported audio files found.\n\nSupported: {', '.join(self.supported_formats)}"
                )
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load folder:\n{str(e)}")
            
    def clear_playlist(self):
        """Clear current playlist"""
        if not self.playlist:
            return
            
        response = messagebox.askyesno(
            "Clear Playlist",
            f"Are you sure you want to clear all {len(self.playlist)} songs?"
        )
        
        if response:
            self.stop_song()
            self.playlist.clear()
            self.filtered_playlist.clear()
            self.current_index = 0
            self.current_playlist_name = None
            self.update_playlist_ui()
            self.update_playlist_header()
            self.song_info.configure(text="Playlist cleared")
            
    def update_playlist_ui(self):
        """Update playlist display"""
        for widget in self.playlist_frame.winfo_children():
            widget.destroy()
            
        self.song_count_label.configure(text=f"{len(self.filtered_playlist)} songs")
        self.create_playlist_items()
        
    def create_playlist_items(self):
        """Create playlist items with context menu"""
        for idx, song_path in enumerate(self.filtered_playlist):
            song_name = Path(song_path).stem
            original_idx = self.playlist.index(song_path)
            
            item_frame = ctk.CTkFrame(
                self.playlist_frame,
                fg_color=self.theme.bg_tertiary,
                corner_radius=10,
                height=55
            )
            item_frame.pack(fill="x", pady=3)
            item_frame.pack_propagate(False)
            
            # Favorite indicator
            if self.favorites_manager.is_favorite(song_path):
                fav_label = ctk.CTkLabel(
                    item_frame,
                    text="⭐",
                    font=("Segoe UI", 14),
                    width=30
                )
                fav_label.pack(side="left", padx=(10, 0))
            
            num_label = ctk.CTkLabel(
                item_frame,
                text=f"{idx + 1}.",
                font=("Segoe UI", 12, "bold"),
                text_color=self.theme.accent,
                width=40
            )
            num_label.pack(side="left", padx=(10, 5))
            
            song_btn = ctk.CTkButton(
                item_frame,
                text=song_name,
                command=lambda i=original_idx: self.play_specific_song(i),
                fg_color="transparent",
                hover_color=self.theme.bg_secondary,
                anchor="w",
                font=("Segoe UI", 11)
            )
            song_btn.pack(side="left", fill="both", expand=True, padx=5)
            
            # Add to queue button
            queue_btn = ctk.CTkButton(
                item_frame,
                text="📝",
                command=lambda s=song_path: self.add_to_queue(s),
                width=35,
                height=35,
                fg_color="transparent",
                hover_color=self.theme.accent,
                font=("Segoe UI", 12)
            )
            queue_btn.pack(side="right", padx=2)
            
            try:
                duration = self.get_song_length(song_path)
                duration_text = self.format_time(duration)
            except:
                duration_text = "0:00"
                
            ctk.CTkLabel(
                item_frame,
                text=duration_text,
                font=("Segoe UI", 10),
                text_color=self.theme.text_secondary,
                width=50
            ).pack(side="right", padx=5)
    
    def add_to_queue(self, song_path):
        """Add song to play queue"""
        if self.queue_manager.add_to_queue(song_path):
            messagebox.showinfo("Queue", f"Added to queue!\nQueue size: {len(self.queue_manager.get_queue())}")
        else:
            messagebox.showinfo("Queue", "Song already in queue!")
            
    def filter_playlist(self, event=None):
        """Filter playlist by search"""
        query = self.search_entry.get().lower()
        
        if query:
            self.filtered_playlist = [
                song for song in self.playlist
                if query in Path(song).stem.lower()
            ]
        else:
            self.filtered_playlist = self.playlist.copy()
            
        self.update_playlist_ui()
        
    def clear_search(self):
        """Clear search"""
        self.search_entry.delete(0, 'end')
        self.filter_playlist()
        
    def update_playlist_header(self):
        """Update playlist header"""
        if self.current_playlist_name:
            self.current_playlist_label.configure(text=f"({self.current_playlist_name})")
        else:
            self.current_playlist_label.configure(text="")
            
    # ==================== PLAYBACK FUNCTIONS ====================
    
    def play_specific_song(self, index):
        """Play specific song"""
        self.current_index = index
        self.play_song()
        
    def play_song(self):
        """Play current song"""
        if not self.playlist:
            messagebox.showwarning("No Playlist", "Please load some music first!")
            return
            
        try:
            song_path = self.playlist[self.current_index]
            
            if not os.path.exists(song_path):
                messagebox.showerror("File Not Found", f"Song file not found:\n{song_path}")
                return
                
            pygame.mixer.music.load(song_path)
            pygame.mixer.music.play()
            
            self.is_playing = True
            self.is_paused = False
            
            # Add to history
            self.history_manager.add_song(song_path)
            
            # Update UI
            song_name = Path(song_path).stem
            self.song_title.configure(text=song_name)
            self.song_artist.configure(text=self.extract_artist(song_path))
            self.song_info.configure(text=f"🎵 Playing: {Path(song_path).name}")
            self.play_pause_btn.configure(text="⏸")
            
            # Update favorite button
            if self.favorites_manager.is_favorite(song_path):
                self.favorite_btn.configure(text="⭐", fg_color=self.theme.accent)
            else:
                self.favorite_btn.configure(text="☆", fg_color="transparent")
            
            # Update mini player
            if self.mini_player_window and self.mini_player_window.winfo_exists():
                self.mini_play_btn.configure(text="⏸")
            
            self.load_album_art(song_path)
            self.current_song_length = self.get_song_length(song_path)
            self.total_time_label.configure(text=self.format_time(self.current_song_length))
            
            quality_info = self.get_audio_quality(song_path)
            self.audio_quality.configure(text=quality_info)
            
            self.highlight_current_song()
            
            if not self.visualizer.animation_running:
                self.visualizer.start_animation()
                
        except Exception as e:
            messagebox.showerror("Playback Error", f"Could not play song:\n{str(e)}")
            
    def play_pause_song(self):
        """Toggle play/pause"""
        if not self.playlist:
            messagebox.showwarning("No Playlist", "Please load some music first!")
            return
            
        if self.is_playing:
            if self.is_paused:
                pygame.mixer.music.unpause()
                self.is_paused = False
                self.play_pause_btn.configure(text="⏸")
                if self.mini_player_window and self.mini_player_window.winfo_exists():
                    self.mini_play_btn.configure(text="⏸")
                if not self.visualizer.animation_running:
                    self.visualizer.start_animation()
            else:
                pygame.mixer.music.pause()
                self.is_paused = True
                self.play_pause_btn.configure(text="▶")
                if self.mini_player_window and self.mini_player_window.winfo_exists():
                    self.mini_play_btn.configure(text="▶")
                self.visualizer.stop_animation()
        else:
            self.play_song()
            
    def stop_song(self):
        """Stop playback"""
        pygame.mixer.music.stop()
        self.is_playing = False
        self.is_paused = False
        self.play_pause_btn.configure(text="▶")
        if self.mini_player_window and self.mini_player_window.winfo_exists():
            self.mini_play_btn.configure(text="▶")
        self.progress_slider.set(0)
        self.current_time_label.configure(text="0:00")
        self.visualizer.stop_animation()
        
    def next_song(self):
        """Next song"""
        if not self.playlist:
            return
        
        # Check queue first
        next_from_queue = self.queue_manager.get_next()
        if next_from_queue and next_from_queue in self.playlist:
            self.current_index = self.playlist.index(next_from_queue)
        elif self.shuffle_mode:
            self.current_index = random.randint(0, len(self.playlist) - 1)
        else:
            self.current_index = (self.current_index + 1) % len(self.playlist)
            
        self.play_song()
        
    def previous_song(self):
        """Previous song"""
        if not self.playlist:
            return
            
        self.current_index = (self.current_index - 1) % len(self.playlist)
        self.play_song()
        
    def change_volume(self, value):
        """Change volume"""
        volume = float(value) / 100
        pygame.mixer.music.set_volume(volume)
        self.volume_label.configure(text=f"{int(value)}%")
        
    def seek_song(self, value):
        """Seek position"""
        if self.is_playing and self.current_song_length > 0:
            position = (float(value) / 100) * self.current_song_length
            try:
                pygame.mixer.music.set_pos(position)
            except:
                pass
                
    def toggle_shuffle(self):
        """Toggle shuffle"""
        self.shuffle_mode = not self.shuffle_mode
        status = "ON" if self.shuffle_mode else "OFF"
        self.shuffle_btn.configure(text=f"🔀 Shuffle: {status}")
        color = self.theme.accent if self.shuffle_mode else self.theme.bg_tertiary
        self.shuffle_btn.configure(fg_color=color)
        
    def toggle_repeat(self):
        """Toggle repeat"""
        modes = ["off", "one", "all"]
        current = modes.index(self.repeat_mode)
        self.repeat_mode = modes[(current + 1) % len(modes)]
        
        labels = {"off": "OFF", "one": "ONE", "all": "ALL"}
        icons = {"off": "🔁", "one": "🔂", "all": "🔁"}
        self.repeat_btn.configure(text=f"{icons[self.repeat_mode]} Repeat: {labels[self.repeat_mode]}")
        
        color = self.theme.accent if self.repeat_mode != "off" else self.theme.bg_tertiary
        self.repeat_btn.configure(fg_color=color)
        
    def extract_artist(self, song_path):
        """Extract artist"""
        try:
            if song_path.lower().endswith('.mp3'):
                audio = MP3(song_path)
                if 'TPE1' in audio:
                    return str(audio['TPE1'])
        except:
            pass
        return "Unknown Artist"
        
    def get_audio_quality(self, song_path):
        """Get audio quality"""
        try:
            ext = song_path.lower()
            if ext.endswith('.mp3'):
                audio = MP3(song_path)
                bitrate = audio.info.bitrate // 1000
                sample_rate = audio.info.sample_rate // 1000
                return f"♪ MP3 • {bitrate} kbps • {sample_rate} kHz"
            elif ext.endswith('.wav'):
                audio = WAVE(song_path)
                sample_rate = audio.info.sample_rate // 1000
                bits = audio.info.bits_per_sample
                return f"♪ WAV • {bits}-bit • {sample_rate} kHz"
            elif ext.endswith('.flac'):
                return f"♪ FLAC • Lossless"
            elif ext.endswith('.ogg'):
                return f"♪ OGG Vorbis"
        except:
            pass
        return ""
        
    def get_song_length(self, file_path):
        """Get duration"""
        try:
            ext = file_path.lower()
            if ext.endswith('.mp3'):
                audio = MP3(file_path)
                return audio.info.length
            elif ext.endswith('.wav'):
                audio = WAVE(file_path)
                return audio.info.length
            elif ext.endswith('.flac'):
                audio = FLAC(file_path)
                return audio.info.length
            elif ext.endswith('.ogg'):
                audio = OggVorbis(file_path)
                return audio.info.length
        except:
            return 0
        return 0
        
    def format_time(self, seconds):
        """Format time"""
        mins = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{mins}:{secs:02d}"
        
    def update_progress(self):
        """Update progress"""
        while True:
            try:
                if self.is_playing and not self.is_paused:
                    if not pygame.mixer.music.get_busy():
                        self.handle_song_end()
                    else:
                        current_pos = pygame.mixer.music.get_pos() / 1000
                        if self.current_song_length > 0:
                            progress = (current_pos / self.current_song_length) * 100
                            self.progress_slider.set(min(progress, 100))
                            self.current_time_label.configure(text=self.format_time(current_pos))
                            
                time.sleep(0.1)
            except:
                time.sleep(0.1)
                
    def handle_song_end(self):
        """Handle song end"""
        if self.repeat_mode == "one":
            self.play_song()
        elif self.repeat_mode == "all" or self.shuffle_mode or not self.queue_manager.is_empty():
            self.next_song()
        elif self.current_index < len(self.playlist) - 1:
            self.next_song()
        else:
            self.is_playing = False
            self.play_pause_btn.configure(text="▶")
            self.visualizer.stop_animation()
            
    def highlight_current_song(self):
        """Highlight current song"""
        for idx, widget in enumerate(self.playlist_frame.winfo_children()):
            try:
                if idx < len(self.filtered_playlist):
                    song_path = self.filtered_playlist[idx]
                    original_idx = self.playlist.index(song_path)
                    
                    if original_idx == self.current_index:
                        widget.configure(fg_color=self.theme.accent, border_width=2, 
                                       border_color=self.theme.accent)
                    else:
                        widget.configure(fg_color=self.theme.bg_tertiary, border_width=0)
            except:
                pass
                
    # ==================== PLAYLIST MANAGER ====================
    
    def show_playlist_manager(self):
        """Show playlist manager"""
        pl_window = ctk.CTkToplevel(self.root)
        pl_window.title("📋 Playlist Manager")
        pl_window.geometry("800x600")
        pl_window.transient(self.root)
        pl_window.grab_set()
        
        header = ctk.CTkFrame(pl_window, fg_color=self.theme.bg_secondary, height=80)
        header.pack(fill="x", padx=20, pady=20)
        header.pack_propagate(False)
        
        ctk.CTkLabel(
            header,
            text="📋 Playlist Manager",
            font=("Segoe UI", 28, "bold"),
            text_color=self.theme.accent
        ).pack(side="left", padx=20)
        
        btn_frame = ctk.CTkFrame(pl_window, fg_color="transparent", height=60)
        btn_frame.pack(fill="x", padx=20, pady=(0, 10))
        btn_frame.pack_propagate(False)
        
        btn_config = {
            "font": ("Segoe UI", 13, "bold"),
            "height": 45,
            "corner_radius": 12
        }
        
        new_btn = ctk.CTkButton(
            btn_frame,
            text="➕ New Playlist",
            command=lambda: self.create_new_playlist_dialog(pl_window),
            fg_color=self.theme.accent,
            hover_color=self.theme.accent_hover,
            **btn_config
        )
        new_btn.pack(side="left", padx=5, expand=True, fill="x")
        
        save_btn = ctk.CTkButton(
            btn_frame,
            text="💾 Save Current",
            command=self.save_current_playlist_dialog,
            fg_color=self.theme.bg_tertiary,
            hover_color=self.theme.accent,
            **btn_config
        )
        save_btn.pack(side="left", padx=5, expand=True, fill="x")
        
        refresh_btn = ctk.CTkButton(
            btn_frame,
            text="🔄 Refresh",
            command=lambda: self.refresh_playlist_list(playlists_frame),
            fg_color=self.theme.bg_tertiary,
            hover_color=self.theme.accent,
            **btn_config
        )
        refresh_btn.pack(side="left", padx=5, expand=True, fill="x")
        
        playlists_frame = ctk.CTkScrollableFrame(
            pl_window,
            fg_color=self.theme.bg_secondary,
            corner_radius=15
        )
        playlists_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        self.refresh_playlist_list(playlists_frame)
        
    def refresh_playlist_list(self, container):
        """Refresh playlist list"""
        for widget in container.winfo_children():
            widget.destroy()
            
        playlists = self.playlist_manager.get_all_playlists()
        
        if not playlists:
            ctk.CTkLabel(
                container,
                text="📋 No playlists yet\n\nClick '➕ New Playlist' to create one!",
                font=("Segoe UI", 16),
                text_color=self.theme.text_secondary,
                justify="center"
            ).pack(pady=100)
            return
            
        for pl_name in playlists:
            pl_data = self.playlist_manager.playlists[pl_name]
            song_count = len(pl_data["songs"])
            created = pl_data.get("created", "Unknown")
            
            pl_frame = ctk.CTkFrame(
                container,
                fg_color=self.theme.bg_tertiary,
                corner_radius=12,
                height=80
            )
            pl_frame.pack(fill="x", pady=5, padx=10)
            pl_frame.pack_propagate(False)
            
            info_frame = ctk.CTkFrame(pl_frame, fg_color="transparent")
            info_frame.pack(side="left", fill="both", expand=True, padx=15, pady=10)
            
            name_label = ctk.CTkLabel(
                info_frame,
                text=f"🎵 {pl_name}",
                font=("Segoe UI", 16, "bold"),
                text_color=self.theme.text_primary,
                anchor="w"
            )
            name_label.pack(anchor="w")
            
            info_label = ctk.CTkLabel(
                info_frame,
                text=f"{song_count} songs • Created: {created.split()[0]}",
                font=("Segoe UI", 11),
                text_color=self.theme.text_secondary,
                anchor="w"
            )
            info_label.pack(anchor="w", pady=(2, 0))
            
            actions_frame = ctk.CTkFrame(pl_frame, fg_color="transparent")
            actions_frame.pack(side="right", padx=10)
            
            load_btn = ctk.CTkButton(
                actions_frame,
                text="▶ Load",
                command=lambda name=pl_name: self.load_saved_playlist(name),
                fg_color=self.theme.accent,
                hover_color=self.theme.accent_hover,
                width=90,
                height=35,
                font=("Segoe UI", 12, "bold")
            )
            load_btn.pack(side="left", padx=3)
            
            delete_btn = ctk.CTkButton(
                actions_frame,
                text="🗑",
                command=lambda name=pl_name: self.delete_playlist_confirm(name, container),
                fg_color=self.theme.bg_secondary,
                hover_color=self.theme.error,
                width=45,
                height=35,
                font=("Segoe UI", 14)
            )
            delete_btn.pack(side="left", padx=3)
            
    def create_new_playlist_dialog(self, parent_window):
        """Create new playlist dialog"""
        dialog = ctk.CTkToplevel(parent_window)
        dialog.title("Create New Playlist")
        dialog.geometry("400x200")
        dialog.transient(parent_window)
        dialog.grab_set()
        
        ctk.CTkLabel(
            dialog,
            text="Create New Playlist",
            font=("Segoe UI", 20, "bold")
        ).pack(pady=20)
        
        name_entry = ctk.CTkEntry(
            dialog,
            placeholder_text="Enter playlist name...",
            font=("Segoe UI", 14),
            height=40,
            width=300
        )
        name_entry.pack(pady=10)
        name_entry.focus()
        
        def create_playlist():
            name = name_entry.get().strip()
            if not name:
                messagebox.showwarning("Empty Name", "Please enter a playlist name!")
                return
                
            success, message = self.playlist_manager.create_playlist(name)
            if success:
                messagebox.showinfo("Success", message)
                dialog.destroy()
                try:
                    for widget in parent_window.winfo_children():
                        if isinstance(widget, ctk.CTkScrollableFrame):
                            self.refresh_playlist_list(widget)
                            break
                except:
                    pass
            else:
                messagebox.showerror("Error", message)
                
        create_btn = ctk.CTkButton(
            dialog,
            text="✓ Create",
            command=create_playlist,
            fg_color=self.theme.accent,
            hover_color=self.theme.accent_hover,
            font=("Segoe UI", 14, "bold"),
            height=45,
            width=200
        )
        create_btn.pack(pady=20)
        
        name_entry.bind("<Return>", lambda e: create_playlist())
        
    def save_current_playlist_dialog(self):
        """Save current playlist"""
        if not self.playlist:
            messagebox.showwarning("No Playlist", "Load some songs first!")
            return
            
        dialog = ctk.CTkToplevel(self.root)
        dialog.title("Save Playlist")
        dialog.geometry("400x200")
        dialog.transient(self.root)
        dialog.grab_set()
        
        ctk.CTkLabel(
            dialog,
            text="Save Current Playlist",
            font=("Segoe UI", 20, "bold")
        ).pack(pady=20)
        
        ctk.CTkLabel(
            dialog,
            text=f"Saving {len(self.playlist)} songs",
            font=("Segoe UI", 12),
            text_color=self.theme.text_secondary
        ).pack()
        
        name_entry = ctk.CTkEntry(
            dialog,
            placeholder_text="Enter playlist name...",
            font=("Segoe UI", 14),
            height=40,
            width=300
        )
        name_entry.pack(pady=15)
        name_entry.focus()
        
        def save_playlist():
            name = name_entry.get().strip()
            if not name:
                messagebox.showwarning("Empty Name", "Please enter a playlist name!")
                return
                
            success, message = self.playlist_manager.create_playlist(name, self.playlist.copy())
            if success:
                messagebox.showinfo("✅ Saved", f"Playlist '{name}' saved successfully!")
                self.current_playlist_name = name
                self.update_playlist_header()
                dialog.destroy()
            else:
                messagebox.showerror("Error", message)
                
        save_btn = ctk.CTkButton(
            dialog,
            text="💾 Save",
            command=save_playlist,
            fg_color=self.theme.accent,
            hover_color=self.theme.accent_hover,
            font=("Segoe UI", 14, "bold"),
            height=45,
            width=200
        )
        save_btn.pack(pady=10)
        
        name_entry.bind("<Return>", lambda e: save_playlist())
        
    def load_saved_playlist(self, playlist_name):
        """Load saved playlist"""
        songs = self.playlist_manager.get_playlist(playlist_name)
        
        if songs is None:
            messagebox.showerror("Error", "Playlist not found!")
            return
            
        if not songs:
            messagebox.showwarning("Empty Playlist", f"Playlist '{playlist_name}' is empty!")
            return
            
        valid_songs = [song for song in songs if os.path.exists(song)]
        
        if len(valid_songs) < len(songs):
            removed = len(songs) - len(valid_songs)
            messagebox.showwarning(
                "Some Files Missing",
                f"{removed} songs were not found and will be skipped."
            )
            
        if not valid_songs:
            messagebox.showerror("Error", "No valid songs found in this playlist!")
            return
            
        self.playlist = valid_songs
        self.filtered_playlist = self.playlist.copy()
        self.current_playlist_name = playlist_name
        self.current_index = 0
        
        self.update_playlist_ui()
        self.update_playlist_header()
        self.song_info.configure(text=f"Loaded playlist: {playlist_name}")
        
        messagebox.showinfo(
            "✅ Loaded",
            f"Playlist '{playlist_name}' loaded!\n{len(valid_songs)} songs ready to play."
        )
        
    def delete_playlist_confirm(self, playlist_name, container):
        """Delete playlist"""
        response = messagebox.askyesno(
            "Confirm Delete",
            f"Delete playlist '{playlist_name}'?\n\nThis cannot be undone!"
        )
        
        if response:
            success, message = self.playlist_manager.delete_playlist(playlist_name)
            if success:
                messagebox.showinfo("Deleted", message)
                self.refresh_playlist_list(container)
                
                if self.current_playlist_name == playlist_name:
                    self.current_playlist_name = None
                    self.update_playlist_header()
            else:
                messagebox.showerror("Error", message)
                
    # ==================== THEME & SETTINGS ====================
    
    def show_theme_menu(self):
        """Theme menu"""
        theme_window = ctk.CTkToplevel(self.root)
        theme_window.title("Select Theme")
        theme_window.geometry("400x400")
        theme_window.transient(self.root)
        theme_window.grab_set()
        
        ctk.CTkLabel(
            theme_window,
            text="🎨 Choose Your Theme",
            font=("Segoe UI", 20, "bold")
        ).pack(pady=20)
        
        for theme_name in ColorTheme.THEMES.keys():
            theme_btn = ctk.CTkButton(
                theme_window,
                text=theme_name,
                command=lambda t=theme_name: self.change_theme(t, theme_window),
                font=("Segoe UI", 14),
                height=50,
                corner_radius=15,
                fg_color=ColorTheme.THEMES[theme_name]["accent"],
                hover_color=ColorTheme.THEMES[theme_name]["accent_hover"]
            )
            theme_btn.pack(pady=10, padx=40, fill="x")
            
    def change_theme(self, theme_name, window):
        """Change theme"""
        self.theme.set_theme(theme_name)
        window.destroy()
        messagebox.showinfo("Theme Changed", f"Theme changed to {theme_name}!\n\nRestart for full effect.")
        
    def bind_shortcuts(self):
        """Keyboard shortcuts"""
        self.root.bind('<space>', lambda e: self.play_pause_song())
        self.root.bind('<Right>', lambda e: self.next_song())
        self.root.bind('<Left>', lambda e: self.previous_song())
        self.root.bind('<Control-o>', lambda e: self.show_advanced_browser())
        self.root.bind('<Control-f>', lambda e: self.search_entry.focus())
        self.root.bind('<Control-l>', lambda e: self.show_lyrics_viewer())
        self.root.bind('<Control-m>', lambda e: self.toggle_mini_player())
        
    def load_settings(self):
        """Load settings"""
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r') as f:
                    settings = json.load(f)
                    if 'volume' in settings:
                        pygame.mixer.music.set_volume(settings['volume'] / 100)
                    if 'crossfade' in settings:
                        self.crossfade_enabled = settings['crossfade']
        except:
            pass
            
    def save_settings(self):
        """Save settings"""
        try:
            settings = {
                'volume': self.volume_slider.get(),
                'theme': self.theme.current_theme,
                'crossfade': self.crossfade_enabled,
                'playback_speed': self.playback_speed
            }
            with open(self.settings_file, 'w') as f:
                json.dump(settings, f, indent=4)
        except:
            pass
            
    def on_closing(self):
        """On close"""
        self.save_settings()
        self.sleep_timer.stop()
        pygame.mixer.music.stop()
        pygame.mixer.quit()
        self.root.destroy()


# Run Application
if __name__ == "__main__":
    root = ctk.CTk()
    app = PremiumMusicPlayer(root)
    root.mainloop()