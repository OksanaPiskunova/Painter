# -*- coding: utf-8 -*-

import sys
import inspect
from PyQt4 import QtCore, QtGui
import controller
import registrator
import plugins.base as base

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8

    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)


class MyGraphicsView(QtGui.QGraphicsView):
    def __init__(self, parent, controller):
        super(MyGraphicsView, self).__init__(parent)
        self.parent = parent
        self.controller = controller
        self.setMouseTracking(True)

    def mousePressEvent(self, QMouseEvent):
        x = QMouseEvent.x()
        y = QMouseEvent.y()
        if QMouseEvent.button() & QtCore.Qt.LeftButton:
            self.controller.add_to_buffer((x, y))
        if QMouseEvent.button() & QtCore.Qt.RightButton:
            self.controller.check_buffer((x, y))
        self._show_scene()

    def mouseMoveEvent(self, QMouseEvent):
        x = QMouseEvent.x()
        y = QMouseEvent.y()
        self.controller.set_curr_position((x, y))
        self._show_scene()

    def _show_scene(self):
        self.scene = self.controller.scene
        self.setScene(self.scene)
        self.show()


class MainWindow(object):
    def __init__(self, main_window):
        # initialize
        self.controller = controller.Controller()

        self.main_window = main_window
        self.current_button_coord = 20
        self.setup_ui()

        self.buttons = {}
        self.drawers = {}

        self.register = registrator.PluginsRegistrator()
        self.register.register_plugins()
        self._search_plugins()

    def _search_plugins(self):
        r = self.register.get_modules()
        for j in r:
            res = getattr(self.register.package_obj, j)
            drawer = None
            figure = None
            for elem in dir(res):
                ge = getattr(res, elem)
                for el in dir(ge):
                    re = getattr(ge, el)
                    if inspect.isclass(re):
                        if issubclass(re, base.Figure):
                            figure = re
                        if issubclass(re, base.Drawer):
                            drawer = re
                if figure and drawer:
                    self.set_plugin_figure_values(figure, drawer)

    def set_plugin_figure_values(self, figure, drawer):
        self.drawers[figure] = drawer()
        self.create_button(self.main_window, figure)
        figure_type = figure.get_type()
        self.controller.drawer.draw_methods[figure_type] = self.drawers[figure].draw
        self.controller.draw_methods[figure_type] = self.drawers[figure].draw_now
        self.controller.factory[figure_type] = figure

    def setup_ui(self):
        # set name and size of the window
        self.main_window.setObjectName(_fromUtf8("MainWindow"))
        self.main_window.resize(820, 600)

        # create central widget
        self.main = QtGui.QWidget(self.main_window)
        self.main_window.setCentralWidget(self.main)

        # create graphic view
        self.graphicsview = MyGraphicsView(self.main_window, self.controller)
        self.graphicsview.setGeometry(QtCore.QRect(0, 0, 680, 540))
        #self.graphicsview.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.graphicsview.AnchorViewCenter = QtGui.QGraphicsView.NoAnchor
        self.graphicsview.setObjectName(_fromUtf8("graphicsView"))

        # create button "Clear"
        self.btn_clear = QtGui.QPushButton(self.main_window)
        self.btn_clear.setGeometry(QtCore.QRect(686, 540, 125, 27))
        self.btn_clear.setObjectName(_fromUtf8("btnClear"))

        # create button "ColorDialog for PenColor"
        self.btn_colordialog_pen = QtGui.QPushButton(self.main_window)
        self.btn_colordialog_pen.setGeometry(QtCore.QRect(5, 542, 35, 35))
        self.btn_colordialog_pen.setObjectName(_fromUtf8("btnColorDlgPen"))

        self.pen_colordialdog = QtGui.QColorDialog()
        self._init_pen()

        # create menu "File"
        self.menubar = QtGui.QMenuBar(self.main_window)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 0, 0))

        # create a trigger-action => binding
        self.menu_file_exit = QtGui.QAction(self.main)
        self.menu_file_exit.setText(self._to_utf("&Exit"))
        self.main_window.connect(self.menu_file_exit,
                                 QtCore.SIGNAL('triggered()'), sys.exit)

        # create a menu
        self.menu_file = self.menubar.addMenu(self._to_utf('&File'))
        self.menu_file.addAction(self.menu_file_exit)
        self.main_window.setMenuBar(self.menubar)

        # create statusbar
        self.statusbar = QtGui.QStatusBar(self.main_window)
        self.main_window.setStatusBar(self.statusbar)

        self.retranslate_ui(self.main_window)

        # button_click
        QtCore.QObject.connect(self.btn_colordialog_pen, QtCore.SIGNAL("clicked()"),
                               self._on_clicked_btn_colordialog_pen)

    def retranslate_ui(self, MainWindow):
        MainWindow.setWindowTitle(self._to_utf("PyPanda"))
        self.btn_clear.setText(self._to_utf("Clear"))

    def _to_utf(self, text):
        return QtGui.QApplication.translate("MainWindow", text, None,
                                            QtGui.QApplication.UnicodeUTF8)

    def create_button(self, main_window, figure_name):
        button = QtGui.QPushButton(main_window)
        button.setGeometry(QtCore.QRect(686, self.current_button_coord, 125, 27))
        QtCore.QObject.connect(button, QtCore.SIGNAL("clicked()"),
                               self._on_clicked_plugin_button)
        button.setText(self._to_utf(figure_name.get_type()))
        self.buttons[button] = figure_name
        self.current_button_coord += 40

    def _init_pen(self):
        self.pen = QtGui.QPen()
        self.pen.setStyle(QtCore.Qt.SolidLine)
        self.pen.setWidth(2)
        self.pen.setBrush(QtCore.Qt.black)
        self.pen.setCapStyle(QtCore.Qt.RoundCap)
        self.pen.setJoinStyle(QtCore.Qt.RoundJoin)

    def _on_clicked_plugin_button(self):
        if not self.controller.is_figure_chosen:
            self.controller.is_figure_chosen = True
            sender = QtCore.QObject.sender(QtCore.QObject())
            figure = self.buttons[sender]
            self.controller.process_plugin_figure(figure, self.drawers[figure])
            self.drawers[figure].set_scene(self.controller.scene)
            self.drawers[figure].set_pen(self.pen)
            self.drawers[figure].init_item()
            self.set_scene()

    def _on_clicked_btn_clear(self):
        self.controller.clear_scene()

    def _on_clicked_btn_colordialog_pen(self):
        self.pen.setColor(self.pen_colordialdog.getColor())
        self.controller.set_pen(self.pen)

    def set_scene(self):
        self.scene = self.controller.scene
        self.graphicsview.setScene(self.scene)
        self.graphicsview.show()


def init():
    # initialize Qt
    app = QtGui.QApplication(sys.argv)

    main_window = QtGui.QMainWindow()

    form = MainWindow(main_window)
    #form.setup_ui(main_window)

    return app, form, main_window

