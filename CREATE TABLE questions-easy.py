import sqlite3
def createquiz_database():
    db = sqlite3.connect('Quizquest.db')
    try:
        cursorobj = db.cursor()
        cursorobj.execute('''CREATE TABLE questionseasy
        (question_id INTEGER PRIMARY KEY AUTOINCREMENT,
        question text,
        answer text ,
        options text);''')

        cursorobj.execute('''CREATE TABLE questionsmedium
        (question_id INTEGER PRIMARY KEY AUTOINCREMENT,
        question text,
        answer text ,
        options text);''')

        cursorobj.execute('''CREATE TABLE questionshard
        (question_id INTEGER PRIMARY KEY AUTOINCREMENT,
        question text,
        answer text ,
        options text);''')
        print('done')
    except Exception as e:
        print(e,'err')
def getquestion(questionid,level='questionseasy'):
    db = sqlite3.connect('Quizquest.db')
    cursorobj = db.cursor()
    try:
        cursorobj.execute('''SELECT question,answer,options FROM ? where question_id = ?''',(level,questionid))
        question,answer,options = cursorobj.fetchone()
    except:
        db.rollback()
        db.close()
    db.close()
    return False

def getAllVerse(chapter):
    chapter = int(chapter)
    dbcon = sqlite3.connect("fullquranDb.db")
    dbcur = dbcon.cursor()
    dbcur.execute("Select count(verse) from quoran where chapter = ?", (chapter,))
    versecount = dbcur.fetchone()
    dbcon.close()
    return list(versecount)[0]

def setquestion(chapter):
    question = f"how many verses are in chapter {chapter}" 
    answer = f"{getAllVerse(chapter)} verses"
    options = f"{getAllVerse(chapter-1)} verses"
    dbcon = sqlite3.connect('Quizquest.db')
    dbcur = dbcon.cursor()
    dbcur.execute('''INSERT into questionseasy(question,answer,options) values(?,?,?)''', (question,answer,options))
    dbcon.commit()
    dbcon.close()
    print('done',chapter)
createquiz_database()
for a in range(1,115):
    setquestion(a)
    print('yeszs')
print('finished')