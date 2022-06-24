search_listWidget = """
            QListWidget{
                border: none;
                border-radius: 5px;
                background: transparent;

            }
            QListWidget QScrollBar{
                width: 10px;
                background: #e4e4e4;
                border-radius: 5px;
                margin: 0px;
            }
            QListWidget QScrollBar::handle:vertical {
                background-color: #d4d4d4;
                border-radius: 10px;
            }
            QListWidget QScrollBar::add-line:vertical {
                height: 0px;
            }
            QListWidget QScrollBar::sub-line:vertical {
                height: 0px;
            }
            QListView::item{
                border-bottom: 1px solid #ededed;
            }
            QListView::item:selected{
                selection-color: black;
                selection-background-color: black;
            }
        """