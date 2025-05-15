class Person:
    def __init__(self, track_id, first_location):
        self.track_id = track_id
        self.passed_lines = []
        self.direction = None
        self.first_location = first_location
        self.items = {} # bbox 형식 {xmin, ymin, xmax, ymax}
        self.feature_vector = None

    def update_position(self, center_x):
        from video_processor import OUTSIDE_LINE, INSIDE_LINE

        if self.first_location < OUTSIDE_LINE:
            if center_x > OUTSIDE_LINE and "outside" not in self.passed_lines:
                self.passed_lines.append("outside")
            elif center_x > INSIDE_LINE and "inside" not in self.passed_lines:
                self.passed_lines.append("inside")
        elif self.first_location > INSIDE_LINE:
            if center_x > INSIDE_LINE and "inside" not in self.passed_lines:
                self.passed_lines.append("inside")
            elif center_x < OUTSIDE_LINE and "outside" not in self.passed_lines:
                self.passed_lines.append("outside")

        if len(self.passed_lines) >= 2:
            if self.passed_lines == ["inside", "outside"]:
                self.direction = "exit"
            elif self.passed_lines == ["outside", "inside"]:
                self.direction = "entry"
