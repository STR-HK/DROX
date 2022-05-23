from PySide2 import QtCore, QtGui, QtWidgets

policyNames = "Fixed", "Minimum", "Maximum", "Preferred", "Expanding"
policyNameDict = {}
policyValueDict = {}
for name in policyNames:
    policy = getattr(QtWidgets.QSizePolicy, name)
    policyNameDict[policy] = name
    policyValueDict[name] = policy


class TestWidget(QtWidgets.QWidget):
    def sizeHint(self):
        return QtCore.QSize(150, 30)

    def minimumSizeHint(self):
        return QtCore.QSize(10, 10)

    def contextMenuEvent(self, event):
        currentPolicy = self.sizePolicy()
        menu = QtWidgets.QMenu()
        group = QtWidgets.QActionGroup(menu, exclusive=True)
        for name in policyNames:
            action = group.addAction(name)
            action.setCheckable(True)
            policy = policyValueDict[name]
            action.setData(policy)
            if policy == currentPolicy.horizontalPolicy():
                action.setChecked(True)
        menu.addActions(group.actions())
        res = menu.exec_(event.globalPos())
        if res:
            # PySide requires reconversion of the data, on PyQt the
            # res.data() alone is enough;
            currentPolicy.setHorizontalPolicy(QtWidgets.QSizePolicy.Policy(res.data()))
            self.setSizePolicy(currentPolicy)
            self.update()

    def paintEvent(self, event):
        qp = QtGui.QPainter(self)
        qp.drawRect(self.rect().adjusted(0, 0, -1, -1))
        text = "{policy}\n{width}x{height}".format(
            policy=policyNameDict[self.sizePolicy().horizontalPolicy()],
            width=self.sizeHint().width(),
            height=self.sizeHint().height(),
        )
        qp.drawText(self.rect(), QtCore.Qt.AlignCenter, text)


app = QtWidgets.QApplication([])

window = QtWidgets.QWidget()
layout = QtWidgets.QHBoxLayout(window)
for i in range(3):
    layout.addWidget(TestWidget())
window.show()

app.exec_()
