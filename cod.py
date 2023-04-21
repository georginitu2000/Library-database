#importarea bibliotecilor necesare

from flask import Flask, redirect, url_for, render_template, request
from flask_mysqldb import MySQL

#conectarea la baza de date

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'admin'
app.config['MYSQL_DB'] = 'biblioteca'
app.config['SECRET_KEY'] = 'nu'

mysql = MySQL(app)

@app.route("/")
def default():
    return redirect('/acasa')

@app.route("/acasa")
def home():
    return render_template("home.html")

#sunt afisate toate informatiile despre carti din mysql sub forma unui tabel in interfata

@app.route("/Carti")
def Carti():
    cur = mysql.connection.cursor()
    cur.execute("select * from carte")
    carteDetails = cur.fetchall()
    cur.close()
    return render_template("carti.html", carteDetails = carteDetails)

#adaugarea unei noi carti in baza de date prin intermediul interfetei

@app.route("/add_carte", methods=['GET', 'POST'])
def add_carte():
    if request.method == 'POST':
        carteDetails = request.form
        carteID = carteDetails['carteID']
        salaID = carteDetails['salaID']
        titlu = carteDetails['titlu']
        autor = carteDetails['autor']
        nrpagini = carteDetails['nrpagini']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO carte VALUES(%s,%s,%s,%s,%s)",
                    (carteID, salaID, titlu, autor, nrpagini))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for("Carti"))
    return render_template("add_carte.html")

#modificarea salii sau a numarului de pagini a unei carti prin intermediul interfetei

@app.route("/mod_carte", methods = ['GET','POST'])
def mod_carte():
    if request.method == 'POST':
        carteDetails = request.form
        carteID = carteDetails['carteID']
        salaID = carteDetails['salaID']
        nrpagini = carteDetails['nrpagini']
        cur = mysql.connection.cursor()
        if salaID:
            cur.execute("update carte set salaID = %s where carteID = %s",(salaID,carteID))
            mysql.connection.commit()
        if nrpagini:
            cur.execute("update carte set nrpagini = %s where carteID = %s",(nrpagini,carteID))
            mysql.connection.commit()
        cur.close()
        return redirect(url_for("Carti"))
    return render_template("mod_carte.html")

#stergerea unei carti dupa titlu prin intermediul interfetei

@app.route("/ster_carte", methods = ['GET','POST'])
def ster_carte():
    if request.method == 'POST':
        carteDetails = request.form
        titlu = carteDetails['titlu']
        cur = mysql.connection.cursor()
        cur.execute("delete from carte where titlu = %s", (titlu,))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for("Carti"))
    return render_template("sterge_carte.html")

#sunt afisate toate informatiile despre sali din mysql sub forma unui tabel in interfata

@app.route("/sala")
def Sala():
    cur = mysql.connection.cursor()
    cur.execute("select * from sală")
    salaDetails = cur.fetchall()
    cur.close()
    return render_template("sala.html", salaDetails = salaDetails)

#sunt afisate toate informatiile despre tipuri din mysql sub forma unui tabel in interfata

@app.route("/tip")
def Tip():
    cur = mysql.connection.cursor()
    cur.execute("select * from tip")
    tipDetails = cur.fetchall()
    cur.close()
    return render_template("tip.html", tipDetails = tipDetails)

#sunt afisate toate informatiile despre studenti din mysql sub forma unui tabel in interfata

@app.route("/studenti")
def Studenti():
    cur = mysql.connection.cursor()
    cur.execute("select * from student")
    studentDetails = cur.fetchall()
    cur.close()
    return render_template("studenti.html", studentDetails = studentDetails)

#adaugarea unui nou student in baza de date prin intermediul interfetei

@app.route("/add_student", methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        studentDetails = request.form
        studentID = studentDetails['studentID']
        nume = studentDetails['nume']
        prenume = studentDetails['prenume']
        varsta = studentDetails['varsta']
        telefon = studentDetails['telefon']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO student VALUES(%s,%s,%s,%s,%s)",
                    (studentID, nume, prenume, varsta, telefon))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for("Studenti"))
    return render_template("add_student.html")

#modificarea varstei sau a telefonului unui student prin intermediul interfetei

@app.route("/mod_student", methods = ['GET','POST'])
def mod_student():
    if request.method == 'POST':
        studentDetails = request.form
        studentID = studentDetails['studentID']
        varsta = studentDetails['varsta']
        telefon = studentDetails['telefon']
        cur = mysql.connection.cursor()
        if varsta:
            cur.execute("update student set varsta = %s where studentID = %s",(varsta,studentID))
            mysql.connection.commit()
        if telefon:
            cur.execute("update student set telefon = %s where studentID = %s",(telefon,studentID))
            mysql.connection.commit()
        cur.close()
        return redirect(url_for("Studenti"))
    return render_template("mod_student.html")

#stergerea unui student dupa ID prin intermediul interfetei

@app.route("/ster_student", methods = ['GET','POST'])
def ster_student():
    if request.method == 'POST':
        studentDetails = request.form
        studentID = studentDetails['studentID']
        cur = mysql.connection.cursor()
        cur.execute("delete from student where studentID = %s", (studentID,))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for("Studenti"))
    return render_template("sterge_student.html")

#sunt afisate toate informatiile despre imprumuturi din mysql sub forma unui tabel in interfata

@app.route("/imprumuturi")
def Imprumuturi():
    cur = mysql.connection.cursor()
    cur.execute("select * from imprumut")
    imprumuturiDetails = cur.fetchall()
    cur.close()
    return render_template("imprumuturi.html", imprumuturiDetails = imprumuturiDetails)

#sunt afisate toate informatiile despre cartile imprumutate din mysql sub forma unui tabel in interfata

@app.route("/cartiimprumutate")
def CartiImprumutate():
    cur = mysql.connection.cursor()
    cur.execute("select * from carte_impr")
    ciDetails = cur.fetchall()
    cur.close()
    return render_template("ci.html", ciDetails = ciDetails)

#sunt afisate anumite aspecte ce tin de gestionarea bibliotecii sub forma de tabele

@app.route("/evidenta", methods = ['GET', 'POST'])
def evidenta():
    return render_template("evidenta.html")

#afiseaza la ce etaj se gaseste fiecare gen literar

@app.route("/genetaj")
def genetaj():
    cur = mysql.connection.cursor()
    cur.execute("select distinct S.etaj as Etaj, T.denumire as Gen "
    "from tip T, sală S "
    "where S.tipID=T.tipID "
    "order by S.etaj asc")
    genetaj = cur.fetchall()
    return render_template("genetaj.html", genetaj = genetaj)

#afiseaza in ce sala se gaseste fiecare gen literar

@app.route("/gensala")
def gensala():
    cur = mysql.connection.cursor()
    cur.execute("select  T.denumire as Gen, S.salaID as SalaID "
    "from  sală S, tip T "
    "where S.tipID=T.tipID "
    "order by S.salaID asc ")
    gensala = cur.fetchall()
    return render_template("gensala.html", gensala = gensala)

#afiseaza studentii care au facut macar un imprumut

@app.route("/studimpr")
def studimpr():
    cur = mysql.connection.cursor()
    cur.execute("select distinct S.nume as Nume, S.prenume as Prenume " 
    "from student S, imprumut I "
    "where S.studentID=I.studentID")
    studimpr = cur.fetchall()
    return render_template("studimpr.html", studimpr = studimpr)

#afiseaza cartile care au fost imprumutate macar o data

@app.route("/carticartiimpr")
def carticartiimpr():
    cur = mysql.connection.cursor()
    cur.execute("select distinct C.titlu as Titlu, C.autor as Autor "
    "from carte_impr CI, carte C "
    "where CI.carteID=C.carteID")
    carticartiimpr = cur.fetchall()
    return render_template("carticartiimpr.html", carticartiimpr = carticartiimpr)

#sunt afisate anumite statistici legate de imprumuturi sub forma de tabele

@app.route("/statistici", methods = ['GET', 'POST'])
def statistici():
    return render_template("statistici.html")

#afiseaza imprumuturile efectuate in cea mai recenta data

@app.route("/imprrecent")
def imprrecent():
    cur = mysql.connection.cursor()
    cur.execute("select  I.data_imprumut,C.carteID,CC.titlu,  CC.autor "
                "from imprumut I, carte_impr C, carte CC "
                "where I.data_imprumut=(select max(I.data_imprumut) from imprumut I) "
                " and I.imprumutID=C.imprumutID and C.carteID=CC.carteID")
    imprrecent = cur.fetchall()
    return render_template("imprrecent.html", imprrecent = imprrecent)

#afiseaza topul studentilor in functie de numarul de imprumuturi pe care l-au facut

@app.route("/topstud")
def topstud():
    cur = mysql.connection.cursor()
    cur.execute("select S.studentID, S.nume, S.prenume, (select COUNT(*) " 
                "from imprumut I " 
                "where I.studentID=S.studentID) as NumarImprumuturi "
                "from student S "
                "order by NumarImprumuturi DESC")
    topstud = cur.fetchall()
    return render_template("topstud.html", topstud = topstud)

#afiseaza topul genurilor literare care au cele mai multe sali in care se gasesc carti

@app.route("/topgen")
def topgen():
    cur = mysql.connection.cursor()
    cur.execute("select T.tipID, T.denumire, (select COUNT(*) from sală S where S.tipID=T.tipID) as nrsali "
                "from tip T "
                "order by nrsali DESC")
    topgen = cur.fetchall()
    return render_template("topgen.html", topgen = topgen)

#afiseaza topul cartilor in functie de numarul datilor in care au fost imprumutate

@app.route("/topcarti")
def topcarti():
    cur = mysql.connection.cursor()
    cur.execute("select C.titlu, C.autor, (select COUNT(*) from carte_impr CC where CC.carteID=C.carteID) as NrImprumuturi "
                "from carte C "
                "order by NrImprumuturi DESC")
    topcarti = cur.fetchall()
    return render_template("topcarti.html", topcarti = topcarti)

#motor de cautare care, in functie de criteriul de cautare ales si de valoarea introdusa, va afisa informatiile necesare sub forma unui tabel

@app.route("/cauta", methods=['GET','POST'])
def cauta():
        if request.method == 'POST':
            data = request.form
            val = data["selection"]
            cheie = data["cheie"]

            #cautare dupa genul literar=>vor fi afisate cartile care apartin genului literar introdus

            if val == "1":
                cur = mysql.connection.cursor()
                rez = cur.execute("select  C.titlu, C.autor, T.denumire "
                "from tip T, sală S, carte C "
                "where C.salaID=S.salaID  AND S.tipID=T.tipID  and T.denumire=%s", (cheie,))
                if rez > 0:
                    gen = cur.fetchall()
                    return render_template("cauta.html",gen=gen)
                else: 
                    return render_template("cauta.html")

            #cautare dupa numarul de pagini=>vor fi afisate cartile care au mai multe pagini decat numarul introdus

            if val == "2":
                cur = mysql.connection.cursor()
                rez = cur.execute("select  C.titlu as Titlu, C.autor as Autor,T.denumire as Gen, C.nrpagini as NumarPagini "
                "from tip T, carte C, sală S "
                "where C.salaID=S.salaID  AND S.tipID=T.tipID and C.nrpagini>%s" , (cheie,))
                if rez > 0:
                    pag = cur.fetchall()
                    return render_template("cauta.html",pag=pag)
                else:
                    return render_template("cauta.html")

            #cautare dupa data=>vor fi afisate cartile care au fost imprumutate in data introdusa

            if val == "3":
                cur = mysql.connection.cursor()
                rez = cur.execute("select CC.titlu,  CC.autor "
                                  "from imprumut I, carte_impr C, carte CC "
                                  "where I.data_imprumut in (select I.data_imprumut from imprumut I where I.data_imprumut=%s)  "
                                  "and I.imprumutID=C.imprumutID and C.carteID=CC.carteID" , (cheie,))
                if rez > 0:
                    data = cur.fetchall()
                    return render_template("cauta.html",data=data)
                else:
                    return render_template("cauta.html")
        
        return render_template("cauta.html")
  

if __name__ == "__main__" :
    app.run(debug=True)
