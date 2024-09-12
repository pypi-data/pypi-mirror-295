class SoccerDimensions:
    def __init__(self, pitch_length=105, pitch_width=68):
        self.length = pitch_length
        self.width = pitch_width
        self.penalty_area_length = 16.5
        self.penalty_area_width = 40.3
        self.six_yard_box_length = 5.5
        self.six_yard_box_width = 18.32
        self.penalty_spot_distance = 11
        self.center_circle_radius = 9.15
        self.penalty_arc_radius = 9.15
        self.goal_width = 7.32
        self.goal_depth = 2.44


class BasketballDimensions:
    def __init__(self, court_type="nba"):
        if court_type == "nba":
            self.length = 94.0
            self.width = 50.0
            self.three_point_radius = 23.75
            self.three_point_line_distance = 3.0
            self.key_width = 16.0
            self.key_height = 19.0
            self.free_throw_line_distance = 15.0
            self.free_throw_circle_radius = 6.0
            self.backboard_width = 6.0
            self.rim_diameter = 1.5
            self.restricted_area_radius = 4.0
            self.center_circle_radius = 6.0
            self.lane_line_distance = 19.0
            self.no_charge_semi_circle_radius = 4.0
            self.backboard_distance = 4.0
            self.lower_defensive_box_distance = 19.0  # New dimension
            self.coaching_box_distance = 28.0  # New dimension
            self.substitution_box_distance = 4.0  # New dimension
            self.game_officials_table_distance = 4.0  # New dimension
            self.midcourt_area_marker_distance = 28.0  # New dimension
            self.baseline_distance = 0.0  # New dimension
            self.sideline_distance = 0.0  # New dimension
        elif court_type == "wnba":
            self.length = 94.0
            self.width = 50.0
            self.three_point_radius = 22.15
            self.three_point_line_distance = 3.0
            self.key_width = 16.0
            self.key_height = 19.0
            self.free_throw_line_distance = 15.0
            self.free_throw_circle_radius = 6.0
            self.backboard_width = 6.0
            self.rim_diameter = 1.5
            self.restricted_area_radius = 4.0
            self.center_circle_radius = 6.0
            self.lane_line_distance = 19.0
            self.no_charge_semi_circle_radius = 4.0
            self.backboard_distance = 4.0
            self.lower_defensive_box_distance = 19.0  # New dimension
            self.coaching_box_distance = 28.0  # New dimension
            self.substitution_box_distance = 4.0  # New dimension
            self.game_officials_table_distance = 4.0  # New dimension
            self.midcourt_area_marker_distance = 28.0  # New dimension
            self.baseline_distance = 0.0  # New dimension
            self.sideline_distance = 0.0  # New dimension


class HandballDimensions:
    def __init__(self, court_length=40, court_width=20):
        self.length = court_length
        self.width = court_width
        self.goal_line_distance = 6
        self.goal_area_length = 6
        self.goal_area_width = 3
        self.free_throw_line_distance = 9
        self.goal_width = 3
        self.goal_height = 2
        self.seven_meter_line = 7
        self.substitution_area_length = 4.5
        self.center_line_width = 0.05
        self.goal_area_line_width = 0.08
