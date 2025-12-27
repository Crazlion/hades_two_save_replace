import sys
import os
import shutil
from pathlib import Path
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QLineEdit, QFileDialog, QMessageBox, QFrame
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QFont, QIcon, QPalette, QColor

class HadesSaveManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("哈迪斯 II 存档管理器")
        self.setMinimumSize(600, 400)
        
        # 默认路径
        default_path = str(Path.home() / "Saved Games" / "Hades II")
        if not os.path.exists(default_path):
             user_profile = os.environ.get("USERPROFILE", "C:\\Users\\Administrator")
             default_path = os.path.join(user_profile, "Saved Games", "Hades II")

        self.save_dir = default_path
        # 初始时设置 bak_dir，随后随 save_dir 变化
        self.update_bak_dir()

        self.setup_ui()
        self.apply_styles()

    def update_bak_dir(self):
        self.bak_dir = os.path.join(self.save_dir, "bak")

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(20)

        # 标题
        title_label = QLabel("哈迪斯 II 存档管理")
        title_label.setObjectName("titleLabel")
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)

        # 文件夹选择行
        folder_layout = QHBoxLayout()
        self.folder_input = QLineEdit(self.save_dir)
        self.folder_input.setReadOnly(True)
        self.folder_input.setPlaceholderText("请选择哈迪斯 II 存档文件夹...")
        
        browse_btn = QPushButton("选择文件夹")
        browse_btn.setFixedWidth(100)
        browse_btn.clicked.connect(self.select_folder)
        
        folder_layout.addWidget(self.folder_input)
        folder_layout.addWidget(browse_btn)
        main_layout.addLayout(folder_layout)

        # 分割线
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setStyleSheet("background-color: #4a0404;")
        main_layout.addWidget(line)

        # 动作按钮
        button_layout = QHBoxLayout()
        button_layout.setSpacing(20)

        self.backup_btn = QPushButton("备份存档")
        self.backup_btn.setFixedHeight(50)
        self.backup_btn.clicked.connect(self.backup_saves)
        
        self.restore_btn = QPushButton("恢复存档")
        self.restore_btn.setFixedHeight(50)
        self.restore_btn.clicked.connect(self.restore_saves)

        button_layout.addWidget(self.backup_btn)
        button_layout.addWidget(self.restore_btn)
        main_layout.addLayout(button_layout)

        # 状态标签
        self.status_label = QLabel("就绪")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setObjectName("statusLabel")
        main_layout.addWidget(self.status_label)

        main_layout.addStretch()

    def apply_styles(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1a0202;
            }
            QWidget {
                color: #e0e0e0;
                font-family: 'Microsoft YaHei', 'Segoe UI', sans-serif;
            }
            #titleLabel {
                font-size: 28px;
                font-weight: bold;
                color: #d4af37; /* Gold */
                margin-bottom: 10px;
                letter-spacing: 2px;
            }
            QLineEdit {
                background-color: #2a0505;
                border: 1px solid #4a0404;
                border-radius: 5px;
                padding: 8px;
                color: #ffcccc;
                font-size: 14px;
            }
            QPushButton {
                background-color: #4a0404;
                border: 1px solid #d4af37;
                border-radius: 5px;
                color: #d4af37;
                font-weight: bold;
                font-size: 16px;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #6a0606;
                color: #ffffff;
            }
            QPushButton:pressed {
                background-color: #2a0202;
            }
            #statusLabel {
                font-style: italic;
                color: #888;
                margin-top: 10px;
            }
            QMessageBox QLabel {
                color: #000000;
            }
            QMessageBox QPushButton {
                background-color: #f0f0f0;
                color: #000000;
                border: 1px solid #ababab;
                min-width: 80px;
            }
        """)

    def select_folder(self):
        dir_path = QFileDialog.getExistingDirectory(self, "选择哈迪斯 II 存档文件夹", self.save_dir)
        if dir_path:
            self.save_dir = dir_path
            self.update_bak_dir()
            self.folder_input.setText(dir_path)
            self.status_label.setText(f"已选择文件夹: {Path(dir_path).name}")

    def backup_saves(self):
        source_dir = Path(self.folder_input.text())
        if not source_dir.exists():
            QMessageBox.critical(self, "错误", f"找不到存档文件夹: {source_dir}")
            return

        # 确保 bak 目录存在于存档文件夹下
        bak_path = Path(self.bak_dir)
        bak_path.mkdir(exist_ok=True)

        files_to_copy = list(source_dir.glob("Profile1*"))
        if not files_to_copy:
            QMessageBox.warning(self, "无文件", "未在选择的文件夹中找到前缀为 'Profile1' 的文件。")
            return

        try:
            for f in files_to_copy:
                shutil.copy2(f, bak_path / f.name)
            
            self.status_label.setText(f"成功备份 {len(files_to_copy)} 个文件至存档目录下的 bak 文件夹")
            QMessageBox.information(self, "成功", f"成功备份 {len(files_to_copy)} 个文件。")
        except Exception as e:
            QMessageBox.critical(self, "错误", f"备份失败: {str(e)}")

    def restore_saves(self):
        dest_dir = Path(self.folder_input.text())
        bak_path = Path(self.bak_dir)

        if not bak_path.exists() or not any(bak_path.iterdir()):
            QMessageBox.critical(self, "错误", "存档目录下的备份文件夹 'bak' 不存在或为空！")
            return

        if not dest_dir.exists():
            QMessageBox.critical(self, "错误", f"找不到目标文件夹: {dest_dir}")
            return

        bak_files = list(bak_path.glob("*"))
        
        # 确认覆盖
        reply = QMessageBox.question(self, "确认恢复", 
                                   f"确定要恢复 {len(bak_files)} 个文件吗？\n这将覆盖存档文件夹中的现有文件。",
                                   QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.No:
            return

        try:
            for f in bak_files:
                shutil.copy2(f, dest_dir / f.name)
            
            self.status_label.setText(f"成功从 bak 文件夹恢复 {len(bak_files)} 个文件")
            QMessageBox.information(self, "成功", f"成功恢复 {len(bak_files)} 个文件。")
        except Exception as e:
            QMessageBox.critical(self, "错误", f"恢复失败: {str(e)}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = HadesSaveManager()
    window.show()
    sys.exit(app.exec())
