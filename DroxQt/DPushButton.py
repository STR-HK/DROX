from PyQt5.QtWidgets import QPushButton
from MyDependencies.MyColors import colorScheme

class DPushButton(QPushButton):
    def __init__(self, *args, **kwargs):
        super(QPushButton, self).__init__(*args, **kwargs)

        self.setStyleSheet(f"""
            f"border: none; border-radius: 5px; background-color: {colorScheme.secondaryContainer}; padding: 10px;"
        """)
