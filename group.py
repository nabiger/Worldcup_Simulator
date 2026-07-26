import random
from match import Match

class Group:
    """کلاس مدیریت یک گروه در مرحله گروهی."""

    def __init__(self, name, teams):
        """
        سازنده کلاس گروه.
        Args:
            name (str): نام گروه
            teams (list of Team): لیست 4 تیم گروه
        """
        self.name = name
        self.teams = teams
        for team in self.teams:
            team.group = self.name

    def play_all_matches(self):
        """انجام تمام مسابقات درون گروهی به صورت دوره ای."""
        for i in range(len(self.teams)):
            for j in range(i + 1, len(self.teams)):
                match = Match(self.teams[i], self.teams[j], is_knockout=False)
                match.play()

    def get_ranking(self):
        """رتبه بندی تیم ها بر اساس امتیاز، تفاضل گل، گل زده و در نهایت قرعه."""
        self.teams.sort(key=lambda t: (
            t.points,
            t.goal_difference(),
            t.goals_for,
            random.random()
        ), reverse=True)
        return self.teams

    def advance_teams(self):
        """برگرداندن دو تیم اول صعودکننده."""
        ranked = self.get_ranking()
        return ranked[0], ranked[1]