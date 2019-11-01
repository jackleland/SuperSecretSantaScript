#!/usr/bin/python
# -*- coding: utf-8 -*-
import random
import smtplib
import glob
import csv
import os


def check_duplicate_pos(a, b):
    # Checks two lists a and b position-wise for whether any items are the same
    assert len(a) == len(b)
    for j in range(len(a)):
        if a[j] == b[j]:
            return False
    return True


def check_banned_pairs(givers, receivers, banned_pairs):
    # Checks whether any givers have receivers from their banned pair list. Returns false is so, otherwise returns true
    for j in range(len(givers)):
        giver = givers[j][0]
        receiver = receivers[j][0]
        if giver in banned_pairs and receiver in banned_pairs[giver]:
                return False
    return True


def load_file(filename):
    # Reads in a csv file containing all givers and their respective banned receivers. Returns a list of givers
    # (strings) and a dictionary of givers and banned receivers.
    file = open(filename, 'r')
    reader = csv.reader(file)
    output = []
    banned = {}
    for row in reader:
        output.append(row[0:2])
        if len(row) >= 3:
            banned[row[0]] = row[2:]
    file.close()
    return output, banned


def secret_santafy(filename, is_test=False, limit=10):
    participants, banned = load_file(filename)
    receivers = []

    is_good = False
    while not is_good:
        # Randomise list and check for duplicates and banned pairs.
        receivers = random.sample(participants, len(participants))
        is_good1 = check_duplicate_pos(participants, receivers)
        is_good2 = True
        if banned:
            is_good2 = check_banned_pairs(participants, receivers, banned)
        is_good = is_good1 and is_good2

    # Username and password retrieved from environment variables.
    username = os.getenv('ACCOUNT_EMAIL')
    password = os.getenv('ACCOUNT_PSWD')
    print(f'Using username {username} to send emails.')
    if not is_test:
        # Connects to gmail and sends boilerplate email to all participants. Nothing is printed to screen.
        print('This is not a test')
        server = smtplib.SMTP("smtp.gmail.com")
        server.starttls()
        server.login(username, password)
        for i in range(len(participants)):
            msg_from = username
            msg_to = participants[i][1]
            msg_body = "Hi {giver}, \n\n\n" \
                       "You've been allocated {receiver} as your present receiver. YAY! \n\n" \
                       "KEEP IT SECRET!!!\n\n" \
                       "Price limit is \xA3{limit}, we shall convene at a large house with a hot tub for present " \
                       "distribution. \n\n\n" \
                       "LOVE YOU \n\n" \
                       "Santa \n\n" \
                       "p.s. If you have any problems contact Jack".format(limit=limit, giver=participants[i][0],
                                                                           receiver=receivers[i][0])
            msg_subject = 'Secret Santa Allocation!'

            # Prepare actual message
            message = """\From: %s\nTo: %s\nSubject: %s\n\n%s""" % (msg_from, msg_to, msg_subject, msg_body)
            server.sendmail(msg_from, msg_to, message.encode("utf-8"))
            print('successfully sent to ' + msg_to)
        server.close()
    else:
        # If in test mode, print givers and receivers to screen.
        for i in range(len(participants)):
            out_string = participants[i][0] + " -> " + receivers[i][0]
            print(out_string)


def choose_csv(retry=False):
    # finds .csv files in current directory and asks user which one to use. Can retry once upon an invalid response.
    i = 0
    options = []
    for file in glob.glob("*.csv"):
        options.append(file)
        print('{}: {}'.format(i, file))
        i += 1
    print('')
    inp = input('Which file would you like to use? (enter the number): ')
    j = int(inp)
    if j in range(i):
        return options[j]
    elif not retry:
        print('Please pick a number from the list next time. You silly.')
        return choose_csv(retry=True)
    else:
        raise ValueError('Inputted value invalid.')


if __name__ == '__main__':
    csv_filename = choose_csv()
    secret_santafy(csv_filename, is_test=False, limit=10)

