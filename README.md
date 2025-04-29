# Archery Score Normaliser

I started this project to create a more open scoring system for the University of Liverpool x Liverpool John Moores University Varsity archery competition. 2023 was the first year that this competition was ever held, thanks to the formation of LJMU's archery club. That year, it was attempted to normalise scores instead of handicaps. This produced some interesting results and required some dubious maths in Excel. Fortunately, UoL won by such a significant margin the maths wasn't really needed. However, to ensure that the system is fair for the future I decided to create a new system. In 2024, this means we can welcome all four of the bowstyles recognised by ArcheryGB. This is an advantage compared to other varsity archery competitions where bowstyles and entrants have to be limited.

Handicaps correspond to a specific score for each round, regardless of the bowstyle or gender. For example, a 567 Portsmouth always corresponds to a handicap of 37. What changes is the handicaps required by each bowstyle and gender to achieve each classification (A3 to EMB or IA3 to IGMB). To achieve MB, a recurve man needs to shoot the score corresponding to a handicap of 37, while a longbow woman only needs to shoot a score corresponding to a handicap of 72. By plotting the handicaps needed to achieve each classification, it can be observed that there is a consistent offset between bowstyle. Using this information, the handicaps shot by archers of varying bowstyles and genders can be normalised to a recurve man. These adjustments allow the direct comparison of skill, rather than raw score.

Features:

- Updated with new indoor classification tables
- Manual or bulk normalisation of scores, using either a .csv file or IANSEO output file
- Automatic conversions between big 10 and small 10 scoring to account for compound indoor rounds

WIP:

- Normalisaiton of handicaps between different rounds in the same result set (i.e. between a 90m 1440 and a 70m 1440)
- Automatic conversion between triple face and single face variants of the same round. The handicaps only differ once you start having misses on the triple spot, ideally archers woudn't be shooting the triple face in these scenarios anyway. Low priority as this is an edge case.
- Better documentation (read: any documentation)

# Installation 

Navigate to "Releases" on the sidebar to the right. Download the .exe from the latest release and run!
