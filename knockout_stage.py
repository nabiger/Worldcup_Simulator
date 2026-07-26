class KnockoutStage:
    """کلاس مدیریت مسابقات در یک مرحله حذفی."""

    def __init__(self, round_name, matches):
        """
        سازنده مرحله حذفی.
        Args:
            round_name (str): نام مرحله
            matches (list of Match): لیست مسابقات این مرحله
        """
        self.round_name = round_name
        self.matches = matches
        self.winners = []

    def play_round(self):
        """اجرای تمام بازی های این مرحله."""
        self.winners = []
        for match in self.matches:
            match.play()
            self.winners.append(match.winner)

    def get_winners(self):
        """برگرداندن لیست تیم های برنده این مرحله."""
        return self.winners

    def display_results(self):
        """چاپ نتایج بازی های این مرحله حذفی."""
        print(f"\n--- {self.round_name} ---")
        for match in self.matches:
            print(match)