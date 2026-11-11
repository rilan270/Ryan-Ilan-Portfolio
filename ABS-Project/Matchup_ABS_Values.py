import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from xgboost import XGBRegressor
import os


# This was a part of a project that I presented at Saberseminar conference in chicago
# I worked on this project with a partner, Jordan Gottlieb. We shared the workload 
# on this project

matplotlib.rcParams['savefig.dpi'] = 600
script_dir = os.path.dirname(os.path.abspath(__file__))
re288 = os.path.join(script_dir, "..", "re288_data", "re288Data.csv")
re288_df = pd.read_csv(re288)

features = [
    "platoon_adv",
    "Rbat+",
    "pit_pas",
    "bat_pas",
    "ERA+",
    "balls",
    "strikes",
    "outs_when_up",
    "1b", "2b", "3b"
]

target = "runs_after_pitch"

print("\n Type in hitter name")
hitter_name = input()
print("\n Type in hitter handedness (L or R)")
hitter_handedness = input()
print("\n Type in the hitters PAs amount")
bat_pas = float(input())
print("\n Type in hitter Rbat+")
hitter_Rbat = float(input())
print("\n Type in pitcher name")
pitcher_name = input()
print("\n Type in pitcher handedness (L or R)")
pitcher_handedness = input()
print("\n Type in the pitchers batters faced amount")
pit_pas = float(input())
print("\n Type in pitcher ERA+")
pitcher_ERA = float(input())

matchup_df = re288_df.copy()
matchup_df["ERA+"] = pitcher_ERA
matchup_df["Rbat+"] = hitter_Rbat
if pitcher_handedness == "L" or pitcher_handedness == "l":
    p_throws = 0
if pitcher_handedness == "R" or pitcher_handedness == "r":
    p_throws = 1
if hitter_handedness == "L" or hitter_handedness == "l":
    stand = 0
if hitter_handedness == "R" or hitter_handedness == "r":
    stand = 1
matchup_df["bat_pas"] = bat_pas
matchup_df["pit_pas"] = pit_pas
matchup_df["stand"] = stand
matchup_df["p_throws"] = p_throws
matchup_df["platoon_adv"] = int(stand != p_throws)
matchup_df["matchup"] = p_throws * 2 + stand
matchup_df_X = matchup_df[features]

loaded_model = XGBRegressor()
model_path = os.path.join(script_dir, "xgb_run_expectancy_model.json")
loaded_model.load_model(model_path)

matchup_preds = loaded_model.predict(matchup_df_X)

matchup_df["model_pred"] = matchup_preds
matchup_df["re288"] = matchup_df["runs_after_count"]
matchup_df["difference"] = matchup_df["model_pred"] - matchup_df["re288"]

matchup_df["base_state"] = (
    matchup_df["1b"].astype(int).astype(str) +
    matchup_df["2b"].astype(int).astype(str) +
    matchup_df["3b"].astype(int).astype(str)
)

base_order = ["000", "100", "010", "110", "001", "101", "011", "111"]

matchup_df["base_state"] = pd.Categorical(matchup_df["base_state"], categories=base_order, ordered=True)

matchup_df["count"] = (
    matchup_df["balls"].astype(str) + "-" +
    matchup_df["strikes"].astype(str)
)

re288_table = matchup_df.pivot_table(
    values="model_pred",
    index=["outs_when_up", "base_state"],
    columns="count",
    aggfunc="mean"
)


def build_called_pitch_value_table(re288_table):
    counts = ["0-0","0-1","0-2","1-0","1-1","1-2","2-0","2-1","2-2","3-0","3-1","3-2"]

    def get_re(table, outs, base_state, count):
        try:
            return table.loc[(outs, base_state), count]
        except KeyError:
            return np.nan

    def next_count_strike(balls, strikes, outs, base_state):
        if strikes == 2:
            new_outs = outs + 1
            if new_outs >= 3:
                return None
            return (new_outs, base_state, "0-0")
        else:
            return (outs, base_state, f"{balls}-{strikes+1}")

    def next_count_ball(balls, strikes, outs, base_state):
        if balls == 3:
            b1 = int(base_state[0])
            b2 = int(base_state[1])
            b3 = int(base_state[2])
            if b1 == 0:
                new_b1, new_b2, new_b3 = 1, b2, b3
            elif b2 == 0:
                new_b1, new_b2, new_b3 = 1, 1, b3
            elif b3 == 0:
                new_b1, new_b2, new_b3 = 1, 1, 1
            else:
                new_b1, new_b2, new_b3 = 1, 1, 1
            new_base_state = f"{new_b1}{new_b2}{new_b3}"
            return (outs, new_base_state, "0-0")
        else:
            return (outs, base_state, f"{balls+1}-{strikes}")

    results = {}

    for outs in [0, 1, 2]:
        for base_state in base_order:
            for count in counts:
                balls, strikes = int(count[0]), int(count[2])

                strike_result = next_count_strike(balls, strikes, outs, base_state)
                if strike_result is None:
                    re_strike = 0.0
                else:
                    new_outs, new_bs, new_count = strike_result
                    re_strike = get_re(re288_table, new_outs, new_bs, new_count)

                ball_result = next_count_ball(balls, strikes, outs, base_state)
                new_outs, new_bs, new_count = ball_result

                if balls == 3 and base_state == "111":
                    re_ball = get_re(re288_table, new_outs, new_bs, new_count) + 1.0
                else:
                    re_ball = get_re(re288_table, new_outs, new_bs, new_count)

                results[(outs, base_state, count)] = re_ball - re_strike

    rows = []
    for outs in [0, 1, 2]:
        for base_state in base_order:
            row = {"outs_when_up": outs, "base_state": base_state}
            for count in counts:
                row[count] = results[(outs, base_state, count)]
            rows.append(row)

    diff_df = pd.DataFrame(rows)
    diff_df["base_state"] = pd.Categorical(diff_df["base_state"], categories=base_order, ordered=True)
    diff_df = diff_df.set_index(["outs_when_up", "base_state"])

    return diff_df


called_pitch_table = build_called_pitch_value_table(re288_table)

CHALLENGE_VALUE = 0.1861

def build_confidence_interval_table(called_pitch_table):
    ci = CHALLENGE_VALUE / (CHALLENGE_VALUE + called_pitch_table.abs())
    return ci

confidence_table = build_confidence_interval_table(called_pitch_table)

def format_bases_from_state(state):
    return (
        f"{'1B' if state[0] == '1' else '—'} "
        f"{'2B' if state[1] == '1' else '—'} "
        f"{'3B' if state[2] == '1' else '—'}"
    )


colors = plt.cm.bwr(np.linspace(0, 1, 256))
colors[:, :3] = colors[:, :3] * 0.6 + 0.4
pastel_cmap = LinearSegmentedColormap.from_list("pastel_bwr", colors)
pastel_cmap_r = pastel_cmap.reversed()



def plot_re_table(table, fig_title, subtitle=None, pct_format=False, cmap=None):
    if cmap is None:
        cmap = pastel_cmap

    sep_row = pd.DataFrame(
        [[np.nan] * len(table.columns)],
        columns=table.columns
    )

    display_table = pd.concat(
        [table.iloc[:8], sep_row, table.iloc[8:16], sep_row, table.iloc[16:]],
        ignore_index=True
    )

    row_labels_base = [
        f"{outs} | {format_bases_from_state(str(state))}"
        for outs, state in table.index
    ]
    row_labels = (
        row_labels_base[:8] + [""] +
        row_labels_base[8:16] + [""] +
        row_labels_base[16:]
    )

    fig, ax = plt.subplots(figsize=(4.9, 5))
    ax.axis("off")

    fmt = (lambda x: f"{x:.0%}" if not np.isnan(x) else "") if pct_format else (lambda x: f"{x:.3f}" if not np.isnan(x) else "")

    t = ax.table(
        cellText=[[fmt(x) for x in row] for row in display_table.values],
        rowLabels=row_labels,
        colLabels=display_table.columns,
        cellLoc="center",
        loc="center",
        bbox=[0.15, 0, 0.85, 1]
    )

    cells = t.get_celld()

    # Header for the row-label column.
    corner_w = cells[(1, -1)].get_width()
    corner_h = cells[(0, 0)].get_height()
    corner = t.add_cell(0, -1, corner_w, corner_h, text="outs | bases",loc="center", facecolor="black")
    corner.get_text().set_color("white")
    corner.get_text().set_weight("bold")
    cells = t.get_celld() 

    norm = matplotlib.colors.TwoSlopeNorm(
        vmin=np.percentile(table.values, 1),
        vcenter=np.percentile(table.values, 50),
        vmax=np.percentile(table.values, 99)
    )

    # setting widths
    for (row, col), cell in cells.items():
        if col == -1:
            cell.set_width(0.06)
        else:
            cell.set_width(0.08)

    # setting colors
    for (row, col), cell in cells.items():
        if row == 0:
            cell.set_facecolor("black")
            cell.set_text_props(color="white", weight="bold")
        elif col == -1:
            cell.set_facecolor("black")
            cell.set_text_props(color="white", weight="bold")
        elif row in [9, 18]:
            pass
        else:
            actual_row = row - 1 if row < 9 else row - 2 if row < 18 else row - 3
            value = table.iloc[actual_row, col]
            color = cmap(norm(value))
            cell.set_facecolor(color)

    for sep_row_idx in [9, 18]:
        for col in range(-1, display_table.shape[1]):
            cell = cells[(sep_row_idx, col)]
            cell.set_facecolor("black")
            cell.set_height(cell.get_height() * 0.3)

    t.auto_set_font_size(False)
    t.set_fontsize(6.5)
    t.scale(1, 1.15)

    plt.suptitle(fig_title, fontsize=14, fontweight="bold", y=0.99)
    if subtitle:
        plt.figtext(0.5, 0.87, subtitle, fontsize=10, ha="center")
    plt.subplots_adjust(left=0.02, right=0.98, top=0.85, bottom=0.02)

avg_run_value = re288_table.values.mean()
avg_chal_value = called_pitch_table.values.mean()

plot_re_table(
    re288_table,
    fig_title=(
        f"Projected Run Expectancy\n"
        f"{hitter_name} ({hitter_handedness}) vs {pitcher_name} ({pitcher_handedness})"
        ),
    subtitle=f"rBAT+: {hitter_Rbat:.0f} | ERA+: {pitcher_ERA:.0f} | Avg Run Value: {avg_run_value:.3f}"
)

plot_re_table(
    called_pitch_table,
    fig_title=(
        f"Correct Challenge Value\n"
        f"{hitter_name} ({hitter_handedness}) vs {pitcher_name} ({pitcher_handedness})"
        ),
    subtitle=f"rBAT+: {hitter_Rbat:.0f} | ERA+: {pitcher_ERA:.0f} | Avg Challenge Value: {avg_chal_value:.3f}",
)

plot_re_table(
    confidence_table,
    fig_title=(
        f"Confidence Thresholds\n"
        f"{hitter_name} ({hitter_handedness}) vs {pitcher_name} ({pitcher_handedness})"
        ),
    subtitle=f"rBAT+: {hitter_Rbat:.0f} | ERA+: {pitcher_ERA:.0f}",
    pct_format=True,
    cmap=pastel_cmap_r,
)



plt.show()