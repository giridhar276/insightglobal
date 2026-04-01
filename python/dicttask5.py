

teams = {
    "TeamA": [
        {"name": "Alice", "role": "Batsman"},
        {"name": "Bob", "role": "Bowler"}
    ],
    "TeamB": [
        {"name": "Charlie", "role": "Allrounder"},
        {"name": "Dave", "role": "Wicketkeeper"}
    ]
}


for teamname, teamlist in teams.items():
    print(teamname)
    print("-------------")
    for player in teamlist:
        print(player['name'])
    print()
