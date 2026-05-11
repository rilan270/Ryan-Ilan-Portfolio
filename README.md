# Ryan-Ilan-Portfolio
Hi, I am Ryan Ilan. 
I am a Bachelor of Science student at CSUN with a Major in Computer Science and a Minor in Data Science. 
I have a passion for sports and data analytics.
Current GPA at CSUN: 3.85

# Experience
- I am currently working with the CSUN baseball team as a data analytics intern.
- Python Libraries:
  - Pybaseball
  - Matplotlib
  - Pandas
  - Numpy

# Projects
- When Should You Challenge? Estimating ABS Challenge Value Using Matchup-Level RE288 Projections
  - Abstract: "Our project researches the value of an ABS Challenge. We used machine learning, specifically an XGBoost model, to create a projection of RE288. We     looked at data from the 2023-2025 seasons and compared it to the baseline standard RE288. Our model includes batter and pitcher statistics for their season        long performances to better estimate a player specific run expectancy. Using this information, we created a strategy for how a team would use this in game         planning their approach to ABS. The model creates a RE288 table with projected numbers for a batter and pitcher matchup. It then calculates the value of a         challenge for each of the 288 situations. Finally, using the breakeven rate formula to get the percentage of correct challenges necessary to net even run          value. Using that percentage, a team would have their player know that if they are more than that percent confident the call was wrong, the player should use      the challenge. Our project also discusses ways the team will implement this information without having a player memorize 288 specific situation values for         numerous different matchups. A broad set of rules will be given to the players so the team may have their strategy implemented the way they want without           overwhelming players with information. Following games, audits will be held with players that are incorrectly using or not using challenges to help the player     learn. The overall goal of this project is to improve how teams utilize ABS Challenges."
  - Project was presented to COMP 542 Course at CSUN.
  - Submitted project to Saberseminar conference in Chicago.
  - Co-Author: Jordan Gottlieb
  - Code for projected run expectancy of a matchup in sample code folder.
  - Tables created for hypothetical Pete Alonso vs Mackenzie Gore matchup included in sample reports.
    - Projected RE288 table is "xRuns_Gore...png"
    - Value of challenge in specific sitaution table is "value_of_challenge.png"
    - Confidence interval for matchup is "confidence_interval.png"
 
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
