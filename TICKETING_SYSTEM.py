from tkinter import *
import tkinter as tk
from tkcalendar import *
from tkinter import messagebox
import datetime
from datetime import date
import csv
from fpdf import FPDF
#creating sql connector
import mysql.connector
mydb=mysql.connector.connect(host="localhost",user="root",passwd="",database="railway")
mycursor=mydb.cursor()
#Funtion to accept  user login_id and password for authentication	
def ulogin():
    root=tk.Tk()
    root.title("Login screen")
    # setting the windows size 
    root.geometry("600x300")  
    username_var.set("") 
    passw_var.set("")
    def authenticate():
        username=username_entry.get() 
        password=passw_entry.get()
        info4="select * from admin where BINARY adminuser= %s and BINARY password= %s"
        row=[username,password]
        mycursor.execute(info4,row)
        data=mycursor.fetchall() 
        if any(data):
            messagebox.showinfo("Information ", "Admin login successful")
            adlogview=tk.Tk()
            adlogview.title("Admin's screen")
            adlogview.geometry("400x300")     
            realloc_btn=tk.Button(adlogview,text="Reallocate seats in a particular train",font=("bold",16),command=reallocate)
            adviewta_btn= tk.Button(adlogview,text = 'Prepare Chart',font=("bold",16),command =adminviewtr)
            exit_btn=tk.Button(adlogview, text ='Exit',font=("bold",16), command = adlogview.destroy)   

            adviewta_btn.grid(row=4,column=3,sticky=W)
            realloc_btn.grid(row=5,column=3,sticky=W)
            exit_btn.grid(row=6, column=3,sticky=W)
            adlogview.mainloop()        
        else:
            info2="select * from users where BINARY userid= %s and BINARY password= %s"
            row=[username,password]
            mycursor.execute(info2,row)
            data=mycursor.fetchall()
            if not any(data):
                messagebox.showinfo("Information ", "wrong userid or password")
                passw_entry.delete(0,tk.END)
                username_entry.delete(0,tk.END)  
            else:
                messagebox.showinfo("Information ", "Login successful ")
                logview=tk.Tk()
                logview.title("OPTIONS SCREEN")
                logview.geometry("300x300")
                var4=IntVar()
                viewta_btn= tk.Button(logview,text = 'View trains',font=("bold",16),command =view)
                reser_btn=tk.Button(logview,text=" Book a ticket",font=("bold",16),command=book)
                
                cancelatic_btn=Button(logview,text="Cancel my ticket",font=("bold",16),command=cancelatic)
                printetic_btn=Button(logview,text="Print E-Ticket",font=("bold",16),command=eticket)
                exit_btn=tk.Button(logview, text ='Exit',font=("bold",16), command = logview.destroy)
                viewta_btn.grid(row=4,column=3)
                reser_btn.grid(row=5,column=3)
                cancelatic_btn.grid(row=6,column=3)
                printetic_btn.grid(row=7,column=3)
                exit_btn.grid(row=8, column=3)
      
                           
        username_var.set("") 
        passw_var.set("") 
	
    # creating a label for 
    # name using widget Label 
    username_label = tk.Label(root, text ='User ID', font=('calibre',16, 'bold')) 

    # creating a entry for input 
    # name using widget Entry 
    username_entry = tk.Entry(root, textvariable = username_var,font=('calibre',16,'normal')) 
    
    # creating a label for password 
    passw_label = tk.Label(root, text = 'Password', font = ('calibre',16,'bold'))
    passw_entry=tk.Entry(root, textvariable = passw_var, font = ('calibre',16,'normal'), show = '*')
    
    # creating a entry for password
    
    sub_btn=tk.Button(root,text = 'Confirm',font=("bold",16),command = authenticate)

    exit_btn=tk.Button(root, text ='Exit', font=("bold",16),command = root.destroy)

    # placing the label and entry in 
    # the required position using grid method
    
    username_label.grid(row=0,column=0,sticky=W) 
    username_entry.grid(row=0,column=3) 
    passw_label.grid(row=1,column=0,sticky=W) 
    passw_entry.grid(row=1,column=3)
    
    sub_btn.grid(row=4,column=3,sticky=S)
    exit_btn.grid(row=4, column=3,sticky=E)
    root.mainloop()

#Function to create new User Registration     
def createacc():
    
    create=tk.Tk()
    create.title("User Registration window")

    # setting the windows size 
    create.geometry("600x300")
    name_var.set("") 
    passw_var.set("")
    userid_var.set("")
    confirmpasswd_var.set("")
    email_var.set("")
    phone_var.set("")

    # defining a function to accept the user registration details  and validate for unique ID, nonempty ID etc
    def submit(): 
    
        name=name_entry.get()
        userid=userid_entry.get()
        password=passw_entry.get()
        confirmpasswd=confirmpasswd_entry.get()
        email=email_entry.get()
        phone=phone_entry.get()
        nflag=False
        uflag=False
        if len(name)==0 or name.isspace()==True:
            messagebox.showwarning("Warning", "User name cannot be empty")
            nflag=True
        if len(userid)==0 or userid.isspace()==True:
            messagebox.showwarning("Warning", "Userid cannot be empty")
            uflag=True
        
            
        if nflag==False and uflag==False:
        # checking if the userid is unique
            info="select * from users where userid= %s"
            row=[userid]
            mycursor.execute(info,row)
            data=mycursor.fetchall()
            if any(data):
            
                messagebox.showwarning("Warning", "username exists , create with unique username")
                userid_entry.delete(0,tk.END)

                c=messagebox.askokcancel(" User's Option", "Want to continue?")
                    
            else:
                flag=True
            
                if len(password)!=8:
                    messagebox.showwarning("Warning", "please enter the password with only 8 characters")
                    flag=False
                
                elif len(password)==8:
                    ca=0
                    cn=0
                    cc=0
                    for i in password:
                        if i.isalpha()==True:
                            if i.isupper()==True:
                                cc=cc+1
                            ca=ca+1
                        if i.isnumeric()==True:
                            cn=cn+1
                    if ca==0 or cn==0 or cc==0:
                    
                        messagebox.showwarning("Warning", "password must contain 1 capital,and alphanumeric")
                
                        flag=False
                if flag==False:
                    passw_entry.delete(0,tk.END)
                    confirmpasswd_entry.delete(0,tk.END)
                          
                elif password==confirmpasswd:
                    info1="insert into users values(%s, %s, %s, %s, %s, %s)"
                    row=[name,userid,password,confirmpasswd,email,phone]
                    mycursor.execute(info1,row)
                    mydb.commit()
                
                    messagebox.showinfo("Information", "Account created Sucessfully")
                    c=messagebox.askokcancel(" User's Option", "Want to continue?")
                                        
                else:
                    messagebox.showwarning("Warning", "your confirm password is incorrect")
                    confirmpasswd_entry.delete(0,tk.END)
                    passw_entry.delete(0,tk.END)
                    c=messagebox.askokcancel(" User's Option", "Want to continue?")
            
            name_var.set("") 
            passw_var.set("")
            userid_var.set("")
            confirmpasswd_var.set("")
            email_var.set("")
            phone_var.set("")
	

    name_label = tk.Label(create, text = 'Name*',justify=LEFT, font=('calibre', 16, 'bold')) 
    name_entry = tk.Entry(create, textvariable = name_var,font=('calibre',16,'normal'))
    
    passw_label = tk.Label(create, text = 'Password*', font = ('calibre',16,'bold'),justify=LEFT) 
    passw_entry=tk.Entry(create, textvariable = passw_var, font = ('calibre',16,'normal'), show = '*') 

    userid_label = tk.Label(create, text = 'Userid*', font=('calibre', 16, 'bold'),justify=LEFT)
    userid_entry = tk.Entry(create, textvariable = userid_var,font=('calibre',16,'normal'))

    confirmpasswd_label = tk.Label(create, text = 'ConfirmPassword*', font = ('calibre',16,'bold'),justify=LEFT)
    confirmpasswd_entry=tk.Entry(create, textvariable = confirmpasswd_var, font = ('calibre',16,'normal'), show = '*')

    email_label = tk.Label(create, text = 'EMail', font=('calibre', 16, 'bold'),justify=LEFT)
    email_entry= tk.Entry(create, textvariable = email_var,font=('calibre',16,'normal'))

    phone_label = tk.Label(create, text = 'Phone', font=('calibre', 16, 'bold'),justify=LEFT)
    phone_entry= tk.Entry(create, textvariable = phone_var,font=('calibre',16,'normal'))
    req_label=tk.Label(create,text="*:Mandatory fields ,cannot be empty",font=('calibre',10),fg="red",justify=LEFT)

    sub_btn=tk.Button(create,text = 'Submit',font=("bold",16),command = submit,justify=LEFT)

    exit_btn=tk.Button(create, text ='Exit',font=("bold",16),command = create.destroy,justify=RIGHT)

    name_label.grid(row=0,column=0,sticky=W) 
    name_entry.grid(row=0,column=1)
    
    userid_label.grid(row=1,column=0,sticky=W)
    userid_entry.grid(row=1,column=1)
    
    passw_label.grid(row=2,column=0,sticky=W) 
    passw_entry.grid(row=2,column=1)
    
    confirmpasswd_label.grid(row=3,column=0,sticky=W)
    confirmpasswd_entry.grid(row=3,column=1)
    
    email_label.grid(row=4,column=0,sticky=W)
    email_entry.grid(row=4,column=1)
    
    phone_label.grid(row=5,column=0,sticky=W)
    phone_entry.grid(row=5,column=1)
    
    req_label.grid(row=6,column=0,sticky=W)
    
    sub_btn.grid(row=7,column=0,sticky=S)
    exit_btn.grid(row=7, column=1,sticky=S)
 
    create.mainloop()

#Function to View the Train availability based on TRain name and date of Jounrney    
def view():
    viewtr=Tk()
    viewtr.title("View the Train availability")
    viewtr.geometry("400x300")
    def getdates():
        cur_date=datetime.date.today()
        #c=date(int(b[2]),int(b[1]),int(b[0]))
        d=cur_date
        l=[]
        for k in range(30):
            delta=datetime.timedelta(k)
            l.append(d+delta)
        return l
    
    def textprint(q):
        textbar=Tk()
        textbar.title("Train availability")
        S = tk.Scrollbar(textbar)
        T = tk.Text(textbar, height=10, width=80)
        S.pack(side=tk.RIGHT, fill=tk.Y)
        T.pack(side=tk.LEFT, fill=tk.Y)
        
        T.config(font=('calibre',14))
        S.config(command=T.yview)
        T.config(yscrollcommand=S.set)
        for m in q:
            T.insert(tk.END, m)
            T.insert(tk.END,"\n")

    def print_answers():
           #print("Q: {}    A:  {} ",format(tkvarq.get(),  answer_entry.get()))
               tr=tkvarq.get()
               dr=dot.get()
               if tr=="Select the trains" or dr=="Select the date":
                   messagebox.showinfo("Information ", "select both the date and train")
               else:
                   info12="select train_no from trains where train_name= %s"
                   mycursor.execute(info12,[tr])
                   vdata=mycursor.fetchall()
                   for i in vdata:
                       tno=i[0]
                   quote=[]
                   info3="select count(*) from passengers where train_no= %s and date_of_journey= %s and seat_type= %s"
                   inp3=[tno,dr,"2AC"]
                   mycursor.execute(info3,inp3)
                   ac2data=mycursor.fetchall()
                   info14="select count(*) from passengers where train_no= %s and date_of_journey= %s and  seat_type= %s"
                   inp14=[tno,dr,"3AC"]
                   mycursor.execute(info14,inp14)
                   ac3data=mycursor.fetchall()
                   info15="select count(*) from passengers where train_no= %s and date_of_journey= %s and seat_type= %s"
                   inp15=[tno,dr,"SL"]
                   mycursor.execute(info15,inp15)
                   sldata=mycursor.fetchall()
        
                   if not any(ac2data):
                       ac2info=72
                   elif not any(ac3data):
                       ac3info=72
                   elif not any (sldata):
                       slinfo=72
                   else:
                       ac2info=72-ac2data[0][0]
                       ac3info=72-ac3data[0][0]
                       slinfo=72-sldata[0][0]
                   stsav=("SL:",slinfo,"2AC:",ac2info,"3AC:",ac3info)
               
                   qtrdata=("train number:",tno,"date of journey:",dr)
                   quote.append(qtrdata)
                   quote.append(stsav)
                
                   textprint(quote)
                         
           
    dates=getdates()
    info11="select distinct(train_name) from trains"
    mycursor.execute(info11)
    vwtrdata=mycursor.fetchall()
    questions=[]
    for i in vwtrdata:
        for j in i:
            questions=questions+[j]
    
    
    tkvarq = StringVar(viewtr)
    dot=StringVar(viewtr)
    
    tkvarq.set("Select the trains")
    dot.set("Select the date")
    utrain=Label(viewtr,text="Train",font=('calibre', 16, 'bold'))
    Dojourn=Label(viewtr,text="DOJ",font=('calibre', 16, 'bold'))
    questions_menu = OptionMenu(viewtr,tkvarq,*questions)
    questions_menu.config(font=("bold",16))
    dottr_menu=OptionMenu(viewtr,dot,*dates)
    dottr_menu.config(font=("bold",16))
    questions_menu.grid(row=1,column=2)
    Dojourn.grid(row=2,column=1)
    utrain.grid(row=1,column=1)
    dottr_menu.grid(row=2,column=2)
 
     
 
    #Submit button
    submit_button = Button(viewtr, text= "  Check availability  ",font=("bold",16), command = print_answers)
    bye_button = Button (viewtr, text = "  Exit. ",font=("bold",16),command = viewtr.destroy)
    
    submit_button.grid(row=3,column=2)
    bye_button.grid(row=4,column=2)
    lbl = Label(viewtr)
    lbl.grid(row=5,column=2)
 
    viewtr.mainloop()

def  adminviewtr():
    
    adviewtr=Tk()
    adviewtr.title("View the Train occupancy Screen")
    adviewtr.geometry("400x300")

    def textprint(q):
        textbar=Tk()
        textbar.title(" Train-Passengers travelling information")
        S = tk.Scrollbar(textbar)
        T = tk.Text(textbar, height=10, width=80)
        S.pack(side=tk.RIGHT, fill=tk.Y)
        T.pack(side=tk.LEFT, fill=tk.Y)
        T.config(font=('calibre',14))
        S.config(command=T.yview)
        T.config(yscrollcommand=S.set)
        for m in q:
            
            T.insert(tk.END, m)
            T.insert(tk.END,"\n")

    def adgetdates():
        
        cur_date=datetime.date.today()
        d=cur_date
        l=[]
        for k in range(30):
            delta=datetime.timedelta(k)
            l.append(d+delta)
        return l
    
    def adprint_answers():
           
               tr=tkvarq.get()
               dr=dot.get()
               if tr=="Select the trains" or dr=="Select the date":
                   messagebox.showinfo("Information ", "please select the date and train")
               else:
                   
                   info12="select train_no from trains where train_name= %s"
                   mycursor.execute(info12,[tr])
                   vdata=mycursor.fetchall()
                   for i in vdata:
                       tno=i[0]
                   quote=[]
                   chk="select pnr_no,name,age,seat_type,berth from passengers where train_no= %s and date_of_journey= %s and status= %s"
                   row=[tno,dr,"CNF"]
                   mycursor.execute(chk,row)
                   data=mycursor.fetchall()
               
                   if not any (data):
                       notr=messagebox.showinfo("Information", "No passengers available on this particular date")
                                     
                   else:
                       quote=[]
                       admntrdata=("train:",tr,"date of journey:",dr)
                       quote.append(admntrdata)
                       for i in range(len(data)):                  
                             t=data[i]
                             h=["pnr no","name","age","seat type","berth"]
                             q=(h[0],":",t[0],h[1],":",t[1],h[2],":",t[2],h[3],":",t[3],h[4],":",t[4])
                             qr={h[0]:t[0],h[1]:t[1],h[2]:t[2],h[3]:t[3],h[4]:t[4]}
                             #adlbl.config(text=q)
                         
                         
                             quote.append(q)
                         
                       textprint(quote)
    dates=adgetdates()
    questions=[]
    info15="select distinct(train_name) from trains"
    
    mycursor.execute(info15)
    advwtrdata=mycursor.fetchall()
    for i in advwtrdata:
        for j in i:
            questions=questions+[j]

    
    
    tkvarq = StringVar(adviewtr)
    dot=StringVar(adviewtr)
    
    tkvarq.set("Select the trains")
    dot.set("Select the date")
    utrain=Label(adviewtr,text="Train",font=('calibre', 16, 'bold'))
    Dojourn=Label(adviewtr,text="DOJ",font=('calibre', 16, 'bold'))
    questions_menu = OptionMenu(adviewtr,tkvarq,*questions)
    questions_menu.config(font=("bold",16))
    dottr_menu=OptionMenu(adviewtr,dot,*dates)
    dottr_menu.config(font=("bold",16))
    questions_menu.grid(row=1,column=2)
    Dojourn.grid(row=2,column=1)
    utrain.grid(row=1,column=1)
    dottr_menu.grid(row=2,column=2)
 
    #Submit button
    adsubmit_button = Button(adviewtr, text= "Show Chart ",font=("bold",16), command = adprint_answers)
    adbye_button = Button (adviewtr, text = "  Exit. ",font=("bold",16),command = adviewtr.destroy)
    
    adsubmit_button.grid(row=3,column=2)
    adbye_button.grid(row=4,column=2)
    #adlbl = Label(adviewtr)
    #adlbl.grid(row=5,column=2)
 
    adviewtr.mainloop()
    
# Function for  booking Module
def book():
   
    #FUNCTION TO CALCULATE TICKET COST
    def ticketcost(noandseat):
             global total,distancefare,fcost
                          
             #a=noandseat+(seatallocate(noandseat,age),)+(date_entry,)
             frtonoandseat=frto+noandseat
             mycursor.execute("select base_fare,distance from trains where start=(%s) and destination=(%s) and train_no=(%s) and seat_type=(%s)",frtonoandseat)
             rec=mycursor.fetchall()
             base=rec[0][0]
             f=open("D:\\CS PROJECT\\codes and files\\using tkinter\\integrate modules\\fare.csv","r")
             my_reader=csv.reader(f)
             next(my_reader)
             for line in my_reader:
                 if line[0]==str(round(rec[0][1],-1)):
                     if frtonoandseat[3]=="2AC":distancefare=int(line[1])
                     elif frtonoandseat[3]=="3AC":distancefare=int(line[2])
                     elif frtonoandseat[3]=="SL":distancefare=int(line[3])
             f.close()
             if food=="VEG":fcost=100
             elif food=="NONVEG":fcost=120
             else:fcost=0
             cost=distancefare+fcost+base
             if age>57 and sex=="F":cost=0.5*cost
             elif age>59 and sex=="M":cost=0.6*cost
             elif age<6:cost=0
             elif age>=6 and age<=12:cost=0.5*cost
             total=total+cost
             return cost

    #FUNCTION TO DETERMINE THE STATUS OF THE TICKET
    def status(noandseat):
             global date_entry
             noseatdate=noandseat+(date_entry,)
             mycursor.execute("select count(*) from passengers where status!='CAN'and train_no=(%s) and seat_type=(%s) and DATE_OF_JOURNEY=(%s)",noseatdate)
             seatsoccupied=mycursor.fetchall()[0][0]
             if seatsoccupied<72:status="CNF"
             elif seatsoccupied>=72 and seatsoccupied<=79:status="RAC"
             elif seatsoccupied>79 and seatsoccupied<=83:status="WL"
             return status
    def allocateberth(coach,seatno):
        if coach=="2AC":
            if seatno%2==0:
                berth="ub"
            else:
                berth="lb"
        elif coach=="3AC" or coach=="SL":
            if seatno%3==0:
                berth="ub"
            elif seatno%3==1:
                berth="lb"
            else:
                berth="mb"
        return berth

    #FUNCTION TO ALLOCATE SEATS
    def seatallocate(noandseat,age):
         global date_entry
         
         noseatdate=noandseat+(date_entry,)
         
         if noandseat[1]=="3AC" or noandseat[1]=="SL":
            if age>60:
                mycursor.execute("select max(seatno) from passengers where train_no=(%s) and seat_type=(%s) and DATE_OF_JOURNEY=(%s) and age>60",noseatdate)
                L=mycursor.fetchall()
                if L[0][0]==None:seatnum=1
                elif L[0][0]==70:
                       mycursor.execute("select seatno from passengers where status='CAN' and train_no=(%s) and seat_type=(%s) and DATE_OF_JOURNEY=(%s)",noseatdate)
                       F=mycursor.fetchall()
                       if F==None:
                           mycursor.execute("select max(seatno) from passengers where status='CNF' and train_no=(%s) and seat_type=(%s) and DATE_OF_JOURNEY=(%s) and age<60",noseatdate)
                           L=mycursor.fetchall()
                           if L[0][0]==None:seatnum=2
                           else:seatnum=L[0][0]+1
                       else:
                           seatnum=F[0][0]
                           canseat=noseatdate+(seatnum,)
                           mycursor.execute("delete from passengers where status='CAN' and train_no=(%s) and seat_type=(%s) and DATE_OF_JOURNEY=(%s) and seatno=(%s)",canseat)
                else:seatnum=L[0][0]+3
                Flag=True
                while Flag==True:
                        numdate=noseatdate+(seatnum,)
                        mycursor.execute("select count(*) from passengers where status='CNF' and train_no=(%s) and seat_type=(%s) and DATE_OF_JOURNEY=(%s) and seatno=(%s)",numdate)
                        L=mycursor.fetchall()
                        if L[0][0]==1:
                             if seatnum==1 or seatnum%3==1:
                                  seatnum=seatnum+3
                             else:seatnum=seatnum+1
                        else:Flag=False
            else:
                  mycursor.execute("select max(seatno) from passengers where train_no=(%s) and seat_type=(%s) and DATE_OF_JOURNEY=(%s) and age<60",noseatdate)
                  L=mycursor.fetchall()
                  if L[0][0]==None:seatnum=2
                  elif L[0][0]==72:
                       mycursor.execute("select seatno from passengers where status='CAN' and train_no=(%s) and seat_type=(%s) and DATE_OF_JOURNEY=(%s)",noseatdate)
                       F=mycursor.fetchall()
                       if F==None:
                            mycursor.execute("select max(seatno) from passengers where status='CNF' and train_no=(%s) and seat_type=(%s) and DATE_OF_JOURNEY=(%s) and age>60",noseatdate)
                            L=mycursor.fetchall()
                            if L[0][0]==None:seatnum=1
                            else:seatnum=L[0][0]+3
                       else:
                           seatnum=F[0][0]
                           canseat=noseatdate+(seatnum,)
                           mycursor.execute("delete from passengers where status='CAN' and train_no=(%s) and seat_type=(%s) and DATE_OF_JOURNEY=(%s) and seatno=(%s)",canseat)
                  else:
                      seatnum=L[0][0]+1
                      if seatnum%3==1:
                         seatnum=seatnum+1
                  Flag=True
                  while Flag==True:
                       numdate=noseatdate+(seatnum,)
                       mycursor.execute("select count(*) from passengers where status='CNF' and train_no=(%s) and seat_type=(%s) and DATE_OF_JOURNEY=(%s) and seatno=(%s)",numdate)
                       L=mycursor.fetchall()
                       if L[0][0]==1:
                              seatnum=seatnum+1
                       else:Flag=False                              
         if noandseat[1]=="2AC":
                if age>60:
                      mycursor.execute("select max(seatno) from passengers where train_no=(%s) and seat_type=(%s) and DATE_OF_JOURNEY=(%s) and age>60",noseatdate)
                      L=mycursor.fetchall()
                      if L[0][0]==None:seatnum=1
                      elif L[0][0]==70:
                         mycursor.execute("select seatno from passengers where status='CAN' and train_no=(%s) and seat_type=(%s) and DATE_OF_JOURNEY=(%s)",noseatdate)
                         F=mycursor.fetchall()
                         if F==None:
                              mycursor.execute("select max(seatno) from passengers where status='CNF' and train_no=(%s) and seat_type=(%s) and DATE_OF_JOURNEY=(%s) and age<60",noseatdate)
                              L=mycursor.fetchall()
                              if L[0][0]==None:seatnum=2
                              else:seatnum=L[0][0]+2
                         else:
                             seatnum=F[0][0]
                             canseat=noseatdate+(seatnum,)
                             mycursor.execute("delete from passengers where status='CAN' and train_no=(%s) and seat_type=(%s) and DATE_OF_JOURNEY=(%s) and seatno=(%s)",canseat)
                      else:seatnum=L[0][0]+2
                      Flag=True
                      while Flag==True:
                           numdate=noseatdate+(seatnum,)
                           mycursor.execute("select count(*) from passengers where status='CNF' and train_no=(%s) and seat_type=(%s) and DATE_OF_JOURNEY=(%s) and seatno=(%s)",numdate)
                           L=mycursor.fetchall()
                           if L[0][0]==1:
                               seatnum=seatnum+2
                           else:Flag=False
                else:
                     mycursor.execute("select max(seatno) from passengers where train_no=(%s) and seat_type=(%s) and DATE_OF_JOURNEY=(%s) and age<60",noseatdate)
                     L=mycursor.fetchall()
                     if L[0][0]==None:seatnum=2
                     elif L[0][0]==72:
                         mycursor.execute("select seatno from passengers where status='CAN' and train_no=(%s) and seat_type=(%s) and DATE_OF_JOURNEY=(%s)",noseatdate)
                         F=mycursor.fetchall()
                         if F==None:
                           mycursor.execute("select max(seatno) from passengers where status='CNF' and train_no=(%s) and seat_type=(%s) and DATE_OF_JOURNEY=(%s) and age>60",noseatdate)
                           L=mycursor.fetchall()
                           if L[0][0]==None:seatnum=1
                           else:seatnum=L[0][0]+2
                         else:
                             seatnum=F[0][0]
                             canseat=noseatdate+(seatnum,)
                             mycursor.execute("delete from passengers where status='CAN' and train_no=(%s) and seat_type=(%s) and DATE_OF_JOURNEY=(%s) and seatno=(%s)",canseat)
                     else:seatnum=L[0][0]+2
                     Flag=True
                     while Flag==True:
                            numdate=noseatdate+(seatnum,)
                            mycursor.execute("select count(*) from passengers where status='CNF' and train_no=(%s) and seat_type=(%s) and DATE_OF_JOURNEY=(%s) and seatno=(%s)",numdate)
                            L=mycursor.fetchall()
                            if L[0][0]==1:
                                 seatnum=seatnum+2
                            else:Flag=False          
         return seatnum
    #FUNCTION TO GENERATE PNR NUMBER
    def pnrgenerate():
            mycursor.execute("select count(*) from passengers")
            totalno=mycursor.fetchall()
            if totalno[0][0]==0:pnr_no=10000000
            else:
                mycursor.execute("select max(pnr_no) from passengers")
                maxn=mycursor.fetchall()
                pnr_no=maxn[0][0]+1
            return pnr_no
        
    def bookprint(q):
        
        textbar=Tk()
        textbar.title("Passengers Booking details")
        S = tk.Scrollbar(textbar)
        T = tk.Text(textbar, height=10, width=80)
        S.pack(side=tk.RIGHT, fill=tk.Y)
        T.pack(side=tk.LEFT, fill=tk.Y)
        T.config(font=('calibre',14))
        S.config(command=T.yview)
        T.config(yscrollcommand=S.set)
        for m in q:
            T.insert(tk.END, m)
            T.insert(tk.END,"\n")
    
    #FUNCTION TO ADD MORE PASSENGERS
    def addmore():
          global total
          global no_of_p
          no_of_p=no_of_p+1
          btsubmit.configure(state='active')
          btaddmore.configure(state='disable')
          btnomore.configure(state='disable')
          if no_of_p <6 :
               passengerdet(noandseat)
          else:
               messagebox.showinfo("Show info","Sorry. Only 5 tickets can be booked at a time")
               messagebox.showinfo("Booking Screen","Cost of the ticket is %s"%total)

    #FUNCTION TO PRINT BOOKING SUCCESS AND TOTAL COST
    def nomore():
           global total, pnr_no
           global q
           j=[]
           j=j+[pnr_no]
           j=j+[total]
           messagebox.showinfo("Booking Screen","Booking Successful")
           #messagebox.showinfo("Booking Screen","PNR Number & Total Cost %s"%j)
           messagebox.showinfo("Booking Screen","Total Cost is %s"%total)
           bookprint(q)
           
           
           
           window.destroy()

    #FUNCTION TO SUBMIT PASSENGER DETAILS
    def submit_details():
             global name,age,food,sex,frto
             global Listoffam,q
             global pnr_no, frto, noandseat ,date_entry  # added new
             
             
             
             name=(lbnentry.get()).upper()
             sex=clicked.get()
             age=int(lbaentry.get())
             food=clicked1.get()
             if food.upper()=="NO":food=None
             coach=noandseat[1]
             stat=status(noandseat)
             if stat=="CNF":
                seatno=seatallocate(noandseat,age)
                ber=allocateberth(coach,seatno)
             
             elif stat=="RAC" or "WL":seatno=None;ber=None
             P=(pnr_no,noandseat[0],noandseat[1],frto[0],frto[1],name,sex,age,food,seatno,stat,date_entry,ticketcost(noandseat),ber)
             
             Listoffam=Listoffam+list(P)
             q.append(P)
             sql_1= "INSERT INTO passengers (pnr_no,train_no,seat_type,START,DESTINATION,name,sex,age,food,seatno,status,DATE_OF_JOURNEY,cost,berth) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
             mycursor.execute(sql_1,P)
             mydb.commit()
             btsubmit.configure(state='disable')
             btaddmore.configure(state='active')
             btnomore.configure(state='active')
             
    #FUNCTION TO OBTAIN PARTICULARS FROM PASSENGER
    def passengerdet(noandseat):
             global lbnentry,lbaentry,lbsentry,lbfentry
             global clicked,clicked1,clicked2
             opt="Y";i=1;Flag=True
             cal.destroy()
             lb15.destroy()
             frame1.destroy()
             lb5.destroy()
             lb5entry.destroy()
             lb6.destroy()
             lb6entry.destroy()
             btget_date.destroy()
             search_button.destroy()
             bt_chkavail.destroy()
             drop2.destroy()

             lb1.grid(row=3,column=0,sticky="w")
             lb1entry.grid(row=3,column=1,sticky="e")
             lb2.grid(row=6,column=0,sticky="w")
             lb2entry.grid(row=6,column=1,sticky="e")
               
             lbn=tk.Label(master=window,text="NAME :  ",font = "Arial 16 bold")
             lbnentry=tk.Entry(window,font=('Arial',14,"bold"))

             options=["M","F"]
             clicked = tk.StringVar(window)
             clicked.set(options[0])
        
             drop=OptionMenu(window,clicked,*options)
                  
             lbs=tk.Label(master=window,text="SEX :  ",font = "Arial 16 bold")
             lbsentry = tk.Label(window,font=('Arial',14,"bold"))
                 
             lba=tk.Label(master=window,text="AGE : ",font = "Arial 16 bold")
             lbaentry=tk.Entry(window,font=('Arial',14,"bold"))

             options1=["VEG","NONVEG","NO"]

             clicked1=tk.StringVar(window)
             clicked1.set(options1[2])

             drop1=OptionMenu(window,clicked1,*options1)
                   
             lbf=tk.Label(master=window,text="FOOD PREFERENCE : ",font = "Arial 16 bold")
              
             lbn.grid(row=28,column=0,sticky="w")
             lbnentry.grid(row=28,column=1,sticky="e")
             lbs.grid(row=30,column=0,sticky="w")
             drop.grid(row=30,column=1,sticky="e")
                  
             lba.grid(row=32,column=0,sticky="w")
             lbaentry.grid(row=32,column=1,sticky="e")

             lbf.grid(row=34,column=0,sticky="w")
             drop1.grid(row=34,column=1,sticky="e") 
                 
             btsubmit.grid(row=37,column=1)
             btsubmit.config(state='active')
             btaddmore.grid(row=39,column=0)
             btaddmore.config(state='disable')
             btnomore.grid(row=39,column=3)
             btnomore.config(state='disable')
                
             return Listoffam

    #FUNCTION TO CHECK AVAILABILITY OF SEATS
    def availability():
             global pnr_no
             global noandseat
             global frtono,frtonotype,no_of_p
             global date_entry
             no_of_p=0
             Flag=True
             i=1
             pno=lb5entry.get()
             ptype=clicked2.get()
             noandseat=(int(pno),ptype)
             noseatdate=noandseat+(date_entry,)
             mycursor.execute("select count(*) from passengers where STATUS='CNF' AND train_no=(%s) and seat_type=(%s) and DATE_OF_JOURNEY=(%s)",noseatdate)
             L=mycursor.fetchall()
             A=72-L[0][0]
                       
             MsgBox = messagebox.askyesno("Total no of seats is %s"%A,"Do you wish to proceed?")
             if MsgBox == True:
                   pnr_no=pnrgenerate()
                   
                   frtono=tuple(frto+(noandseat[0],));frtonotype=frtono+(noandseat[1],)
                   
                   i=0
                   no_of_p=1
                   Listoffam=passengerdet(noandseat)
                   
                       
             else:
                   messagebox.showinfo("Booking Screen","Thank you")
                   window.destroy()                               
#FUNCTION TO OBTAIN FROM,TO             
    def userinput():
             book_fr=lb1entry.get()
             book_to=lb2entry.get()
             return book_fr,book_to

    #FUNCTION TO CHECK IF BOOKING CAN BE DONE FOR SELECTED DATE
    def advancebooking():
             global frto,date_entry,date2
             frto=userinput()
             lb4.config(text=cal.get_date())
             date_entry=cal.get_date()
             x = datetime.datetime.now()
             year, month, day = map(int, date_entry.split('/'))
             date1 = datetime.date(year, month, day)
             date2=0
             if date1.year == x.year:
                 if date1.month ==  x.month:
                    date2 = date1.day-x.day
                 elif date1.month-x.month == 1:
                    if x.month in (1,3,5,7,8,10,12):
                       date2 = (31-x.day)+date1.day
                    elif x.month in (4,6,9,11):
                       date2 = (30-x.day)+date1.day
                    elif x.month==2 and x.year%4==0:
                       date2 = (29-x.day)+date1.day
                    else:
                       date2 = (28-x.day)+date1.day
             elif date1.year == x.year+1 and x.month==12 and date1.month==1:
                  date2 = (31-x.day)+date1.day      
             else: date2=31
             if date2 <= 30 and date2 >=0:
                  messagebox.showinfo("Booking Screen","You can book a ticket")
             elif date2 < 0:
                  messagebox.showinfo("Booking Screen","Please enter a valid date")
             else:
                  messagebox.showinfo("Booking Screen","Cannot book beyond 30 days")
             search_button.configure(state='active')
             return date_entry
    #FUNCTION TO DISPLAY TRAINS AVAILABLE
    def display_trains(myresult):
             lb1.grid_forget()
             lb1entry.grid_forget()
             lb2.grid_forget()
             lb2entry.grid_forget()
             lb3.grid_forget()
             cal.grid_forget()
             lb4.grid_forget()
             btget_date.grid_forget()
             search_button.grid_forget()
             allowed.grid_forget()
                 
             frame1.grid(row=5,column=0,padx=10)
             lb14=tk.Label(master=frame1,text="Train-no.Train-name           From          To          Class  Dist.Base-Fare",relief="raised")
             lb14.grid(row=6,column=0)
             i = 7
             for x in myresult:
                lb15=tk.Label(master=frame1,text=x,font = "Arial 10 italic")
                lb15.grid(row=i,column=0)
                i=i+1
                      
             lb5.grid(row=23,column=0,sticky="w")
             lb5entry.grid(row=23,column=1,sticky="e")
             lb6.grid(row=30,column=0,sticky="w")
             drop2.grid(row=30,column=1,sticky="e")
             bt_chkavail.grid(row=35,column=4)
    def startdestprint():
        info90="Select start,destination from trains"
        mycursor.execute(info90)
        stde=mycursor.fetchall()
        stdest=[]
        detail=["start | destination"]
        stdest=stdest+detail
        for row in stde:
            stdest=stdest+[row]
        textbar=Tk()
        textbar.title("start destination details")
        S = tk.Scrollbar(textbar)
        T = tk.Text(textbar, height=10, width=80)
        S.pack(side=tk.RIGHT, fill=tk.Y)
        T.pack(side=tk.LEFT, fill=tk.Y)
        T.config(font=('calibre',14))
        S.config(command=T.yview)
        T.config(yscrollcommand=S.set)
        for m in stdest:
            T.insert(tk.END, m)
            T.insert(tk.END,"\n")

    #FUNCTION TO OBTAIN TRAINS AVAILABLE
    def searchtrain():
             srchinfo="select train_no,train_name,start,destination,seat_type,distance,base_fare from trains where start=(%s) and destination=(%s)"
             mycursor.execute(srchinfo,frto)
             myresult = mycursor.fetchall()
             if myresult==[]:
                 messagebox.showinfo("Unavailable","Please enter valid start and destination.")
                 messagebox.showinfo("Information","please click the 'Available Routes 'Button")
                 search_button.configure(state='disable')
                 
             else:
               if date2==0:
                  mycursor.execute("SELECT COUNT(*) FROM trains where start=(%s) and destination=(%s) and timediff(departure,current_time)> 050000",frto)
                  T = mycursor.fetchall()
                  if T[0][0]==0:
                    messagebox.showinfo("Sorry","Booking has to be done atleast 5 hours prior to departure")
                    search_button.configure(state='disable')
               else:
                    display_trains(myresult)
        

    date_entry=""
    pnr_no=0
    noandseat=tuple()
    global Listoffam
    Listoffam=[]
    global total
    total=0
    global q
    q=[]
    
    #frto=("ABC","XYZ")
    window = tk.Tk()
    window.title("Welcome To Ticket Reservation System")

    label=tk.Label(master=window,text="BOOKING SCREEN",font = "Helvetica 25 bold italic",relief="raised")
    label.grid(row=1,column=1)

    lb1=tk.Label(master=window,text="FROM: ",font = "Arial 16 bold")
    lb1.grid(row=3,column=0,sticky="w")
    lb1entry=tk.Entry(window,font=('Arial',14,"bold"))
    lb1entry.grid(row=3,column=1,sticky="e")

    lb2=tk.Label(master=window,text="TO: ",font = "Arial 16 bold")
    lb2.grid(row=6,column=0,sticky="w")
    lb2entry=tk.Entry(window,font=('Arial',14,"bold"))
    lb2entry.grid(row=6,column=1,sticky="e")

    lb3=tk.Label(master=window,text="DATE OF JOURNEY: ",font = "Arial 16 bold")
    lb3.grid(row=9,column=0,sticky="w")

    x = datetime.datetime.now()

    cal = Calendar(window,selectmode='day',date_pattern='yyyy/mm/dd')
    cal.grid(row=15,column=1)

    lb4=tk.Label(window,text="",font = ('Arial',14,"bold"))
    lb4.grid(row=9,column=1,sticky="e")

    btget_date=tk.Button(window,text = "Submit Date Of Journey",font = "Arial 16 bold",command = advancebooking)
    btget_date.grid(row=18,column=4)

    search_button=tk.Button(window,text = "Search Train",font = "Arial 16 bold",command = searchtrain)
    search_button.grid(row=21,column=4)
    search_button.configure(state='disable')
    allowed=tk.Button(window,text = "Available Routes For Booking",font = "Arial 12 bold",command = startdestprint)
    allowed.grid(row=22,column=0,sticky="e")
    
    lb5=tk.Label(master=window,text="ENTER THE PREFERRED TRAIN NUMBER :",font = "Arial 16 bold")
    lb5entry=tk.Entry(window,font=('Arial',14,"bold"))

    options2=["SL","2AC","3AC"]

    clicked2 = tk.StringVar(window)
    clicked2.set(options2[0])

    drop2=tk.OptionMenu(window,clicked2,*options2)
                  
    lb6=tk.Label(master=window,text="ENTER THE PREFERRED CLASS :",font = "Arial 16 bold")
    lb6entry=tk.Entry(window,font=('Arial',14,"bold"))

    frame1=tk.Frame(master=window)
    lb15=tk.Label(master=window,text=" ")

    bt_chkavail=tk.Button(window,text = "Check availabilty of seats",font = "Arial 16 bold",command = availability)
    btsubmit=tk.Button(window,text = "Submit",font = "Arial 16 bold",command = submit_details)

    btaddmore=tk.Button(window,text="add more passengers",font = "Arial 16 bold",command = addmore)
    btnomore=tk.Button(window,text="No more to add",font = "Arial 16 bold",command = nomore)

    window.mainloop()

#Function to print E-Ticket
def eticket():
    etic = Tk()
    etic.title("ETICKET SCREEN")
    etic.geometry("600x200")

    def close_window(): 
        etic.destroy()
    def print_answers():
        
        pnrnum=pnr_entry.get()
        info3="select name,age,berth,seatno,status from passengers where pnr_no= %s and status= %s"
        info4="select train_no,seat_type,pnr_no,date_of_journey from passengers where pnr_no= %s and status= %s"
        info5="select start,destination,departure from trains where train_no= %s"
        canpnr=[pnrnum,"CNF"]
        mycursor.execute(info3,canpnr)
        data=mycursor.fetchall()
        
        paldata=["Name","Age","Berth","SeatNo","Status"]
        if not any(data):
            messagebox.showinfo("INFORMATION","INVALID PNR")
        else:
            
            mycursor.execute(info4,canpnr)
            cmndata=mycursor.fetchall()
            train=cmndata[0][0]
            coach=cmndata[0][1]
            pnr=cmndata[0][2]
            doj=cmndata[0][3]
            t=[train]
            mycursor.execute(info5,t)
            trdata=mycursor.fetchall()
        
            
            board=trdata[0][0]
            dest=trdata[0][1]
            depart=trdata[0][2]
            cmnlist=[train,coach,pnr,doj]
            cmnlists=["Train :",train," Coach :",coach," PNR:",pnr,"Date of Journey:",doj]
            statdata=[" Boarding Station:",board," Destination Station:",dest,"Time of Departure:",depart]
            filename="eticket.txt"
            with open(filename,"w",newline="")as f:
                a=csv.writer(f,delimiter=",")
                a.writerow(cmnlists)
                a.writerow(statdata)
                
                a.writerow(paldata)
                
                a.writerows(data)
                
                messagebox.showinfo("Information","ETicket has been created")
                
            def ticpdf():
                pdf = FPDF() 
                pdf.add_page()
                pdf.set_font("Arial", size = 12)
                pdf.cell(200, 10, txt = "Vidya Mandir Railway Reservation System", ln = 1, align = 'C') 
                pdf.cell(200,10,txt="*****************************************************",ln=2,align="C")
                pdf.cell(200, 10, txt = "Students Project", ln = 3, align = 'C')
                pdf.cell(200,10,txt="*****************************************************",ln=4,align="C")
                
                 
                f = open("eticket.txt", "r") 
                # insert the texts in pdf
                for x in f: 
                    pdf.cell(200, 10, txt = x, ln = 1, align = 'L')
                    pdf.cell(200,10,txt="~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~",ln=1,align="L")

                pdf.output(str(pnr)+"_Eticket.pdf")
            ticpdf()

    tic = Label(etic, text ='Ticket', font = ("bold",20)) 
        
    lblpnr = Label(etic, text ="Enter the PNR number", font = ('calibre', 16, 'bold')) 
        
    pnr_entry = Entry(etic,font=("bold",16), width=30)
        

    submit_button = Button(etic, text= "Submit",font=("bold",16),command = print_answers)
    bye_button = Button (etic, text = "Exit",font=("bold",16), command = close_window)
    tic.grid(row=1,column=1)
    lblpnr.grid(row=2,column=0)
    pnr_entry.grid(row=2,column=1)

    submit_button.grid(row=9,column=0)
    bye_button.grid(row=9,column=1)

#Function to cancel the ticket based on PNR number
def cancelatic():
    ctic = Tk()
    ctic.title("Ticket Cancellation window")
    ctic.geometry("600x200")
            
    def scrollbar(x):
            seat=tk.Tk()
            seat.title("Passenger List Cancellation  window")
            seat.geometry("500x500")
            yscrollbar = Scrollbar(seat) 
            yscrollbar.pack(side = RIGHT, fill = Y)
            label = Label(seat, text = "Select the Passenger whose seat you want to cancel :  ", 
              font = ("Times New Roman", 16),  
              padx = 10, pady = 10)
            label.pack() 
            listbo = Listbox(seat, selectmode = "multiple",  yscrollcommand = yscrollbar.set)
            listbo.config(font="12")
            listbo.pack(padx = 10, pady = 10, expand = YES, fill = "both")
            def select():
                reslist=list()
                seleccion = listbo.curselection()
                if seleccion==():
                    messagebox.showinfo("Information ", "No passenger is selected")
                else:
                    for i in seleccion:
                        entrada = listbo.get(i)
                        reslist.append(entrada)
                    for val in reslist:
                        #print(val)
                        #print(val[0],"is name")
                        pasname=val[0]
                        pnrnum=pnr_entry.get()
                    
                        inscan="insert into cancelled select * from passengers where name= %s and pnr_no= %s"
                        mycursor.execute(inscan,[pasname,pnrnum])
                    
                        info5="update passengers set status='CAN' where name= %s and pnr_no = %s"
                        row=[pasname,pnrnum]
                        mycursor.execute(info5,row)
                        mydb.commit()
                        messagebox.showinfo("Information ", "Ticket sucessfully cancelled")
                    
  
                    
            for each_item in range(len(x)): 
          
                listbo.insert(END, x[each_item]) 
                listbo.itemconfig(each_item, bg = "white")
                    
            yscrollbar.config(command = listbo.yview)
            cancelbtn = Button(seat, text="Cancel the ticket",font=("bold",12), command=select)
            cancexit= Button(seat,text="Exit",font=("bold",12),command=seat.destroy)
            cancelbtn.pack()
            cancexit.pack()
            seat.mainloop()
    
    def close_window(): 
        ctic.destroy()
    def print_answers():
        
        pnrnum=pnr_entry.get()
        info3="select name, train_no,seatno from passengers where pnr_no= %s and status !='CAN'"
        canpnr=[pnrnum]
        mycursor.execute(info3,canpnr)
        data=mycursor.fetchall()
        if not any(data):
                    #print("no passengers with such pnr number")
                    messagebox.showinfo("Information ", "INVALID PNR NUMBER")
                    
        else:
            x=list(data)
            scrollbar(x)

    tic = Label(ctic, text ='CANCEL A TICKET', font = ("bold",20)) 
        
    lblpnr = Label(ctic, text ="Enter pnr number", font = ('calibre', 16, 'bold')) 
        
    pnr_entry = Entry(ctic,font=("bold",16), width=30)
        

    submit_button = Button(ctic, text= "Submit",font=("bold",16),command = print_answers)
    bye_button = Button (ctic, text = "exit",font=("bold",16), command = close_window)
    tic.grid(row=1,column=1)
    lblpnr.grid(row=2,column=0)
    pnr_entry.grid(row=2,column=1)

    submit_button.grid(row=9,column=0)
    bye_button.grid(row=9,column=1)
    
#Function to reallocate the Ticket for senior citizen(s) based on cancellation ticket of Lower berth
def reallocate():
    info7="select name,pnr_no from passengers"
    mycursor.execute(info7)
    chk1=mycursor.fetchall()
    info9="select name,pnr_no from cancelled"
    mycursor.execute(info9)
    chk2=mycursor.fetchall()
    ch=0
    task=False
    while ch<len(chk2):
        rec=chk2[ch]
        #print(rec,"is from cancelled")
        canpnr=rec[1]
        canname=rec[0]
        ch=ch+1
        p=0
        while p <len(chk1):
            prec=chk1[p]
            #print(prec)
            if canpnr==prec[1] and canname==prec[0]:
                info8="update cancelled set status='nb' where name= %s and pnr_no= %s"
                redata=[canname,canpnr]
                mycursor.execute(info8,redata)
                mydb.commit()
            p=p+1
    
    info2="select name,age,seatno,berth,date_of_journey,train_no,pnr_no from passengers"
    mycursor.execute(info2)
    travel=mycursor.fetchall()
    info3="select age,seatno,berth,date_of_journey,train_no,pnr_no,name,status from cancelled"
    mycursor.execute(info3)
    canceltravel=mycursor.fetchall()
    for k in canceltravel:
        cseat=k[1]
        cberth=k[2]
        cdate=k[3]
        ctrain=k[4]
        cpnr=k[5]
        cname=k[6]
        cstatus=k[7]
        for j in travel:
            pname=j[0]
            page=j[1]
            pseat=j[2]
            pberth=j[3]
            pdate=j[4]
            ptrain=j[5]
            ppnr=j[6]
                                   
            if cstatus=="nb": 
                if cberth=="lb":
                    if pdate==cdate and ptrain==ctrain:
                        if page>=60 and pberth!="lb":
                            info4="update passengers set berth= %s ,seatno= %s where name= %s and pnr_no= %s"
                            info5="update passengers set berth= %s , seatno= %s where name= %s and pnr_no= %s"
                            info6="update cancelled set berth= %s , seatno= %s where name= %s and pnr_no= %s"
                            row=[cberth,cseat,pname,ppnr]
                            mycursor.execute(info4,row)
                            mycursor.execute(info5,[pberth,pseat,cname,cpnr])
                            mycursor.execute(info6,[pberth,pseat,cname,cpnr])
                            mydb.commit()
                            task=True
    if task==True:
        messagebox.showinfo("Information ", "Seat(s)are successfully reallocated")
    else:
        messagebox.showinfo("Information ", " No Seat(s)to be reallocated")

#Function to attach School Logo on the Welcome Screen     
def photo():
    bl=Canvas(root,width=1500,height=1500)
    bl.pack()
    myimage=PhotoImage(file='C:\\Users\\Pictures\\project snapsots\\vm logo.png')
    bl.create_image(0,0,anchor=NW,image=myimage)



# MAIN 
root = Tk()
root.title("Welcome Window")
root.geometry("600x400")
root.config(bg="white")

c="Y"
username_var = tk.StringVar()
name_var = tk.StringVar() 
passw_var = tk.StringVar()
userid_var=tk.StringVar()
confirmpasswd_var=tk.StringVar()
email_var=tk.StringVar()
phone_var=tk.StringVar()

bl=Canvas(root,width=120,height=120)
bl.config(bg="white")
bl.pack()
myimage=PhotoImage(file='C:\\Users\\Pictures\\project snapsots\\vidya mandir logo.png')
bl.create_image(10,20,anchor=NW,image=myimage)

    
w = Label(root, text ='Welcome to Vidya Mandir Railway Resevation system', font =('calibre', 16),bg="green",fg="white") 
w.pack() 

menubutton = Menubutton(root, text = "Click here to start", font =('calibre', 16),relief=RAISED,bg="gold") 
	
menubutton.menu = Menu(menubutton) 
menubutton["menu"]= menubutton.menu

var2 = IntVar() 
var3 = IntVar() 
menubutton.menu.add_checkbutton(label = "Create an account", command = createacc)
menubutton.menu.add_checkbutton(label = "Login", command = ulogin) 
menubutton.menu.add_checkbutton(label = "Find Trains ", command = view)
menubutton.menu.add_checkbutton(label = "Quit", command=root.destroy)
exitm_button = Button (root, text = "Exit",font=('calibre', 16),bg="red",fg="white",command = root.destroy)

	
menubutton.pack()
exitm_button.pack(side=BOTTOM)
root.mainloop()

# END OF code 
