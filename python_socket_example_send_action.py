""" Python Example for controling the game through the socket
as well as reading (s, a, r, s') information"""

import socket
import random
from random import randint
import csv
# actions to make the agent perform over and over
action_sequence = ["up", "up", "stay", "down", "down", "down", "stay", "up", "stay"]

states = ['1empty', '1good', '1bad', '2empty', '2good', '2bad', '3empty',
'3good', '3bad', '4empty', '4good', '4bad', '5empty', '5good',
'5bad', '6empty', '6good', '6bad', '7empty', '7good', '7bad']

actions = ["up","down","stay"]

t = dict()

output_csv = open('ComplexPattern.csv',"wb")

for i in range(0,len(states)):
    s = states[i]
    t[s] = dict()
    for j in range(0,len(actions)):
        a = actions[j]
        t[s][a] = 0.05

# for key in t:
#     for v in t[key]:
#         print(str(key)+"  "+str(v)+"  "+str(t[key][v]))


# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = ('localhost', 24383)
sock.connect(server_address) # connect

i = 0
gamma = 0.5
alpha = 0.1
exploring_rate = 0.8
prev_new_state = ""
while True:
    # for action in action_sequence:
    if i == 0:
        lst = []
        ind = random.randint(0,2)
        first_act = actions[ind]
        sock.sendall(first_act)
        print "send first action: ", first_act
        d = sock.recv(1024).strip()
        old_state, action, reward, new_state = d.split(',')
        reward = float(reward)
        for v in actions:
            lst.append(t[new_state][v])
        print("OLD STATE "+str())
        t[old_state][action] = (1-alpha)*(t[old_state][action]) + alpha*(reward + (gamma*max(lst)))
        prev_new_state = new_state


    else:
        r = random.randint(0,1)
        if r < exploring_rate:
            lst = []
            index = random.randint(0,2)
            a = actions[index]
            # print "send random action: ", action
            sock.sendall(a)
            print "send random action: ", action
            d = sock.recv(1024).strip()
            old_state, action, reward, new_state = d.split(',')
            reward = float(reward)
            for v in actions:
                lst.append(t[new_state][v])
            t[old_state][action] = (1-alpha)*(t[old_state][action]) + alpha*(reward + (gamma*max(lst)))
            prev_new_state = new_state

        elif r > exploring_rate:
            lst = []
            act_lst = []
            for v in actions:
                lst.append(t[prev_new_state][v])
                act_lst.append(v)
            act = act_lst[lst.index(max(lst))]
            sock.sendall(act)
            print "send policy action: ", act
            d = sock.recv(1024).strip() # need the receive in order to send separate messages
            print "received:", d        # (blocking socket)
            old_state, action, reward, new_state = d.split(',')
            reward = float(reward)
            # print(old_state)
            # print(action)
            # print(reward)
            # print(new_state)
            # print(t[old_state][action])
            for v in actions:
                lst.append(t[new_state][v])
            print(lst)
            t[old_state][action] = (1-alpha)*(t[old_state][action]) + alpha*(reward + (gamma*max(lst)))
            prev_new_state = new_state





    i = i + 1
    print("exp ====== "+str(exploring_rate))
    print("IIIIIIIIII   ========   "+str(i))
    if i%3000 == 0:
        exploring_rate = exploring_rate*exploring_rate
    if i >= 10000: # stop repeating after 100 times
        break

# dict_copy = copy(t)
for key in t:
    for v in t[key]:
        print(str(key)+"  "+str(v)+"  "+str(t[key][v]))
output_csv.write('ComplexPattern\n')
output_csv.write('Q values\n')
for i in range(0,len(states)):
    for j in range(0,len(actions)):
        output_csv.write(states[i]+','+actions[j]+','+str(t[states[i]][actions[j]])+'\n')
output_csv.write('Best policy\n')
for i in range(0,len(states)):
    arr = []
    direct = []
    for j in range(0,len(actions)):
        direct.append(actions[j])
        arr.append(t[states[i]][actions[j]])
    maximum = arr.index(max(arr))
    best = direct[maximum]
    output_csv.write(states[i]+','+best+'\n')
