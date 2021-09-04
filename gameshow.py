import json
import random


def create_question_sheet(questions):
  questions_copy = questions.copy()
  random.shuffle(questions_copy)
  return {
    "current": 0,
    "list": questions_copy
  }


def write_current_question(question_sheet):
  f = open("gameshow_question", "w")
  current_question = question_sheet["list"][question_sheet['current']]
  text = ""
  text += f"{current_question['q']}\n\n"
  text += f"Answer: {current_question['a']}"
  f.write(text)
  f.close()


def create_scoreboard(players):
  scoreboard = dict()
  for p in players:
    scoreboard[p["name"].lower()] = {
      "name": p["name"],
      "score": 0
    }
  return scoreboard


def set_player_score(scoreboard, player_name, score):
  scoreboard[player_name]["score"] = score

def write_current_score(scoreboard):
  f = open("gameshow_score", "w")
  text = ""
  for player in scoreboard.values():
    name = player["name"]
    score = player["score"]
    text += f"{name}: {score}\n"
  f.write(text)
  f.close()


def main():
  f = open("gameshow.config.json")
  config = json.load(f)
  f.close()

  scoreboard = create_scoreboard(config["players"])
  write_current_score(scoreboard)
  question_sheet = create_question_sheet(config["questions"])
  write_current_question(question_sheet)

  
  cmd = ""
  while cmd != "exit":
    cmds = cmd.split(" ")
    try:
      if (cmds[0] == "next"):
        if question_sheet["current"] < len(question_sheet["list"]) - 1:
          question_sheet["current"] += 1
        else:
          print("End of questions!")
        write_current_question(question_sheet)
      elif (cmds[0] == "back"):
        if question_sheet["current"] > 0:
          question_sheet["current"] -= 1
        else:
          print("At start of questions!")
        write_current_question(question_sheet)
      elif (cmds[0] == "add"):
        set_player_score(scoreboard, cmds[1], scoreboard[cmds[1]]["score"] + int(cmds[2]))
        write_current_score(scoreboard)
      elif (cmds[0] == "inc"):
        set_player_score(scoreboard, cmds[1], scoreboard[cmds[1]]["score"] + 1)
        write_current_score(scoreboard)
      elif (cmds[0] == "set"):
        set_player_score(scoreboard, cmds[1], int(cmds[2]))
        write_current_score(scoreboard)
      else:
        print("next - Go to next question")
        print("add <name> <amount> - Add amount to players score")
        print("inc <name> - Increment players score by one")
        print("set <name> <amount> - Set players score to amount")
    except KeyError:
      print("Invalid input (KeyError)")
      pass
    except ValueError:
      print("Numerical input expected (ValueError)")
      pass
    cmd = input(">")

if __name__ == "__main__":
  main()