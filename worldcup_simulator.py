
# دانشجو: نیکان بختیازی
# شماره دانشجویی : 3861692929
# عنوان پروژه: شبیه ساز جام جهانی
# تاریخ تحویل: 1405/05/04


import csv
import os
import random
import matplotlib.pyplot as plt

# ایمپورت کردن ماژول‌های ساخته شده
from team import Team
from match import Match
from group import Group
from knockout_stage import KnockoutStage


class WorldCupSimulator:
    """کلاس اصلی شبیه ساز جام جهانی شامل تمامی مراحل و منوها."""

    def __init__(self):
        self.teams = []
        self.groups = []
        self.round_of_16 = None
        self.quarterfinals = None
        self.semifinals = None
        self.final = None
        self.champion = None
        self.bracket_history = []
        self.is_teams_loaded = False
        self.is_groups_drawn = False

    def load_teams_from_csv(self):
        """دریافت مسیر فایل از کاربر و بارگذاری تیم ها."""
        file_path = input("\nلطفاً مسیر کامل فایل CSV خود را وارد کنید (مثلاً C:\\data\\teams.csv): ")
        file_path = file_path.strip().replace('"', '').replace("'", "")
        
        if not os.path.exists(file_path):
            print(f"خطا: فایلی در مسیر '{file_path}' پیدا نشد!")
            return False

        self.teams = []
        try:
            with open(file_path, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    team = Team(
                        name=row['name'],
                        attack=int(row['attack']),
                        defense=int(row['defense']),
                        rank=int(row['rank'])
                    )
                    self.teams.append(team)
            self.is_teams_loaded = True
            print("تیم ها با موفقیت بارگذاری شدند.")
            return True
        except Exception as e:
            print(f"خطا در خواندن فایل: {e}")
            return False

    def seed_and_draw_groups(self):
        """سیدبندی و قرعه کشی 8 گروه به صورت تصادفی."""
        sorted_teams = sorted(self.teams, key=lambda t: t.rank)
        
        pots = [
            sorted_teams[0:8],   # Seed 1
            sorted_teams[8:16],  # Seed 2
            sorted_teams[16:24], # Seed 3
            sorted_teams[24:32]  # Seed 4
        ]
        
        group_names = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
        self.groups = []
        
        for name in group_names:
            group_teams = []
            for pot in pots:
                selected_team = random.choice(pot)
                group_teams.append(selected_team)
                pot.remove(selected_team)
            self.groups.append(Group(name, group_teams))
            
        self.is_groups_drawn = True
        print("قرعه کشی گروه ها با موفقیت انجام شد.")

    def run_group_stage(self, display=True):
        """اجرای تمام بازی های مرحله گروهی."""
        if display:
            print("\n--- نتایج مرحله گروهی ---")
            
        for group in self.groups:
            group.play_all_matches()
            if display:
                print(f"\nGroup {group.name}")
                ranking = group.get_ranking()
                for i, team in enumerate(ranking, 1):
                    print(f"{i}. {team.name}: {team.points} pts, GD {team.goal_difference():+d}, GF {team.goals_for}")

    def setup_knockout_bracket(self):
        """تنظیم بازی های مرحله حذفی براساس قانون فیفا."""
        advancing = {}
        for group in self.groups:
            first, second = group.advance_teams()
            advancing[group.name] = (first, second)

        r16_matches = [
            Match(advancing['A'][0], advancing['B'][1], True),
            Match(advancing['C'][0], advancing['D'][1], True),
            Match(advancing['E'][0], advancing['F'][1], True),
            Match(advancing['G'][0], advancing['H'][1], True),
            Match(advancing['B'][0], advancing['A'][1], True),
            Match(advancing['D'][0], advancing['C'][1], True),
            Match(advancing['F'][0], advancing['E'][1], True),
            Match(advancing['H'][0], advancing['G'][1], True)
        ]
        self.round_of_16 = KnockoutStage('Round of 16', r16_matches)

    def run_knockout_stage(self, display=True):
        """اجرای تمام مراحل حذفی تا تعیین قهرمان."""
        self.round_of_16.play_round()
        r16_winners = self.round_of_16.get_winners()
        if display:
            self.round_of_16.display_results()

        qf_matches = [
            Match(r16_winners[0], r16_winners[1], True),
            Match(r16_winners[2], r16_winners[3], True),
            Match(r16_winners[4], r16_winners[5], True),
            Match(r16_winners[6], r16_winners[7], True)
        ]
        self.quarterfinals = KnockoutStage('Quarterfinals', qf_matches)
        self.quarterfinals.play_round()
        qf_winners = self.quarterfinals.get_winners()
        if display:
            self.quarterfinals.display_results()

        sf_matches = [
            Match(qf_winners[0], qf_winners[1], True),
            Match(qf_winners[2], qf_winners[3], True)
        ]
        self.semifinals = KnockoutStage('Semifinals', sf_matches)
        self.semifinals.play_round()
        sf_winners = self.semifinals.get_winners()
        if display:
            self.semifinals.display_results()

        final_match = [Match(sf_winners[0], sf_winners[1], True)]
        self.final = KnockoutStage('Final', final_match)
        self.final.play_round()
        self.champion = self.final.get_winners()[0]
        if display:
            self.final.display_results()
            print(f"\n🏆 Champion: {self.champion.name} 🏆\n")
            
        self.bracket_history = [self.round_of_16, self.quarterfinals, self.semifinals, self.final]

    def run_full_simulation(self, display=True):
        """اجرای کامل یک دوره مسابقات."""
        for team in self.teams:
            team.reset_stats()
            
        self.seed_and_draw_groups()
        self.run_group_stage(display=display)
        self.setup_knockout_bracket()
        self.run_knockout_stage(display=display)
        return self.champion

    def most_likely_champion(self, num_simulations=1000):
        """شبیه سازی چند باره جام و گزارش درصد شانس قهرمانی هر تیم."""
        if num_simulations <= 0:
            print("خطا: تعداد شبیه سازی باید عددی مثبت باشد.")
            return

        champions_count = {team.name: 0 for team in self.teams}
        print(f"\nدر حال شبیه سازی {num_simulations} بار... لطفاً صبر کنید.")
        
        for _ in range(num_simulations):
            champion = self.run_full_simulation(display=False)
            champions_count[champion.name] += 1
            
        print(f"\n{num_simulations} شبیه سازی انجام شد.")
        print("درصد قهرمانی هر تیم:")
        
        sorted_champs = sorted(champions_count.items(), key=lambda x: x[1], reverse=True)
        top_teams = []
        top_percentages = []
        
        for name, count in sorted_champs:
            if count > 0:
                percentage = (count / num_simulations) * 100
                print(f"{name}: {percentage:.1f}%")
                if percentage >= 1.0:
                    top_teams.append(name)
                    top_percentages.append(percentage)

        try:
            plt.figure(figsize=(10, 6))
            plt.bar(top_teams, top_percentages, color='skyblue')
            plt.xlabel('Teams')
            plt.ylabel('Win Probability (%)')
            plt.title(f'World Cup 2026 Champion Probability ({num_simulations} Simulations)')
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.show()
        except Exception:
            pass

    def display_bracket(self):
        """نمایش آخرین براکت حذفی."""
        if not self.bracket_history:
            print("خطا: هنوز هیچ شبیه سازی کاملی انجام نشده است.")
            return
            
        print("\n--- Knockout Bracket ---")
        for stage in self.bracket_history:
            stage.display_results()
            if stage.round_name == 'Final':
                print(f"\nChampion: {stage.get_winners()[0].name}")

    def menu(self):
        """نمایش منوی اصلی و دریافت انتخاب کاربر."""
        while True:
            print("\n*** شبیه ساز جام جهانی ***")
            print("1. بارگذاری تیم ها از فایل CSV")
            print("2. انجام قرعه کشی گروه ها (سیدبندی خودکار)")
            print("3. اجرای مرحله گروهی و نمایش جدول هر گروه")
            print("4. اجرای کامل جام (گروهی + حذفی) و نمایش قهرمان")
            print("5. شبیه سازی چند باره و گزارش درصد قهرمانی")
            print("6. نمایش براکت حذفی آخرین شبیه سازی")
            print("7. خروج")
            
            choice = input("لطفاً یک گزینه انتخاب کنید: ")
            
            if choice == '1':
                self.load_teams_from_csv()
            elif choice == '2':
                if not self.is_teams_loaded:
                    print("خطا: ابتدا تیم ها را بارگذاری کنید.")
                else:
                    self.seed_and_draw_groups()
            elif choice == '3':
                if not self.is_groups_drawn:
                    print("خطا: ابتدا قرعه کشی باید انجام شده باشد.")
                else:
                    self.run_group_stage()
            elif choice == '4':
                if not self.is_teams_loaded:
                    print("خطا: ابتدا تیم ها را بارگذاری کنید.")
                else:
                    self.run_full_simulation()
            elif choice == '5':
                if not self.is_teams_loaded:
                    print("خطا: ابتدا تیم ها را بارگذاری کنید.")
                else:
                    try:
                        num = input("تعداد شبیه سازی را وارد کنید (پیش فرض 1000): ")
                        num = int(num) if num.strip() else 1000
                        self.most_likely_champion(num)
                    except ValueError:
                        print("خطا: لطفاً یک عدد صحیح وارد کنید.")
            elif choice == '6':
                if not self.is_teams_loaded:
                    print("خطا: ابتدا تیم ها را بارگذاری کنید.")
                else:
                    self.display_bracket()
            elif choice == '7':
                print("خروج از برنامه...")
                break
            else:
                print("گزینه نامعتبر است. لطفاً دوباره تلاش کنید.")

if __name__ == "__main__":
    simulator = WorldCupSimulator()
    simulator.menu()