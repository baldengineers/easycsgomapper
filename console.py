from PySide.QtCore import *
from PySide.QtGui import *
import webbrowser

class Console(QDialog):
    def __init__(self, parent):
        super(Console, self).__init__(parent)
        self.parent = parent
        
        self.setWindowTitle("Developer Console")
        self.desc = 'Developer console for The Mapper version r %s. Current commands are: print <variable>, help, restart, exit, func <function>, wiki, py <python function>.\n' %(self.parent.VERSION)

        self.prev_text = QTextEdit("<Bald Engineers Developer Console>")
        self.prev_text.setText(self.desc)
        self.prev_text.setReadOnly(True)
        
        self.curr_text = QLineEdit()
        self.curr_text_btn = QPushButton("Enter")
        self.curr_text_btn.clicked.connect(self.console_enter)
        
        self.curr_text_layout = QHBoxLayout()
        self.curr_text_layout.addWidget(self.curr_text)
        self.curr_text_layout.addWidget(self.curr_text_btn)
        
        self.console_form = QFormLayout()
        self.console_form.addRow(self.prev_text)
        self.console_form.addRow(self.curr_text_layout)
        
        self.setLayout(self.console_form)
        self.show()

    def console_enter(self):        
        command = ""
        char_num = 0
        text = self.curr_text.displayText()
        text_prefix = text + " --> "
        
        command = text.split()[0]
        
        try:
            value = text.split()[1]
        except IndexError:
            value = ""

        if command == "print":

            try:
                new_text = text_prefix + str(eval(value))
            except Exception as e:
                new_text = text_prefix + str(e)

        elif command == "help":
            new_text = text_prefix + self.desc

        elif command == "exit":
            self.parent.close_application()
            
        elif command == "restart":
            self.parent.close_application(True)

        elif command == "pootis":
            new_text = '<img src="icons/thedoobs.jpg">'

        elif command == "sterries" or command == "jerries":
            new_text = text_prefix + "Gimme all those berries, berries, berries!"
            

        elif command == "sideshow":
            new_text = ''
            self.sideshow()
        elif command == "func":
            try:
                eval("self.parent."+value + "()")
                new_text = text_prefix + "Function "+value+" has been run."
            except Exception as e:
                new_text = text_prefix + str(e)

        elif command == "wiki":
            try:
                webbrowser.open("http://github.com/baldengineers/easytf2_mapper/wiki")
                new_text = text_prefix + "Wiki has been opened in your default browser"
            except Exception as e:
                print(str(e))
                
        elif command == "py":
            try:
                new_text = text_prefix + str(eval(value))
            except Exception as e:
                new_text = text_prefix + str(e)
        else:
            new_text = text_prefix + "\"" + command + "\" is not a valid command"

        self.prev_text.append(new_text)
        self.curr_text.setText("")

    def sideshow(self):
        self.gif("icons/sideshow.gif", (350,262,154,103), "SIDESHOW", "icons/ss.ico")

    def heavy(self):
        self.gif("icons/heavy.gif", (350,262,150,99), "DANCE HEAVY DANCE!")

    def gif(self, file, geo, title, icon="icons\icon.ico"):
        self.gif = QLabel()
        movie = QMovie(file)
        self.gif.setMovie(movie)
        self.gif.setGeometry(geo[0],geo[1],geo[2],geo[3])
        self.gif.setWindowTitle(title)
        self.gif.setWindowIcon(QIcon(icon))
        self.gif.show()

        movie.start()
