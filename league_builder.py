import csv
import os
import re

class LeagueBuilder:

   FIELDNAMES = ("name", "height", "soccerexp", "guardians")
   TEAMS  = ("Dragons", "Sharks", "Raptors")
   OUTFILENAME = "teams.txt"

   def __init__(self, filename):
       self.filename = filename
       self.teamdict = {}
       self.teamlenth = len(self.TEAMS)
       for team in self.TEAMS:
           self.teamdict[team] = []

   #persit the players to the team file
   def persist(self):
      fh = open(self.OUTFILENAME, "w")
      for team in self.teamdict:
          fh.write(" "*8+team+os.linesep)
          playerids = self.teamdict[team]
          for pid in playerids:
             player = self.playermap[pid]
             name = player["name"]
             exper = player["soccerexp"]
             guardians = player["guardians"]
             player_line = "{0},{1},{2}".format(name, exper, guardians)
             player_line+=os.linesep
             fh.write(player_line)
          fh.write(os.linesep)

   #generate the letters
   def genLetters(self):
    for playerid in self.playermap:
       player = self.playermap[playerid]
       playername = re.sub(r"\s+", '_', player['name']) #using regex replace any number of spaces with a "_"

       with open("letters/{}.txt".format(playername), "w") as player_file:
           letterbody = """Dear {0},
           Please be advised that {1} will be on the {2} team for this season soccer league.
           
           Practice will be starting on Jan, 11.
                             
           Best regards,
                              
           Coach Guido van Rossum
          
           """.format(player['guardians'], player['name'], player['team'])
           player_file.write(str(letterbody))
           player_file.close()

   #assign player to teamdict
   def assignteam(self, playerid, team):
       self.teamdict[team].append(playerid)
       player = self.playermap[playerid]
       player['team'] = team

   def distributeplayers(self):
       playeridswithexp = []
       playeridswithoutexp = []
       #seperate the players into experienced list and no experience
       for playerid in self.playermap:
           player = self.playermap[playerid]
           if player['soccerexp'] == "YES":
               playeridswithexp.append(player["id"])
           else:
               playeridswithoutexp.append(player["id"])

       #using modulus distribute the players onto the 3 teams
       for i,playerid in enumerate(playeridswithexp):
           team = self.TEAMS[i % self.teamlenth]
           self.assignteam(playerid,team)

       # again using modulus distribute the remaining players onto the 3 teams
       for i,playerid in enumerate(playeridswithoutexp):
           team = self.TEAMS[i % self.teamlenth]
           #assign the player using the playerid to a team in self.teamdict
           self.assignteam(playerid, team)

   #load the players into a dictionary of dictionaries
   def loadplayers(self):
      self.playermap = {}
      with open(self.filename) as csvfile:
        playerreader = csv.DictReader(csvfile, self.FIELDNAMES)
        playerlist = list(playerreader)
        # enumerate of the playerlist using i to assing a playerid
        # this playerid is used to reference the player dict that contains all the player info
        for i,player in enumerate(playerlist[1:]):
             playerid  =  i+1
             player["id"] = playerid
             self.playermap[playerid] = player

if __name__ == "__main__":
   filename = "soccer_players.csv"
   lb = LeagueBuilder(filename)
   lb.loadplayers()
   lb.distributeplayers()
   lb.persist()
   lb.genLetters()