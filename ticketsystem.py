import random
import os
from datetime import datetime
import re
import unicodedata
from os import listdir
from os.path import isfile, join

statuse = {"1": "Fertig", "2": "Offen", "3": "In Bearbeitung"}

class Ticket:
  titel = ""
  problem = ""
  datum = ""
  zustaendigkeit = 0
  ort_raum = ""
  prio = 2
  status = statuse.get("2")
  filename = ""
  def __init__(self, t, d, p, z, o, pr):
    self.titel = t
    self.datum = d
    self.problem = p
    self.zustaendigkeit = z
    self.ort_raum = o
    self.prio = pr
    self.filename = self.slugify(self.titel + " " + str(self.datum), allow_unicode=True) + ".txt"
  def show(self):
    print("Datum: %s\nTitel: '%s'\nProblem: '%s'\nZusändigkeit: '%d'\nOrt/Raum: '%s'\nPrio: '%d'\nStatus: '%s'"%(self.datum, self.titel, self.problem, self.zustaendigkeit, self.ort_raum, self.prio, self.status))

  def update(self, column, value):
    setattr(self, column, value)

  def create(self):
    file = open("tickets/" + self.filename, "w")
    file.write("Datum: %s\nTitel: '%s'\nProblem: '%s'\nZusändigkeit: '%d'\nOrt/Raum: '%s'\nPrio: '%d'\nStatus: '%s'"%(self.datum, self.titel, self.problem, self.zustaendigkeit, self.ort_raum, self.prio, self.status))
    file.close()
    print("Das Ticket wurde abgespeichert!")

  def save(self):
    self.create()

  def slugify(self, value, allow_unicode=False):
    value = unicodedata.normalize('NFKC', str(value))
    value = re.sub(r'[^\w\s-]', '', value.lower())
    return re.sub(r'[-\s]+', '-', value).strip('-_')

class TicketList:
  ticketlist = []
  def __init__(self):
    mypath = "./tickets/"
    self.ticketlist = [f for f in listdir(mypath) if isfile(join(mypath, f))]

  def getlist(self):
    return self.ticketlist
  
  def get(self, filename):
    with open("tickets/" + filename, "r") as file:
      lines = file.readlines()
      t = ""
      p = ""
      d = ""
      z = 0
      o = ""
      pr = 2
      for index, line in enumerate(lines, start=0):
        if index == 0:
          d = re.match(r'Datum: (.*)', line).groups()[0]
        if index == 1:
          t = re.match(r'Titel: \'(.*)\'', line).groups()[0]
        if index == 2:
          p = re.match(r'Problem: \'(.*)\'', line).groups()[0]
        if index == 3:
          z = int(re.match(r'Zusändigkeit: \'(.*)\'',line).groups()[0])
        if index == 4:
          o = re.match(r'Ort\/Raum: \'(.*)\'', line).groups()[0]
        if index == 5:
          pr = int(re.match(r'Prio: \'(.*)\'', line).groups()[0])
      return Ticket(t,d,p,z,o,pr)

def cls():
  os.system('cls' if os.name=='nt' else 'clear')

def main():
  cont = True
  action = -1
  while(cont):
    cls()
    if action == -1:
      action = int(input("Was wollen Sie machen?\n[1] Ticket hinzufügen\n[2] Tickets auflisten\n\n[0] Programm beenden.\n\nIhre Auswahl: "))

    if action == 1:

      datum = datetime.now(tz=None)
      zahl1 = random.randint(1, 10)
      zahl2 = random.randint(1, 10)
      cls()
      titel = input("Titel:\n")
      cls()
      problem = input("Beschreibung:\n")
      cls()
      zustaendigkeit = int(input("Zuständigkeit:\n[1] Software\n[2] Hardware\n[3] Telefon\n[4] Strom\n[5] Netzwerk\n\n"))
      cls()
      ort_raum = input("Welcher Raum?\n")
      cls()
      security_answer = int(input("Sicherheitsfrage: Was ist " + str(zahl1) + " * " + str(zahl2) + "?\n"))
      if(security_answer == zahl1 * zahl2):
        prio = int(input("Priorität:\n[1] 24 Stunden\n[2] 48 Stunden\n"))
        cls()
        bestaetigen = input("Ist diese Information korrekt?\n\nTitel: '%s'\nProblem: '%s'\nZusändigkeit: '%d'\nOrt/Raum: '%s'\nPrio: '%d'\n---------------------------\nKorrekt (y/n)\n"%(titel, problem, zustaendigkeit, ort_raum, prio))
        if bestaetigen == "y":
          Ticket(titel, datum, problem, zustaendigkeit, ort_raum, prio).create()
          action = -1
        else:
          print("Alles klar, abgebrochen.")
    elif action == 2:
      cls()
      print("Die Tickets:")
      tl = TicketList()
      tickets = tl.getlist()
      if len(tickets) > 0:
        for index, ticketname in enumerate(tickets, start=1):
          print("[%d] %s"%(index, ticketname))
        print("\n[0] Zurück zum Menu\n\n")
        usethisticket = int(input("Welches Ticket wollen sie?\n\nIhre Auswahl: "))
        if usethisticket == 0:
          action = -1
          continue
        ticket = tl.get(tickets[usethisticket - 1])
        cls()
        ticket.show()
        print()
        todo = int(input("Was wollen Sie mit dem Ticket machen?\n[1] Status ändern\n[2] Löschen\n\n[0] Zurück zur Ticketliste\n\nIhre Auswahl: "))
        cls()
        if todo == 2:
          if input("Wollen sie das Ticket wirklich löschen? (y/n) ") == "y":
            os.remove("./tickets/%s"%(ticket.filename))
            print("Das Ticket wurde entfernt")
            input("Drücken Sie >Enter< um zurück ins Menü zu gelangen.")
          else:
            print("abgebrochen")
        elif todo == 1:
          status = input("Welches Status hat das Ticket? Zurzeit: '%s'\n[1] Fertig\n[2] Offen\n[3] In Bearbeitung\n[0] Abbruch\n\nIhre Auswahl: "%(ticket.status))
          if status == 0:
            print("Abgebrochen")
            action = -1
            continue
          ticket.update("status", status)
          print("Ticket wurde aktualisiert.")
          save = input("Wollen sie das Ticket speichern? (y/n) ")
          if save == "y":
            ticket.save()
        elif todo == 0:
          action = 2
          continue
      else:
        print("Sie haben keine Tickets")
        input("Drücken Sie >Enter< um zurück ins Menü zu gelangen.")
        action = -1
    elif action == 0:
      cont = False


if __name__ == "__main__":
  main()
