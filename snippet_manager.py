import customtkinter as ctk
from tkinter import messagebox
import json
import os
import sys

def get_data_file_path():
    """Kullanıcının AppData klasöründe veri dosyası yolu döndürür"""
    if sys.platform == "win32":
        # Windows için AppData/Local klasörü
        app_data = os.path.join(os.environ['LOCALAPPDATA'], 'SnippetManager')
    else:
        # Linux/Mac için home directory
        app_data = os.path.join(os.path.expanduser('~'), '.snippet_manager')
    
    # Klasör yoksa oluştur
    if not os.path.exists(app_data):
        os.makedirs(app_data)
    
    return os.path.join(app_data, 'snippets_data.json')

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class SnippetManager(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Kod Bloğu Yöneticisi")
        self.geometry("1100x700")

        self.current_theme = "dark"
        self.snippets = {}
        self.selected_snippet = None
        self.is_editing = False
        self.original_description = None  
        self.data_file = get_data_file_path()  # Değişti

        self.create_ui()
        self.load_data()  

        self.set_editable(True)

    def create_ui(self):
        self.sidebar = ctk.CTkFrame(self, width=280, corner_radius=0)
        self.sidebar.pack(side="left", fill="y")

        ctk.CTkLabel(
            self.sidebar, text="Kod Bloğu Listesi", font=ctk.CTkFont(size=18, weight="bold")
        ).pack(pady=(20, 10))

        self.snippet_listbox = ctk.CTkTextbox(self.sidebar, width=260, height=520, state="disabled", wrap="none")
        self.snippet_listbox.pack(padx=10, pady=10, fill="y")
        self.snippet_listbox.bind("<Button-1>", self.on_snippet_click)

        self.theme_button = ctk.CTkButton(self.sidebar, text="🌗 Tema Değiştir", command=self.toggle_theme)
        self.theme_button.pack(pady=(10, 20))

        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(side="right", expand=True, fill="both", padx=10, pady=10)

        ctk.CTkLabel(self.main_frame, text="Açıklama", font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w", pady=(5, 0))
        self.desc_entry = ctk.CTkTextbox(self.main_frame, height=60)
        self.desc_entry.pack(fill="x", padx=5, pady=(0, 10))

        ctk.CTkLabel(self.main_frame, text="Kod Bloğu", font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w", pady=(10, 0))
        self.code_text = ctk.CTkTextbox(
            self.main_frame,
            height=300,
            font=ctk.CTkFont(family="JetBrains Mono", size=13),
            corner_radius=10
        )
        self.code_text.pack(fill="both", expand=True, padx=5, pady=(0, 10))
        self.update_code_colors() 

        self.button_frame = ctk.CTkFrame(self.main_frame)
        self.button_frame.pack(fill="x", pady=10)

        self.add_button = ctk.CTkButton(self.button_frame, text="➕ Yeni", command=self.new_snippet)
        self.add_button.pack(side="left", padx=5)

        self.save_button = ctk.CTkButton(self.button_frame, text="💾 Kaydet", command=self.save_snippet)
        self.save_button.pack(side="left", padx=5)

        self.edit_button = ctk.CTkButton(self.button_frame, text="✏️ Düzenle", command=self.start_edit)
        self.edit_button.pack(side="left", padx=5)

        self.delete_button = ctk.CTkButton(self.button_frame, text="🗑️ Sil", command=self.delete_snippet)
        self.delete_button.pack(side="left", padx=5)

        self.copy_button = ctk.CTkButton(self.button_frame, text="📋 Kopyala", command=self.copy_code)
        self.copy_button.pack(side="left", padx=5)

    def refresh_list(self):
        self.snippet_listbox.configure(state="normal")
        self.snippet_listbox.delete("1.0", "end")
        for desc in self.snippets:
            prefix = ">> " if desc == self.selected_snippet else "• "
            color = "#E34234" if desc == self.selected_snippet else "#FFFFFF"
            self.snippet_listbox.insert("end", f"{prefix}{desc}\n", desc)
            self.snippet_listbox.tag_config(desc, foreground=color)
        self.snippet_listbox.configure(state="disabled")

    def on_snippet_click(self, event):
        if self.is_editing:
            messagebox.showwarning("Uyarı", "Önce değişiklikleri kaydedin veya 'Yeni' butonuna basın!")
            return
            
        index = self.snippet_listbox.index(f"@{event.x},{event.y}")
        line = self.snippet_listbox.get(f"{index} linestart", f"{index} lineend").strip()
        if line.startswith("• ") or line.startswith(">> "):
            desc = line[3:] if line.startswith(">> ") else line[2:]
            self.selected_snippet = desc
            self.show_snippet(desc)
            self.refresh_list()

    def show_snippet(self, desc):
        self.desc_entry.configure(state="normal")
        self.code_text.configure(state="normal")
        
        self.desc_entry.delete("1.0", "end")
        self.code_text.delete("1.0", "end")
        self.desc_entry.insert("1.0", desc)
        self.code_text.insert("1.0", self.snippets.get(desc, ""))
        
        self.is_editing = False
        self.original_description = None
        self.set_editable(False)  

    def new_snippet(self):
        """Yeni ekleme için temiz ekran aç"""
        self.desc_entry.configure(state="normal")
        self.code_text.configure(state="normal")
        self.desc_entry.delete("1.0", "end")
        self.code_text.delete("1.0", "end")
        
        self.selected_snippet = None
        self.is_editing = False
        self.original_description = None
        self.set_editable(True)
        self.refresh_list()  

    def save_snippet(self):
        desc = self.desc_entry.get("1.0", "end").strip()
        code = self.code_text.get("1.0", "end").strip()
        
        if not desc or not code:
            messagebox.showwarning("Uyarı", "Açıklama ve kod boş olamaz!")
            return

        if self.is_editing and self.original_description and self.original_description != desc:
            if self.original_description in self.snippets:
                del self.snippets[self.original_description]

        self.snippets[desc] = code
        self.selected_snippet = desc
        self.is_editing = False
        self.original_description = None
        self.refresh_list()
        self.set_editable(False)
        self.save_data()  
        messagebox.showinfo("Kaydedildi", "Kod bloğu başarıyla kaydedildi!")

    def delete_snippet(self):
        if self.selected_snippet and self.selected_snippet in self.snippets:
            del self.snippets[self.selected_snippet]
            self.selected_snippet = None
            self.is_editing = False
            self.original_description = None
            self.refresh_list()
            self.new_snippet()
            self.save_data()  
            messagebox.showinfo("Silindi", "Kod bloğu silindi!")
        else:
            messagebox.showwarning("Uyarı", "Silinecek kod seçilmedi!")

    def start_edit(self):
        if not self.selected_snippet:
            messagebox.showwarning("Uyarı", "Düzenlemek için bir kod seçin!")
            return
        
        self.is_editing = True
        self.original_description = self.selected_snippet
        self.set_editable(True)

    def copy_code(self):
        code = self.code_text.get("1.0", "end").strip()
        if code:
            self.clipboard_clear()
            self.clipboard_append(code)
            messagebox.showinfo("Kopyalandı", "Kod panoya kopyalandı!")

    def set_editable(self, editable: bool):
        state = "normal" if editable else "disabled"
        self.desc_entry.configure(state=state)
        self.code_text.configure(state=state)

    def toggle_theme(self):
        if self.current_theme == "dark":
            ctk.set_appearance_mode("light")
            self.current_theme = "light"
        else:
            ctk.set_appearance_mode("dark")
            self.current_theme = "dark"
        self.update_code_colors() 

    def update_code_colors(self):
        """Temaya göre kod bloğu renklerini ayarla"""
        if self.current_theme == "dark":
            self.code_text.configure(
                text_color="#00FFAA",  
                fg_color="#1E1E1E"     
            )
        else:
            self.code_text.configure(
                text_color="#0066CC",  
                fg_color="#F5F5F5"      
            )

    def save_data(self):
        """Verileri JSON dosyasına kaydet"""
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(self.snippets, f, ensure_ascii=False, indent=2)
        except Exception as e:
            messagebox.showerror("Hata", f"Veri kaydedilemedi: {e}")

    def load_data(self):
        """JSON dosyasından verileri yükle"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    self.snippets = json.load(f)
                self.refresh_list()
            except Exception as e:
                messagebox.showerror("Hata", f"Veri yüklenemedi: {e}")


if __name__ == "__main__":
    app = SnippetManager()
    app.mainloop()