# Ryan-Ilan-Portfolio
Hi, I am Ryan Ilan. 
I am a Bachelor of Science student at CSUN with a Major in Computer Science and a Minor in Data Science. 
I have a passion for sports and data analytics.
- Current GPA at CSUN: 3.66
- Expected Graduation Date: Spring 2027

# Experience
- I am currently working with sportFX.ai as a computer vision intern.
- I am also currently working for the CSUN Baseball team as a Data Analyst.
- I am presenting a research project at Saberseminar 2026 in Chicago on August 29th. 
- Python Libraries:
  - Pybaseball
  - Matplotlib
  - Pandas
  - Numpy
  - and more
 
# Reach Me
- Email: rilan270@gmail.com
- Connect with me on LinkedIn: [Ryan Ilan](https://www.linkedin.com/in/ryan-ilan/)

# Projects
- When Should You Challenge? Estimating ABS Challenge Value Using Matchup-Level RE288 Projections
  - Abstract: "Our project researches the value of an ABS Challenge. We used machine learning, specifically an XGBoost model, to create a projection of RE288. We looked at data from the 2023-2025 seasons and compared it to the baseline standard RE288. Our model includes batter and pitcher statistics for their season long performances to better estimate a player specific run expectancy. Using this information, we created a strategy for how a team would use this in game planning their approach to ABS. The model creates an RE288 table with projected numbers for a batter and pitcher matchup. It then calculates the value of a challenge for each of the 288 situations. Finally, the program calculates the confidence threshold needed to return zero run value. As a player, you would estimate your confidence the umpire was wrong. If your confidence is greater than the situation's confidence threshold, you would use your challenge. Our project also delivers an interpretable version of these charts for players and coaches to understand. Our decision matrix is the culmination of our research and explains what the value of a challenge is most dependent on. It is not reasonable to assume players can quantify their confidence in the short window after an umpire makes their call. Let alone, be able to remember all the possible matchups they might face and then the 288 situations for that specific matchup. The decision matrix is a simplified version of our charts that will guide players on our challenge strategy. In addition to the Decision Matrix, we would implement post game audits following games. These will be held with players so that they will learn from their experience. The overall goal of this project is to improve how teams utilize ABS Challenges."
  - Project was presented to COMP 542 Course at CSUN.
  - Project was presented at Saberseminar 2026 conference in Chicago.
      - [Link to watch presentation](https://www.youtube.com/watch?v=HhQHP0xGNOk)
  - Co-Author: Jordan Gottlieb
  - Code for projected run expectancy of a matchup in sample code folder.
  - Tables created for hypothetical Hitter Friendly matchup included in sample reports.
  - Decision Matrix is also available to view in Sample Reports. 
 
- Spray Charts
  - Using python, I wrote a program that takes data collected by a Trackman and generates a PDF with spray charts.
  - I used the data from the 2025 CSUN Fall scrimmages to test my program.
  - I was asked to create this to have defensive positioning charts for coaching staff.
  - The spray charts include:
    - Color coded ball in play icons.
    - Outline of CSUN field with dimensions.
      - To generate the outline, I followed the trackman bearing measurement field set up.
      - Dead center was 0° with the left field line being -45° and right field line being 45°.
      - CSUN has right field, center field, power alleys, and left field distances listed.
      - Original version of outfield wall was pointed and did not reflect real shape of the CSUN wall.
      - Used google maps calculate distance feature to measure more distance datapoints along wall.
      - Used inverse cosine to calculate angle with two distances, adjacnet being down right or left field line and the point I was measuring along the wall being         the hypotenuse.
      - Allowed me to better draw real CSUN wall shape.
    - CSUN logo faded into center field grass.
    - Features of every baseball field to further illustrate where the batted ball landed.
      - Infield dirt and grass, bases, and pitching mound.

- Hitter Reports
  - Using python, I created a script that takes data collected by Trackman systems and creates a PDF report of a hitter's season.
  - I used the data from the CSUN Baseball Fall scrimmages to generate my first reports.
  - My reports feature the following:
    - Launch Angle and Average Exit Velocity Visual.
    - Color coded spray chart of batter's hits overlayed onto a field with CSUN's logo and dimensions.
    - 3 Metrics tables each with Totals and split to show stats VS. either handed pitcher
      - Standard Metrics (AVG, OBP, SLG, OPS, Hits, PA)
      - Approach Metrics (Swing Rate, Contact Rate, In vs Out of zone, K%, BB%)
      - Contact Quality Metrics (AVG EV, Launch Angle, Hard Hit Rate, etc.)
    - Strike zone showcasing batters swing and whiff rates in divided parts of the zone.
    - A second page or "back side" to the report splitting the 3 tables and their respective stats by pitch type instead of pitcher handedness.
   
- Pitcher Profiles
  - Using python, I helped review code that created reports from data collected by Trackman system at CSUN.

- Note Taking Software
  - For my Intro to Software Engineering course, I worked in a team of 4 building a note taking software.
  - The software was called "CuteNote" and it was an offline notebook style application.
  - Customizable background colors, fonts, font color, font size and stickers.
  - My contribution to the software was the settings page which let the user customize the theme of the application to their preferences.
  - I also ran the test cases to ensure the software met our requirements.
  - We used agile development method, github for version control, and other software engineering techniques learned in the course.

# Currently Working on These Projects:
- Stuff+ Model for CSUN Baseball Team
- Computer Vision Project "What Pitch am I Throwing?"
  - Using computer vision to extract data from MLB broadcasts of pitcher's motions up until their release point. using two machine learning models to predict what pitch type is being thrown. The goal of the project is to identify when a pitcher has a tell in their motion.
- WATCHER Project with ARCS Lab at CSUN.
  - Wheelchair Navigation Team
  - Computer Vision Object Detection surrounding wheelchair
