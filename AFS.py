"""

Anti-forensic Software
File Encrypt Service
Copyright 2022. sjrjq all rights reserved.

"""

from PyQt5.QtWidgets import *
import sys
import base64
import hashlib
from Cryptodome import Random
from Cryptodome.Cipher import AES
import random
import string

filelist = [None]
n=1024	
rand_str = ""	

for i in range(n):
    rand_str += str(random.choice(string.ascii_letters + string.digits))

ENCRYPT_MESSAGE = "THIS FILE WAS ENCRYPTED BY AFS.. Copyright 2022. sjrjq all rights reserved. "
class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setupUI()

        self.BS = 16

        self.pad = lambda s: s + ( self.BS- len(s.encode('utf-8')) % self.BS) * chr(self.BS - len(s.encode('utf-8')) % self.BS)

        self.unpad = lambda s : s[0:-s[-1]]

        self.key = hashlib.sha256(rand_str.encode()).digest()

       


    def setupUI(self):
        
        self.setGeometry(500,500,500,500)
        self.setWindowTitle("AFS [Open Source]")
 
        self.OnOpenDocument_Button = QPushButton("File Open")
        self.OnOpenDocument_Button.clicked.connect(self.OnOpenDocument)

        self.Button2 = QPushButton("Encrypt")
        self.Button2.clicked.connect(self.letsgo)

        self.label = QLabel()
        self.label.setText("Copyright 2022. sjrjq all rights reserved.")

        layout = QVBoxLayout()
        layout.addWidget(self.OnOpenDocument_Button)
        layout.addWidget(self.Button2)
        layout.addWidget(self.label)
 
        self.setLayout(layout)
 
    def OnOpenDocument(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', "", "All Files(*);; PE files(*.exe)", '/home')
        if fname[0]:
            filelist[0] = fname[0]
        else:
            QMessageBox.about(self, "Warning!", "Please select file.")

    def encrypt( self, raw ):
        raw = self.pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new( self.key, AES.MODE_CFB, iv)
        return base64.b64encode( iv + cipher.encrypt( raw.encode('utf-8') ))

    def encrypt_str( self, raw ):
        return self.encrypt(raw).decode('utf-8')

    def letsgo(self):
        with open(filelist[0], 'rb') as infile:
            s3 = infile.readlines()
            a = self.encrypt_str(str(s3))
            
            with open(filelist[0], 'w') as infile2:
                infile2.write(ENCRYPT_MESSAGE + a)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    app.exec_()