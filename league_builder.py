import csv
import os

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

   def persist(self):
      fh = open(self.OUTFILENAME, "w")
      for team in self.teamdict:
          fh.write(team+os.linesep)
          playerids = self.teamdict[team]
          for pid in playerids:
             player = self.playermap[pid]
             name = player["name"]
             exper = player["soccerexp"]
             guardians = player["guardians"]
             player_line = "{0},{1},{2}".format(name, exper, guardians)
             player_line+=os.linesep
             fh.write(player_line)

   def assignteam(self,playerid,team):
       self.teamdict[team].append(playerid)

   def distributeplayers(self):
       playeridswithexp = []
       playeridswithoutexp = []
       for playerid in self.playermap:
           player = self.playermap[playerid]
           if player['soccerexp'] == "YES":
               playeridswithexp.append(player["id"])
           else:
               playeridswithoutexp.append(player["id"])
       for i,playerid in enumerate(playeridswithexp):
           team = self.TEAMS[i % self.teamlenth]
           self.assignteam(playerid,team)
       for i,playerid in enumerate(playeridswithoutexp):
           team = self.TEAMS[i % self.teamlenth]
           self.assignteam(playerid,team)

   def loadplayers(self):
      self.playermap = {}
      with open(self.filename) as csvfile:
        playerreader = csv.DictReader(csvfile, self.FIELDNAMES)
        playerlist = list(playerreader)
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