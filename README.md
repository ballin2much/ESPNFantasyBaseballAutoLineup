# ESPN Fantasy Baseball Auto Lineup

## :question: What is this?
My friend plays fantasy baseball on [ESPN](https://www.espn.com/fantasy/baseball/) where there is no button to auto set your lineup. He asked if I could write a script that would auto-set his lineup for him and this is what I came up with. 

## :floppy_disk: Tech Stack
- Main app and classes are written in [Python](https://www.python.org/)
- [Selenium Python](https://selenium-python.readthedocs.io/installation.html) for browser automation
- [Poetry](https://python-poetry.org/) is used for virtual environment and package/dependency management
- [Docker Compose](https://docs.docker.com/) to make it easier to setup
- [Git](https://git-scm.com/) and [Github](https://github.com/) for version control and change management

## :gear: Setup
- Download [Docker](https://docs.docker.com/get-docker/)
- [Download the repository](https://github.com/ballin2much/ESPNFantasyBaseballAutoLineup/archive/refs/heads/main.zip)
- You need to get a copy of your ESPN cookies and save them in the root folder. To do so I downloaded the [EditThisCookie](https://www.editthiscookie.com/) chrome extension, logged into the ESPN site, and [exported my cookies](https://www.editthiscookie.com/blog/2014/03/import-export-cookies/) as a JSON. Once downloaded, place the JSON file into the root folder of the repository saved as ***cookies.json***.
- Go to the homepage of your fantasy baseball and copy the url. It should be similar to the link below:
    >https://fantasy.espn.com/baseball/team?leagueId=123456789&teamId=1&seasonId=2023
- Create a file titled ***.env*** in the root of the folder. Here you'll need to set an environmental variable named ***fantasy_url*** such as below.
```
fantasy_url = "https://fantasy.espn.com/baseball/team?leagueId=168120278&teamId=9&seasonId=2023&scoringPeriodId=7&statSplit=singleScoringPeriod"
```
- Navigate to the root folder of the container and type the below command
``` console
ballin2much@PC:~/ESPNFantasyBaseballAutoLineup $ docker compose up
```
- Your team should be set for the current day! I would recommend scheduling the above command to run daily (such as by using cron on Linux).