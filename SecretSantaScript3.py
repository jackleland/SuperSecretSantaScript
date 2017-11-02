#!/usr/bin/python
# -*- coding: utf-8 -*-
import random
import smtplib
import glob
import csv
import os


def check_duplicate_pos(a, b):
    for j in range(len(a)):
        if a[j] == b[j]:
            return False
            
    return True


def check_banned_pairs(list1, list2, banned_pairs):
    for j in range(len(list1)):
        for k in range(len(banned_pairs)):
            if ((list1[j][0] == banned_pairs[k][0]) and (list2[j][0] == banned_pairs[k][1])) \
                    or ((list1[j][0] == banned_pairs[k][1]) and (list2[j][0] == banned_pairs[k][0])):
                return False
    return True


def load_file(filename):
    file = open(filename, 'r')
    reader = csv.reader(file)
    output = []
    for row in reader:
        output.append(row)
    file.close()
    return output


def secret_santafy(filename):
    participants = load_file(filename)
    print(participants[:][3])

    isGood = False
    while not isGood:
        receivers = random.sample(participants, len(participants))
        isGood1 = check_duplicate_pos(participants, receivers)
        isGood2 = check_banned_pairs(participants, receivers, participants[:][3])
        isGood = isGood1 and isGood2

    username = os.getenv('ACCOUNT_EMAIL')
    password = os.getenv('ACCOUNT_PSWD')
    # server = smtplib.SMTP("smtp.gmail.com", 587)
    # server.starttls()
    # server.login(username, password)

    for i in range(len(participants)):
        out_string = participants[i][0] + " -> " + receivers[i][0]
        print(out_string)

        msg_from = username
        msg_to = participants[i][1]
        msg_body = "Hi {giver}, \n\n\n" \
                   "You've been allocated {receiver} as your present receiver. YAY! \n\n" \
                   "Limit is &#163;10, we shall convene at some point for present distribution. \n\n\n" \
                   "LOVE YOU \n\n" \
                   "Santa".format(giver=participants[i][0], receiver=receivers[i][0])
        msg_subject = 'Secret Santa Allocation!'
        # Prepare actual message
        message = """\From: %s\nTo: %s\nSubject: %s\n\n%s""" % (msg_from, msg_to, msg_subject, msg_body)

        # server.sendmail(msg_from, msg_to, message)

        # print('successfully sent to ' + msg_to)

    # server.close()


def list_csv_options():
    i = 0
    options = []
    for file in glob.glob("*.csv"):
        options.append(file)
        print('{}: {}'.format(i, file))
        i += 1
    print('')
    print('Which file would you like to use? (enter the number): ')



if __name__ == '__main__':
    list_csv_options()
    secret_santafy('cdtpeeps.csv')
