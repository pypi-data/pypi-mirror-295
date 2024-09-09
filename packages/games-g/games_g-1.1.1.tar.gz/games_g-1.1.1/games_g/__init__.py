import random
import pyttsx3
import pyaudio

#set text to speech engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

##############################Guess The Number Console Game#########################################################
def GuessTheNumber() :
        print("Welcome in Number Guessing Game \n")
        speak("Welcome in Number Guessing Game")
        print("Application Type : Console Game")
        speak("Application Type : Console Game")
        print("Version : 2.0.1 LTS")
        speak("Version : 2.0.1 LTS")
        print("Developer : GHANSHYAM VAJA","\n")
        speak("Developer : GHANSHYAM vaja")
        rand = 0
        randomNumber = 0
        userNumber = 0
        chooseLevel = 0
        easyCount = 5
        mediumCount = 7
        hardCount = 10
        ultrahardCount = 15
        leftCount = 0

        print("    Level         Range       Turns")
        print("1 - Easy       (1 to 100)       5\n2 - Medium     (1 to 1000)      7\n3 - Hard       (1 to 10000)     10\n4 - Ultra Hard (1 to 100000)    15")
        speak("1 for Easy       Range = 1 to 100       turns = 5\n")
        speak("2 for Medium     Range = 1 to 1000      turns=7\n")
        speak("3 for Hard       Range=1 to 10000     turns=10\n")
        speak("4 for Ultra Hard Range=1 to 100000    turns=15")
        print(" \nChoose Level(1 | 2 | 3 | 4 ) : ", end ="")
        speak("Choose Level between 1 to 4")
        try:
            chooseLevel = int(input())
        except:
            print("Enter Level between 1 to 4")
        while (chooseLevel <= 0 or chooseLevel > 4) :
            print("Choose Level(1 | 2 | 3 | 4) : ", end ="")
            speak("Choose Level")
            try:
                chooseLevel = int(input())
            except:
                print("Enter Level between 1 to 4")
        if (chooseLevel == 1) :
            randomNumber = random.randint(0, 101)
        elif(chooseLevel == 2) :
            randomNumber = random.randint(0, 1001)
        elif(chooseLevel == 3) :
            randomNumber = random.randint(0, 10001)
        else :
            randomNumber = random.randint(0,100001)
        while True :
            if (easyCount == 0 or mediumCount == 0 or hardCount == 0 or ultrahardCount == 0) :
                print("\n---------------------------------------------")
                print("GAME OVER", end ="")
                speak("GAME OVER")
                break
            print(" \nGuess A Number Between 1 To ", end ="")
            speak(" \nGuess A Number Between 1 To")
            if (chooseLevel == 1) :
                easyCount -= 1
                leftCount = easyCount
                print("100", end ="")
                speak("100")
            elif(chooseLevel == 2) :
                mediumCount -= 1
                leftCount = mediumCount
                print("1000", end ="")
                speak("1000")
            elif(chooseLevel == 3) :
                hardCount -= 1
                leftCount = hardCount
                print("10000", end ="")
                speak("10000")
            else :
                ultrahardCount -= 1
                leftCount = ultrahardCount
                print("100000", end ="")
                speak("100000")
            print(" : ", end ="")
            try:
                userNumber = int(input())
            except:
                print("Enter valid Value : ")
            if (userNumber == randomNumber) :
                print("\n---------------------------------------------")
                print(" \nCongratulations, Your Guess Is Correct, YOU WON.....")
                speak("Congratulations, Your Guess Is Correct, YOU WON.....")
            elif(userNumber > randomNumber) :
                print("Your Guess Is Large     Available Turn : " + str(leftCount))
                speak("Your Guess Is Large")
                speak("Available Turn : " + str(leftCount))
            elif(userNumber > 0) :
                print("Your Guess Is Small     Available Turn : " + str(leftCount))
                speak("Your Guess Is Small")
                speak("Available Turn : " + str(leftCount))
            if((userNumber > 0) == False) :
                    break
        print(" \n---------------------------------------------")
        print("Your Answer Is : ")
        print(randomNumber)
        speak("Your Answer Is ")
        speak(randomNumber)
        print("---------------------------------------------")
###################################################################################################################

####################################Snake and Ladder Console Game##################################################
class Play_With_Computer :
    WONPOINT = 100
    rand =  random.randint(1, 7)
    rollDice = ' '
    playerPosition = 0
    computerPosition = 0
    playerDice = 0
    computerDice = 0
    Name = None
    Snake_Mouth_Position = [0] * (8)
    Snake_Tail_Position = [0] * (8)
    Ladder_Up_Position = [0] * (8)
    Ladder_Down_Position = [0] * (8)
    flag = 0
    Level = ' '
    ctr = 0
    def PlayerAndComputerPosition(self) :
                if (Play_With_Computer.playerPosition > Play_With_Computer.WONPOINT) :
                    Play_With_Computer.playerPosition -= Play_With_Computer.playerDice
                if (Play_With_Computer.computerPosition > Play_With_Computer.WONPOINT) :
                    Play_With_Computer.computerPosition -= Play_With_Computer.computerDice
                # playerPosition With Snake_Tail_Position
                i = 0
                while (i < 8) :
                    if (self.Level == '1' and i < 3) :
                        if (Play_With_Computer.playerPosition == Play_With_Computer.Snake_Mouth_Position[i]) :
                            Play_With_Computer.playerPosition = Play_With_Computer.Snake_Tail_Position[i]
                        elif(Play_With_Computer.computerPosition == Play_With_Computer.Snake_Mouth_Position[i]) :
                            Play_With_Computer.computerPosition = Play_With_Computer.Snake_Tail_Position[i]
                    elif(self.Level == '2' and i < 5) :
                        if (Play_With_Computer.playerPosition == Play_With_Computer.Snake_Mouth_Position[i]) :
                            Play_With_Computer.playerPosition = Play_With_Computer.Snake_Tail_Position[i]
                        elif(Play_With_Computer.computerPosition == Play_With_Computer.Snake_Mouth_Position[i]) :
                            Play_With_Computer.computerPosition = Play_With_Computer.Snake_Tail_Position[i]
                    else :
                        if (Play_With_Computer.playerPosition == Play_With_Computer.Snake_Mouth_Position[i]) :
                            Play_With_Computer.playerPosition = Play_With_Computer.Snake_Tail_Position[i]
                        elif(Play_With_Computer.computerPosition == Play_With_Computer.Snake_Mouth_Position[i]) :
                            Play_With_Computer.computerPosition = Play_With_Computer.Snake_Tail_Position[i]
                    i += 1
                # playerPosition With Ladder
                i = 0
                while (i < 8) :
                    if (self.Level == '1' and i < 3) :
                        if (Play_With_Computer.playerPosition == Play_With_Computer.Ladder_Down_Position[i]) :
                            Play_With_Computer.playerPosition = Play_With_Computer.Ladder_Up_Position[i]
                        elif(Play_With_Computer.computerPosition == Play_With_Computer.Ladder_Down_Position[i]) :
                            Play_With_Computer.computerPosition = Play_With_Computer.Ladder_Up_Position[i]
                    elif(self.Level == '2' and i < 5) :
                        if (Play_With_Computer.playerPosition == Play_With_Computer.Ladder_Down_Position[i]) :
                            Play_With_Computer.playerPosition = Play_With_Computer.Ladder_Up_Position[i]
                        elif(Play_With_Computer.computerPosition == Play_With_Computer.Ladder_Down_Position[i]) :
                            Play_With_Computer.computerPosition = Play_With_Computer.Ladder_Up_Position[i]
                    else :
                        if (Play_With_Computer.playerPosition == Play_With_Computer.Ladder_Down_Position[i]) :
                            Play_With_Computer.playerPosition = Play_With_Computer.Ladder_Up_Position[i]
                        elif(Play_With_Computer.computerPosition == Play_With_Computer.Ladder_Down_Position[i]) :
                            Play_With_Computer.computerPosition = Play_With_Computer.Ladder_Up_Position[i]
                    i += 1
                # player position display
                print("\n--------------------->Player\'s Position<---------------------------")
                speak("Player\'s Position")
                i = 0
                while (i < 2) :
                    if (i == 0) :
                        print(f" \n                         YOU -> {Play_With_Computer.Name}  = {Play_With_Computer.playerPosition}")
                        speak(f" \n                         YOU -> {Play_With_Computer.Name}  = {Play_With_Computer.playerPosition}")
                    else :
                        print(f"                         COMPUTER = {Play_With_Computer.computerPosition}")
                        speak(f"                         COMPUTER = {Play_With_Computer.computerPosition}")
                    i += 1
    def IsWon(self) :
        if (Play_With_Computer.playerPosition == Play_With_Computer.WONPOINT) :
            print("\n---------------------WINNER------------------------------- \n")
            print(f"                          CONGRATS {Play_With_Computer.Name}")
            print("\n---------------------WINNER------------------------------- \n")
            speak("\n---------------------WINNER------------------------------- \n")
            speak(f"                          CONGRATS {Play_With_Computer.Name}")
            speak("\n---------------------WINNER------------------------------- \n")
            self.flag = 1
        if (Play_With_Computer.computerPosition == Play_With_Computer.WONPOINT) :
            print("\n--------------------------------WINNER---------------------------- \n")
            print("                              COMPUTER \n")
            print("                            YOU LOSE !!!!!")
            print("\n------------------------------------------------------------------ \n")
            speak("WINNER")
            speak("COMPUTER")
            speak("YOU LOSE")
            self.flag = 1
    # setGame()
    def setGame(self) :
        print("-------------------------->SET GAME<------------------------------- \n", end ="")
        speak("SET GAME")
        print("         Levels :   1 - EASY     2 - MEDIUM     3 - HARD \n \n", end ="")
        speak("Levels")
        speak("1 - EASY")
        speak("2 - MEDIUM")
        speak("3 - HARD")
        print("Choose a Level (1 | 2 | 3 ) : ", end ="")
        speak("Choose a Level")
        speak("1 or 2 or 3 ")
        self.Level = input()[0]
        while (self.Level != '1' and self.Level != '2' and self.Level != '3') :
            print("Choose a valid Level (1 | 2 | 3 ) : ", end ="")
            speak("Choose a valid Level")
            self.Level = input()[0]
        print(" \nEnter Your Name : ", end ="")
        speak("Enter Your Name")
        Play_With_Computer.Name = input()
    def SnakesAndLaddersPosition(self) :
        if (self.Level == '1') :
            # Snake Mouth Position Setting
            Play_With_Computer.Snake_Mouth_Position[0] = random.randint(95, (99 - 95) + 95)
            Play_With_Computer.Snake_Mouth_Position[1] = random.randint(60, (65 - 60) + 60)
            Play_With_Computer.Snake_Mouth_Position[2] = random.randint(30, (35 - 30) + 30)
            # Snake Tail Position Setting
            Play_With_Computer.Snake_Tail_Position[0] = random.randint(24, (26 - 24) + 24)
            Play_With_Computer.Snake_Tail_Position[1] = random.randint(51, (56 - 51) + 51)
            Play_With_Computer.Snake_Tail_Position[2] = random.randint(15, (19 - 15) + 15)
        elif(self.Level == '2') :
            # Snake Mouth Position Setting
            Play_With_Computer.Snake_Mouth_Position[0] = random.randint(98, (99 - 98) + 98)
            Play_With_Computer.Snake_Mouth_Position[1] = random.randint(87, (87 - 81) + 81)
            Play_With_Computer.Snake_Mouth_Position[2] = random.randint(55, (59 - 55) + 55)
            Play_With_Computer.Snake_Mouth_Position[3] = random.randint(32, (38 - 32) + 32)
            Play_With_Computer.Snake_Mouth_Position[4] = random.randint(15, (19 - 15) + 15)
            # Snake Tail Position Setting
            Play_With_Computer.Snake_Tail_Position[0] = random.randint(51, (56 - 51) + 51)
            Play_With_Computer.Snake_Tail_Position[1] = random.randint(72, (78 - 72) + 72)
            Play_With_Computer.Snake_Tail_Position[2] = random.randint(41, (42 - 41) + 41)
            Play_With_Computer.Snake_Tail_Position[3] = random.randint(26, (29 - 26) + 26)
            Play_With_Computer.Snake_Tail_Position[4] = random.randint(6,  (9 - 6) + 6)
        else :
            # Snake Mouth Position Setting
            Play_With_Computer.Snake_Mouth_Position[0] = random.randint(98, (99 - 98) + 98)
            Play_With_Computer.Snake_Mouth_Position[1] = random.randint(92, (96 - 92) + 92)
            Play_With_Computer.Snake_Mouth_Position[2] = random.randint(71, (74 - 71) + 71)
            Play_With_Computer.Snake_Mouth_Position[3] = random.randint(62, (65 - 62) + 62)
            Play_With_Computer.Snake_Mouth_Position[4] = random.randint(41, (42 - 41) + 41)
            Play_With_Computer.Snake_Mouth_Position[5] = random.randint(65, (69 - 65) + 65)
            Play_With_Computer.Snake_Mouth_Position[6] = random.randint(24, (26 - 24) + 24)
            Play_With_Computer.Snake_Mouth_Position[7] = random.randint(15, (19 - 15) + 15)
            # Snake Tail Position Setting
            Play_With_Computer.Snake_Tail_Position[0] = random.randint(51, (56 - 51) + 51)
            Play_With_Computer.Snake_Tail_Position[1] = random.randint(41, (45 - 41) + 41)
            Play_With_Computer.Snake_Tail_Position[2] = random.randint(32, (36 - 32) + 32)
            Play_With_Computer.Snake_Tail_Position[3] = random.randint(22, (26 - 22) + 22)
            Play_With_Computer.Snake_Tail_Position[4] = random.randint(26, (29 - 26) + 26)
            Play_With_Computer.Snake_Tail_Position[5] = random.randint(15, (19 - 15) + 15)
            Play_With_Computer.Snake_Tail_Position[6] = random.randint(15, (19 - 15) + 15)
            Play_With_Computer.Snake_Tail_Position[7] = random.randint(6, (9 - 6) + 6)
        if (self.Level == '1') :
            # Ladder Down Position Setting
            Play_With_Computer.Ladder_Down_Position[0] = random.randint(6, (9 - 6) + 6)
            Play_With_Computer.Ladder_Down_Position[1] = random.randint(65, (69 - 65) + 65)
            Play_With_Computer.Ladder_Down_Position[2] = random.randint(87, (87 - 81) + 81)
            # Laddet Up Position Setting
            Play_With_Computer.Ladder_Up_Position[0] = random.randint(81, (87 - 81) + 81)
            Play_With_Computer.Ladder_Up_Position[1] = random.randint(92, (96 - 92) + 92)
            Play_With_Computer.Ladder_Up_Position[2] = random.randint(96, (99 - 96) + 96)
        elif(self.Level == '2') :
            # Ladder Down Position Setting
            Play_With_Computer.Ladder_Down_Position[0] = random.randint(15, (19 - 15) + 15)
            Play_With_Computer.Ladder_Down_Position[1] = random.randint(37, (38 - 37) + 37)
            Play_With_Computer.Ladder_Down_Position[2] = random.randint(51, (59 - 51) + 51)
            Play_With_Computer.Ladder_Down_Position[3] = random.randint(65, (69 - 65) + 65)
            Play_With_Computer.Ladder_Down_Position[4] = random.randint(81, (86 - 81) + 81)
            # Ladder Up Position Setting
            Play_With_Computer.Ladder_Up_Position[0] = random.randint(81, (86 - 81) + 81)
            Play_With_Computer.Ladder_Up_Position[1] = random.randint(41, (42 - 41) + 41)
            Play_With_Computer.Ladder_Up_Position[2] = random.randint(81, (86 - 81) + 81)
            Play_With_Computer.Ladder_Up_Position[3] = random.randint(92, (96 - 92) + 92)
            Play_With_Computer.Ladder_Up_Position[4] = random.randint(96, (99 - 96) + 96)
        else :
            # Ladder Down Position Setting
            Play_With_Computer.Ladder_Down_Position[0] = random.randint(6, (9 - 6) + 6)
            Play_With_Computer.Ladder_Down_Position[1] = random.randint(24, (26 - 24) + 24)
            Play_With_Computer.Ladder_Down_Position[2] = random.randint(36, (38 - 36) + 36)
            Play_With_Computer.Ladder_Down_Position[3] = random.randint(41, (45 - 41) + 41)
            Play_With_Computer.Ladder_Down_Position[4] = random.randint(54, (59 - 54) + 54)
            Play_With_Computer.Ladder_Down_Position[5] = random.randint(68, (69 - 68) + 68)
            Play_With_Computer.Ladder_Down_Position[6] = random.randint(72, (78 - 72) + 72)
            Play_With_Computer.Ladder_Down_Position[7] = random.randint(81, (86 - 81) + 81)
            # Ladder Up Position Setting
            Play_With_Computer.Ladder_Up_Position[0] = random.randint(81, (87 - 81) + 81)
            Play_With_Computer.Ladder_Up_Position[1] = random.randint(92, (96 - 92) + 92)
            Play_With_Computer.Ladder_Up_Position[2] = random.randint(74, (78 - 74) + 74)
            Play_With_Computer.Ladder_Up_Position[3] = random.randint(65, (69 - 65) + 65)
            Play_With_Computer.Ladder_Up_Position[4] = random.randint(81, (87 - 81) + 81)
            Play_With_Computer.Ladder_Up_Position[5] = random.randint(74, (78 - 74) + 74)
            Play_With_Computer.Ladder_Up_Position[6] = random.randint(95, (96 - 95) + 95)
            Play_With_Computer.Ladder_Up_Position[7] = random.randint(92, (99 - 92) + 92)
    def SnakesAndLaddersPositionPrint(self) :
        print(" \n-------->SNAKES POSITION           |      LADDERS POSITION <--------- \n", end ="")
        speak("SNAKES POSITION and LADDERS POSITION")
        if (self.Level == '1') :
            i = 0
            while (i < 3) :
                if (i == 0) :
                    print(f"               {Play_With_Computer.Snake_Mouth_Position[i]}     to   {Play_With_Computer.Snake_Tail_Position[i]}      |    0{Play_With_Computer.Ladder_Down_Position[i]}     to    {Play_With_Computer.Ladder_Up_Position[i]}")
                else :
                    print(f"               {Play_With_Computer.Snake_Mouth_Position[i]}     to   {Play_With_Computer.Snake_Tail_Position[i]}      |    {Play_With_Computer.Ladder_Down_Position[i]}     to    {Play_With_Computer.Ladder_Up_Position[i]}")
                i += 1
        elif(self.Level == '2') :
            i = 0
            while (i < 5) :
                if (i == 0) :
                    print(f"               {Play_With_Computer.Snake_Mouth_Position[i]}     to   {Play_With_Computer.Snake_Tail_Position[i]}      |    {Play_With_Computer.Ladder_Down_Position[i]}     to    {Play_With_Computer.Ladder_Up_Position[i]}")
                elif(i == 4) :
                    print(f"               {Play_With_Computer.Snake_Mouth_Position[i]}     to   0{Play_With_Computer.Snake_Tail_Position[i]}      |    {Play_With_Computer.Ladder_Down_Position[i]}     to    {Play_With_Computer.Ladder_Up_Position[i]}")
                else :
                    print(f"               {Play_With_Computer.Snake_Mouth_Position[i]}     to   {Play_With_Computer.Snake_Tail_Position[i]}      |    {Play_With_Computer.Ladder_Down_Position[i]}     to    {Play_With_Computer.Ladder_Up_Position[i]}")
                i += 1
        else :
            i = 0
            while (i < 8) :
                if (i == 0) :
                    print(f"               {Play_With_Computer.Snake_Mouth_Position[i]}     to   {Play_With_Computer.Snake_Tail_Position[i]}      |    0{Play_With_Computer.Ladder_Down_Position[i]}     to    {Play_With_Computer.Ladder_Up_Position[i]}")
                elif(i == 7) :
                    print(f"               {Play_With_Computer.Snake_Mouth_Position[i]}     to   0{Play_With_Computer.Snake_Tail_Position[i]}      |    {Play_With_Computer.Ladder_Down_Position[i]}     to    {Play_With_Computer.Ladder_Up_Position[i]}")
                else :
                    print(f"               {Play_With_Computer.Snake_Mouth_Position[i]}     to   {Play_With_Computer.Snake_Tail_Position[i]}      |    {Play_With_Computer.Ladder_Down_Position[i]}     to    {Play_With_Computer.Ladder_Up_Position[i]}")
                i += 1
        print("------------------------------------------------------------------- \n", end ="")
    def RollDice(self) :
        print(" \n----------------------->Roll The Dice<-----------------------------\n", end ="")
        speak("Roll The Dice")
        print(f" \n            {Play_With_Computer.Name}\'s Turn (Enter character \"R\" or \"r\" ) : ", end ="")
        speak("Enter character Capital or Small R")
        Play_With_Computer.rollDice = input()
        while (Play_With_Computer.rollDice != 'R' and Play_With_Computer.rollDice != 'r') :
            print("               Enter Valid Character R or r : ", end ="")
            speak("Enter Valid Character Capital or Small R")
            Play_With_Computer.rollDice = input()
        Play_With_Computer.playerDice = random.randint(1, (6 - 1) + 1)
        Play_With_Computer.playerPosition += Play_With_Computer.playerDice
        print(f"                     Your Dice Score : {Play_With_Computer.playerDice}")
        I = 0
        while (I < 8) :
            if (self.Level == '1' and I < 3) :
                if (Play_With_Computer.playerPosition == Play_With_Computer.Snake_Mouth_Position[I]) :
                    print(f" \n        --------->Oops, {Play_With_Computer.Name} Swallowed By Snake<---------")
                    speak(f"Oops, {Play_With_Computer.Name} Swallowed By Snake")
                elif(Play_With_Computer.playerPosition == Play_With_Computer.Ladder_Down_Position[I]) :
                    print(f" \n            ----->Hurry, {Play_With_Computer.Name} Climb Up The Ladder<-----")
                    speak(f">Hurry, {Play_With_Computer.Name} Climb Up The Ladder")
            elif(self.Level == '2' and I < 5) :
                if (Play_With_Computer.playerPosition == Play_With_Computer.Snake_Mouth_Position[I]) :
                    print(f" \n        --------->Oops, {Play_With_Computer.Name} Swallowed By Snake<---------")
                    speak(f"nOops, {Play_With_Computer.Name} Swallowed By Snake")
                elif(Play_With_Computer.playerPosition == Play_With_Computer.Ladder_Down_Position[I]) :
                    print(f" \n            ----->Hurry, {Play_With_Computer.Name} Climb Up The Ladder<-----")
                    speak(f"Hurry, {Play_With_Computer.Name} Climb Up The Ladder")
            else :
                if (Play_With_Computer.playerPosition == Play_With_Computer.Snake_Mouth_Position[I]) :
                    print(f" \n        --------->Oops, {Play_With_Computer.Name} Swallowed By Snake<---------")
                    speak(f"Oops, {Play_With_Computer.Name} Swallowed By Snake")
                elif(Play_With_Computer.playerPosition == Play_With_Computer.Ladder_Down_Position[I]) :
                    print(f" \n            ----->Hurry, {Play_With_Computer.Name} Climb Up The Ladder<-----")
                    speak(f"Hurry, {Play_With_Computer.Name} Climb Up The Ladder")
            I += 1
        print("\n                   Computer\'s Turn (Wait) : ", end ="")
        speak("Computer\'s Turn (Wait)")
        Play_With_Computer.computerDice = random.randint(1, (6 - 1) + 1)
        Play_With_Computer.computerPosition += Play_With_Computer.computerDice
        try :
            # Thread
            k = 0
            while (k < 5) :
                Thread.sleep(501)
                k += 1
        except Exception as expn :
            if (random.randint(6, (9 - 6) + 6)% 2 == 0) :
                print(f"R \n                   Computer\'s Dice Score : {Play_With_Computer.computerDice}")
            else :
                print(f"r \n                   Computer\'s Dice Score : {Play_With_Computer.computerDice}")
            I = 0
        while (I < 8) :
            if (self.Level == '1' and I < 3) :
                if (Play_With_Computer.computerPosition == Play_With_Computer.Snake_Mouth_Position[I]) :
                    print(" \n       -------->Computer Swallowed By Snake<---------")
                    speak("Computer Swallowed By Snake")
                elif(Play_With_Computer.computerPosition == Play_With_Computer.Ladder_Down_Position[I]) :
                    print(" \n       -------->Computer Climb Up The Ladder<-------")
                    speak("Computer Climb Up The Ladder")
            elif(self.Level == '2' and I < 5) :
                if (Play_With_Computer.computerPosition == Play_With_Computer.Snake_Mouth_Position[I]) :
                    print(" \n       -------->Computer Swallowed By Snake<---------")
                    speak("Computer Swallowed By Snake")
                elif(Play_With_Computer.computerPosition == Play_With_Computer.Ladder_Down_Position[I]) :
                    print(" \n       -------->Computer Climb Up The Ladder<-------")
                    speak("Computer Climb Up The Ladder")
            else :
                if (Play_With_Computer.computerPosition == Play_With_Computer.Snake_Mouth_Position[I]) :
                    print(" \n       -------->Computer Swallowed By Snake<---------")
                    speak("Computer Swallowed By Snake")
                elif(Play_With_Computer.computerPosition == Play_With_Computer.Ladder_Down_Position[I]) :
                    print(" \n       -------->Computer Climb Up The Ladder<-------")
                    speak("Computer Climb Up The Ladder")
            I += 1
        if (self.flag != 1) :
            self.PlayerAndComputerPosition()
            self.IsWon()
#Play_with_friends class
class Play_With_friends :
    WONPOINT = 100
    rand =  random.randint(1, 7)
    n = 100
    rollDice = ' '
    playerPosition = [0] * (n)
    diceScore = [0] * (n)
    Names = [None] * (n)
    Snake_Mouth_Position = [0] * (8)
    Snake_Tail_Position = [0] * (8)
    Ladder_Up_Position = [0] * (8)
    Ladder_Down_Position = [0] * (8)
    flag = 0
    Level = ' '
    Count = 0
    Snake_flag = 0
    Ladder_flag = 0
    # setGame()
    def setGame(self) :
        print("-------------------------->SET GAME<------------------------------- \n", end ="")
        speak("SET GAME")
        print("         Levels :   1 - EASY     2 - MEDIUM     3 - HARD \n \n", end ="")
        speak("Levels")
        speak("1 - EASY")
        speak("2 - MEDIUM")
        speak("3 - HARD")
        print("Choose a Level (1 | 2 | 3 ) : ", end ="")
        speak("Choose a Level")
        speak("1 or 2 or 3 ")
        self.Level = input()
        while (self.Level != '1' and self.Level != '2' and self.Level != '3') :
            print("Choose a valid Level (1 | 2 | 3 ) : ", end ="")
            speak("Choose a valid Level")
            self.Level = input()
    # setPlayer()
    def SetPlayer(self) :
        print(" \nEnter no. of Players : ", end ="")
        speak("Enter number of Players")
        try:
            Play_With_friends.n = int(input())
        except:
            printf("Enter valid Value : ")
        while (self.n < 0) :
            print("Enter Valid no. of Players : ")
            speak("Enter Valid no. of Players")
            Play_With_friends.n = input()
        print(" \nEnter players Names : ")
        speak("Enter players Names")
        i = 0
        while (i < Play_With_friends.n) :
            print(f"player {i + 1}  : ", end ="")
            speak(f"Enter player {i + 1}  Name")
            Play_With_friends.Names[i] = input()
            i += 1
    def SnakesAndLaddersPosition(self) :
        if (self.Level == '1') :
            # Snake Mouth Position Setting
            Play_With_friends.Snake_Mouth_Position[0] = random.randint(95, (99 - 95) + 95)
            Play_With_friends.Snake_Mouth_Position[1] = random.randint(60, (65 - 60) + 60)
            Play_With_friends.Snake_Mouth_Position[2] = random.randint(30, (35 - 30) + 30)
            # Snake Tail Position Setting
            Play_With_friends.Snake_Tail_Position[0] = random.randint(24, (26 - 24) + 24)
            Play_With_friends.Snake_Tail_Position[1] = random.randint(51, (56 - 51) + 51)
            Play_With_friends.Snake_Tail_Position[2] = random.randint(15, (19 - 15) + 15)
        elif(self.Level == '2') :
            # Snake Mouth Position Setting
            Play_With_friends.Snake_Mouth_Position[0] = random.randint(98, (99 - 98) + 98)
            Play_With_friends.Snake_Mouth_Position[1] = random.randint(87, (87 - 81) + 81)
            Play_With_friends.Snake_Mouth_Position[2] = random.randint(55, (59 - 55) + 55)
            Play_With_friends.Snake_Mouth_Position[3] = random.randint(32, (38 - 32) + 32)
            Play_With_friends.Snake_Mouth_Position[4] = random.randint(15, (19 - 15) + 15)
            # Snake Tail Position Setting
            Play_With_friends.Snake_Tail_Position[0] = random.randint(51, (56 - 51) + 51)
            Play_With_friends.Snake_Tail_Position[1] = random.randint(72, (78 - 72) + 72)
            Play_With_friends.Snake_Tail_Position[2] = random.randint(41, (42 - 41) + 41)
            Play_With_friends.Snake_Tail_Position[3] = random.randint(26, (29 - 26) + 26)
            Play_With_friends.Snake_Tail_Position[4] = random.randint(6,  (9 - 6) + 6)
        else :
            # Snake Mouth Position Setting
            Play_With_friends.Snake_Mouth_Position[0] = random.randint(98, (99 - 98) + 98)
            Play_With_friends.Snake_Mouth_Position[1] = random.randint(92, (96 - 92) + 92)
            Play_With_friends.Snake_Mouth_Position[2] = random.randint(71, (74 - 71) + 71)
            Play_With_friends.Snake_Mouth_Position[3] = random.randint(62, (65 - 62) + 62)
            Play_With_friends.Snake_Mouth_Position[4] = random.randint(41, (42 - 41) + 41)
            Play_With_friends.Snake_Mouth_Position[5] = random.randint(65, (69 - 65) + 65)
            Play_With_friends.Snake_Mouth_Position[6] = random.randint(24, (26 - 24) + 24)
            Play_With_friends.Snake_Mouth_Position[7] = random.randint(15, (19 - 15) + 15)
            # Snake Tail Position Setting
            Play_With_friends.Snake_Tail_Position[0] = random.randint(51, (56 - 51) + 51)
            Play_With_friends.Snake_Tail_Position[1] = random.randint(41, (45 - 41) + 41)
            Play_With_friends.Snake_Tail_Position[2] = random.randint(32, (36 - 32) + 32)
            Play_With_friends.Snake_Tail_Position[3] = random.randint(22, (26 - 22) + 22)
            Play_With_friends.Snake_Tail_Position[4] = random.randint(26, (29 - 26) + 26)
            Play_With_friends.Snake_Tail_Position[5] = random.randint(15, (19 - 15) + 15)
            Play_With_friends.Snake_Tail_Position[6] = random.randint(15, (19 - 15) + 15)
            Play_With_friends.Snake_Tail_Position[7] = random.randint(6, (9 - 6) + 6)
        if (self.Level == '1') :
            # Ladder Down Position Setting
            Play_With_friends.Ladder_Down_Position[0] = random.randint(6, (9 - 6) + 6)
            Play_With_friends.Ladder_Down_Position[1] = random.randint(65, (69 - 65) + 65)
            Play_With_friends.Ladder_Down_Position[2] = random.randint(87, (87 - 81) + 81)
            # Laddet Up Position Setting
            Play_With_friends.Ladder_Up_Position[0] = random.randint(81, (87 - 81) + 81)
            Play_With_friends.Ladder_Up_Position[1] = random.randint(92, (96 - 92) + 92)
            Play_With_friends.Ladder_Up_Position[2] = random.randint(96, (99 - 96) + 96)
        elif(self.Level == '2') :
            # Ladder Down Position Setting
            Play_With_friends.Ladder_Down_Position[0] = random.randint(15, (19 - 15) + 15)
            Play_With_friends.Ladder_Down_Position[1] = random.randint(37, (38 - 37) + 37)
            Play_With_friends.Ladder_Down_Position[2] = random.randint(51, (59 - 51) + 51)
            Play_With_friends.Ladder_Down_Position[3] = random.randint(65, (69 - 65) + 65)
            Play_With_friends.Ladder_Down_Position[4] = random.randint(81, (86 - 81) + 81)
            # Ladder Up Position Setting
            Play_With_friends.Ladder_Up_Position[0] = random.randint(81, (86 - 81) + 81)
            Play_With_friends.Ladder_Up_Position[1] = random.randint(41, (42 - 41) + 41)
            Play_With_friends.Ladder_Up_Position[2] = random.randint(81, (86 - 81) + 81)
            Play_With_friends.Ladder_Up_Position[3] = random.randint(92, (96 - 92) + 92)
            Play_With_friends.Ladder_Up_Position[4] = random.randint(96, (99 - 96) + 96)
        else :
            # Ladder Down Position Setting
            Play_With_friends.Ladder_Down_Position[0] = random.randint(6, (9 - 6) + 6)
            Play_With_friends.Ladder_Down_Position[1] = random.randint(24, (26 - 24) + 24)
            Play_With_friends.Ladder_Down_Position[2] = random.randint(36, (38 - 36) + 36)
            Play_With_friends.Ladder_Down_Position[3] = random.randint(41, (45 - 41) + 41)
            Play_With_friends.Ladder_Down_Position[4] = random.randint(54, (59 - 54) + 54)
            Play_With_friends.Ladder_Down_Position[5] = random.randint(68, (69 - 68) + 68)
            Play_With_friends.Ladder_Down_Position[6] = random.randint(72, (78 - 72) + 72)
            Play_With_friends.Ladder_Down_Position[7] = random.randint(81, (86 - 81) + 81)
            # Ladder Up Position Setting
            Play_With_friends.Ladder_Up_Position[0] = random.randint(81, (87 - 81) + 81)
            Play_With_friends.Ladder_Up_Position[1] = random.randint(92, (96 - 92) + 92)
            Play_With_friends.Ladder_Up_Position[2] = random.randint(74, (78 - 74) + 74)
            Play_With_friends.Ladder_Up_Position[3] = random.randint(65, (69 - 65) + 65)
            Play_With_friends.Ladder_Up_Position[4] = random.randint(81, (87 - 81) + 81)
            Play_With_friends.Ladder_Up_Position[5] = random.randint(74, (78 - 74) + 74)
            Play_With_friends.Ladder_Up_Position[6] = random.randint(95, (96 - 95) + 95)
            Play_With_friends.Ladder_Up_Position[7] = random.randint(92, (99 - 92) + 92)
    def SnakesAndLaddersPositionPrint(self) :
        print(" \n-------->SNAKES POSITION           |      LADDERS POSITION <--------- \n", end ="")
        speak("SNAKES POSITION and LADDERS POSITION")
        if (self.Level == '1') :
            i = 0
            while (i < 3) :
                if (i == 0) :
                    print(f"               {Play_With_friends.Snake_Mouth_Position[i]}     to   {Play_With_friends.Snake_Tail_Position[i]}      |    0{Play_With_friends.Ladder_Down_Position[i]}     to    {Play_With_friends.Ladder_Up_Position[i]}")
                else :
                    print(f"               {Play_With_friends.Snake_Mouth_Position[i]}     to   {Play_With_friends.Snake_Tail_Position[i]}      |    {Play_With_friends.Ladder_Down_Position[i]}     to    {Play_With_friends.Ladder_Up_Position[i]}")
                i += 1
        elif(self.Level == '2') :
            i = 0
            while (i < 5) :
                if (i == 0) :
                    print(f"               {Play_With_friends.Snake_Mouth_Position[i]}     to   {Play_With_friends.Snake_Tail_Position[i]}      |    {Play_With_friends.Ladder_Down_Position[i]}     to    {Play_With_friends.Ladder_Up_Position[i]}")
                elif(i == 4) :
                    print(f"               {Play_With_friends.Snake_Mouth_Position[i]}     to   0{Play_With_friends.Snake_Tail_Position[i]}      |    {Play_With_friends.Ladder_Down_Position[i]}     to    {Play_With_friends.Ladder_Up_Position[i]}")
                else :
                    print(f"               {Play_With_friends.Snake_Mouth_Position[i]}     to   {Play_With_friends.Snake_Tail_Position[i]}      |    {Play_With_friends.Ladder_Down_Position[i]}     to    {Play_With_friends.Ladder_Up_Position[i]}")
                i += 1
        else :
            i = 0
            while (i < 8) :
                if (i == 0) :
                    print(f"               {Play_With_friends.Snake_Mouth_Position[i]}     to   {Play_With_friends.Snake_Tail_Position[i]}      |    0{Play_With_friends.Ladder_Down_Position[i]}     to    {Play_With_friends.Ladder_Up_Position[i]}")
                elif(i == 7) :
                    print(f"               {Play_With_friends.Snake_Mouth_Position[i]}     to   0{Play_With_friends.Snake_Tail_Position[i]}      |    {Play_With_friends.Ladder_Down_Position[i]}     to    {Play_With_friends.Ladder_Up_Position[i]}")
                else :
                    print(f"               {Play_With_friends.Snake_Mouth_Position[i]}     to   {Play_With_friends.Snake_Tail_Position[i]}      |    {Play_With_friends.Ladder_Down_Position[i]}     to    {Play_With_friends.Ladder_Up_Position[i]}")
                i += 1
        print("------------------------------------------------------------------- \n", end ="")
    def RollDice(self) :
        print("\n------------------------>Roll The Dice<--------------------------\n", end ="")
        speak("Roll The Dice")
        i = 0
        while (i < Play_With_friends.n) :
            print(f" \n           {Play_With_friends.Names[i]}\'s Turn (Enter character "R" or "r" ) : ", end ="")
            speak(f"{Play_With_friends.Names[i]}\'s Turn")
            speak("Enter Capital or Small R")
            Play_With_friends.rollDice = input()
            while (Play_With_friends.rollDice != 'R' and Play_With_friends.rollDice != 'r') :
                print("\n           Enter Valid Character R or r : ")
                speak("Enter Valid Capital or Small R")
                Play_With_friends.rollDice = input()
            Play_With_friends.diceScore[i] = random.randint(1, (6 - 1) + 1)
            Play_With_friends.playerPosition[i] += Play_With_friends.diceScore[i]
            print(f"                     dice Score = {Play_With_friends.diceScore[i]}")
            speak(f"dice Score = {Play_With_friends.diceScore[i]}")
            I = 0
            while (I < Play_With_friends.n) :
                k = 0
                while (k < 8) :
                    if (self.Level == '1' and I < 3) :
                        if (Play_With_friends.playerPosition[I] == Play_With_friends.Snake_Mouth_Position[k] and (Play_With_friends.playerPosition[I] != 0 and Play_With_friends.Snake_Mouth_Position[k] != 0)) :
                            print(" \n        --------->Oops, Swallowed By Snake<---------")
                            speak("Oops, Swallowed By Snake")
                        elif(Play_With_friends.playerPosition[I] == Play_With_friends.Ladder_Down_Position[k] and (Play_With_friends.playerPosition[I] != 0 and Play_With_friends.Ladder_Down_Position[k] != 0)) :
                            print(" \n            ----->Hurry, Climb Up The Ladder<-----")
                            speak("Hurry, Climb Up The Ladder")
                    elif(self.Level == '2' and I < 5) :
                        if (Play_With_friends.playerPosition[I] == Play_With_friends.Snake_Mouth_Position[k]  and (Play_With_friends.playerPosition[I] != 0 and Play_With_friends.Snake_Mouth_Position[k] != 0)) :
                            print(" \n        --------->Oops, Swallowed By Snake<---------")
                            speak("Oops, Swallowed By Snake")
                        elif(Play_With_friends.playerPosition[I] == Play_With_friends.Ladder_Down_Position[k] and (Play_With_friends.playerPosition[I] != 0 and Play_With_friends.Ladder_Down_Position[k] != 0)) :
                            print(" \n            ----->Hurry, Climb Up The Ladder<-----")
                            speak("Hurry, Climb Up The Ladder")
                    else :
                        if (Play_With_friends.playerPosition[I] == Play_With_friends.Snake_Mouth_Position[k] and (Play_With_friends.playerPosition[I] != 0 and Play_With_friends.Snake_Mouth_Position[k] != 0)) :
                            print(" \n        --------->Oops, Swallowed By Snake<---------")
                            speak("Oops, Swallowed By Snake")
                        elif(Play_With_friends.playerPosition[I] == Play_With_friends.Ladder_Down_Position[k] and (Play_With_friends.playerPosition[I] != 0 and Play_With_friends.Ladder_Down_Position[k] != 0)) :
                            print(" \n            ----->Hurry, Climb Up The Ladder<-----")
                            speak("Hurry, Climb Up The Ladder")
                    k += 1
                I += 1
            if (self.flag != 1) :
                self.PlayerPosition()
                self.IsWon()
            i += 1
    def PlayerPosition(self) :
        i = 0
        while (i < Play_With_friends.n) :
            if (Play_With_friends.playerPosition[i] > Play_With_friends.WONPOINT) :
                Play_With_friends.playerPosition[i] -= Play_With_friends.diceScore[i]
            i += 1
        # playerPosition With Snake_Tail_Position
        i = 0
        while (i < Play_With_friends.n) :
            if (self.Level == '1') :
                if (Play_With_friends.playerPosition[i] == Play_With_friends.Snake_Mouth_Position[0]) :
                    Play_With_friends.playerPosition[i] = Play_With_friends.Snake_Tail_Position[0]
                elif(Play_With_friends.playerPosition[i] == Play_With_friends.Snake_Mouth_Position[1]) :
                    Play_With_friends.playerPosition[i] = Play_With_friends.Snake_Tail_Position[1]
                elif(Play_With_friends.playerPosition[i] == Play_With_friends.Snake_Mouth_Position[2]) :
                    Play_With_friends.playerPosition[i] = Play_With_friends.Snake_Tail_Position[2]
            elif(self.Level == '2') :
                if (Play_With_friends.playerPosition[i] == Play_With_friends.Snake_Mouth_Position[0]) :
                    Play_With_friends.playerPosition[i] = Play_With_friends.Snake_Tail_Position[0]
                elif(Play_With_friends.playerPosition[i] == Play_With_friends.Snake_Mouth_Position[1]) :
                    Play_With_friends.playerPosition[i] = Play_With_friends.Snake_Tail_Position[1]
                elif(Play_With_friends.playerPosition[i] == Play_With_friends.Snake_Mouth_Position[2]) :
                    Play_With_friends.playerPosition[i] = Play_With_friends.Snake_Tail_Position[2]
                elif(Play_With_friends.playerPosition[i] == Play_With_friends.Snake_Mouth_Position[3]) :
                    Play_With_friends.playerPosition[i] = Play_With_friends.Snake_Tail_Position[3]
                elif(Play_With_friends.playerPosition[i] == Play_With_friends.Snake_Mouth_Position[4]) :
                    Play_With_friends.playerPosition[i] = Play_With_friends.Snake_Tail_Position[4]
                else :
                    pass
            else :
                if (Play_With_friends.playerPosition[i] == Play_With_friends.Snake_Mouth_Position[0]) :
                    Play_With_friends.playerPosition[i] = Play_With_friends.Snake_Tail_Position[0]
                elif(Play_With_friends.playerPosition[i] == Play_With_friends.Snake_Mouth_Position[1]) :
                    Play_With_friends.playerPosition[i] = Play_With_friends.Snake_Tail_Position[1]
                elif(Play_With_friends.playerPosition[i] == Play_With_friends.Snake_Mouth_Position[2]) :
                    Play_With_friends.playerPosition[i] = Play_With_friends.Snake_Tail_Position[2]
                elif(Play_With_friends.playerPosition[i] == Play_With_friends.Snake_Mouth_Position[3]) :
                    Play_With_friends.playerPosition[i] = Play_With_friends.Snake_Tail_Position[3]
                elif(Play_With_friends.playerPosition[i] == Play_With_friends.Snake_Mouth_Position[4]) :
                    Play_With_friends.playerPosition[i] = Play_With_friends.Snake_Tail_Position[4]
                elif(Play_With_friends.playerPosition[i] == Play_With_friends.Snake_Mouth_Position[5]) :
                    Play_With_friends.playerPosition[i] = Play_With_friends.Snake_Tail_Position[5]
                elif(Play_With_friends.playerPosition[i] == Play_With_friends.Snake_Mouth_Position[6]) :
                    Play_With_friends.playerPosition[i] = Play_With_friends.Snake_Tail_Position[6]
                elif(Play_With_friends.playerPosition[i] == Play_With_friends.Snake_Mouth_Position[7]) :
                    Play_With_friends.playerPosition[i] = Play_With_friends.Snake_Tail_Position[7]
            i += 1
        # playerPosition With Ladder
        i = 0
        while (i < Play_With_friends.n) :
            if (self.Level == '1') :
                if (Play_With_friends.playerPosition[i] == Play_With_friends.Ladder_Down_Position[0]) :
                    Play_With_friends.playerPosition[i] = Play_With_friends.Ladder_Up_Position[0]
                elif(Play_With_friends.playerPosition[i] == Play_With_friends.Ladder_Down_Position[1]) :
                    Play_With_friends.playerPosition[i] = Play_With_friends.Ladder_Up_Position[1]
                elif(Play_With_friends.playerPosition[i] == Play_With_friends.Ladder_Down_Position[2]) :
                    Play_With_friends.playerPosition[i] = Play_With_friends.Ladder_Up_Position[2]
            elif(self.Level == '2') :
                if (Play_With_friends.playerPosition[i] == Play_With_friends.Ladder_Down_Position[0]) :
                    Play_With_friends.playerPosition[i] = Play_With_friends.Ladder_Up_Position[0]
                elif(Play_With_friends.playerPosition[i] == Play_With_friends.Ladder_Down_Position[1]) :
                    Play_With_friends.playerPosition[i] = Play_With_friends.Ladder_Up_Position[1]
                elif(Play_With_friends.playerPosition[i] == Play_With_friends.Ladder_Down_Position[2]) :
                    Play_With_friends.playerPosition[i] = Play_With_friends.Ladder_Up_Position[2]
                elif(Play_With_friends.playerPosition[i] == Play_With_friends.Ladder_Down_Position[3]) :
                    Play_With_friends.playerPosition[i] = Play_With_friends.Ladder_Up_Position[3]
                elif(Play_With_friends.playerPosition[i] == Play_With_friends.Ladder_Down_Position[4]) :
                    Play_With_friends.playerPosition[i] = Play_With_friends.Ladder_Up_Position[4]
            else :
                if (Play_With_friends.playerPosition[i] == Play_With_friends.Ladder_Down_Position[0]) :
                    Play_With_friends.playerPosition[i] = Play_With_friends.Ladder_Up_Position[0]
                elif(Play_With_friends.playerPosition[i] == Play_With_friends.Ladder_Down_Position[1]) :
                    Play_With_friends.playerPosition[i] = Play_With_friends.Ladder_Up_Position[1]
                elif(Play_With_friends.playerPosition[i] == Play_With_friends.Ladder_Down_Position[2]) :
                    Play_With_friends.playerPosition[i] = Play_With_friends.Ladder_Up_Position[2]
                elif(Play_With_friends.playerPosition[i] == Play_With_friends.Ladder_Down_Position[3]) :
                    Play_With_friends.playerPosition[i] = Play_With_friends.Ladder_Up_Position[3]
                elif(Play_With_friends.playerPosition[i] == Play_With_friends.Ladder_Down_Position[4]) :
                    Play_With_friends.playerPosition[i] = Play_With_friends.Ladder_Up_Position[4]
                elif(Play_With_friends.playerPosition[i] == Play_With_friends.Ladder_Down_Position[5]) :
                    Play_With_friends.playerPosition[i] = Play_With_friends.Ladder_Up_Position[5]
                elif(Play_With_friends.playerPosition[i] == Play_With_friends.Ladder_Down_Position[6]) :
                    Play_With_friends.playerPosition[i] = Play_With_friends.Ladder_Up_Position[6]
                elif(Play_With_friends.playerPosition[i] == Play_With_friends.Ladder_Down_Position[7]) :
                    Play_With_friends.playerPosition[i] = Play_With_friends.Ladder_Up_Position[7]
            i += 1
        # player position display
        print("\n------------------:::::Player\'s Position:::::------------------ \n")
        speak("Player\'s Position")
        i = 0
        while (i < Play_With_friends.n) :
            self.Count = 1
            if (Play_With_friends.diceScore[i] > 0) :
                print(f"CURRENT :                    {Play_With_friends.Names[i]}  = {Play_With_friends.playerPosition[i]}")
                speak(f"CURRENT :                    {Play_With_friends.Names[i]}  = {Play_With_friends.playerPosition[i]}")
            else :
                print(f"CURRENT :                    {Play_With_friends.Names[i]}  = {Play_With_friends.playerPosition[i]}")
                speak(f"CURRENT :                    {Play_With_friends.Names[i]}  = {Play_With_friends.playerPosition[i]}")
            if (i == Play_With_friends.n - 1) :
                print("------------------------------------------------------------------- ", end ="")
            self.Count += 1
            Play_With_friends.diceScore[i] = 0
            i += 1
    def IsWon(self) :
        i = 0
        while (i < Play_With_friends.n) :
            if (Play_With_friends.playerPosition[i] == Play_With_friends.WONPOINT) :
                print("\n-------------------------WINNER----------------------------------- \n")
                print(f"                          CONGRATS {Play_With_friends.Names[i]}")
                speak(f"CONGRATS {Play_With_friends.Names[i]} you won.")
                print("\n-------------------------WINNER----------------------------------- \n")
                self.flag = 1
                break
            if (self.flag == 1) :
                break
            i += 1

def SnakeAndLadder() :
    print("                 Welcome To SNACK AND LADDER GAME \n-------------------------------------------------------------------\n")
    speak("Welcome To SNACK AND LADDER GAME")
    print("Application Type : Console Game")
    speak("Application Type : Console Game")
    print("Version : 1.0.1 LTS")
    speak("Version : 1.0.1 LTS")
    print("Developer : GHANSHYAM VAJA")
    speak("Developer : GHANSHYAM vaja")
    print("-------------------------------------------------------------------")
    playWith = ' '
    print("\n       1 - play With Computer         2 - play With friends")
    print(" \nEnter Your choice (1 | 2) : ", end ="")
    speak("Enter Your choice")
    speak("1 for play With Computer")
    speak("2 for play With friends")
    playWith = input()
    while (playWith != '1' and playWith != '2') :
        print(" \nEnter valid choice (1 | 2) : ", end ="")
        speak("Enter valid choice")
        speak("1 or 2")
        playWith = input()
    print(" \n::::::::::::::::::::---->WINPOINT : 100<----:::::::::::::::::::: \n")
    speak("WINPOINT 100")
    if (playWith == '1') :
        obj = Play_With_Computer()
        i = 1
        while (obj.flag != 1) :
            if (i == 1) :
                obj.setGame()
                obj.SnakesAndLaddersPosition()
            obj.SnakesAndLaddersPositionPrint()
            if (i == 1) :
                print("\n-------------------::Lets Start The Game::------------------------- ", end ="")
                speak("Lets Start The Game")
            obj.RollDice()
            # obj.PlayerPosition();
            # obj.IsWon();
            i = 2
    else :
        obj2 = Play_With_friends()
        k = 1
        while (obj2.flag != 1) :
            if (k == 1) :
                obj2.setGame()
                obj2.SetPlayer()
                obj2.SnakesAndLaddersPosition()
            obj2.SnakesAndLaddersPositionPrint()
            if (k == 1) :
                print("\n-------------------::Lets Start The Game::------------------------- ", end ="")
                speak("Lets Start The Game")
            obj2.RollDice()
            k = 2