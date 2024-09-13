from .color import Color


class Font:

    def __init__(self, family="Sans"):
        self.family = family
        self.weight = "normal"
        self.slant = "normal"
        self.size = 0.5


class SceneItem:

    def __init__(self, item_type):
        self.location = (0, 0)
        self.item_type = item_type


class Shape(SceneItem):

    def __init__(self, shape_type):
        super().__init__("shape")
        self.shape_type = shape_type
        self.fill = Color()
        self.stroke = None
        self.stroke_thickness = 0.5


class TextPath(SceneItem):

    def __init__(self, content):
        super().__init__("text")
        self.content = content
        self.font = Font()


class Rectangle(Shape):

    def __init__(self, w=1.0, h=1.0):
        super().__init__("rect")
        self.w = w
        self.h = h


class Scene:

    def __init__(self):
        self.items = []
        self.size = (100, 100)
