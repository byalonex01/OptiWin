import sys
import psutil
import subprocess
import os
import json
from datetime import datetime
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QGroupBox, QProgressBar, QMessageBox, QTabWidget
)
from PyQt6.QtCore import Qt, QTimer, QThread, pyqtSignal
from PyQt6.QtGui import QFont, QColor, QIcon
from PyQt6.QtGui import QPalette


class SystemMonitor(QThread):
    """Sistem bilgilerini gerçek zamanda güncelleyen thread"""
    data_updated = pyqtSignal(dict)
    
    def run(self):
        while True:
            try:
                data = {
                    'cpu': psutil.cpu_percent(interval=1),
                    'memory': psutil.virtual_memory().percent,
                    'memory_used': psutil.virtual_memory().used / (1024**3),
                    'memory_total': psutil.virtual_memory().total / (1024**3),
                    'disk': psutil.disk_usage('/').percent,
                    'disk_used': psutil.disk_usage('/').used / (1024**3),
                    'disk_total': psutil.disk_usage('/').total / (1024**3),
                }
                self.data_updated.emit(data)
            except Exception as e:
                print(f"Hata: {e}")


class OptimizationEngine:
    """Optimizasyon işlemlerini yapan motor"""
    
    @staticmethod
    def clean_temp_files():
        """Geçici dosyaları temizle"""
        try:
            subprocess.run(['cmd', '/c', 'del /q /s %temp%\\*'], shell=True, capture_output=True)
            return True, "Geçici dosyalar temizlendi ✓"
        except Exception as e:
            return False, f"Hata: {str(e)}"
    
    @staticmethod
    def disable_telemetry():
        """Windows telemetrisini kapat"""
        try:
            services = ['DiagTrack', 'dmwappushservice', 'OneSyncSvc']
            for service in services:
                subprocess.run(['cmd', '/c', f'net stop {service}'], shell=True, capture_output=True)
                subprocess.run(['cmd', '/c', f'sc config {service} start=disabled'], shell=True, capture_output=True)
            return True, "Telemetri kapatıldı ✓"
        except Exception as e:
            return False, f"Hata: {str(e)}"
    
    @staticmethod
    def disable_startup_apps():
        """Başlangıç uygulamalarını devre dışı bırak"""
        try:
            subprocess.run(['cmd', '/c', 'taskkill /F /IM OneDrive.exe'], shell=True, capture_output=True)
            return True, "Başlangıç uygulamaları optimize edildi ✓"
        except Exception as e:
            return False, f"Hata: {str(e)}"
    
    @staticmethod
    def clear_cache():
        """DNS ve tarayıcı cache'ini temizle"""
        try:
            subprocess.run(['cmd', '/c', 'ipconfig /flushdns'], shell=True, capture_output=True)
            return True, "Cache temizlendi ✓"
        except Exception as e:
            return False, f"Hata: {str(e)}"
    
    @staticmethod
    def defrag_disk():
        """Disk defragmentasyonu (Windows 10/11)"""
        try:
            subprocess.run(['cmd', '/c', 'defrag C: /U /V'], shell=True, capture_output=True)
            return True, "Disk optimize edildi ✓"
        except Exception as e:
            return False, f"Hata: {str(e)}"


class MainWindow(QMainWindow):
    """OptiWin Ana Penceresi"""
    
    def __init__(self):
        super().__init__()
        self.optimization_engine = OptimizationEngine()
        self.monitor = SystemMonitor()
        self.monitor.data_updated.connect(self.update_system_info)
        self.monitor.start()
        
        self.init_ui()
        self.apply_dark_theme()
        
    def init_ui(self):
        """Kullanıcı arayüzünü oluştur"""
        self.setWindowTitle('OptiWin - Windows Optimizasyon Aracı v1.0')
        self.setGeometry(100, 100, 1000, 700)
        
        # Ana widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Başlık
        title = QLabel('🖥️ OptiWin - Windows Optimizasyon Aracı')
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title.setFont(title_font)
        main_layout.addWidget(title)
        
        # Tab widget
        tabs = QTabWidget()
        
        # Tab 1: Dashboard
        dashboard_tab = self.create_dashboard_tab()
        tabs.addTab(dashboard_tab, "📊 Dashboard")
        
        # Tab 2: Optimizasyon
        optimization_tab = self.create_optimization_tab()
        tabs.addTab(optimization_tab, "⚡ Optimizasyon")
        
        # Tab 3: Ayarlar
        settings_tab = self.create_settings_tab()
        tabs.addTab(settings_tab, "⚙️ Ayarlar")
        
        main_layout.addWidget(tabs)
        
    def create_dashboard_tab(self):
        """Dashboard sekmesini oluştur"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Sistem Durumu Grubu
        system_group = QGroupBox("📊 Sistem Durumu")
        system_layout = QVBoxLayout()
        
        # CPU
        cpu_layout = QHBoxLayout()
        cpu_layout.addWidget(QLabel("CPU Kullanımı:"))
        self.cpu_bar = QProgressBar()
        cpu_layout.addWidget(self.cpu_bar)
        self.cpu_label = QLabel("0%")
        cpu_layout.addWidget(self.cpu_label)
        system_layout.addLayout(cpu_layout)
        
        # RAM
        ram_layout = QHBoxLayout()
        ram_layout.addWidget(QLabel("RAM Kullanımı:"))
        self.ram_bar = QProgressBar()
        ram_layout.addWidget(self.ram_bar)
        self.ram_label = QLabel("0%")
        ram_layout.addWidget(self.ram_label)
        system_layout.addLayout(ram_layout)
        
        # DISK
        disk_layout = QHBoxLayout()
        disk_layout.addWidget(QLabel("Disk Kullanımı:"))
        self.disk_bar = QProgressBar()
        disk_layout.addWidget(self.disk_bar)
        self.disk_label = QLabel("0%")
        disk_layout.addWidget(self.disk_label)
        system_layout.addLayout(disk_layout)
        
        system_group.setLayout(system_layout)
        layout.addWidget(system_group)
        
        # Sistem Bilgileri
        info_group = QGroupBox("ℹ️ Sistem Bilgileri")
        info_layout = QVBoxLayout()
        
        import platform
        info_text = f"""
        İşletim Sistemi: {platform.system()} {platform.release()}
        İşlemci: {platform.processor()}
        Python Sürümü: {platform.python_version()}
        Bilgisayar Adı: {os.getenv('COMPUTERNAME')}
        """
        info_label = QLabel(info_text)
        info_layout.addWidget(info_label)
        
        info_group.setLayout(info_layout)
        layout.addWidget(info_group)
        
        layout.addStretch()
        widget.setLayout(layout)
        return widget
    
    def create_optimization_tab(self):
        """Optimizasyon sekmesini oluştur"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Hızlı İşlemler
        quick_group = QGroupBox("⚡ Hızlı İşlemler")
        quick_layout = QVBoxLayout()
        
        # Buton 1: Geçici Dosyaları Temizle
        btn_temp = QPushButton("🧹 Geçici Dosyaları Temizle")
        btn_temp.clicked.connect(lambda: self.run_optimization(self.optimization_engine.clean_temp_files, btn_temp))
        quick_layout.addWidget(btn_temp)
        
        # Buton 2: Telemetri Kapat
        btn_telemetry = QPushButton("🔒 Windows Telemetrisini Kapat")
        btn_telemetry.clicked.connect(lambda: self.run_optimization(self.optimization_engine.disable_telemetry, btn_telemetry))
        quick_layout.addWidget(btn_telemetry)
        
        # Buton 3: Başlangıç Uygulamalarını Optimize Et
        btn_startup = QPushButton("🚀 Başlangıç Uygulamalarını Optimize Et")
        btn_startup.clicked.connect(lambda: self.run_optimization(self.optimization_engine.disable_startup_apps, btn_startup))
        quick_layout.addWidget(btn_startup)
        
        # Buton 4: Cache Temizle
        btn_cache = QPushButton("💾 Cache Temizle (DNS)")
        btn_cache.clicked.connect(lambda: self.run_optimization(self.optimization_engine.clear_cache, btn_cache))
        quick_layout.addWidget(btn_cache)
        
        # Buton 5: Disk Optimize
        btn_defrag = QPushButton("💿 Disk'i Optimize Et")
        btn_defrag.clicked.connect(lambda: self.run_optimization(self.optimization_engine.defrag_disk, btn_defrag))
        quick_layout.addWidget(btn_defrag)
        
        quick_group.setLayout(quick_layout)
        layout.addWidget(quick_group)
        
        # Otomatik Optimizasyon
        auto_group = QGroupBox("🤖 Otomatik Optimizasyon")
        auto_layout = QVBoxLayout()
        
        btn_auto = QPushButton("▶️ Tümünü Çalıştır (Otomatik Optimizasyon)")
        btn_auto.clicked.connect(self.run_full_optimization)
        btn_auto.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold; padding: 10px;")
        auto_layout.addWidget(btn_auto)
        
        auto_group.setLayout(auto_layout)
        layout.addWidget(auto_group)
        
        layout.addStretch()
        widget.setLayout(layout)
        return widget
    
    def create_settings_tab(self):
        """Ayarlar sekmesini oluştur"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Tema Ayarları
        theme_group = QGroupBox("🎨 Tema Ayarları")
        theme_layout = QVBoxLayout()
        
        btn_dark = QPushButton("🌙 Koyu Tema")
        btn_dark.clicked.connect(self.apply_dark_theme)
        theme_layout.addWidget(btn_dark)
        
        btn_light = QPushButton("☀️ Açık Tema")
        btn_light.clicked.connect(self.apply_light_theme)
        theme_layout.addWidget(btn_light)
        
        theme_group.setLayout(theme_layout)
        layout.addWidget(theme_group)
        
        # Bilgiler
        info_group = QGroupBox("ℹ️ Hakkında")
        info_layout = QVBoxLayout()
        
        about_text = """
        OptiWin v1.0
        
        Windows 10 ve 11 için modern optimizasyon aracı
        
        Özellikler:
        • Sistem Monitoring
        • Otomatik Temizlik
        • Telemetri Yönetimi
        • Performance Boost
        
        Geliştirici: ByAloenx
        Lisans: MIT
        """
        info_label = QLabel(about_text)
        info_layout.addWidget(info_label)
        
        info_group.setLayout(info_layout)
        layout.addWidget(info_group)
        
        layout.addStretch()
        widget.setLayout(layout)
        return widget
    
    def update_system_info(self, data):
        """Sistem bilgilerini güncelle"""
        try:
            # CPU
            self.cpu_bar.setValue(int(data['cpu']))
            self.cpu_label.setText(f"{int(data['cpu'])}%")
            
            # RAM
            self.ram_bar.setValue(int(data['memory']))
            self.ram_label.setText(f"{int(data['memory'])}% ({data['memory_used']:.1f}/{data['memory_total']:.1f} GB)")
            
            # DISK
            self.disk_bar.setValue(int(data['disk']))
            self.disk_label.setText(f"{int(data['disk'])}% ({data['disk_used']:.1f}/{data['disk_total']:.1f} GB)")
        except Exception as e:
            print(f"Güncelleme hatası: {e}")
    
    def run_optimization(self, optimization_func, button):
        """Optimizasyon işlemini çalıştır"""
        button.setEnabled(False)
        button.setText("⏳ İşleniyor...")
        
        success, message = optimization_func()
        
        if success:
            QMessageBox.information(self, "Başarılı ✓", message)
        else:
            QMessageBox.warning(self, "Hata ⚠️", message)
        
        button.setEnabled(True)
        button.setText(button.text().replace("⏳ İşleniyor...", ""))
    
    def run_full_optimization(self):
        """Tam optimizasyon çalıştır"""
        reply = QMessageBox.question(
            self, 
            "Uyarı", 
            "Tam optimizasyon çalıştırılacak. Bunu devam ettirmek istiyor musunuz?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            operations = [
                (self.optimization_engine.clean_temp_files, "Geçici dosyalar temizleniyor..."),
                (self.optimization_engine.disable_telemetry, "Telemetri kapatıldı..."),
                (self.optimization_engine.clear_cache, "Cache temizleniyor..."),
            ]
            
            for op, msg in operations:
                self.statusBar().showMessage(msg)
                success, result = op()
                if not success:
                    QMessageBox.warning(self, "Hata", result)
                    break
            
            self.statusBar().showMessage("Optimizasyon tamamlandı ✓")
            QMessageBox.information(self, "Başarılı", "Tüm optimizasyonlar tamamlandı!")
    
    def apply_dark_theme(self):
        """Koyu tema uygula"""
        dark_stylesheet = """
            QMainWindow { background-color: #1e1e1e; color: #ffffff; }
            QWidget { background-color: #1e1e1e; color: #ffffff; }
            QGroupBox { border: 2px solid #404040; border-radius: 5px; margin-top: 10px; padding-top: 10px; color: #ffffff; }
            QGroupBox::title { subcontrol-origin: margin; left: 10px; padding: 0 3px 0 3px; }
            QPushButton { background-color: #0078d4; color: #ffffff; border: none; padding: 8px; border-radius: 4px; font-weight: bold; }
            QPushButton:hover { background-color: #1084d8; }
            QPushButton:pressed { background-color: #005a9e; }
            QLabel { color: #ffffff; }
            QProgressBar { background-color: #3e3e3e; border: 1px solid #404040; border-radius: 4px; }
            QProgressBar::chunk { background-color: #0078d4; }
            QTabWidget::pane { border: 1px solid #404040; }
            QTabBar::tab { background-color: #2e2e2e; color: #ffffff; padding: 8px 20px; border: 1px solid #404040; }
            QTabBar::tab:selected { background-color: #0078d4; }
        """
        self.setStyleSheet(dark_stylesheet)
    
    def apply_light_theme(self):
        """Açık tema uygula"""
        light_stylesheet = """
            QMainWindow { background-color: #ffffff; color: #000000; }
            QWidget { background-color: #ffffff; color: #000000; }
            QGroupBox { border: 2px solid #d0d0d0; border-radius: 5px; margin-top: 10px; padding-top: 10px; color: #000000; }
            QGroupBox::title { subcontrol-origin: margin; left: 10px; padding: 0 3px 0 3px; }
            QPushButton { background-color: #0078d4; color: #ffffff; border: none; padding: 8px; border-radius: 4px; font-weight: bold; }
            QPushButton:hover { background-color: #1084d8; }
            QPushButton:pressed { background-color: #005a9e; }
            QLabel { color: #000000; }
            QProgressBar { background-color: #f0f0f0; border: 1px solid #d0d0d0; border-radius: 4px; }
            QProgressBar::chunk { background-color: #0078d4; }
            QTabWidget::pane { border: 1px solid #d0d0d0; }
            QTabBar::tab { background-color: #f0f0f0; color: #000000; padding: 8px 20px; border: 1px solid #d0d0d0; }
            QTabBar::tab:selected { background-color: #0078d4; color: #ffffff; }
        """
        self.setStyleSheet(light_stylesheet)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()