from optparse import Values
from tkinter import*
from PIL import Image,ImageTk
from tkinter import ttk
import random
import mysql.connector
from tkinter import messagebox

class Current_Holdings_Zerodha:
    def __init__(self,root):
        self.root=root
        self.root.title("navaservices2020@gmail.com")
        self.root.geometry("1360x770+0+0")#1100x420+425+230

        #====================right side img=============================880,325
        img1=Image.open(r"C:\Users\navna\Music\Nava Services\iaf-full-width.jpg")
        img1=img1.resize((880,470),Image.ANTIALIAS)
        self.photoimg1=ImageTk.PhotoImage(img1)

        lblimg=Label(self.root,image=self.photoimg1,bd=0,relief=RIDGE)
        lblimg.place(x=0,y=0,width=880,height=470)

        img2=Image.open(r"C:\Users\navna\Music\Nava Services\fd-piggy.png")
        img2=img2.resize((470,400),Image.ANTIALIAS)
        self.photoimg2=ImageTk.PhotoImage(img2)

        lblimg=Label(self.root,image=self.photoimg2,bd=0,relief=RIDGE)
        lblimg.place(x=880,y=325,width=470,height=400)

        #=================Title======================

        lbl_title=Label(self.root,text="Zerodha Dashboard", font=("times new roman",16,"bold"),bg="white",fg="royalblue",bd=4,relief=RIDGE)
        lbl_title.place(x=880,y=0,width=490,height=40) # width=1295

        
        #================Variables==================
        self.var_serial_no=StringVar()
        self.var_company_name=StringVar()
        self.var_shares=IntVar()
        self.var_avg_price=DoubleVar()
        self.var_investment=DoubleVar()
        self.var_total_investment=DoubleVar()

        #================lebel frame===================

        labelframeleft=LabelFrame(self.root,bd=2,relief=RIDGE,text="Order Details",font=("times new roman",12,"bold"),padx=2)
        labelframeleft.place(x=880,y=45,width=440,height=280)#width=400 y=35 height=440

        #===============lables and entries=================
        #Serial No

        lbl_cust_ref=Label(labelframeleft,text="Serial No:-",font=("arial",11),padx=2,pady=6)
        lbl_cust_ref.grid(row=0,column=0,sticky=W)

        txtref=ttk.Entry(labelframeleft,width=30,textvariable=self.var_serial_no,font=("arial",11,"bold"))
        txtref.grid(row=0,column=1)#textvariable=self.var_cust_no,

        #Company Name

        lbl_cust_ref=Label(labelframeleft,text="Company Name:-",font=("arial",11),padx=2,pady=6)
        lbl_cust_ref.grid(row=1,column=0,sticky=W)

        txtname=ttk.Entry(labelframeleft,width=30,textvariable=self.var_company_name,font=("arial",11,"bold"))
        txtname.grid(row=1,column=1)#textvariable=self.var_cust_name,

        #Shares

        lbl_cust_ref=Label(labelframeleft,text="Shares:-",font=("arial",11),padx=2,pady=6)
        lbl_cust_ref.grid(row=2,column=0,sticky=W)

        txtmob=ttk.Entry(labelframeleft,width=30,textvariable=self.var_shares,font=("arial",11,"bold"))
        txtmob.grid(row=2,column=1)#textvariable=self.var_mobile,

        #Avg Price

        lbl_cust_ref=Label(labelframeleft,text="Avg Price:-",font=("arial",11),padx=2,pady=6)
        lbl_cust_ref.grid(row=3,column=0,sticky=W)

        txtemail=ttk.Entry(labelframeleft,width=30,textvariable=self.var_avg_price,font=("arial",11,"bold"))
        txtemail.grid(row=3,column=1) #textvariable=self.var_email,

        #Investment

        lbl_cust_ref=Label(labelframeleft,text="Investment:-",font=("arial",11),padx=2,pady=6)
        lbl_cust_ref.grid(row=4,column=0,sticky=W)

        txtid=ttk.Entry(labelframeleft,width=30,textvariable=self.var_investment,font=("arial",11,"bold"))
        txtid.grid(row=4,column=1)#textvariable=self.var_id_number,

        #Total  Investment
        lbl_total_investment=Label(labelframeleft,text="Total Investment:-",font=("arial",11),padx=2,pady=6)
        lbl_total_investment.grid(row=5,column=0,sticky=W)

        txttotal_investment=ttk.Entry(labelframeleft,width=30,textvariable=self.var_total_investment,font=("arial",11,"bold"))
        txttotal_investment.grid(row=5,column=1,sticky=W)

        #=====================btn==============================
        btn_frame=Frame(labelframeleft,bd=2,relief=RIDGE)
        btn_frame.place(x=0,y=200,width=410,height=50) #height=25

        btn_add=Button(btn_frame,text="Buy",command=self.add_stocks,font=("arial",11),bg="green",fg="white",width=10) #,"bold"
        btn_add.grid(row=0,column=0,padx=1)#command=self.add_stocks,

        btn_update=Button(btn_frame,text="Update",command=self.update,font=("arial",11),bg="royalblue",fg="white",width=10) #,"bold"
        btn_update.grid(row=0,column=1,padx=1)#command=self.update,

        btn_delete=Button(btn_frame,text="Sell",command=self.Sell,font=("arial",11),bg="red",fg="white",width=10) #,"bold"
        btn_delete.grid(row=0,column=2,padx=1)#command=self.Sell,

        btn_reset=Button(btn_frame,text="Reset",command=self.reset,font=("arial",11),bg="dark orange",fg="white",width=10) #,"bold"
        btn_reset.grid(row=0,column=3,padx=1)#command=self.reset,


        #=================holdings table frame============================

        Table_frame=LabelFrame(self.root,bd=2,relief=RIDGE,text="Zerodha Holding Details And Search System",font=("times new roman",12,"bold"),padx=2)
        Table_frame.place(x=0,y=470,width=880,height=280) 
        #labelframeleft.place(x=5,y=35,width=380,height=470)


        labelSearchBy=Label(Table_frame,text="Search By:",bg="royalblue",fg="black",font=("arial",10,"bold"))
        labelSearchBy.grid(row=0,column=0,sticky=W,padx=2)

        self.search_var=StringVar()
        combo_search=ttk.Combobox(Table_frame,textvariable=self.search_var,font=("arial",10,"bold"),width=12,state="readonly")
        combo_search["value"]=("Serial","Company")
        combo_search.current(0)
        combo_search.grid(row=0,column=1,padx=2)

        self.txt_search=StringVar()
        txtSearch=ttk.Entry(Table_frame,width=30,textvariable=self.txt_search,font=("arial",10,"bold"))
        txtSearch.grid(row=0,column=2,padx=2)#textvariable=self.txt_search,

        btn_search=Button(Table_frame,text="Search",command=self.search,font=("arial",10,"bold"),bg="green",fg="white",width=15)
        btn_search.grid(row=0,column=3,padx=1)#command=self.search,

        btn_Showall=Button(Table_frame,text="Show All",command=self.fetch_data,font=("arial",10,"bold"),bg="dark orange",fg="white",width=15)
        btn_Showall.grid(row=0,column=4,padx=1)#command=self.fetch_data,

        btn_Showall=Button(Table_frame,text="Total Investment",command=self.total,font=("arial",10,"bold"),bg="royalblue",fg="white",width=15)
        btn_Showall.grid(row=0,column=5,padx=1)#command=self.total,

        #=================show data table===============

        detail_table=Frame(Table_frame,bd=2,relief=RIDGE)
        detail_table.place(x=0,y=30,width=880,height=180) #width=860

        scroll_x=ttk.Scrollbar(detail_table,orient=HORIZONTAL)
        scroll_y=ttk.Scrollbar(detail_table,orient=VERTICAL)

        self.Holding_Details_Table=ttk.Treeview(detail_table,column=("serial","company","shares","avg_price","investment"),xscrollcommand=scroll_x.set,yscrollcommand=scroll_y.set)
        scroll_x.pack(side=BOTTOM,fill=X)
        scroll_y.pack(side=RIGHT,fill=Y)

        scroll_x.config(command=self.Holding_Details_Table.xview)
        scroll_y.config(command=self.Holding_Details_Table.yview)

        self.Holding_Details_Table.heading("serial",text="Serial No")
        self.Holding_Details_Table.heading("company",text="Company Name")
        self.Holding_Details_Table.heading("shares",text="Shares")
        self.Holding_Details_Table.heading("avg_price",text="Average Price")
        self.Holding_Details_Table.heading("investment",text="Investment")

        self.Holding_Details_Table["show"]="headings"

        self.Holding_Details_Table.column("serial",width=100)
        self.Holding_Details_Table.column("company",width=100)
        self.Holding_Details_Table.column("shares",width=100)
        self.Holding_Details_Table.column("avg_price",width=100)
        self.Holding_Details_Table.column("investment",width=100)

        self.Holding_Details_Table.pack(fill=BOTH,expand=1)
        self.Holding_Details_Table.bind("<ButtonRelease-1>",self.get_cursor)
        self.fetch_data()

    def add_stocks(self):
        if self.var_company_name.get()=="" or self.var_shares.get()=="":
            messagebox.showerror("Error","All fields are required",parent=self.root)
        else:
            try:
                conn=mysql.connector.connect(host="localhost",username="root",password="MySQL$2022",database="nava_services")
                my_cursor=conn.cursor()
                my_cursor.execute("insert into zerodha values(%s,%s,%s,%s,%s)",(
                                                                                                self.var_serial_no.get(),
                                                                                                self.var_company_name.get(),
                                                                                                self.var_shares.get(),
                                                                                                self.var_avg_price.get(),
                                                                                                self.var_investment.get()
                                                                                            ))


                conn.commit()
                self.fetch_data()
                conn.close()
                messagebox.showinfo("Success","Stock has been added",parent=self.root)

            except Exception as es:
                messagebox.showwarning("Warning",f"Something went wrong:{str(es)}",parent=self.root)

    def fetch_data(self):
        conn=mysql.connector.connect(host="localhost",username="root",password="MySQL$2022",database="nava_services")
        my_cursor=conn.cursor()
        my_cursor.execute("select * from zerodha")
        rows=my_cursor.fetchall()
        if len(rows)!=0:
            self.Holding_Details_Table.delete(*self.Holding_Details_Table.get_children())
            for i in rows:
                self.Holding_Details_Table.insert("",END,values=i)
            conn.commit()
        conn.close()

    def get_cursor(self,event=""):
        cursor_row=self.Holding_Details_Table.focus()
        content=self.Holding_Details_Table.item(cursor_row)
        row=content["values"]

        self.var_serial_no.set(row[0]),
        self.var_company_name.set(row[1]),
        self.var_shares.set(row[2]),
        self.var_avg_price.set(row[3]),
        self.var_investment.set(row[4])

    def update(self):
        if self.var_serial_no.get()=="":
            messagebox.showerror("Error","Please enter serial number",parent=self.root)

        else:
            conn=mysql.connector.connect(host="localhost",username="root",password="MySQL$2022",database="nava_services")
            my_cursor=conn.cursor()
            my_cursor.execute("update zerodha set Company=%s,Shares=%s,AvgPrice=%s,Investment=%s where Serial=%s",(
                                                                                                                    self.var_company_name.get(),
                                                                                                                    self.var_shares.get(),
                                                                                                                    self.var_avg_price.get(),
                                                                                                                    self.var_investment.get(),
                                                                                                                    self.var_serial_no.get()
                                                                                                                    ))
            conn.commit()
            self.fetch_data()
            conn.close()
            messagebox.showinfo("Update","Holding details has been updated successfully",parent=self.root)

    
    def Sell(self):
        Sell=messagebox.askyesno("navaservices2020@gmail.com","Do you want sell this stock",parent=self.root)
        if Sell>0:
            conn=mysql.connector.connect(host="localhost",username="root",password="MySQL$2022",database="nava_services")
            my_cursor=conn.cursor()
            query="delete from zerodha where Serial=%s"
            value=(self.var_serial_no.get(),)
            my_cursor.execute(query,value)
        else:
            if not Sell:
                return
        conn.commit()
        self.fetch_data()
        conn.close()

    def reset(self):
        self.var_serial_no.set(""),
        self.var_company_name.set(""),
        self.var_shares.set(""),
        self.var_avg_price.set(""),
        self.var_investment.set("")
        self.var_total_investment.set("")


    def search(self):
        conn=mysql.connector.connect(host="localhost",username="root",password="MySQL$2022",database="nava_services")
        my_cursor=conn.cursor()

        my_cursor.execute("select * from zerodha where "+str(self.search_var.get())+" LIKE '%"+str(self.txt_search.get())+"%'")
        rows=my_cursor.fetchall()
        if len (rows)!=0:
            self.Holding_Details_Table.delete(*self.Holding_Details_Table.get_children())
            for i in rows:
                self.Holding_Details_Table.insert("",END,values=i)
            conn.commit()
        conn.close()

    def total(self):
        conn=mysql.connector.connect(host="localhost",username="root",password="MySQL$2022",database="nava_services")
        my_cursor=conn.cursor()
        my_cursor.execute("select round(SUM(Investment),2) from zerodha")
        row=my_cursor.fetchone()
        self.var_total_investment.set(row)



if __name__ == "__main__":
    root=Tk()
    obj=Current_Holdings_Zerodha(root)
    root.mainloop()