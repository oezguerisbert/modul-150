import random
import os
from datetime import datetime


class Ticket:
  titel = ""
  problem = ""
  datum = ""
  zustaendigkeit = 0
  ort_raum = ""
  prio = 2
  def __init__(self, t, d, p, z, o, pr):
    self.titel = t
    self.datum = d
    self.problem = p
    self.zustaendigkeit = z
    self.ort_raum = o
    self.prio = pr

  def create(self):
    file = open("tickets.txt", "a+")
    file.write("Datum: %s\nTitel: '%s'\nProblem: '%s'\nZusändigkeit: '%d'\nOrt/Raum: '%s'\nPrio: '%d'\n------------------------------\n"%(self.datum, self.titel, self.problem, self.zustaendigkeit, self.ort_raum, self.prio))
    file.close()
    print("Das Ticket wurde abgespeichert!")

class TicketList:
  ticketlist = ""
  def __init__(self):
    with open("tickets.txt", 'r') as file:
      for line in file:
        self.ticketlist = self.ticketlist + line + "\n"

  def list(self):
    print(self.ticketlist)


def cls():
  os.system('cls' if os.name=='nt' else 'clear')

cls()
action = int(input("Was wollen Sie machen?\n[1] Ticket hinzufügen\n[2] Tickets auflisten\n\n"))

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
    else:
      print("Alles klar, abgebrochen.")
elif action == 2:
  TicketList().list()
