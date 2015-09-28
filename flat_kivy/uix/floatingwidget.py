
from kivy.properties import (NumericProperty, ReferenceListProperty,
                             ObjectProperty)
from kivy.uix.widget import Widget


class FloatingWidget(Widget):
    """
    This widget automatically positions itself relative to its target.
    It accepts only one child, and sets that child to its size/position.

    Obviously, you may get undefined behavior if you add this widget to a
    layout or other widget that positions its children.
    """

    # Position relative to parent, in percentage.
    # 0.0, 0.0 if bottom-left corner of parent, 1.0,
    # 1.0 is top-right corner of parent, etc.
    x_rel = NumericProperty(0)
    y_rel = NumericProperty(0)
    pos_rel = ReferenceListProperty(x_rel, y_rel)

    # both x and y axes...
    padding = NumericProperty(0)

    target = ObjectProperty(None)

    def __init__(self, **kw):
        super(FloatingWidget, self).__init__(**kw)
        self._prev_target = None

        self.bind(
            padding=self._update,
            pos_rel=self._update,
            target=self._bind_target,
        )

    def add_widget(self, w, **kw):
        if len(self.children) > 1:
            raise ValueError("FloatingWidget only accepts one child.")

        super(FloatingWidget, self).add_widget(w, **kw)

    def on_pos(self, *ar):
        if self.children:
            self.children[0].pos = self.pos

    def on_size(self, *ar):
        if self.children:
            self.children[0].size = self.size

    def _bind_target(self, *ar):
        target = self.target

        # Unbind from previous target, if we had one.
        if self._prev_target is not None:
            self._prev_target.unbind(
                size=self._update,
                pos=self._update
            )

        # Bind to new target, if we have one.
        if target is not None:
            target.bind(
                size=self._update,
                pos=self._update
            )

        self._prev_target = target

    def _update(self, *ar):
        """
        Position the FloatingWidget relative to the target.
        """
        target = self.target
        if target is not None:
            w = target.width - self.width - self.padding * 2
            h = target.height - self.height - self.padding * 2

            self.x = self.x_rel * w + self.padding
            self.y = self.y_rel * h + self.padding
