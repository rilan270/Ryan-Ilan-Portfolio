import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Circle, Polygon
from matplotlib.backends.backend_pdf import PdfPages
from PIL import Image
import numpy as np
import os
import argparse

# ------------------------
# Load file
# ------------------------
parser = argparse.ArgumentParser()
parser.add_argument("file", help="CSV file name inside Data/combined_data")
args = parser.parse_args()

CSUN_BASE_DIR = r"C:\Users\rbi39252\Box\Baseball\CSUN Baseball Projects\CSUN_Baseball"
data_dir = os.path.join(CSUN_BASE_DIR, "Data", "combined_data")
file_name = os.path.join(data_dir, args.file)

try:
    df = pd.read_csv(file_name)
except FileNotFoundError:
    print(f"File {file_name} not found. Please check the file name and try again.")
    raise SystemExit(1)

# ------------------------
# Dates
# ------------------------
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
first_date = df["Date"].min().strftime("%m-%d-%Y")
final_date = df["Date"].max().strftime("%m-%d-%Y")

# Filter only CSUN pitchers
df = df[df['PitcherTeam'] == 'CAL_MAT']

# ------------------------
# Load logos
# ------------------------
img_path = os.path.join(CSUN_BASE_DIR, "Resources", "images", "logo.png")
img = Image.open(img_path).resize((150, 150), Image.Resampling.LANCZOS).convert("RGB")

#transparent background logo
trans_img_path = os.path.join(CSUN_BASE_DIR, "Resources", "images", "logo_transparent.png")
trans_img = Image.open(trans_img_path)
trans_img.resize((150, 41), Image.Resampling.LANCZOS)
trans_img.convert("RGB")

# ------------------------
# Settings
# ------------------------
FIELD_SCALE = 1  # adjust if needed

# ------------------------
# Functions
# ------------------------
def polar_to_cart(r, theta_deg):
    theta = np.deg2rad(theta_deg)
    return r * np.sin(theta), r * np.cos(theta)

def draw_csun_field(ax):
    # -------------------------
    # Field outline
    # -------------------------
    field_outline = [
        polar_to_cart(330, -45), polar_to_cart(330, -40), polar_to_cart(335, -35),
        polar_to_cart(340, -31), polar_to_cart(345, -28), polar_to_cart(350, -25.5),
        polar_to_cart(355, -23.5), polar_to_cart(360, -21.5), polar_to_cart(365, -19.5),
        polar_to_cart(370, -18), polar_to_cart(375, -16.5), polar_to_cart(380, -15.5),
        polar_to_cart(385, -14), polar_to_cart(387, -13.5), polar_to_cart(390, -13),
        polar_to_cart(392, -12.3), polar_to_cart(394, -11), polar_to_cart(396, -9),
        polar_to_cart(397, -7), polar_to_cart(398, -5), polar_to_cart(399, -3),
        polar_to_cart(400,  0), polar_to_cart(399,  3), polar_to_cart(398,  5),
        polar_to_cart(397,  7), polar_to_cart(396,  10), polar_to_cart(394,  10.5),
        polar_to_cart(392,  11), polar_to_cart(390,  11.44), polar_to_cart(385,  12.6),
        polar_to_cart(380,  13.8), polar_to_cart(375,  15), polar_to_cart(370,  16.44),
        polar_to_cart(365,  17.9), polar_to_cart(360,  19.5), polar_to_cart(355,  21.27),
        polar_to_cart(350,  23.2), polar_to_cart(345,  25.4), polar_to_cart(340,  28),
        polar_to_cart(335,  31), polar_to_cart(330,  35), polar_to_cart(325,  40),
        polar_to_cart(325,  45), (0,0)
    ]

    field_poly = Polygon(
        field_outline,
        closed=True,
        facecolor='#9fd19f',
        edgecolor='black',
        lw=1.2,
        zorder=0
    )
    ax.add_patch(field_poly)

    # -------------------------
    # Infield dirt
    # -------------------------
    infield_radius = 160
    theta = np.linspace(-45, 45, 300)
    arc_pts = [[infield_radius*np.sin(np.deg2rad(t)), infield_radius*np.cos(np.deg2rad(t))] for t in theta]
    dirt_pts = np.vstack([[[0,0]], arc_pts, [[0,0]]])
    ax.add_patch(Polygon(dirt_pts, closed=True, facecolor="#efe3cf", edgecolor="black", lw=1.2, zorder=2))

    # -------------------------
    # INFIELD GRASS (diamond, not used for base placement)
    # -------------------------
    grass_size = 90
    half = grass_size / 2

    grass = Polygon(
        [[-half, half],
        [0, grass_size],
        [half, half],
        [0, 0]],
        closed=True,
        facecolor="#9fd39b",
        edgecolor="black",
        lw=1.2,
        zorder=3
    )
    ax.add_patch(grass)

    # -------------------------
    # Bases
    # -------------------------
    base_dist = 90
    base_size = 18
    half_base = base_size / 2

    def polar(dist, ang_deg):
        ang = np.deg2rad(ang_deg)
        return np.array([dist * np.sin(ang), dist * np.cos(ang)])

    angle_1b, angle_3b = -45, 45
    c1, c3 = polar(base_dist, angle_1b), polar(base_dist, angle_3b)

    def inward_shift(center):
        return np.array([-1,0]) if center[0]>0 else np.array([1,0])
    n1, n3 = inward_shift(c1)/np.linalg.norm(inward_shift(c1)), inward_shift(c3)/np.linalg.norm(inward_shift(c3))
    first_pt, third_pt = c1 + n1*half_base, c3 + n3*half_base
    second_pt = np.array([0, base_dist*np.sqrt(2)])

    def draw_base(cx, cy):
        s = base_size/2
        square = np.array([[-s,0],[0,s],[s,0],[0,-s]]) + np.array([cx,cy])
        ax.add_patch(Polygon(square, facecolor="white", edgecolor="black", lw=1.3, zorder=5))

    draw_base(*first_pt)
    draw_base(*second_pt)
    draw_base(*third_pt)

    # -------------------------
    # Home plate
    # -------------------------
    plate_y_offset = 6
    home = Polygon([[-9, plate_y_offset],[9, plate_y_offset],[9, plate_y_offset-7],
                    [0, plate_y_offset-13],[-9, plate_y_offset-7]],
                   facecolor="white", edgecolor="black", lw=1.3, zorder=5)
    ax.add_patch(home)

    # -------------------------
    # Pitcher's mound
    # -------------------------
    mound = Circle((0,60.5), radius=9, facecolor="#d2b48c", edgecolor="black", lw=1.2, zorder=4)
    ax.add_patch(mound)

    # CENTER FIELD LOGO (watermark)
    # -------------------------

    logo_img = trans_img

    # Center position
    logo_x = 0
    logo_y = 260

    logo_height = 40
    img_width, img_height = logo_img.size
    aspect_ratio = img_width / img_height
    logo_width = logo_height * aspect_ratio

    ax.imshow(
        logo_img,
        extent=[
            logo_x - logo_width/2,
            logo_x + logo_width/2,
            logo_y - logo_height/2,
            logo_y + logo_height/2
        ],
        alpha=0.4,
        zorder=1.8
    )

    # -------------------------
    # Axis
    # -------------------------
    ax.set_aspect('equal')
    ax.set_xlim(-360/FIELD_SCALE, 360/FIELD_SCALE)
    ax.set_ylim(-7/FIELD_SCALE, 410/FIELD_SCALE)
    ax.axis('off')

def draw_spray_chart(ax, pitcher_data):
    ax.set_facecolor("none")
    hits = pitcher_data[pitcher_data['Bearing'].between(-40, 50)]

    hit_colors = {'Single':'#1f77b4','Double':'#ff7f0e','Triple':'#2ca02c','HomeRun':'#d62728'}
    out_colors = {'Out':'#000000','Error':'#000000','FieldersChoice':'#000000'}

    for hit_type,color in hit_colors.items():
        subset = hits[hits['PlayResult']==hit_type]
        if not subset.empty:
            x = subset['Distance']*np.sin(np.deg2rad(subset['Bearing']))
            y = subset['Distance']*np.cos(np.deg2rad(subset['Bearing']))
            ax.scatter(x, y, c=color, s=30, alpha=1.0, edgecolor='black', zorder=6, label=hit_type)

    for bip_type,color in out_colors.items():
        subset = hits[hits['PlayResult']==bip_type]
        if not subset.empty:
            x = subset['Distance']*np.sin(np.deg2rad(subset['Bearing']))
            y = subset['Distance']*np.cos(np.deg2rad(subset['Bearing']))
            ax.scatter(x, y, c=color, s=30, alpha=1.0, edgecolor='white', zorder=6, label=bip_type)

    ax.legend(title="Hit Type", loc="lower left", bbox_to_anchor=(0.08, 0.03),
              fontsize=8, title_fontsize=9, frameon=True, framealpha=0.9)
    ax.set_aspect('equal')
    ax.set_xlim(-360/FIELD_SCALE, 360/FIELD_SCALE)
    ax.set_ylim(-7/FIELD_SCALE, 410/FIELD_SCALE)
    ax.axis('off')

# ------------------------
# Create PDF
# ------------------------
reports_dir = os.path.join(CSUN_BASE_DIR, "Reports")
pdf_path = os.path.join(reports_dir, "pitcher_spray_chart_fall.pdf")

with PdfPages(pdf_path) as pdf:
    for pitcher_name in df['Pitcher'].unique():
        pitcher_data = df[df['Pitcher'] == pitcher_name]
        pitcher_data_RHH = pitcher_data[pitcher_data['BatterSide'] == 'Right']
        pitcher_data_LHH = pitcher_data[pitcher_data['BatterSide'] == 'Left']

        # Loop through hitter sides
        for side, pdata in zip(['Right-Handed', 'Left-Handed'], [pitcher_data_RHH, pitcher_data_LHH]):
            if pdata.empty:
                continue

            fig = plt.figure(figsize=(8.5, 11), facecolor="white")
            fig.figimage(img, xo=40, yo=980, zorder=10)
            fig.suptitle(f"\n{pitcher_name}\nSpray Chart vs {side} Hitters\n{first_date} to {final_date}",
                         fontsize=16, fontweight='bold', color='black')

            ax_spray = fig.add_axes([0.05, 0.05, 0.9, 0.95])
            ax_spray.set_aspect('equal')
            ax_spray.axis('off')

            draw_csun_field(ax_spray)
            draw_spray_chart(ax_spray, pdata)

            pdf.savefig(fig)
            plt.close(fig)
