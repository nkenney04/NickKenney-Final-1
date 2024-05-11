from PyQt6.QtWidgets import *
from gui import *
import csv

class Logic(QMainWindow,Ui_VotingBox):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.submit_button.clicked.connect(lambda : self.submit())
        self.restart_button.clicked.connect(lambda : self.restart_poll())

    def restart_poll(self):
        '''
        This function clears all input boxes and removes all info from vote_log.csv
        '''
        open('vote_log.csv', 'w').close()
        self.id_box.clear()
        self.id_message.setText('')
        self.submit_message.setText('')

    def count_votes(self):
        '''
        1. The first portion of this function creates variables for each of the candidates
        and sets them to 0. These will then be used to determine the number of votes for each.
        2.The second portion opens the file for reading and creates the 'reader' variable.
        3.Finally, the reader iterates through the file, counting each time
        the voted name shows up.
        :return:  joe_votes, james_votes, sal_votes, brian_votes, total_votes
        '''
    #1
        global total_votes
        global joe_votes
        global james_votes
        global sal_votes
        global brian_votes
        joe_votes = 0
        james_votes = 0
        sal_votes = 0
        brian_votes = 0
    #2
        total_votes = len(open('vote_log.csv', 'r').readlines())
        test_file = open('vote_log.csv', 'r')
        reader = csv.reader(test_file)
    #3
        for line in reader:
            if line[1] == 'joe':
                joe_votes += 1
            elif line[1] == 'james':
                james_votes += 1
            elif line[1] == 'sal':
                sal_votes += 1
            elif line[1] == 'brian':
                brian_votes += 1
        return joe_votes, james_votes, sal_votes, brian_votes, total_votes

    def check_for_dupe(self):
        '''
        This function gets the id_input from the gui and converts it to a string. The Reader
        then goes line by line to see if that ID has already been used. If so,
        variable 'dupe' is set to true.
        :return: Dupe
        '''
        global dupe
        id_input = self.id_box.text()
        str_input = str(id_input)
        test_file = open('vote_log.csv', 'r')
        csv_reader = csv.reader(test_file)
        dupe = False
        for line in csv_reader:
            if line[0] == str_input:
                dupe = True
    def submit(self):
        '''
        1. This first part of this function calls check_for_dupe to receive a boolean value
        to determine if the ID number has been previously used.
        2. This second part of the function looks to see what radio button was selected, and
        temporarily assigns a name to Vote_Choice.
        3. The third part of this function uses a try and except block to raise errors for
        duplicate IDs, non-digit entries, and entries that are not 7 characters.
        If it meets criteria, the Voter ID, and Vote_Choice are sent to the vote_log.csv
        4. The final portion uses the variables from count_votes() and outputs the number of votes
        for each person to the gui.

        '''
    #1
        self.check_for_dupe()
        id_input = self.id_box.text()
        test_file = open('vote_log.csv', 'a')
        csv_writer = csv.writer(test_file)
        self.success_msg.setText('')
        self.id_message.setText('')
    #2
        try:
            if self.radio_joe.isChecked():
                Vote_choice = 'joe'
            elif self.radio_james.isChecked():
                Vote_choice = 'james'
            elif self.radio_sal.isChecked():
                Vote_choice = 'sal'
            elif self.radio_brian.isChecked():
                Vote_choice = 'brian'
            else:
                raise ValueError('No Vote Choice selected')
    #3
            if not id_input.isdigit():
                raise ValueError('ID Must be all digits')
            elif len(id_input) != 7:
                raise ValueError('ID Must be 7 Characters')
            elif dupe == True:
                raise ValueError('This ID has already Voted!')
            else:
                self.success_msg.setText(f'Vote submitted for {Vote_choice}!')
                csv_writer.writerow([id_input, Vote_choice])
                test_file.close()
                self.count_votes()
            #4
                self.submit_message.setText(f'Total Votes:{total_votes}\nJoe:{joe_votes}\nJames:{james_votes}\nSal:{sal_votes}\nBrian:{brian_votes}')
                self.id_box.clear()
        except ValueError as e:
            self.id_message.setText(f'Invalid:{e}')
        except:
            self.id_message.setText('Unknown error')