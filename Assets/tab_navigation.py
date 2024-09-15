def on_key_down(self, instance, keyboard, keycode, text, modifiers):
        # print(f"Keycode: {keycode}")
        if keycode == 43:
            # Collect all focusable widgets
            focusable_widgets = []
            for widget in self.walk(restrict=True):
                if hasattr(widget, 'focus') and widget.is_focusable:
                    focusable_widgets.append(widget)

            # for x in focusable_widgets: print(x.)
            # Find the currently focused widget
            focused_widget = next((w for w in focusable_widgets if w.focus), None)
            # print(focused_widget)
            if focused_widget:
                # Find the index of the focused widget
                index = focusable_widgets.index(focused_widget)
                # Move focus to the next widget, wrapping around if necessary
                next_index = (index + 1) % len(focusable_widgets)
            else:
                next_index = 0
            focusable_widgets[next_index].focus = True
            return True  # Indicate that the event was handled

        return False  # Indicate that the event was not handled