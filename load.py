from app import load


def print_cons(text):
    print('     ' + text)
    print('         ' + str(machine.consult([text])))


machine = load('machine0.5')

print_cons('Im not happy')
# print_cons('If you want god to laugh, tell him your plans')
# print_cons('Nothing good happens after 2:00am')
# print_cons('He got the job he deserve')
#
# print('happiness, love')
# print_cons('Finally friday, I cant wait to enjoy the weekend.')
# print_cons('I love you')
#
# print_cons('I am thankful about us being friends')
# print_cons('Happiness is waking up 5 minutes later')
#
# print('sadness, worry')
# print_cons('That in the wall is a spider. They are like my greatest fear, so... Who will kill it?')
# print_cons('He dump me. I dont know what to do right now. I\'m felling awful')
# print_cons('Nobody likes me, it is really bad to live always alone')
# print_cons('I miss you')
# print_cons('bad week. i am afraid the next will be the same')
#
# print('surprise')
# print_cons('Thats new, I dint expect it. But it is a good surprise')
# print_cons('You are the best thing ever happened to me')
# print_cons('I dint expect that present, it was the best msi laptop ever')
#
# print('hate')
# print_cons('I hate eating that. Dont make me')
# print_cons(
#     'Treat me bad so a can hate you in peace. If a dint made myself clear. I wish you to die, but far away from me')
# print_cons('You should go away and ruin others people lifes. Leave my day free of you.')
# print_cons('That book is really bad. It was like throwing your money. A refund please...')
