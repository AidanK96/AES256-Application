# -*- coding: utf-8 -*-
#Imports
import tkinter as tk 
from tkinter import *
from Crypto.Cipher import AES
import os
import hashlib
from Crypto.Util.Padding import pad
from Crypto.Util.Padding import unpad
from tkinter.filedialog import askopenfilename
from tkinter import simpledialog
import ctypes 
from tkinter import filedialog
import shutil
###########################################################################################################################################################################################################################
BLOCK_SIZE = 65536 #Block size initialisation to 64kb
IV = '16 bit IV 16 bit' #16 bit initialisation vector
file1 = hashlib.sha1() 

    
#Function for encrypting folders
def encryptFolder():
     folder_encrypt = filedialog.askdirectory()                                                     #Creates a dialog box, selected folder is passed to variable
     if folder_encrypt:                                                                             #If the user has selected a folder to encrypt
           dirName = simpledialog.askstring("Dirname", "Enter Dirname", parent=win)                 #Creates a dialog box for the user to enter the dirname for the encrypted folder to be saved as, passes it to a variable
           shutil.make_archive(dirName, 'zip', folder_encrypt)                                      #Creates a temporary zip file of the directory/folder
     else:
         ctypes.windll.user32.MessageBoxW(0, "Invalid Folder", "Error", 1)                          #Error handling for if the user does not select anything
         return
   
     if dirName: #If the user has entered a directory name
        password = simpledialog.askstring("Password", "Enter Password", parent=win)                 #Takes a password from the dialog box
        password = password.encode() 
        key = hashlib.sha256(password).digest()                                                     #Creates a 256bit key from the digest of the encoded password
     else:
         ctypes.windll.user32.MessageBoxW(0, "Invalid Name", "Error", 1)
         return
     #Reads folder/directory
     with open(dirName+'.zip', 'rb') as f:                                    
        fb = f.read(BLOCK_SIZE)                                         
        while len(fb) > 0:                                              
            file1.update(fb)                                            
            fb = f.read(BLOCK_SIZE)                                     
     #Folder encryption    
     with open(dirName+'.zip','rb') as f:
        origional_file= f.read()
        objEnc = AES.new(key, AES.MODE_CBC, IV=bytes(IV, encoding='utf-8'))
        ciphertext = objEnc.encrypt(pad(origional_file, AES.block_size))
     #Saving encrypted folder as .enc and removing temporary .zip file
     with open(dirName+'.enc', 'wb') as wf:                                   
        wf.write(ciphertext)          
     os.remove(dirName+'.zip')
    
#Function for encrypting files
def encrypt():
    
     fileEncrypt = askopenfilename(title="Select File To Encrypt", filetypes=[("All Files", "*.*")])    #Creates a dialog box, selected file is passed to variable
     if fileEncrypt: #If the user has selected a file to encrypt
        password = simpledialog.askstring("Password", "Enter Password", parent=win) 
        password = password.encode()
        key = hashlib.sha256(password).digest()
     else:
         ctypes.windll.user32.MessageBoxW(0, "Invalid File", "Error", 1)                                 #If no file is selected error
         return
         
     #Reads file to be encrypted
     with open(fileEncrypt,'rb') as f:                                                                   #opens file to be encrypted in bytes
        fb = f.read(BLOCK_SIZE)                                                                      
        while len(fb) > 0:                                              
            file1.update(fb)                                            
            fb = f.read(BLOCK_SIZE)                                     
     #Encrypts the file chosen by the user      
     with open(fileEncrypt,'rb') as f:
        origional_file= f.read()
        objEnc = AES.new(key, AES.MODE_CBC, IV=bytes(IV, encoding='utf-8'))                              #objectEncrypt aes encryption method
        ciphertext = objEnc.encrypt(pad(origional_file, AES.block_size))                             
     fileName = simpledialog.askstring("File Name", "Enter New Filename",parent=win)  
     #Writes the encrypted file with the name chosen by the user
     with open(fileName+'.enc','wb') as wf:                                   
        wf.write(ciphertext)             

#Function for decrypting files and folders
def decrypt():
    #Select file or folder to decrypt
    fileDecrypt = askopenfilename(title="Select File/Folder To Decrypt", filetypes=[("All Files", "*.*")])
    if fileDecrypt:                                                                                      #If the user selects a file to decrypt enter password, if the password does not match decryption will fail
        password = simpledialog.askstring("Password", "Enter Password", parent=win) 
        password = password.encode()
        key = hashlib.sha256(password).digest()
    else:
        ctypes.windll.user32.MessageBoxW(0, "Invalid File", "Error", 1)                                 #If no file is selected error
        return
        
    #Opens the decrypted file, begins decryption
    with open(fileDecrypt,'rb') as rf:                                                                  #read bytes as read file
        ciphertext= rf.read()                                                                           #encrypted file =  read file.read
        objDec = AES.new(key, AES.MODE_CBC, IV=bytes(IV, encoding='utf-8'))                             #object decrypt = new aes object
        ciphertext = unpad(objDec.decrypt(ciphertext), AES.block_size)                                  #unpadding and decryption method
    fileName = simpledialog.askstring("File Name", "Enter New Filename", parent=win)                    #Asks for the decrpted file/folders name(folders must be saved as .zip)
    #Creates decrypted file
    with open(fileName,'wb') as wrf:        
         wrf.write(ciphertext) 
         with open(fileName,'rb') as qrf:                    
            qrfb = qrf.read(BLOCK_SIZE)                                                                 #reads by block size                             
            while len(qrfb) > 0:                                                                        #while greater than 0 keep reading block size                          
               file1.update(qrfb)                                                                       #updates file1 with new blocksize                            
               qrfb = qrf.read(BLOCK_SIZE)                                                              #reads next block
    os.remove(fileDecrypt)                                                                              #removes encrypted file
#######################################################################################################################################################################################################################      
#Tkinter GUI
win = tk.Tk()
#FAQ Wwindow
def helps():
    top = Toplevel()
    top.title("FAQ")
    top.minsize(width=300, height=250)
    top.maxsize(width=300, height=250)
    text = Label(top, text="For instructions on the use of the application  \n and further help consult the user guide located \n in the application folder")
    text.place(x=25, y=25)
#Main window
win.title("AES256 Encryption") #Title of the main window
menubar = Menu(win) #Creates the menubar for the main window
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Quit", command=win.destroy)
menubar.add_cascade(label="File", menu=filemenu)
optionmenu = Menu(menubar, tearoff=0)
optionmenu.add_command(label="Help",command=helps)
menubar.add_cascade(label="Options",menu=optionmenu)

#The buttons for the main window
action = tk.Button(win, text="Encrypt Folder",command=encryptFolder).place(relx=0.35, rely=0.10, height=50, width=150)
action = tk.Button(win, text="Encrypt",command=encrypt).place(relx=0.35, rely=0.25, height=50, width=150)
action = tk.Button(win, text="Decrypt File/Folder",command=decrypt).place(relx=0.35, rely=0.40, height=50, width=150)
action = tk.Button(win, text="FAQ",command=helps).place(relx=0.35,rely=0.55, height=50, width=150)
action = tk.Button(win, text="Exit",command=win.destroy).place(relx=0.35, rely=0.70, height=50, width=150)

#sizing features of the main window
win.minsize(width=500,height=500)
win.maxsize(width=500,height=500)
win.iconbitmap('Logo.ico')

win.config(menu=menubar)
win.mainloop()
