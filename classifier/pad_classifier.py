class PadClassifier:
    """
    تشخیص خانواده یک Pad
    """

    def classify(self, pad):

        if pad.shape is None:
            return "UNKNOWN"


        shape = pad.shape.lower()


        if shape == "circle":
            return "CIRCLE"


        if shape == "rectangle":
            return "RECTANGLE"


        if shape == "rounded_rectangle":
            return "ROUNDED_RECTANGLE"


        return "CUSTOM"



class PadClassifier_old:

    def classify(self, pad):

        shape = pad.shape.lower()

        if shape == "circle":
            return "CIRCLE"

        elif shape == "rectangle":
            return "RECTANGLE"

        elif shape == "rounded_rectangle":
            return "ROUNDED_RECTANGLE"

        else:
            return "CUSTOM"
