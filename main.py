import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import os
import subprocess
import platform
from pathlib import Path

class ImageToPDFConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("✨ Image to PDF Converter Pro")
        self.root.geometry("1100x750")
        self.root.configure(bg="#1a1a2e")
        self.root.resizable(True, True)
        
        # Modern color scheme
        self.colors = {
            'bg_primary': '#1a1a2e',
            'bg_secondary': '#16213e',
            'bg_card': '#0f3460',
            'accent': '#e94560',
            'accent_hover': '#c73650',
            'success': '#27ae60',
            'warning': '#f39c12',
            'text_primary': '#ffffff',
            'text_secondary': '#bdc3c7',
            'border': '#34495e'
        }
        
        # Store selected images and thumbnails
        self.image_files = []
        self.thumbnails = {}
        
        self.setup_styles()
        self.setup_ui()
        
    def setup_styles(self):
        """Configure modern ttk styles"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure progressbar style
        style.configure("Modern.Horizontal.TProgressbar",
                       background=self.colors['accent'],
                       troughcolor=self.colors['bg_secondary'],
                       borderwidth=0,
                       lightcolor=self.colors['accent'],
                       darkcolor=self.colors['accent'])
        
    def setup_ui(self):
        # Main container with padding
        main_container = tk.Frame(self.root, bg=self.colors['bg_primary'])
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header section
        self.create_header(main_container)
        
        # Action buttons section
        self.create_action_buttons(main_container)
        
        # Content area with file list and thumbnails
        self.create_content_area(main_container)
        
        # Progress and status section
        self.create_progress_section(main_container)
        
    def create_header(self, parent):
        """Create modern header with gradient-like effect"""
        header_frame = tk.Frame(parent, bg=self.colors['bg_primary'])
        header_frame.pack(fill=tk.X, pady=(0, 30))
        
        # Main title with emoji
        title_label = tk.Label(
            header_frame,
            text="🖼️ ➡️ 📄",
            font=("Segoe UI Emoji", 32),
            bg=self.colors['bg_primary'],
            fg=self.colors['text_primary']
        )
        title_label.pack()
        
        title_text = tk.Label(
            header_frame,
            text="Image to PDF Converter Pro",
            font=("Segoe UI", 24, "bold"),
            bg=self.colors['bg_primary'],
            fg=self.colors['text_primary']
        )
        title_text.pack(pady=(5, 0))
        
        subtitle = tk.Label(
            header_frame,
            text="Transform your images into beautiful PDF documents",
            font=("Segoe UI", 11),
            bg=self.colors['bg_primary'],
            fg=self.colors['text_secondary']
        )
        subtitle.pack(pady=(5, 0))
        
    def create_action_buttons(self, parent):
        """Create modern action buttons with hover effects"""
        button_container = tk.Frame(parent, bg=self.colors['bg_primary'])
        button_container.pack(pady=(0, 25))
        
        # Button frame with card-like appearance
        button_card = tk.Frame(
            button_container, 
            bg=self.colors['bg_card'],
            relief=tk.FLAT,
            bd=0
        )
        button_card.pack(padx=20, pady=10)
        
        # Add some padding inside the card
        inner_frame = tk.Frame(button_card, bg=self.colors['bg_card'])
        inner_frame.pack(padx=25, pady=20)
        
        # Select images button
        self.select_btn = self.create_modern_button(
            inner_frame,
            text="📁 Select Images",
            command=self.select_images,
            bg_color=self.colors['success'],
            hover_color='#229954'
        )
        self.select_btn.pack(side=tk.LEFT, padx=(0, 15))
        
        # Clear selection button
        self.clear_btn = self.create_modern_button(
            inner_frame,
            text="🗑️ Clear All",
            command=self.clear_selection,
            bg_color=self.colors['warning'],
            hover_color='#e67e22'
        )
        self.clear_btn.pack(side=tk.LEFT, padx=(0, 15))
        
        # Convert button
        self.convert_btn = self.create_modern_button(
            inner_frame,
            text="✨ Convert to PDF",
            command=self.convert_to_pdf,
            bg_color=self.colors['accent'],
            hover_color=self.colors['accent_hover'],
            state=tk.DISABLED
        )
        self.convert_btn.pack(side=tk.LEFT)
        
    def create_modern_button(self, parent, text, command, bg_color, hover_color, state=tk.NORMAL):
        """Create a modern button with hover effects"""
        btn = tk.Button(
            parent,
            text=text,
            command=command,
            font=("Segoe UI", 11, "bold"),
            bg=bg_color,
            fg=self.colors['text_primary'],
            activebackground=hover_color,
            activeforeground=self.colors['text_primary'],
            relief=tk.FLAT,
            bd=0,
            padx=25,
            pady=12,
            cursor="hand2",
            state=state
        )
        
        # Hover effects
        def on_enter(e):
            if btn['state'] != tk.DISABLED:
                btn.config(bg=hover_color)
                
        def on_leave(e):
            if btn['state'] != tk.DISABLED:
                btn.config(bg=bg_color)
                
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        
        return btn
        
    def create_content_area(self, parent):
        """Create content area with file list and thumbnail preview"""
        content_container = tk.Frame(parent, bg=self.colors['bg_primary'])
        content_container.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        # Left side - File list
        self.create_file_list_section(content_container)
        
        # Right side - Thumbnail preview
        self.create_thumbnail_section(content_container)
        
    def create_file_list_section(self, parent):
        """Create modern file list with card design"""
        list_container = tk.Frame(parent, bg=self.colors['bg_primary'])
        list_container.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Card for file list
        list_card = tk.Frame(
            list_container,
            bg=self.colors['bg_card'],
            relief=tk.FLAT,
            bd=0
        )
        list_card.pack(fill=tk.BOTH, expand=True)
        
        # Header for file list
        list_header = tk.Frame(list_card, bg=self.colors['bg_card'])
        list_header.pack(fill=tk.X, padx=20, pady=(20, 10))
        
        list_title = tk.Label(
            list_header,
            text="📋 Selected Images",
            font=("Segoe UI", 14, "bold"),
            bg=self.colors['bg_card'],
            fg=self.colors['text_primary']
        )
        list_title.pack(side=tk.LEFT)
        
        self.file_count_label = tk.Label(
            list_header,
            text="0 files",
            font=("Segoe UI", 10),
            bg=self.colors['bg_card'],
            fg=self.colors['text_secondary']
        )
        self.file_count_label.pack(side=tk.RIGHT)
        
        # Main content area with listbox and controls
        content_frame = tk.Frame(list_card, bg=self.colors['bg_card'])
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        # Listbox container
        listbox_container = tk.Frame(content_frame, bg=self.colors['bg_card'])
        listbox_container.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Modern listbox
        self.listbox = tk.Listbox(
            listbox_container,
            font=("Segoe UI", 10),
            bg=self.colors['bg_secondary'],
            fg=self.colors['text_primary'],
            selectbackground=self.colors['accent'],
            selectforeground=self.colors['text_primary'],
            relief=tk.FLAT,
            bd=0,
            highlightthickness=0,
            activestyle='none'
        )
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Bind selection event for thumbnail preview
        self.listbox.bind('<<ListboxSelect>>', self.on_file_select)
        
        # Modern scrollbar
        scrollbar = tk.Scrollbar(
            listbox_container,
            bg=self.colors['bg_secondary'],
            troughcolor=self.colors['bg_secondary'],
            activebackground=self.colors['accent'],
            relief=tk.FLAT,
            bd=0,
            width=12
        )
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.listbox.yview)
        
        # Control buttons for reordering
        control_frame = tk.Frame(content_frame, bg=self.colors['bg_card'])
        control_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(15, 0))
        
        # Reorder label
        reorder_label = tk.Label(
            control_frame,
            text="📝 Reorder",
            font=("Segoe UI", 10, "bold"),
            bg=self.colors['bg_card'],
            fg=self.colors['text_primary']
        )
        reorder_label.pack(pady=(0, 10))
        
        # Move up button
        self.move_up_btn = self.create_control_button(
            control_frame,
            text="⬆️",
            command=self.move_up,
            tooltip="Move selected image up"
        )
        self.move_up_btn.pack(pady=(0, 5))
        
        # Move down button
        self.move_down_btn = self.create_control_button(
            control_frame,
            text="⬇️",
            command=self.move_down,
            tooltip="Move selected image down"
        )
        self.move_down_btn.pack(pady=(0, 15))
        
        # Remove button
        self.remove_btn = self.create_control_button(
            control_frame,
            text="❌",
            command=self.remove_selected,
            tooltip="Remove selected image",
            bg_color=self.colors['accent']
        )
        self.remove_btn.pack(pady=(0, 15))
        
        # Separator
        separator = tk.Frame(control_frame, bg=self.colors['text_secondary'], height=1)
        separator.pack(fill=tk.X, pady=(0, 15))
        
        # Auto-sort button
        self.sort_btn = self.create_control_button(
            control_frame,
            text="🔤",
            command=self.sort_alphabetically,
            tooltip="Sort alphabetically",
            bg_color=self.colors['success']
        )
        self.sort_btn.pack()
        
    def create_control_button(self, parent, text, command, tooltip="", bg_color=None):
        """Create a small control button for reordering"""
        if bg_color is None:
            bg_color = self.colors['bg_secondary']
            
        btn = tk.Button(
            parent,
            text=text,
            command=command,
            font=("Segoe UI", 12),
            bg=bg_color,
            fg=self.colors['text_primary'],
            activebackground=self.colors['accent'],
            activeforeground=self.colors['text_primary'],
            relief=tk.FLAT,
            bd=0,
            width=3,
            height=1,
            cursor="hand2"
        )
        
        # Hover effects
        def on_enter(e):
            btn.config(bg=self.colors['accent'])
            
        def on_leave(e):
            btn.config(bg=bg_color)
            
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        
        # Tooltip (simple implementation)
        if tooltip:
            def show_tooltip(e):
                # Simple tooltip - could be enhanced with a proper tooltip widget
                pass
            btn.bind("<Button-3>", show_tooltip)  # Right click for tooltip
        
        return btn
        
    def create_thumbnail_section(self, parent):
        """Create thumbnail preview section"""
        thumbnail_container = tk.Frame(parent, bg=self.colors['bg_primary'])
        thumbnail_container.pack(side=tk.RIGHT, fill=tk.Y, padx=(10, 0))
        
        # Card for thumbnail
        thumbnail_card = tk.Frame(
            thumbnail_container,
            bg=self.colors['bg_card'],
            relief=tk.FLAT,
            bd=0,
            width=300
        )
        thumbnail_card.pack(fill=tk.BOTH, expand=True)
        thumbnail_card.pack_propagate(False)
        
        # Header for thumbnail
        thumbnail_header = tk.Frame(thumbnail_card, bg=self.colors['bg_card'])
        thumbnail_header.pack(fill=tk.X, padx=20, pady=(20, 10))
        
        thumbnail_title = tk.Label(
            thumbnail_header,
            text="🖼️ Preview",
            font=("Segoe UI", 14, "bold"),
            bg=self.colors['bg_card'],
            fg=self.colors['text_primary']
        )
        thumbnail_title.pack()
        
        # Thumbnail display area
        self.thumbnail_frame = tk.Frame(thumbnail_card, bg=self.colors['bg_card'])
        self.thumbnail_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        # Default message
        self.thumbnail_label = tk.Label(
            self.thumbnail_frame,
            text="Select an image\nto see preview",
            font=("Segoe UI", 12),
            bg=self.colors['bg_card'],
            fg=self.colors['text_secondary'],
            justify=tk.CENTER
        )
        self.thumbnail_label.pack(expand=True)
        
        # Image info label
        self.image_info_label = tk.Label(
            self.thumbnail_frame,
            text="",
            font=("Segoe UI", 9),
            bg=self.colors['bg_card'],
            fg=self.colors['text_secondary'],
            justify=tk.CENTER,
            wraplength=250
        )
        self.image_info_label.pack(pady=(10, 0))
        
    def create_progress_section(self, parent):
        """Create modern progress and status section"""
        progress_container = tk.Frame(parent, bg=self.colors['bg_primary'])
        progress_container.pack(fill=tk.X)
        
        # Progress card
        progress_card = tk.Frame(
            progress_container,
            bg=self.colors['bg_card'],
            relief=tk.FLAT,
            bd=0
        )
        progress_card.pack(fill=tk.X, padx=20, pady=10)
        
        # Progress content
        progress_content = tk.Frame(progress_card, bg=self.colors['bg_card'])
        progress_content.pack(fill=tk.X, padx=20, pady=15)
        
        # Progress bar
        self.progress = ttk.Progressbar(
            progress_content,
            mode='determinate',
            length=400,
            style="Modern.Horizontal.TProgressbar"
        )
        self.progress.pack(fill=tk.X, pady=(0, 10))
        
        # Status label
        self.status_label = tk.Label(
            progress_content,
            text="🚀 Ready to convert images to PDF",
            font=("Segoe UI", 10),
            bg=self.colors['bg_card'],
            fg=self.colors['text_secondary']
        )
        self.status_label.pack()
        
    def on_file_select(self, event):
        """Handle file selection in listbox"""
        selection = self.listbox.curselection()
        if selection:
            index = selection[0]
            if index < len(self.image_files):
                self.show_thumbnail(self.image_files[index])
                # Update status with current selection info
                filename = os.path.basename(self.image_files[index])
                self.status_label.config(text=f"📷 Viewing: {filename} ({index+1}/{len(self.image_files)})")
        else:
            self.clear_thumbnail()
            
    def show_thumbnail(self, image_path):
        """Display thumbnail for selected image"""
        try:
            # Clear previous thumbnail
            for widget in self.thumbnail_frame.winfo_children():
                widget.destroy()
                
            # Load and resize image
            img = Image.open(image_path)
            
            # Calculate thumbnail size maintaining aspect ratio
            max_size = (250, 250)
            img.thumbnail(max_size, Image.Resampling.LANCZOS)
            
            # Convert to PhotoImage
            photo = ImageTk.PhotoImage(img)
            
            # Store reference to prevent garbage collection
            self.current_thumbnail = photo
            
            # Display thumbnail
            thumbnail_label = tk.Label(
                self.thumbnail_frame,
                image=photo,
                bg=self.colors['bg_card'],
                relief=tk.FLAT,
                bd=2
            )
            thumbnail_label.pack(pady=10)
            
            # Display image info
            filename = os.path.basename(image_path)
            file_size = os.path.getsize(image_path)
            size_str = self.format_file_size(file_size)
            
            # Get image dimensions
            original_img = Image.open(image_path)
            width, height = original_img.size
            
            info_text = f"{filename}\n{width} × {height} pixels\n{size_str}"
            
            info_label = tk.Label(
                self.thumbnail_frame,
                text=info_text,
                font=("Segoe UI", 9),
                bg=self.colors['bg_card'],
                fg=self.colors['text_secondary'],
                justify=tk.CENTER,
                wraplength=250
            )
            info_label.pack(pady=(10, 0))
            
        except Exception as e:
            # Show error message
            error_label = tk.Label(
                self.thumbnail_frame,
                text=f"Cannot preview\n{os.path.basename(image_path)}",
                font=("Segoe UI", 10),
                bg=self.colors['bg_card'],
                fg=self.colors['warning'],
                justify=tk.CENTER
            )
            error_label.pack(expand=True)
            
    def clear_thumbnail(self):
        """Clear thumbnail display"""
        for widget in self.thumbnail_frame.winfo_children():
            widget.destroy()
            
        self.thumbnail_label = tk.Label(
            self.thumbnail_frame,
            text="Select an image\nto see preview",
            font=("Segoe UI", 12),
            bg=self.colors['bg_card'],
            fg=self.colors['text_secondary'],
            justify=tk.CENTER
        )
        self.thumbnail_label.pack(expand=True)
        
    def open_file(self, filepath):
        """Open file with default system application"""
        try:
            if platform.system() == 'Darwin':       # macOS
                subprocess.call(('open', filepath))
            elif platform.system() == 'Windows':    # Windows
                os.startfile(filepath)
            else:                                   # linux variants
                subprocess.call(('xdg-open', filepath))
        except Exception as e:
            messagebox.showerror("Error", f"Could not open file: {str(e)}")
            
    def select_images(self):
        """Open file dialog to select image files"""
        file_types = [
            ("Image files", "*.jpg *.jpeg *.png *.bmp *.tiff *.gif *.webp"),
            ("JPEG files", "*.jpg *.jpeg"),
            ("PNG files", "*.png"),
            ("All files", "*.*")
        ]
        
        files = filedialog.askopenfilenames(
            title="🖼️ Select Image Files",
            filetypes=file_types
        )
        
        if files:
            # Add new files to existing selection
            for file in files:
                if file not in self.image_files:
                    self.image_files.append(file)
            
            self.update_file_list()
            self.update_convert_button()
            
    def clear_selection(self):
        """Clear all selected images"""
        self.image_files.clear()
        self.thumbnails.clear()
        self.update_file_list()
        self.update_convert_button()
        self.clear_thumbnail()
        self.status_label.config(text="🧹 Selection cleared - Ready for new images")
        
    def update_file_list(self):
        """Update the listbox with selected files"""
        self.listbox.delete(0, tk.END)
        for i, file in enumerate(self.image_files, 1):
            filename = os.path.basename(file)
            # Add file size info
            try:
                size = os.path.getsize(file)
                size_str = self.format_file_size(size)
                display_text = f"{i:2d}. {filename} ({size_str})"
            except:
                display_text = f"{i:2d}. {filename}"
            self.listbox.insert(tk.END, display_text)
            
        # Update file count
        count = len(self.image_files)
        self.file_count_label.config(text=f"{count} file{'s' if count != 1 else ''}")
            
    def format_file_size(self, size_bytes):
        """Format file size in human readable format"""
        if size_bytes < 1024:
            return f"{size_bytes} B"
        elif size_bytes < 1024 * 1024:
            return f"{size_bytes / 1024:.1f} KB"
        else:
            return f"{size_bytes / (1024 * 1024):.1f} MB"
            
    def update_convert_button(self):
        """Enable/disable convert button based on selection"""
        if self.image_files:
            self.convert_btn.config(
                state=tk.NORMAL,
                bg=self.colors['accent']
            )
            count = len(self.image_files)
            self.status_label.config(text=f"✅ {count} image{'s' if count != 1 else ''} selected - Ready to convert!")
        else:
            self.convert_btn.config(
                state=tk.DISABLED,
                bg=self.colors['border']
            )
            self.status_label.config(text="📁 No images selected - Click 'Select Images' to begin")
            
    def convert_to_pdf(self):
        """Convert selected images to PDF"""
        if not self.image_files:
            messagebox.showwarning("⚠️ No Images", "Please select images first!")
            return
            
        # Ask for output file location
        output_file = filedialog.asksaveasfilename(
            title="💾 Save PDF as",
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
        )
        
        if not output_file:
            return
            
        try:
            self.progress.config(maximum=len(self.image_files))
            self.progress['value'] = 0
            self.root.update()
            
            # Convert images to PIL Image objects
            images = []
            for i, image_file in enumerate(self.image_files):
                filename = os.path.basename(image_file)
                self.status_label.config(text=f"🔄 Processing {filename}... ({i+1}/{len(self.image_files)})")
                self.root.update()
                
                # Open and convert image
                img = Image.open(image_file)
                
                # Convert to RGB if necessary (for PDF compatibility)
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                    
                images.append(img)
                
                # Update progress
                self.progress['value'] = i + 1
                self.root.update()
                
            # Save as PDF
            self.status_label.config(text="💾 Saving PDF document...")
            self.root.update()
            
            if images:
                # Save the first image as PDF with the rest as additional pages
                images[0].save(
                    output_file,
                    "PDF",
                    resolution=100.0,
                    save_all=True,
                    append_images=images[1:] if len(images) > 1 else []
                )
                
            self.progress['value'] = len(self.image_files)
            self.status_label.config(text=f"🎉 PDF created successfully: {os.path.basename(output_file)}")
            
            # Ask if user wants to open the PDF
            result = messagebox.askyesno(
                "🎉 Success!", 
                f"PDF created successfully!\n\n📄 File: {os.path.basename(output_file)}\n📁 Location: {os.path.dirname(output_file)}\n📊 Pages: {len(images)}\n\nWould you like to open the PDF now?"
            )
            
            if result:
                self.open_file(output_file)
            
        except Exception as e:
            messagebox.showerror("❌ Error", f"An error occurred during conversion:\n\n{str(e)}")
            self.status_label.config(text="❌ Error occurred during conversion")
        finally:
            self.progress['value'] = 0
            
    def move_up(self):
        """Move selected image up in the list"""
        selection = self.listbox.curselection()
        if not selection:
            return
            
        index = selection[0]
        if index > 0:
            # Swap items in the list
            self.image_files[index], self.image_files[index-1] = self.image_files[index-1], self.image_files[index]
            
            # Update the display
            self.update_file_list()
            
            # Maintain selection on the moved item
            self.listbox.selection_set(index-1)
            self.listbox.see(index-1)
            
            # Update thumbnail if this item is selected
            self.on_file_select(None)
            
    def move_down(self):
        """Move selected image down in the list"""
        selection = self.listbox.curselection()
        if not selection:
            return
            
        index = selection[0]
        if index < len(self.image_files) - 1:
            # Swap items in the list
            self.image_files[index], self.image_files[index+1] = self.image_files[index+1], self.image_files[index]
            
            # Update the display
            self.update_file_list()
            
            # Maintain selection on the moved item
            self.listbox.selection_set(index+1)
            self.listbox.see(index+1)
            
            # Update thumbnail if this item is selected
            self.on_file_select(None)
            
    def remove_selected(self):
        """Remove selected image from the list"""
        selection = self.listbox.curselection()
        if not selection:
            return
            
        index = selection[0]
        if index < len(self.image_files):
            # Remove from list
            removed_file = self.image_files.pop(index)
            
            # Update display
            self.update_file_list()
            self.update_convert_button()
            
            # Clear thumbnail if this was the selected item
            if not self.image_files:
                self.clear_thumbnail()
            else:
                # Select next item or previous if at end
                new_index = min(index, len(self.image_files) - 1)
                self.listbox.selection_set(new_index)
                self.on_file_select(None)
            
            self.status_label.config(text=f"🗑️ Removed {os.path.basename(removed_file)}")
            
    def sort_alphabetically(self):
        """Sort images alphabetically by filename"""
        if len(self.image_files) < 2:
            return
            
        # Sort by filename
        self.image_files.sort(key=lambda x: os.path.basename(x).lower())
        
        # Update display
        self.update_file_list()
        
        # Clear selection and thumbnail
        self.listbox.selection_clear(0, tk.END)
        self.clear_thumbnail()
        
        self.status_label.config(text="🔤 Images sorted alphabetically")

def main():
    root = tk.Tk()
    
    # Hide console window on Windows
    try:
        import sys
        if sys.platform == "win32":
            import ctypes
            ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
    except:
        pass  # Silently continue if hiding console fails
    
    # Set window icon (if available)
    try:
        root.iconbitmap(default="icon.ico")  # You can add an icon file
    except:
        pass
    
    # Center window on screen
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (1100 // 2)
    y = (root.winfo_screenheight() // 2) - (750 // 2)
    root.geometry(f"1100x750+{x}+{y}")
    
    app = ImageToPDFConverter(root)
    root.mainloop()

if __name__ == "__main__":
    main()
