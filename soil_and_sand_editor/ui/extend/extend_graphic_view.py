from PySide6.QtCore import Qt, QPoint
from PySide6.QtWidgets import QGraphicsView


class ExtendGraphicView(QGraphicsView):

    def __init__(self, *args):
        super().__init__(*args)
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)

    def wheelEvent(self, event) -> None:
        if self.scene() and len(self.scene().items()) == 0:
            return 
        else:
            wheel_value = event.angleDelta().y()
            scale_factor = self.transform().m11()

            if (scale_factor < 0.5 and wheel_value < 0) or (scale_factor > 50 and wheel_value > 0):
                return

            if wheel_value > 0:
                self.scale(1.2, 1.2)
            else:
                self.scale(1.0 / 1.2, 1.0 / 1.2)

            self.update()
