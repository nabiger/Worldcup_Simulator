import random
import numpy as np

class Team:
    """کلاس تیم ملی فوتبال برای نگهداری اطلاعات و شبیه سازی عملکرد تیم."""

    def __init__(self, name, attack, defense, rank):
        """
        سازنده کلاس تیم.
        Args:
            name (str): نام تیم
            attack (int): قدرت حمله تیم
            defense (int): قدرت دفاع تیم
            rank (int): رتبه فیفا تیم
        """
        self.name = name
        self.attack = attack
        self.defense = defense
        self.rank = rank
        
        self.goals_for = 0
        self.goals_against = 0
        self.points = 0
        self.group = None

    def goal_difference(self):
        """برگرداندن تفاضل گل تیم."""
        return self.goals_for - self.goals_against

    def reset_stats(self):
        """صفر کردن آمار تیم برای شبیه سازی مجدد."""
        self.goals_for = 0
        self.goals_against = 0
        self.points = 0
        self.group = None

    def simulate_match(self, opponent, is_knockout=False):
        """
        شبیه سازی نتیجه بازی با تیم حریف.
        Args:
            opponent (Team): تیم حریف
            is_knockout (bool): آیا بازی در مرحله حذفی است یا خیر
        Returns:
            tuple: (گل های خودی، گل های حریف، برنده مسابقه، پنالتی خودی، پنالتی حریف)
        """
        lambda_self = (self.attack / 100) * 1.5 + (1 - opponent.defense / 100) * 0.8
        lambda_opp = (opponent.attack / 100) * 1.5 + (1 - self.defense / 100) * 0.8

        goals_self = np.random.poisson(lambda_self)
        goals_opp = np.random.poisson(lambda_opp)

        winner = None
        pen_self = None
        pen_opp = None

        if goals_self > goals_opp:
            winner = self
        elif goals_opp > goals_self:
            winner = opponent
        else:
            if is_knockout:
                lambda_self_et = lambda_self * 0.33
                lambda_opp_et = lambda_opp * 0.33
                
                goals_self += np.random.poisson(lambda_self_et)
                goals_opp += np.random.poisson(lambda_opp_et)
                
                if goals_self > goals_opp:
                    winner = self
                elif goals_opp > goals_self:
                    winner = opponent
                else:
                    pen_self, pen_opp, winner = self._simulate_penalties(opponent)
            else:
                winner = None

        return goals_self, goals_opp, winner, pen_self, pen_opp

    def _simulate_penalties(self, opponent):
        """شبیه سازی ضربات پنالتی."""
        p_self = 0.75 + (self.attack - opponent.defense) / 250
        p_self = max(0.6, min(0.9, p_self))
        
        p_opp = 0.75 + (opponent.attack - self.defense) / 250
        p_opp = max(0.6, min(0.9, p_opp))
        
        pen_self_goals = 0
        pen_opp_goals = 0
        
        for _ in range(5):
            if random.random() < p_self:
                pen_self_goals += 1
            if random.random() < p_opp:
                pen_opp_goals += 1
                
        while pen_self_goals == pen_opp_goals:
            scored_self = random.random() < p_self
            scored_opp = random.random() < p_opp
            
            if scored_self:
                pen_self_goals += 1
            if scored_opp:
                pen_opp_goals += 1
                
            if pen_self_goals != pen_opp_goals:
                break
                
        winner = self if pen_self_goals > pen_opp_goals else opponent
        return pen_self_goals, pen_opp_goals, winner