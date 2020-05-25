import random
import csv

class Qlearning:
  def __init__(self, actions, alpha=0.2, gamma=0.9, epsilon=0.2):
    self.q_table = {}
    self.actions = actions    # Number of actions possible.
    self.alpha = alpha        # Learning rate. Higher value means new value is less important.
    self.gamma = gamma        # Discount factor. Higher value means focus on future reward.
    self.epsilon = epsilon    # Exploration factor. Higher means more exploration.

  # Return reward of (state, action) pair, 0 by default
  def getValue(self, state, action):
    return self.q_table.get( (state, action) , 0.0);

  # Update reward of (state, action) pair
  def update_table(self, state, action, reward, next_state):
    maxq = max([self.getValue(next_state, a) for a in range(self.actions)])
    self.q_table[(state, action)] = self.getValue(state, action) + self.alpha * (reward + self.gamma * maxq - self.getValue(state, action))

  # Choose best action to take or explore new action
  def take_action(self, state, possible_actions):
    if random.uniform(0, 1) < self.epsilon:
      #Explore: select a random action
      action_index = random.choice(possible_actions)
    else:
      #Exploit: select best action
      action_values = [self.getValue(state, a) for a in possible_actions]
      possible_index = action_values.index(max(action_values))
      action_index = possible_actions[possible_index]

    return action_index

  def saveTo(self, filename, settings):
    File = open(filename, "w")
    for row in settings:
      File.write("N=" + str(row[0]) + " | alpha=" + str(row[1]) + " | gamma=" + str(row[2]) + " | epsilon=" + str(row[3]) + " |\n")
    File.write("\nQ-Table\n")
    table = {}
    for key in self.q_table:
      if key[0] in table:
        table[key[0]][key[1]] = float("%.2f" % self.q_table.get(key, 0.0))
      else:
        table[key[0]] = [0.0 for a in range(self.actions)]
        table[key[0]][key[1]] = float("%.2f" % self.q_table.get(key, 0.0))

    for key in table:
      File.write(str(key))
      cursor = len(str(key))
      while cursor < 15:
        File.write(" ")
        cursor += 1
      File.write("=>")
      cursor += 2
      while cursor < 22:
        File.write(" ")
        cursor += 1

      array = table.get(key)

      for value in array:
        File.write("|")
        if len(str(value)) < 6:
          File.write(" " * (6-len(str(value))))
        File.write(str(value))
        File.write(" ")
      File.write("|")
      File.write("\n")

    File.close()

  def csvTo(self, filename, settings):
    with open(filename, "w", newline="") as File:
      writer = csv.writer(File, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
      writer.writerow(["N", "alpha", "gamma", "epsilon"])
      for row in settings:
        writer.writerow([row[0], row[1], row[2], row[3]])
      writer.writerow([])

      header = ["S"]
      for i in range(self.actions):
        header.append(i)
      writer.writerow(header)

      table = {}
      for key in self.q_table:
        if key[0] in table:
          table[key[0]][key[1]] = float("%.2f" % self.q_table.get(key, 0.0))
        else:
          table[key[0]] = [0.0 for a in range(self.actions)]
          table[key[0]][key[1]] = float("%.2f" % self.q_table.get(key, 0.0))
      for key in table:
        writer.writerow([key] + table[key])
