class Match:
    """کلاس مدیریت و اجرای یک مسابقه بین دو تیم."""

    def __init__(self, team1, team2, is_knockout=False):
        """
        سازنده کلاس مسابقه.
        Args:
            team1 (Team): تیم اول
            team2 (Team): تیم دوم
            is_knockout (bool): آیا بازی حذفی است
        """
        self.team1 = team1
        self.team2 = team2
        self.goals1 = 0
        self.goals2 = 0
        self.is_knockout = is_knockout
        self.winner = None
        self.pen1 = None
        self.pen2 = None

    def play(self):
        """اجرای مسابقه، محاسبه نتیجه و به روزرسانی آمار تیم ها."""
        self.goals1, self.goals2, self.winner, self.pen1, self.pen2 = self.team1.simulate_match(self.team2, self.is_knockout)
        
        if not self.is_knockout:
            self.team1.goals_for += self.goals1
            self.team1.goals_against += self.goals2
            self.team2.goals_for += self.goals2
            self.team2.goals_against += self.goals1
            
            if self.winner == self.team1:
                self.team1.points += 3
            elif self.winner == self.team2:
                self.team2.points += 3
            else:
                self.team1.points += 1
                self.team2.points += 1

    def __str__(self):
        """نمایش نتیجه مسابقه."""
        result = f"{self.team1.name} {self.goals1}-{self.goals2} {self.team2.name}"
        if self.pen1 is not None and self.pen2 is not None:
            result += f" ({self.pen1}-{self.pen2} pens)"
        if self.is_knockout and self.winner:
            result += f" -> برنده: {self.winner.name}"
        return result