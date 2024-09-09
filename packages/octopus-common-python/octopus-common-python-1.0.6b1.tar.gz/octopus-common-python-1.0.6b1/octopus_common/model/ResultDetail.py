class ResultDetail:
    classType = None

    def __init__(self, class_type=None):
        if class_type is not None:
            self.classType = class_type
