from PyQt6 import QtCore, QtWidgets
from PyQt6.QtGui import QFont

from GUI_Package.IPAddressesTab import IPAddressTab
from GUI_Package.CyberScriptsTab import CyberScriptsTab
from GUI_Package.OutputLogsTab import OutputLogsTab


# TODO 30/04/2023 Or: add background colors to tabs


class TabBar(QtWidgets.QTabBar):
    def tabSizeHint(self, index):
        s = QtWidgets.QTabBar.tabSizeHint(self, index)
        s.transpose()
        s.setHeight(80)
        s.setWidth(200)
        return s

    def paintEvent(self, event):
        painter = QtWidgets.QStylePainter(self)
        opt = QtWidgets.QStyleOptionTab()

        for i in range(self.count()):
            self.initStyleOption(opt, i)
            painter.drawControl(QtWidgets.QStyle.ControlElement.CE_TabBarTabShape, opt)
            painter.save()

            s = opt.rect.size()
            s.transpose()
            r = QtCore.QRect(QtCore.QPoint(), s)
            r.moveCenter(opt.rect.center())
            opt.rect = r

            c = self.tabRect(i).center()
            painter.translate(c)
            painter.rotate(90)
            painter.translate(-c)
            painter.drawControl(QtWidgets.QStyle.ControlElement.CE_TabBarTabLabel, opt)
            painter.restore()


class TabWidget(QtWidgets.QTabWidget):
    def __init__(self, *args, **kwargs):
        QtWidgets.QTabWidget.__init__(self, *args, **kwargs)
        self.setTabBar(TabBar(self))
        self.setTabPosition(QtWidgets.QTabWidget.TabPosition.West)
        self.setFixedHeight(800)
        self.setFixedWidth(1200)


class ProxyStyle(QtWidgets.QProxyStyle):
    def drawControl(self, element, opt, painter, widget):
        if element == QtWidgets.QStyle.ControlElement.CE_TabBarTabLabel:
            # ic = self.pixelMetric(QtWidgets.QStyle.PM_TabBarIconSize)
            r = QtCore.QRect(opt.rect)
            text_width = opt.fontMetrics.boundingRect(opt.text).width()
            width = 0 if opt.icon.isNull() else opt.rect.width() + self.pixelMetric(
                QtWidgets.QStyle.PixelMetric.PM_TabBarIconSize)
            r.setHeight(text_width + width + 40)
            r.moveBottom(opt.rect.bottom())
            opt.rect = r
        QtWidgets.QProxyStyle.drawControl(self, element, opt, painter, widget)


if __name__ == '__main__':
    import sys

    font = QFont("Arial", 16)
    app = QtWidgets.QApplication(sys.argv)
    QtWidgets.QApplication.setStyle(ProxyStyle())
    w = TabWidget()
    w.tabBar().setFont(font)
    w.addTab(IPAddressTab(), "IP Addresses")
    w.addTab(CyberScriptsTab(), "Cyber Scripts")
    w.addTab(OutputLogsTab(), "Output Logs")

    w.show()

    sys.exit(app.exec())
