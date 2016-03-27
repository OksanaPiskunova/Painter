# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtCore, QtGui
import drawer

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

    def mousePressEvent(self, mouse_event):
        if mouse_event.button() & QtCore.Qt.LeftButton:
            x = mouse_event.x()
            y = mouse_event.y()
            self.controller.add_to_buffer((x, y))
        if mouse_event.button() & QtCore.Qt.RightButton:
            self.controller.check_buffer()
        self._show_scene()

    def _show_scene(self):
        self.scene = self.controller.scene
        self.setScene(self.scene)
        self.show()


class MainWindow(object):
    def __init__(self):
        # initialize shared_drawer
        self.controller = drawer.Controller()
        #self.scene = self.controller.scene

    def setup_ui(self, main_window):
        # set name and size of the window
        main_window.setObjectName(_fromUtf8("MainWindow"))
        main_window.resize(820, 600)

        # create central widget
        self.main = QtGui.QWidget(main_window)
        main_window.setCentralWidget(self.main)

        # create graphic view
        self.graphicsview = MyGraphicsView(main_window, self.controller)
        self.graphicsview.setGeometry(QtCore.QRect(0, 0, 680, 540))
        #self.graphicsview.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.graphicsview.AnchorViewCenter = QtGui.QGraphicsView.NoAnchor
        self.graphicsview.setObjectName(_fromUtf8("graphicsView"))

        # create button "Draw all"
        self.btn_draw_all = QtGui.QPushButton(main_window)
        self.btn_draw_all.setGeometry(QtCore.QRect(686, 10, 125, 27))
        self.btn_draw_all.setObjectName(_fromUtf8("btnDrawAll"))

        # create button "Draw line"
        self.btn_draw_line = QtGui.QPushButton(main_window)
        self.btn_draw_line.setGeometry(QtCore.QRect(686, 60, 125, 27))
        self.btn_draw_line.setObjectName(_fromUtf8("btnDrawLine"))

        # create button "Draw Polygon"
        self.btn_draw_polygon = QtGui.QPushButton(main_window)
        self.btn_draw_polygon.setGeometry(QtCore.QRect(686, 100, 125, 27))
        self.btn_draw_polygon.setObjectName(_fromUtf8("btnDrawPolygon"))

        # create button "Draw Triangle"
        self.btn_draw_triangle = QtGui.QPushButton(main_window)
        self.btn_draw_triangle.setGeometry(QtCore.QRect(686, 140, 125, 27))
        self.btn_draw_triangle.setObjectName(_fromUtf8("btnDrawTriangle"))

        # create button "Draw Quadrangle"
        self.btn_draw_quadrangle = QtGui.QPushButton(main_window)
        self.btn_draw_quadrangle.setGeometry(QtCore.QRect(686, 180, 125, 27))
        self.btn_draw_quadrangle.setObjectName(_fromUtf8("btnDrawQuadrangle"))

        # create button "Draw Rectangle"
        self.btn_draw_rectangle = QtGui.QPushButton(main_window)
        self.btn_draw_rectangle.setGeometry(QtCore.QRect(686, 220, 125, 27))
        self.btn_draw_rectangle.setObjectName(_fromUtf8("btnDrawRectangle"))

        # create button "Draw Square"
        self.btn_draw_square = QtGui.QPushButton(main_window)
        self.btn_draw_square.setGeometry(QtCore.QRect(686, 260, 125, 27))
        self.btn_draw_square.setObjectName(_fromUtf8("btnDrawSquare"))

        # create button "Draw Ellipse"
        self.btn_draw_ellipse = QtGui.QPushButton(main_window)
        self.btn_draw_ellipse.setGeometry(QtCore.QRect(686, 300, 125, 27))
        self.btn_draw_ellipse.setObjectName(_fromUtf8("btnDrawEllipse"))

        # create button "Draw Circle"
        self.btn_draw_circle = QtGui.QPushButton(main_window)
        self.btn_draw_circle.setGeometry(QtCore.QRect(686, 340, 125, 27))
        self.btn_draw_circle.setObjectName(_fromUtf8("btnDrawCircle"))

        # create button "Clear"
        self.btn_clear = QtGui.QPushButton(main_window)
        self.btn_clear.setGeometry(QtCore.QRect(686, 540, 125, 27))
        self.btn_clear.setObjectName(_fromUtf8("btnClear"))

        # create menu "File"
        self.menubar = QtGui.QMenuBar(main_window)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 0, 0))

        # create a trigger-action => binding
        self.menu_file_exit = QtGui.QAction(self.main)
        self.menu_file_exit.setText(self._to_utf("&Выход"))
        main_window.connect(self.menu_file_exit,
                            QtCore.SIGNAL('triggered()'), sys.exit)

        # create a menu
        self.menu_file = self.menubar.addMenu(self._to_utf('&Файл'))
        self.menu_file.addAction(self.menu_file_exit)
        main_window.setMenuBar(self.menubar)

        # create statusbar
        self.statusbar = QtGui.QStatusBar(main_window)
        main_window.setStatusBar(self.statusbar)

        self.retranslate_ui(main_window)

        # button_click
        QtCore.QObject.connect(self.btn_draw_all, QtCore.SIGNAL("clicked()"),
                               self._on_clicked_btn_draw_all)
        QtCore.QObject.connect(self.btn_draw_line, QtCore.SIGNAL("clicked()"),
                               self._on_clicked_btn_draw_line)
        QtCore.QObject.connect(self.btn_draw_polygon, QtCore.SIGNAL("clicked()"),
                               self._on_clicked_btn_draw_polygon)
        QtCore.QObject.connect(self.btn_draw_quadrangle, QtCore.SIGNAL("clicked()"),
                               self._on_clicked_btn_draw_quadrangle)
        QtCore.QObject.connect(self.btn_draw_triangle, QtCore.SIGNAL("clicked()"),
                               self._on_clicked_btn_draw_triangle)
        QtCore.QObject.connect(self.btn_draw_rectangle, QtCore.SIGNAL("clicked()"),
                               self._on_clicked_btn_draw_rectangle)
        QtCore.QObject.connect(self.btn_draw_square, QtCore.SIGNAL("clicked()"),
                               self._on_clicked_btn_draw_square)
        QtCore.QObject.connect(self.btn_draw_ellipse, QtCore.SIGNAL("clicked()"),
                               self._on_clicked_btn_draw_ellipse)
        QtCore.QObject.connect(self.btn_draw_circle, QtCore.SIGNAL("clicked()"),
                               self._on_clicked_btn_draw_circle)
        QtCore.QObject.connect(self.btn_clear, QtCore.SIGNAL("clicked()"),
                               self._on_clicked_btn_clear)

    def retranslate_ui(self, MainWindow):
        MainWindow.setWindowTitle(self._to_utf("Окошечко"))
        self.btn_draw_all.setText(self._to_utf("Нарисовать все"))
        self.btn_draw_line.setText(self._to_utf("Линия"))
        self.btn_draw_polygon.setText(self._to_utf("Многоугольник"))
        self.btn_draw_quadrangle.setText(self._to_utf("Четырехугольник"))
        self.btn_draw_triangle.setText(self._to_utf("Треугольник"))
        self.btn_draw_rectangle.setText(self._to_utf("Прямоугольник"))
        self.btn_draw_square.setText(self._to_utf("Квадрат"))
        self.btn_draw_ellipse.setText(self._to_utf("Эллипс"))
        self.btn_draw_circle.setText(self._to_utf("Круг"))
        self.btn_clear.setText(self._to_utf("Очистить"))

    def _to_utf(self, text):
        return QtGui.QApplication.translate("MainWindow", text, None,
                                            QtGui.QApplication.UnicodeUTF8)

    def _on_clicked_btn_draw_all(self):
        self.controller.process_list()
        self.set_scene()

    def _on_clicked_btn_draw_line(self):
        self.controller.process_line()

    def _on_clicked_btn_draw_polygon(self):
        self.controller.process_polygon()

    def _on_clicked_btn_draw_quadrangle(self):
        self.controller.process_quadrangle()

    def _on_clicked_btn_draw_triangle(self):
        self.controller.process_triangle()

    def _on_clicked_btn_draw_rectangle(self):
        self.controller.process_rectangle()

    def _on_clicked_btn_draw_square(self):
        self.controller.process_square()

    def _on_clicked_btn_draw_ellipse(self):
        self.controller.process_ellipse()

    def _on_clicked_btn_draw_circle(self):
        self.controller.process_circle()

    def _on_clicked_btn_clear(self):
        self.controller.clear_scene()

    def set_scene(self):
        self.scene = self.controller.scene
        self.graphicsview.setScene(self.scene)
        self.graphicsview.show()


def init():
    # initialize Qt
    app = QtGui.QApplication(sys.argv)

    main_window = QtGui.QMainWindow()

    form = MainWindow()
    form.setup_ui(main_window)

    return app, form, main_window

