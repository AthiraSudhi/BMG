from flask import Flask, render_template, request, redirect,session
from DBConnection import Db

app = Flask(__name__)
app.secret_key="abc"


@app.route('/',methods=['get'])
def login():
    db = Db()
    res = db.select("select * from books")
    return render_template("index.html",data=res)


# MODULE ADMIN

@app.route('/log',methods=['get'])
def log():

    return render_template("admin/login_temp.html",)

@app.route('/login_in',methods=['post'])
def login_in():
    name=request.form['na']
    psd=request.form['ps']
    db=Db()
    log=db.selectOne("select * from login where Username='"+name+"' and Password='"+psd+"' ")

    if log is not None:
        if log['Usertype']== 'admin':
            session['lg'] = "lin"
            return '<script>alert("login successfully");window.location="/adminhome"</script>'
        elif log['Usertype']== 'store':
            session['lid']=log['login_id']
            session['lg']="lin"
            return '<script>alert("login successfully");window.location="/storehome"</script>'
        elif log['Usertype']=='user':
            session['lid']=log['login_id']
            session['lg']="lin"
            return '<script>alert("Login Successfully");window.location="/userhome"</script>'
        else:
            return '<script>alert("invalid");window.location="/log"</script>'

    else:
        return '<script>alert("no such user");window.location="/log"</script>'


@app.route('/adminhome',methods=['get'])
def adminhome():
    if session['lg']!="lin":
        return'<script>alert("please login  first");window.location="/log"</script>'
    return render_template("admin/index.html")


@app.route('/viewstore',methods=['get'])
def viewstore():
    if session['lg']!="lin":
        return'<script>alert("please login  first");window.location="/log"</script>'
    session["head"]="View Stores"
    db = Db()
    frm = db.select("select * from store,login where store.store_id=login.login_id and Usertype='pending'")
    return render_template("admin/viewstore.html",data=frm)



@app.route('/approvedstore',methods=['get'])
def approvedstore():
    if session['lg'] != "lin":
        return '<script>alert("please login  first");window.location="/log"</script>'
    session["head"]="View Approved Stores"
    db=Db()
    approved=db.select("select * from store,login where store.store_id=login.login_id and Usertype='store'")
    return render_template("admin/viewapprovedstore.html",data=approved)


@app.route('/approved/<bid>')
def approved(bid):
    if session['lg'] != "lin":
        return '<script>alert("please login  first");window.location="/log"</script>'
    db=Db()
    db.update("update login set Usertype='store' where login_id='"+bid+"' ")
    return '<script>alert("Approved");window.location="/viewstore"</script>'



@app.route('/rejectstore/<bid>')
def rejectstore(bid):
    if session['lg'] != "lin":
        return '<script>alert("please login  first");window.location="/log"</script>'
    db=Db()
    db.delete("delete from login where login_id='"+bid+"'")
    db.delete("delete from store where store_id='"+bid+"'")
    return '<script>alert("ok");window.location="/viewstore"</script>'


@app.route('/viewcomplaints',methods=['get'])
def compaints():
    if session['lg'] != "lin":
        return '<script>alert("please login  first");window.location="/log"</script>'
    session["head"]="View Complaints"
    db=Db()
    re=db.select("select * from complaints,users where complaints.userid=users.userid")
    return render_template("admin/viewcomplaint.html",data=re)



@app.route('/reply/<rid>',methods=['get'])
def reply(rid):
    if session['lg'] != "lin":
        return '<script>alert("please login  first");window.location="/log"</script>'
    session["head"]="Reply"
    db=Db()
    rep=db.selectOne("select * from complaints where cmpid='"+rid+"'")
    return render_template("admin/reply.html",data=rep,rid=rid)



@app.route('/updatereply/<rid>',methods=['post'])
def updatereply(rid):
    if session['lg'] != "lin":
        return '<script>alert("please login  first");window.location="/log"</script>'
    re=request.form['reply']
    db=Db()
    db.update("update complaints set reply='"+re+"',replyDate=curdate() where cmpid='"+rid+"' ")
    return '<script>alert("Update Reply");window.location="/viewcomplaints"</script>'



@app.route('/viewreviews',methods=['get'])
def viewreviews():
    session["head"]="View Reviews"
    db=Db()
    review=db.select("select * from reviews,users where reviews.userid=users.userid")
    return render_template("/admin/review.html",data=review)


@app.route('/viewusers',methods=['get'])
def viewusers():
    if session['lg'] != "lin":
        return '<script>alert("please login  first");window.location="/log"</script>'
    session["head"]="View Users"
    db=Db()
    user=db.select("select * from users")
    return render_template("admin/viewuser.html",data=user)




@app.route('/adminpass',methods=['get'])
def adminpass():
    if session['lg'] != "lin":
        return '<script>alert("please login  first");window.location="/log"</script>'
    session["head"]="Change Password"
    return render_template("admin/password.html")


@app.route('/adminpassword',methods=['post'])
def adminpassword():
    currentpass = request.form['cupass']
    newpass=request.form['nepass']
    confirmpass=request.form['copass']

    db = Db()
    res=db.selectOne("select * from login where Password='"+currentpass+"' and Usertype='admin'")
    if res is not None:
        if newpass == confirmpass:
            db.update("update login set Password='"+confirmpass+"' where Usertype='admin'")
            return '<script>alert("Password changed Successfully");window.location="/adminhome"</script>'
        else:
            return '<script>alert("Mismatch Password");window.location="/adminpass"</script>'
    else:
        return '<script>alert("Incorrect Password");window.location="/adminpass"</script>'




# MODULE STORE



@app.route('/storegister',methods=['get'])
def storegister():
    return render_template("storeRegistration.html")

@app.route('/registore',methods=['get'])
def registore():
    session["head"]="Store Registration"
    return render_template("store/storeregister.html")

@app.route('/storegistration',methods=['post'])
def storegistration():
    sname=request.form['sname']
    place=request.form['splace']
    email=request.form['email']
    phn=request.form['phn']
    img=request.files['img']
    password=request.form['pas']
    import datetime
    dt=datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    img.save(r"C:\Users\athir\PycharmProjects\BookMangement\static\image\\" + dt + '.jpg')
    path="/static/image/" + dt + '.jpg'
    db=Db()
    em= db.selectOne("select * from login WHERE Username='"+email+"'")
    if em is not None:
        return '<script>alert("Email already exits");window.location="/storegister"</script>'
    else:
        res=db.insert("insert into login(Username,Password,Usertype) VALUES ('"+email+"','"+password+"','pending')")
        db.insert("insert into store(store_id,storename,place,email,phonenumber,Image) VALUES ('"+str(res)+"','"+sname+"','"+place+"','"+email+"','"+phn+"','"+path+"')")
        return'<script>alert("Store Added Successfully");window.location="/log"</script>'


@app.route('/storehome',methods=['get'])
def storehome():
    return render_template("store/index.html")


@app.route('/addbook',methods=['get'])
def addbook():
    if session['lg'] != "lin":
        return '<script>alert("please login  first");window.location="/log"</script>'
    session["head"]="Add Books"
    return render_template("store/addbook.html")


@app.route('/addbooks',methods=['post'])
def addbooks():
    if session['lg'] != "lin":
        return '<script>alert("please login  first");window.location="/log"</script>'
    bname=request.form['bname']
    price=request.form['price']
    catgry=request.form['category']
    author=request.form['author']
    img=request.files['img']
    import datetime
    dt=datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    img.save(r"C:\Users\athir\PycharmProjects\BookMangement\static\image\\" + dt + '.jpg')
    path="/static/image/" + dt + '.jpg'
    db=Db()
    db.insert("insert into books(bookname,price,category,author,image,storeid) VALUES ('"+bname+"','"+price+"','"+catgry+"','"+author+"','"+path+"','"+str(session['lid'])+"')")
    return '<script>alert("Book Added Successfully");window.location="/storehome"</script>'



@app.route('/viewbook',methods=['get'])
def viewbook():
    if session['lg'] != "lin":
        return '<script>alert("please login  first");window.location="/log"</script>'
    session["head"]="View Books"
    db=Db()
    bk=db.select("select * from books where storeid='"+str(session['lid'])+"'")
    return render_template("store/viewbook.html",data=bk)


@app.route('/editbook/<bid>',methods=['get'])
def editbook(bid):
    if session['lg'] != "lin":
        return '<script>alert("please login  first");window.location="/log"</script>'
    session["head"]="Edit Book"
    db=Db()
    bok=db.selectOne("select * from books where bookid='"+bid+"'")
    return render_template("store/editbook.html",data=bok,bid=bid)

@app.route('/editbooks/<bid>',methods=['post'])
def editbooks(bid):
    if session['lg'] != "lin":
        return '<script>alert("please login  first");window.location="/log"</script>'
    bname = request.form['bname']
    price = request.form['price']
    catgry = request.form['category']
    author = request.form['author']
    img = request.files['img']
    import datetime
    dt = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    img.save(r"C:\Users\athir\PycharmProjects\BookMangement\static\image\\" + dt + '.jpg')
    path = "/static/image/" + dt + '.jpg'
    db=Db()
    if request.files!="":
        if img.filename!="":
            db.update("update books set bookname='"+bname+"',price='"+price+"',category='"+catgry+"',author='"+author+"',image='"+path+"' where bookid='"+bid+"'")
            return '<script>alert("Updated Successfully");window.location="/viewbook"</script>'
        else:
            db.update( "update books set bookname='"+bname+"',price='"+price+"',category='"+catgry+"',author='"+author+"' where bookid='"+bid+"'")
            return '<script>alert("Updated Successfully");window.location="/viewbook"</script>'
    else:
        db.update("update books set bookname='"+bname+"',price='"+price+"',category='"+catgry+"',author='"+author+"' where bookid='"+bid+"'")
        return '<script>alert("Updated Successfully");window.location="/viewbook"</script>'


@app.route('/delbook/<bid>')
def delbook(bid):
    if session['lg'] != "lin":
        return '<script>alert("please login  first");window.location="/log"</script>'
    db=Db()
    db.delete("delete from books where bookid='"+bid+"'")
    return '<script>alert("Deleted");window.location="/viewbook"</script>'


@app.route('/vieworder',methods=['get'])
def vieworder():
    if session['lg'] != "lin":
        return '<script>alert("please login  first");window.location="/log"</script>'
    session["head"]="View Orders"
    db=Db()
    # rdr=db.select("select * from orders,users where orders.userid=users.userid and users.userid='"+str(session['lid'])+"'")
    rdr=db.select("select * from users,books,orders,order_sub where orders.userid=users.userid and order_sub.bookid=books.bookid AND books.storeid='"+str(session['lid'])+"'")
    return render_template("store/vieworder.html",data=rdr)





# @app.route('/viewsuborder/<oid>',methods=['get'])
# def viewsuborder(oid):
#     if session['lg'] != "lin":
#         return '<script>alert("please login  first");window.location="/log"</script>'
#     session["head"]="View Order Details"
#     db=Db()
#     sub=db.select("select * from order_sub,books,orders where order_sub.bookid=books.bookid and order_sub.orderid=orders.order_id  and orders.order_id ='"+oid+"'")
#     return render_template("store/viewsuborder.html",data=sub)



@app.route('/chat/<uid>',methods=['get'])
def chat(uid):
    db=Db()
    res=db.select("select * from chat where senderid='"+str(session['lid'])+"' and receiverid='"+uid+"' or(senderid='"+uid+"' and receiverid='"+str(session['lid'])+"') order by chatid asc")
    print(res)
    return render_template("store/chat.html",uid=uid,data=res)


@app.route('/addchat/<uid>',methods=['post'])
def addchat(uid):
    message=request.form['message']
    db=Db()
    db.insert("insert into chat(senderid,receiverid,message,date,type) VALUES ('"+str(session['lid'])+"','"+uid+"','"+message+"',curdate(),'store')")
    return '<script>alert("Message Send");window.location="/chat/'+uid+'"</script>'




@app.route('/changepass',methods=['get'])
def changepass():
    return render_template("store/password.html")


@app.route('/changepassword',methods=['post'])
def changepassword():
    currentpass = request.form['cupass']
    newpass=request.form['nepass']
    confirmpass=request.form['copass']
    db = Db()
    res=db.selectOne("select * from login where Password='"+currentpass+"' and login_id='"+str(session['lid'])+"'")
    if res is not None:
        if newpass == confirmpass:
            db.update("update login set Password='"+confirmpass+"' where login_id='"+str(session['lid'])+"'")
            return '<script>alert("Password changed Successfully");window.location="/storehome"</script>'
        else:
            return '<script>alert("Mismatch Password");window.location="/changepass"</script>'
    else:
        return '<script>alert("Incorrect Password");window.location="/changepass"</script>'




# MODULE USER



@app.route('/usersre',methods=['get'])
def usersre():
    return render_template("userRegistration.html")


@app.route('/useregiter',methods=['get'])
def useregister():
    session["head"]="User Registration"
    return render_template("user/userResiter.html")


@app.route('/useregistration',methods=['post'])
def useregistration():
    name=request.form['name']
    place=request.form['place']
    email=request.form['email']
    phn=request.form['phn']
    password=request.form['pass']
    db=Db()
    eml=db.selectOne("select * from login WHERE Username='"+email+"'")
    if eml is not None:
          return '<script>alert("Email already exits");window.location="/usersre"</script>'
    else:
        ris=db.insert("insert into login(Username,Password,Usertype) VALUES ('"+email+"','"+password+"','user')")
        db.insert("insert into users(userid,username,place,email,phonenumber) VALUES ('"+str(ris)+"','"+name+"','"+place+"','"+email+"','"+phn+"')")
        return '<script>alert("Register Successfully");window.location="/log"</script>'


@app.route('/userhome',methods=['get'])
def userhome():
    if session['lg'] != "lin":
        return '<script>alert("please login  first");window.location="/log"</script>'
    return render_template("user/index.html")


@app.route('/viewapstore',methods=['get'])
def viewapstore():
    if session['lg'] != "lin":
        return '<script>alert("please login  first");window.location="/log"</script>'
    session["head"]="View Store"
    db=Db()
    aps=db.select("select * from store,login where store.store_id=login.login_id and Usertype='store' ")
    return render_template("user/viewstore.html",data=aps)


@app.route('/viewallbook/<sid>',methods=['get'])
def viewallbook(sid):
    if session['lg'] != "lin":
        return '<script>alert("please login  first");window.location="/log"</script>'
    db=Db()
    # sid=session['sid']
    bkk=db.select("select * from books,store where books.storeid=store.store_id and books.storeid='"+sid+"' ")
    return render_template("user/viewbooks.html",data=bkk,sid=sid)



@app.route('/quantity/<bid>',methods=['get'])
def quantity(bid):
    if session['lg'] != "lin":
        return '<script>alert("please login  first");window.location="/log"</script>'
    return render_template("user/quantity.html",data=bid,bid=bid)


@app.route('/quantity_post/<bid>',methods=['post'])
def quantity_post(bid):
    if session['lg'] != "lin":
        return '<script>alert("please login  first");window.location="/log"</script>'
    quantity=request.form['quantity']
    db=Db()
    # session['sid']=sid
    db.insert("insert into cart(userid,bookid,quantity) VALUES('"+str(session['lid'])+"','"+bid+"','"+quantity+"') ")
    return '<script>alert("OK");window.location="/viewapstore"</script>'


@app.route('/viewishlist',methods=['get'])
def viewishlist():
    if session['lg'] != "lin":
        return '<script>alert("please login  first");window.location="/log"</script>'
    session["head"]="View Cart"
    db=Db()
    a=0
    b=0
    wish=db.select("select * from cart,books,users where cart.bookid=books.bookid and cart.userid=users.userid and users.userid='"+str(session['lid'])+"' ")
    res=db.selectOne("select sum(cart.quantity*books.price) as amount from cart,books,users where cart.bookid=books.bookid and cart.userid=users.userid and users.userid='"+str(session['lid'])+ "'")
    if res['amount'] is not None:
        a=int(res['amount'])

    else:
        a=0

    t=a+b
    session['total']=t
    if(t==0) :
            session['head']=""

    return render_template("user/viewwishlist.html",data=wish,t=t)


@app.route('/removebook/<bid>')
def removebook(bid):

    db=Db()
    db.delete("delete from cart where bookid='"+bid+"'")
    return'<script>alert("Removed");window.location="/viewishlist"</script>'


@app.route('/paymethod/<t>',methods=['get'])
def paymethod(t):
    if session['lg'] != "lin":
        return '<script>alert("please login  first");window.location="/log"</script>'
    return render_template("user/paymethod.html",t=t)


@app.route('/paymentmethod/<t>',methods=['post'])
def paymentmethod( t):
 if session['lg'] != "lin":
        return '<script>alert("please login  first");window.location="/log"</script>'
 session["head"]="Payment Method"
 method=request.form['method']
 db=Db()
 if method=='offline':
    db = Db()
    storeids = []
    sums = []
    res1 = db.select( "select sum(cart.quantity*books.price) as amount,cart.*,books.*,users.* from cart,books,users where cart.bookid=books.bookid and cart.userid=users.userid and users.userid='" + str(session['lid']) + "' group by storeid")
    for i in res1:
        if i['storeid'] not in storeids:
            storeids.append(i['storeid'])
            sums.append(i['amount'])

    for sid in range(0, len(storeids)):
        res = db.insert("insert into orders(userid,orderDate,paymentStatus,Amount,storeid) VALUES('" + str(session['lid']) + "',curdate(),'offline','" + str(sums[sid]) + "','" + str(storeids[sid]) + "')")
        res2 = db.select("select * from cart,books where books.bookid=cart.bookid and  userid='" + str(session['lid']) + "' and storeid='" + str(storeids[sid]) + "'")
        for i in res2:
            db.insert("insert into order_sub(bookid,orderid,quantity) values('" + str(i['bookid']) + "','" + str(res) + "','" + str(i['quantity']) + "') ")
            db.delete("delete from cart where cartid ='" + str(i['cartid']) + "'")
    return '<script>alert("paid succefully");window.location="/userhome"</script>'

 else:
        return redirect("/onpayment")
        # res = db.insert("insert into orders(userid,orderDate,paymentStatus,Amount) VALUES('" + str(session['lid']) + "',curdate(),'" + method + "','" + t + "')")
        # met = db.insert("insert into order_sub(bookid,orderid,quantity) values('" + bid + "','" + str(res) + "',quantity) ")
        # return '<script>window.location="/onlinepayment"</script>'


@app.route('/onpayment',methods=['get'])
def onpayment():
    if session['lg'] != "lin":
        return '<script>alert("please login  first");window.location="/log"</script>'
    return render_template("user/payment.html")


@app.route('/onlinepayment',methods=['post'])
def onlinepayment():
    # method = request.form['method']
    bank = request.form['bank']
    ifsc = request.form['ifsc']
    acno = request.form['acno']
    # amount=request.form['amonut']
    # t=request.session['total']
    db = Db()
    pay = db.select("select * from bank where bankname='"+bank+"' and IFSC='"+ifsc+"' and acno='"+acno+"' and userid='"+str(session['lid'])+"'")
    if pay is  None:
        return '<script>alert("no account");window.location="/"</script>'
    else:
        db=Db()
        storeids=[]
        sums=[]
        res1 = db.select("select sum(cart.quantity*books.price) as amount,cart.*,books.*,users.* from cart,books,users where cart.bookid=books.bookid and cart.userid=users.userid and users.userid='" + str( session['lid']) + "' group by storeid")
        for i in res1:
            if i['storeid'] not in storeids:
                storeids.append(i['storeid'])
                sums.append(i['amount'])

        for sid in range(0,len(storeids)):
            res = db.insert("insert into orders(userid,orderDate,paymentStatus,Amount,storeid) VALUES('" + str(session['lid']) + "',curdate(),'online','" + str(sums[sid]) + "','"+str(storeids[sid])+"')")
            res2  = db.select("select * from cart,books where books.bookid=cart.bookid and  userid='" + str(session['lid']) + "' and storeid='" + str(storeids[sid]) + "'")
            for i in res2:
                db.insert("insert into order_sub(bookid,orderid,quantity) values('"+str(i['bookid'])+"','" + str(res) + "','" + str(i['quantity']) + "') ")
                db.delete("delete from cart where cartid ='"+str(i['cartid'])+"'")
    return '<script>alert("paid succefully");window.location="/userhome"</script>'







                    #     if t==0 :
    #        return '<script>alert("payment successfull");window.location="/viewishlist"</script>'
    #     else:
    #         return '<script>alert("Less Balance");window.location="/onlinepayment"</script>'
    #
    # else:
    #     return '<script>alert("No such Bank account");window.location="/onlinepayment"</script>'
    #




@app.route('/sendreview',methods=['get'])
def sendreview():
    if session['lg'] != "lin":
        return '<script>alert("please login  first");window.location="/log"</script>'
    session["head"]="Send Reviews"
    return render_template("user/review.html",)


@app.route('/sendreviews',methods=['post'])
def sendreviews():
    if session['lg'] != "lin":
        return '<script>alert("please login  first");window.location="/log"</script>'
    review=request.form['review']
    db=Db()
    db.insert("insert into reviews(review,reviewDate,userid)VALUES('"+review+"',curdate(),'"+str(session['lid'])+"')")
    return '<script>alert("Ok");window.location="/userhome"</script>'


@app.route('/sendcom',methods=['get'])
def sendcom():
    if session['lg'] != "lin":
        return '<script>alert("please login  first");window.location="/log"</script>'
    session["head"] = "Send Complaints"
    return render_template("user/complaints.html")


@app.route('/sendcmplnt',methods=['post'])
def sendcmplnt():
    if session['lg'] != "lin":
        return '<script>alert("please login  first");window.location="/log"</script>'
    complaint=request.form['complaint']
    db=Db()
    db.insert("insert into complaints(complaints,cmpDate,reply,replyDate,userid) VALUES ('"+complaint+"',curdate(),'pending','pending','"+str(session['lid'])+"')")
    return '<script>alert("OK");window.location="/userhome"</script>'


@app.route('/viewreply',methods=['get'])
def viewreply():
    if session['lg'] != "lin":
        return '<script>alert("please login  first");window.location="/log"</script>'
    session["head"]="View Reply"
    db=Db()
    rep=db.select("select * from complaints where userid='"+str(session['lid'])+"'")
    return render_template("user/viewreply.html",data=rep)




@app.route('/userprofile',methods=['get'])
def userprofile():
    db=Db()
    us=db.selectOne("select * from users where userid='"+str(session['lid'])+"'")
    return render_template("user/profile.html",data=us)



@app.route('/edituserprofile',methods=['post'])
def edituserprofile():
    name = request.form['name']
    place = request.form['place']
    email = request.form['email']
    phn = request.form['phn']
    # password = request.form['pass']
    db = Db()
    db.update("update users set username='"+name+"',place='"+place+"',email='"+email+"',phonenumber='"+phn+"'where userid='"+str(session['lid'])+"'")
    return '<script>alert("Profile Updated");window.location="/userhome"</script>'



@app.route('/profile',methods=['get'])
def profile():
    db=Db()
    dt=db.selectOne("select * from store where store_id='"+str(session['lid'])+"'")
    return render_template("store/profile.html",data=dt)


@app.route('/editprofile',methods=['post'])
def editprofile():
    sname = request.form['sname']
    place = request.form['splace']
    email = request.form['email']
    phn = request.form['phn']
    img = request.files['img']
    import datetime
    dt = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    img.save(r"C:\Users\athir\PycharmProjects\BookMangement\static\image\\" + dt + '.jpg')
    path = "/static/image/" + dt + '.jpg'
    db = Db()
    if request.files!="":
        if img.filename!="":
            db.update("update store set storename='"+sname+"',place='"+place+"',email='"+email+"',phonenumber='"+phn+"',Image='"+path+"' where store_id='"+str(session['lid'])+"'")
            return '<script>alert("Profile Updated");window.location="/storehome"</script>'
        else:
            db.update("update store set storename='" + sname + "',place='" + place + "',email='" + email + "',phonenumber='" + phn + "'where store_id='"+str(session['lid'])+"'")
            return '<script>alert("Profile Updated");window.location="/storehome"</script>'
    else:
        db.update("update store set storename='" + sname + "',place='" + place + "',email='" + email + "',phonenumber='" + phn + "'where store_id='"+str(session['lid'])+"'")
        return '<script>alert("Profile Updated");window.location="/storehome"</script>'




@app.route('/logout')
def logout():
    session.clear()
    session['lg'] = ""
    return redirect('/log')



@app.route('/chatt/<sid>',methods=['get'])
def chatt(sid):
    db=Db()
    res=db.select("select * from chat where senderid='"+str(session['lid'])+"' and receiverid='"+sid+"' or(senderid='"+sid+"' and receiverid='"+str(session['lid'])+"') order by chatid asc")
    return render_template("user/chat.html",sid=sid,data=res)


@app.route('/addchatt/<sid>',methods=['post'])
def addchatt(sid):
    message=request.form['message']
    db=Db()
    db.insert("insert into chat(senderid,receiverid,message,date,type) VALUES ('"+str(session['lid'])+"','"+sid+"','"+message+"',curdate(),'user')")
    return '<script>alert("Message Send");window.location="/chatt/'+sid+'"</script>'






@app.route('/userpass',methods=['get'])
def userpass():
    return render_template("user/password.html")


@app.route('/userpassword',methods=['post'])
def userpassword():
    currentpass = request.form['cupass']
    newpass=request.form['nepass']
    confirmpass=request.form['copass']
    db = Db()
    res=db.selectOne("select * from login where Password='"+currentpass+"' and login_id='"+str(session['lid'])+"'")
    if res is not None:
        if newpass == confirmpass:
            db.update("update login set Password='"+confirmpass+"' where login_id='"+str(session['lid'])+"'")
            return '<script>alert("Password changed Successfully");window.location="/userhome"</script>'
        else:
            return '<script>alert("Mismatch Password");window.location="/userpass"</script>'
    else:
        return '<script>alert("Incorrect Password");window.location="/userpass"</script>'







if __name__ == '__main__':
    app.run(port=1234)
