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
  q_file = open("gameshow_question", "w")
  a_file = open("gameshow_answer", "w")
  print("question_sheet_current:", question_sheet['current'])
  q_number = question_sheet['current'] + 1
  print("question_sheet_current again:", question_sheet['current'])
  current_question = question_sheet["list"][question_sheet['current']]
  question_text = f"{q_number}. {current_question['q']}\n\n"
  answer_text = f"Answer: {current_question['a']}"
  q_file.write(question_text)
  a_file.write(answer_text)
  q_file.close()
  a_file.close()


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
      if (cmds[0] == "next" or cmds[0] == "n"):
        if question_sheet["current"] < len(question_sheet["list"]) - 1:
          question_sheet["current"] += 1
          write_current_question(question_sheet)
        else:
          print("End of questions!")
      elif (cmds[0] == "back" or cmds[0] == "b"):
        if question_sheet["current"] > 0:
          question_sheet["current"] -= 1
          write_current_question(question_sheet)
        else:
          print("At start of questions!")
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