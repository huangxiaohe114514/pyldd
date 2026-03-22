import sys
import time
import psutil
import socket
import threading
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QMenu, QGraphicsDropShadowEffect
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QObject, QPropertyAnimation, QEasingCurve, QRect, QPoint
from PyQt6.QtGui import QPainter, QColor, QPen, QFont, QCursor


class NetworkMonitor(QObject):
    network_changed = pyqtSignal(bool)
    
    def __init__(self):
        super().__init__()
        self.last_status = self.check_network()
        self.running = True
        
    def check_network(self):
        try:
            socket.create_connection(("8.8.8.8", 53), timeout=3)
            return True
        except:
            return False
            
    def start_monitoring(self):
        def monitor():
            while self.running:
                current_status = self.check_network()
                if current_status != self.last_status:
                    self.last_status = current_status
                    self.network_changed.emit(current_status)
                time.sleep(2)
        
        thread = threading.Thread(target=monitor, daemon=True)
        thread.start()
        
    def stop(self):
        self.running = False


class BluetoothMonitor(QObject):
    bluetooth_changed = pyqtSignal(bool)
    
    def __init__(self):
        super().__init__()
        self.last_status = False
        self.running = True
        
    def check_bluetooth(self):
        try:
            import winreg
            key = win