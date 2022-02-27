from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from tkinter import simpledialog
from tkinter import ttk
from datetime import datetime
from datetime import timedelta
import smtplib, ssl
from email.mime.text import MIMEText
import pickle



#____________________________________________________________________________________________________________________________
def send_email(b,c):
    port = 587  
    smtp_server = "smtp.gmail.com"
    sender_email = 'ethexislibrary@gmail.com'
    receiver_email = b
    password = 'jvscbo23'
    message = f"""Χαίρεται!!!! Όπως έχουμε καταγράψει, φαίνεται πως δανείστηκες το βιβλίο:{c} πριν αρκετό καιρό.\n
Θα είμασταν χαρούμενοι αν επικοινωνούσες μαζί μας για το σημείο της μελέτης σου, ώστε να μας βοηθήσεις στη διαχείριση των βιβλίων
    """


    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, port) as server:
        try:
            server.ehlo()  
            server.starttls(context=context)
            server.ehlo()  
            server.login(sender_email, password)
            msg = MIMEText(message,)
            msg['Body'] = message
            msg['Subject'] = 'Δανεισμός Βιβλίου'
            msg['To'] = receiver_email
            server.sendmail(sender_email, receiver_email, msg.as_string())
        except:
            print(2)
        


def time(x):
    if x != '':
        return int(x/5)+62
    
def choose(L, a, b):
    if a.get():
        for i in L:
            if i.name == b.get().strip(' '):
                return i
    else:
        for i in L:
            if i.title == b.get().strip(' '):
                return i

def findindex(indexyouwant , L):
    for i in enumerate(list(L)):
        if i[1] == indexyouwant:
            return i[0]
        
def uppersm(a):
    if a[0].isalpha():
        return f'{a[0].upper()}'+f'{a[0].lower()}'
    else:
        return f'{a[0]}'

def writedatabase(a, L):
    f = open(a, 'wb')
    pickle.dump(L, f)
    f.close()
        
def exists(a,b,L):
    if (a in L) and (b in L):
        for i in Con.L:
            if a.get() == i.name and b.get() == i.title:
                return False
    return True
    
def createwin(a,b,c,d,e,f,g,h):
    conlook = ConLook(a,e)
    conlook.v1.set(a)
    conlook.v2.set(b)
    conlook.v3.set(c)
    conlook.v4.set(d)
    conlook.v5.set(e)
    conlook.v6.set(f)
    conlook.v7.set(g)
    conlook.e1.insert(0, a)
    conlook.e2.insert(0, b)
    conlook.e3.insert(0, c)
    conlook.e4.insert(0, d)
    conlook.e5.insert(0, e)
    conlook.e6.insert(0, f)
    conlook.e7.insert(0, g)
    conlook.e8.insert(0, h)
    conlook.master.withdraw()

def choosecont(cont,L):
    for i in L:
        if cont == i.__repr__():
            return i
#____________________________________________________________________________________________________________________________
class Con():
    L = []
    def __init__(self, name, phone1, phone2, email, title, author, day,
                 month, year, pages='', sndml = True):
        self.name = name
        self.phone1 = phone1
        self.phone2 = phone2
        self.email = email
        self.title = title
        self.author = author
        self.day = day
        self.month = month
        self.year = year
        self.pages = pages
        self.sndml = sndml
        Con.L.append(self)
        Con.L.sort()

    def __repr__(self):
        return f'{self.name}-{self.title}'

    def __lt__(self, other):
        return (self.name).lower() < (other.name).lower()

    def dl(self):
        del Con.L[findindex(self, Con.L)] 
        del self 
#____________________________________________________________________________________________________________________________    


#main παραθυρο----------------------------------------------------------------

class main_w():
    def __init__(self, toplevel):
        self.toplevel = toplevel
        self.toplevel.geometry('790x490+500+150')
        self.toplevel.resizable(False, True)
        self.toplevel.title('{:>100s}'.format('EhexisLib'))
        self.toplevel.iconbitmap('world-book-day.ico')
        self.f = Frame(self.toplevel, bg = '#9590DE', height = 1000, width = 790)
        self.f.place(x = 0, y = 0)
        im3 = PhotoImage(file = '+.GIF')
        self.im3 = im3
        im4 = PhotoImage(file = 'glass.GIF')
        self.im4 = im4
        self.b1 = Button(self.f, bg = '#9590DE',bd = 1, image = self.im4, command = self.openConLook2)
        self.b1.place(x =690,y =5)
        self.b2 = Button(self.f, bg = '#9590DE', bd = 1,
                         image = self.im3,command = self.crconlook, height = 90, width =90)
        self.b2.place(x=690,y=380)
        self.search = Entry(self.toplevel, width = 51, bd = 3, font = ('Helvetica', 18))
        self.search.place(x = 10, y = 10)
        self.search.bind('<Any-KeyPress>', self.crlist)
        self.search.bind('<Return>',self.openConLook2ev)
        self.f.bind('<Button-1>', self.nofocus)

        self.lab = Label(self.toplevel, text = 'Search by:', font = ('Helvetica', 12,'bold'),
                         bg = '#aba7e5')
        self.lab.place(x= 690,y=82)
        s = ttk.Style(self.toplevel)
        s.configure('TRadiobutton', background = '#aba7e5', font = ('Helvetica', 10,'bold'))
        self.a = IntVar()
        self.r1 = ttk.Radiobutton(self.toplevel,
                                  text = 'Name', variable = self.a, value= 1, command = self.crlist2)
        self.r2 = ttk.Radiobutton(self.toplevel,
                                  text = 'Book', variable = self.a, value = 0,command = self.crlist2)
        self.r1.place(x=690, y = 110)
        self.r2.place(x=690, y = 130)
        self.r1.invoke()
        
    def nofocus(self, event):
        self.f.focus_force()

    def crlist(self,event):
        self.search.after(1, self.crlist2)

    def crlist2(self):
        global Lbox
        try:
            Lbox.destroy()
            del Lbox
        except:
            pass
        Lis = []
        l = len(self.search.get().strip(' '))
        for i in Con.L:
            if self.search.get() != '':
                if self.a.get():
                    if self.search.get().strip(' ').replace(' ','').isalpha():
                        if self.search.get().lower().strip(' ').replace(' ','') == i.name[0:l].lower().replace(' ',''):
                            Lis.append(i)
                    else:
                        if self.search.get().strip(' ') == i.name[0:l]:
                            Lis.append(i)
                else:
                    if self.search.get().strip(' ').replace(' ','').isalpha():
                        if self.search.get().lower().strip(' ').replace(' ','') == i.title[0:l].lower().replace(' ',''):
                            Lis.append(i)
                    else:
                        if self.search.get().strip(' ') == i.title[0:l]:
                            Lis.append(i)                    
        if len(Lis) != 0 and l != 0:
            Lis.sort()
            Lbox = Listbox(self.f , activestyle = 'none', width = 74,
                           bd = 0, font = ('Helvetica', 13, 'bold'))
            for i in Lis:
                Lbox.insert(END, i)
            Lbox.lift()
            Lbox.place(x = 11, y = 43)
            Lbox.bind('<Double-Button-1>', self.openConLook)
            Lbox.bind('<Return>', self.openConLook)            

    def notebookcreator(self):
        global nbook
        try:
            nbook.destroy()
            del nbook
        except:
            pass
        st = ttk.Style(self.toplevel)
        st.configure('TNotebook', tabposition = 'wn', background = '#9590DE')
        nbook = ttk.Notebook(self.f, height = 415, width = 650)
        i = 0
        if len(Con.L) != 0:
            Lis = [Con.L[0]]
            while i < len(Con.L)-1:
                if uppersm(Con.L[i].__repr__()) == uppersm(Con.L[i+1].__repr__()):
                    Lis.append(Con.L[i+1].__repr__())
                    i += 1
                    continue
                else:
                    f = Frame(self.f, bg = '#aca7e4')
                    yScrl = Scrollbar(f, orient = VERTICAL)
                    yScrl.pack(fill = BOTH, expand = True, side = RIGHT)
                    Libox = Listbox(f, yscrollcommand = yScrl.set,
                        font=("Helvetica",10,'bold'), bg="#aca7e4", width=100, activestyle = 'none')                    
                    b = uppersm(f'{Con.L[i].__repr__()}')
                    Libox.pack(fill = BOTH, expand = True, side = LEFT)
                    yScrl['command'] = Libox.yview
                    nbook.add(f, text = b)
                    for j in Lis:
                        Libox.insert(END, j)
                        Libox.bind('<Double-Button-1>', self.openConLook)
                        Libox.bind('<Return>', self.openConLook) 
                    Lis = [Con.L[i+1].__repr__()]
                    i += 1
                    continue
            f = Frame(self.f, bg = '#aca7e4')
            yScrl = Scrollbar(f, orient = VERTICAL)
            yScrl.pack(fill = BOTH, expand = True, side = RIGHT)
            Libox = Listbox(f, yscrollcommand = yScrl.set,
                font=("Helvetica",10,'bold'), bg="#aca7e4", width=100, activestyle = 'none')
            b = uppersm(f'{Con.L[i].__repr__()}')
            Libox.pack(fill = BOTH, expand = True, side = LEFT)
            yScrl['command'] = Libox.yview
            nbook.add(f, text = b)
            for j in Lis:
                Libox.insert(END, j)
            Libox.bind('<Double-Button-1>', self.openConLook)
            Libox.bind('<Return>', self.openConLook) 
            nbook.place(x=3,y=55)      
    
    def crconlook(self):
        self.toplevel.withdraw()
        conlook = ConLook()
        conlook.top.withdraw()
        conlook.master.deiconify()

    def openConLook(self, event):
        Listbox = event.widget
        if Listbox.size() != 0:
            i = choosecont(Listbox.get(Listbox.curselection()[0]), Con.L)
            createwin(i.name, i.phone1, i.phone2, i.email, i.title,
                      i.author, f'{i.day}/{i.month}/{i.year}', i.pages)
            self.toplevel.withdraw()


    def openConLook2ev(self, event):
        self.openConLook2()
        
    def openConLook2(self):
            i = choose(Con.L, self.a, self.search)
            if i != None:
                createwin(i.name, i.phone1, i.phone2, i.email, i.title,
                          i.author, f'{i.day}/{i.month}/{i.year}', i.pages)
                self.toplevel.withdraw()
            else:
                messagebox.showwarning('Unknown contact', 'Contact not found!', parent = self.toplevel) 
        
#===============================================================================
class ConLook(Con):
    L = []
    def __init__(self, name = '', title = ''):
        # Παραθυρο προβολης
        self.name = name
        self.title = title
        im_pencil = PhotoImage(file = 'pencil.GIF')
        self.im_pencil = im_pencil
        im_check = PhotoImage(file = 'check.GIF')
        self.im_check = im_check
        im_x = PhotoImage(file = 'x.GIF')
        self.im_x = im_x
        self.top = Toplevel()
        self.top.resizable(False, False)
        self.top.geometry('600x500+500+100')
        self.top.title('{:>80s}'.format('EhexisLib'))
        self.top.iconbitmap('world-book-day.ico')
        self.top.bind('<Destroy>', self.delayclose)
        self.f = Frame(self.top, bg = '#9590DE', height =  500,width = 600)
        self.f.pack(anchor = E)                     

        self.l1 = Label(self.f, text = 'Name:    ', bg = '#7871d5', fg = '#000000', font = ('Helvetica', 18, 'bold'))
        self.l2 = Label(self.f,  text = 'Phone 1:', bg = '#7871d5', fg = '#000000', font = ('Helvetica', 18, 'bold'))
        self.l3 = Label(self.f,  text = 'Phone 2:', bg = '#7871d5', fg = '#000000', font = ('Helvetica', 18, 'bold'))
        self.l4 = Label(self.f,  text = 'Email:    ', bg = '#7871d5', fg = '#000000', font = ('Helvetica', 18, 'bold'))
        self.l5 = Label(self.f,  text = 'Book:    ', bg = '#7871d5', fg = '#000000', font = ('Helvetica', 18, 'bold'))
        self.l6 = Label(self.f,  text = 'Author: ', bg = '#7871d5', fg = '#000000', font = ('Helvetica', 18, 'bold'))
        self.l7 = Label(self.f,  text = 'Date:     ', bg = '#7871d5', fg = '#000000', font = ('Helvetica', 18, 'bold'))

        self.l1.place(x = 20, y = 10)
        self.l2.place(x = 20, y = 60)
        self.l3.place(x = 20, y = 110)
        self.l4.place(x = 20, y = 160)
        self.l5.place(x = 20, y= 260)
        self.l6.place(x = 20, y = 310)
        self.l7.place(x = 20, y  = 360)

        
        self.v1 = StringVar()
        self.v2 = StringVar()
        self.v3 = StringVar()
        self.v4 = StringVar()
        self.v5 = StringVar()
        self.v6 = StringVar()
        self.v7 = StringVar()
        
        self.L1 = Label(self.f, textvariable = self.v1, bg = '#9590DE',
                        fg = 'black', font = ('Arial', 13), wraplength = '350')         
        self.L2 = Label(self.f, textvariable = self.v2, bg = '#9590DE',
                        fg = 'black', font = ('Arial', 13), wraplength = '350')
        self.L3 = Label(self.f, textvariable = self.v3, bg = '#9590DE',
                        fg = 'black', font = ('Arial', 13), wraplength = '350')
        self.L4 = Label(self.f, textvariable = self.v4, bg = '#9590DE',
                        fg = 'black', font = ('Arial', 13), wraplength = '350')
        self.L5 = Label(self.f, textvariable = self.v5, bg = '#9590DE',
                        fg = 'black', font = ('Arial', 13), wraplength = '350')
        self.L6 = Label(self.f, textvariable = self.v6, bg = '#9590DE',
                        fg = 'black', font = ('Arial', 13), wraplength = '350')
        self.L7 = Label(self.f, textvariable = self.v7, bg = '#9590DE',
                        fg = 'black', font = ('Arial', 13), wraplength = '350')
        
        self.L1.place(x = 130, y = 15)        
        self.L2.place(x = 130, y = 65)
        self.L3.place(x = 130, y = 115)
        self.L4.place(x = 130, y = 165)
        self.L5.place(x = 130, y = 265)
        self.L6.place(x = 130, y = 315)
        self.L7.place(x = 130, y = 365)
        self.v1.set('')      

        self.b_pencil = Button(self.f,image=im_pencil,
                height=100,
                width=100,command=self.openpencil)
        self.b_pencil.place(x = 486, y = 5)
        
        im_bin = PhotoImage(file = 'bin.GIF')
        self.im_bin = im_bin
        self.b_bin = Button(self.f, image = im_bin, height = 100,
                            width = 100, command = self.delete)
        self.b_bin.place(x = 486, y = 350)

        im_back2 = PhotoImage(file = 'back2.GIF')
        self.im_back2 = im_back2
        self.b_back2 = Button(self.f, image = im_back2, bd = 1, height = 50, width = 100, command = self.close)
        self.b_back2.place(x = 5 , y = 425)
       
# επεξεργασια των στοιχείων=========================================
        self.master = Toplevel()
        self.master.bind('<Destroy>', self.delayclose)
        self.master.resizable(False, False)
        self.master.geometry('500x500+600+50')
        self.master.title('{:>70s}'.format('EhexisLib'))
        self.master.iconbitmap('world-book-day.ico')
        
        self.f2 = Frame(self.master, bg = '#9590DE',
        height =  600,width = 350)
        self.f2.pack(fill = BOTH, expand = 1 )
        
#Ετικέτες---------------------------------------------------------------------------------------------
        l1 = Label(self.f2, text = 'Name:    ', bg = '#6159ce',
        bd = 4,relief = RIDGE, fg = 'black', font = ('Helvetica',18,'bold'))
        
        l2 = Label(self.f2, text = 'Phone 1:', bg = '#6159ce',bd = 4,relief = RIDGE,
        fg = 'black', font = ('Helvetica',18,'bold'))
        
        l3 = Label(self.f2, text = 'Phone 2:', bg = '#6159ce',bd = 4,relief = RIDGE,
        fg = 'black', font = ('Helvetica',18,'bold'))
        
        l4 = Label(self.f2, text = 'Email:    ', bg = '#6159ce',bd = 4,relief = RIDGE,
        fg = 'black', font = ('Helvetica',18,'bold'))
        
        l5 = Label(self.f2, text = 'Book:    ', bg = '#6159ce',bd = 4,relief = RIDGE,
        fg = 'black', font = ('Helvetica',18,'bold'))
        
        l6 = Label(self.f2, text = 'Author: ', bg = '#6159ce',bd = 4,relief = RIDGE,
        fg = 'black', font = ('Helvetica',18,'bold'))

        l7 = Label(self.f2, text = 'Date:     ', bg = '#6159ce',bd = 4,relief = RIDGE,
        fg = 'black', font = ('Helvetica',18,'bold'))

        l8 = Label(self.f2, text = 'Pages:', bg = '#6159ce',bd = 0,relief = RIDGE,
        fg = 'black', font = ('Helvetica',14,'bold'))
        
        l1.place(x = 0, y= 0)
        l2.place(x = 0, y= 50)
        l3.place(x = 0, y= 100)
        l4.place(x = 0, y= 150)
        l5.place(x = 0, y= 250)
        l8.place(x = 0, y= 290)
        l6.place(x = 0, y = 330)
        l7.place(x = 0, y= 380)
        
#---------------------------------------------------------------------------------------
#εισαγωγές κειμένου------------------------------------------------------------------
        self.e1 = Entry(self.f2, bd = 3 , relief = SUNKEN, width = 40, font = ('Halvetica',12),
        bg = 'white', fg = 'black', insertbackground = 'black')
        
        self.e2 = Entry(self.f2, bd = 3 , relief = SUNKEN, width = 40, font = ('Halvetica',12),
        bg = 'white', fg = 'black', insertbackground = 'black')
        
        self.e3 = Entry(self.f2, bd = 3 , relief = SUNKEN, width = 40, font = ('Halvetica',12),
        bg = 'white', fg = 'black', insertbackground = 'black')
        
        self.e4 = Entry(self.f2, bd = 3 , relief = SUNKEN, width = 40, font = ('Halvetica',12),
        bg = 'white', fg = 'black', insertbackground = 'black')
        
        self.e5 = Entry(self.f2, bd = 3 , relief = SUNKEN, width = 40, font = ('Halvetica',12),
        bg = 'white', fg = 'black', insertbackground = 'black')

        self.e8 = Entry(self.f2, bd = 1 , relief = SUNKEN, width = 4, font = ('Halvetica',10),
        bg = 'white', fg = 'black', insertbackground = 'black')        
        
        self.e6 = Entry(self.f2, bd = 3 , relief = SUNKEN, width = 40, font = ('Halvetica',12),
        bg = 'white', fg = 'black', insertbackground = 'black')

        self.e7 = Entry(self.f2, bd = 3 , relief = SUNKEN, width = 10, font = ('Halvetica',12),
        bg = 'white', fg = 'black', insertbackground = 'black')

        
        self.e1.place(x = 120, y = 5)
        self.e2.place(x = 120, y = 55)
        self.e3.place(x = 120, y = 105)
        self.e4.place(x = 120, y = 155)
        self.e5.place(x = 120, y = 255)
        self.e6.place(x = 120, y = 335)
        self.e7.place(x = 120, y = 385)
        self.e8.place(x = 70, y = 293)
#----------------------------------------------------------------------------------------------------------
#κουμπιά---------------------------------------------------------------------------------------------------
        self.b_x = Button(self.f2,image=self.im_x,height=59,width=59,
        bg='#f4e7c9',command=self.cancel)
        self.b_x.place(x = 275, y = 425)
        self.master.bind('<Escape>', self.invkb_x)


        self.b_check = Button(self.f2,image=self.im_check,height=59,width=59,
        bg='#f4e7c9',command=self.save)
        self.b_check.place(x = 175, y = 425)
        self.e1.bind('<Return>', self.invkb_chck)
        self.e2.bind('<Return>', self.invkb_chck)
        self.e3.bind('<Return>', self.invkb_chck)
        self.e4.bind('<Return>', self.invkb_chck)
        self.e5.bind('<Return>', self.invkb_chck)
        self.e6.bind('<Return>', self.invkb_chck)
        self.e7.bind('<Return>', self.invkb_chck)
        self.e8.bind('<Return>', self.invkb_chck)
        
#--------------------------------------------------------------------------------------------------------
#συναρτήσεις---------------------------------------------------------------------------------------------   
            
    def invkb_chck(self, event):
        self.b_check.invoke()
        
    def invkb_x(self, event):
        self.b_x.invoke()

    def delete(self):
        self.b_pencil.config(state = DISABLED)
        self.b_bin.config(state = DISABLED)
        self.b_back2.config(state = DISABLED)
        if messagebox.askyesno('Delete Contact', 'Are you sure you want to delete the contact?', parent = self.f2):
            choosecont(self.__repr__(), Con.L).dl()
            appwin.notebookcreator()
            self.top.destroy()
            self.master.destroy()
            writedatabase('Contacts.txt', Con.L)
            appwin.toplevel.deiconify()
            del self
        else:
            self.b_pencil.config(state = NORMAL)
            self.b_bin.config(state = NORMAL)
            self.b_back2.config(state = NORMAL)           
            
    def delayclose(self, event):
        appwin.toplevel.after(1, self.close)
    
    def close(self):
        self.master.destroy()
        self.top.destroy()
        del self
        appwin.toplevel.deiconify()
        appwin.crlist2()
            
    def save(self):
        a = 0
        L = []
        for i in ([self.e1,self.v1],[self.e2,self.v2],
                  [self.e3,self.v3],[self.e4,self.v4],[self.e5,self.v5],
                 [self.e6,self.v6],[self.e7,self.v7]):
            if i[0].get() != i[1].get():
                a += 1
                L.append(i)
        if a != 0 :
            if messagebox.askyesno('Save Contact', 'Save?', parent = self.f2):
                if self.e1.get() != '' and self.e5.get() != '':
                    if  exists(self.e1, self.e5, L):
                        if self.e7.get().count('/') == 2:
                            L1 = self.e7.get().split('/')
                            Ls = [i.lstrip('0') for i in L1]
                            try:
                                datetime(int(Ls[2]),int(Ls[1]),int(Ls[0]))
                                for j in L:
                                    j[1].set(j[0].get())
                                try:
                                    choosecont(self.__repr__(), Con.L).dl()
                                except:
                                    pass
                                if self.e8.get().lstrip('-').isdigit():
                                    con = Con(self.v1.get(), self.v2.get(),
                                              self.v3.get(), self.v4.get(), self.v5.get(),
                                            self.v6.get(), int(Ls[0]), int(Ls[1]), int(Ls[2]),
                                              int(self.e8.get()))
                                    self.top.deiconify()
                                    self.master.withdraw()
                                    self.name = self.v1.get()
                                    self.ltitle = self.v5.get()
                                    appwin.crlist2()
                                    appwin.notebookcreator()
                                    writedatabase('Contacts.txt', Con.L)
                                              
                                elif self.e8.get() == '':
                                    con = Con(self.v1.get(), self.v2.get(),
                                        self.v3.get(), self.v4.get(), self.v5.get(),
                                        self.v6.get(), int(Ls[0]), int(Ls[1]), int(Ls[2]))
                                    self.top.deiconify()
                                    self.master.withdraw()
                                    self.name = self.v1.get()
                                    self.title = self.v5.get()
                                    appwin.crlist2()
                                    appwin.notebookcreator()
                                    writedatabase('Contacts.txt', Con.L)

                                else:
                                    messagebox.showwarning('Pages?', 'Number of pages is natural.\n Leave it empty if is is unknown.', parent = self.f2) 
                            except:
                                messagebox.showwarning('Wrong Date',"That's not a date (dd/mm/yyyy)", parent = self.f2) 

                        else:
                           messagebox.showwarning('Wrong Date', "Date should be:\n dd/mm/yyyy", parent = self.f2)
                    else:
                        messagebox.showwarning('Contact exists', "Contact seems to exists, please alter the name", parent = self.f2)
                        self.e1.focus_set()
                else:
                    messagebox.showwarning('Required entries', 'Name and Book are necessary.', parent = self.f2)
        else:
            self.master.withdraw()
            self.top.deiconify()                       
     
            
    def openpencil(self):
        self.top.withdraw()
        self.master.deiconify()

 
    def cancel(self):        
        if messagebox.askyesno('Cancel Contact', 'Cancel?', parent = self.f2):
            if self.v1.get() != '':
                self.master.withdraw()
                self.top.deiconify()
                for i in ([self.e1,self.v1],[self.e2,self.v2],
                  [self.e3,self.v3],[self.e4,self.v4],[self.e5,self.v5],
                          [self.e6,self.v6], [self.e7,self.v7]):
                    i[0].delete(0, END)
                    i[0].insert(1,i[1].get())
                self.top.deiconify()
                self.master.withdraw()
            else:                
                self.top.destroy()
                self.master.destroy()
                del self              
                appwin.toplevel.deiconify()
        


if __name__ == '__main__':
    root = Tk()
    appwin = main_w(root)
    b = datetime.now()
    try:
        f = open('Contacts.txt', 'rb')
        Con.L = pickle.load(f)
        Con.L.sort()
        f.close()
        for i in Con.L:
            if i.pages != '':        
                a = time(i.pages)
                c = datetime.now() - timedelta(a)
                if datetime(i.year, i.month, i.day)<=datetime(c.year, c.month, c.day) and i.sndml:
                    send_email(i.email, i.title)
                    i.sndml = False
                    writedatabase('Contacts.txt', Con.L)
                if datetime(i.year, i.month, i.day)<=datetime(c.year, c.month, c.day)-timedelta(7):
                    if messagebox.askyesno('Returning books',
                                           f'{i.name} has kept the book {i.title}\n of {i.author} for too long.\n Have you communicated?',
                                           parent = root):
                        if messagebox.askyesno('Returning books', 'Is the book back?', parent = root):
                            i.dl()
                            writedatabase('Contacts.txt', Con.L)                        
                        else:
                            days = simpledialog.askinteger('Days', 'In how much will be the book returned?\n(days)', parent=root)                     
                            if days==None:
                                i.pages = ''
                            else:
                                i.day,i.month,i.year = b.day,b.month,b.year
                                i.pages = 5*days - 310
                                i.sndml = True
                                writedatabase('Contacts.txt', Con.L)                                                        
                    else:
                        messagebox.showinfo('Try to communicate', f'Name:{i.name}\nPhone(s):{i.phone1},{i.phone2}\ne-mail:{i.email}',parent = root)
                        i.day,i.month,i.year = b.day,b.month,b.year
                        i.pages = -310
                        i.sndml = True
                        writedatabase('Contacts.txt', Con.L)                    
        appwin.notebookcreator()
            
    except:
        pass
    root.mainloop()
    

    
 
