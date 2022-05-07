import sqlite3

def getAllChapters():
    dbcon = sqlite3.connect("fullquranDb.db")
    dbcur = dbcon.cursor()
    dbcur.execute("Select count(DISTINCT chapter) from quoran")
    chaptercount = dbcur.fetchone()
    dbcon.close()
    return list(chaptercount)[0]

def getAllVerse(chapter):
    chapter = int(chapter)
    dbcon = sqlite3.connect("fullquranDb.db")
    dbcur = dbcon.cursor()
    dbcur.execute("Select count(verse) from quoran where chapter = ?", (chapter,))
    versecount = dbcur.fetchone()
    dbcon.close()
    return list(versecount)[0]

def getAllEngContext():
    dbcon = sqlite3.connect("fullquranDb.db")
    dbcur = dbcon.cursor()
    dbcur.execute("Select english_content From quoran ")
    context = dbcur.fetchall()
    dbcon.close()
    return list(context)
    klis = list(getAllEngContext())
    for a in klis:
        a,=a
        print(a[:]) 

def getEngContext(chapter,verse):
    chapter = int(chapter)
    verse = int(verse)
    dbcon = sqlite3.connect("fullquranDb.db")
    dbcur = dbcon.cursor()
    dbcur.execute("Select english_content from quoran where chapter = ? and verse = ?",(chapter,verse))
    context = dbcur.fetchone()
    dbcon.close()
    return list(context)[0]

def getArbContext(chapter,verse):
    chapter = int(chapter)
    verse = int(verse)
    dbcon = sqlite3.connect("fullquranDb.db")
    dbcur = dbcon.cursor()
    dbcur.execute("Select arabic_content from quoran where chapter = ? and verse = ?",(chapter,verse))
    context = dbcur.fetchone()
    dbcon.close()
    return list(context)[0]

def addToBookmark(chapter,verse):
    chapter = int(chapter)
    verse = int(verse)
    dbcon = sqlite3.connect("fullquranDb.db")
    dbcur = dbcon.cursor()
    dbcur.execute("Update quoran SET bookmarked = 'True' where chapter = ? and verse = ? ",(chapter,verse))
    dbcon.commit()
    dbcon.close()

def removeBookmark(chapter,verse):
    chapter = int(chapter)
    verse = int(verse)
    dbcon = sqlite3.connect("fullquranDb.db")
    dbcur = dbcon.cursor()
    dbcur.execute("Update quoran SET bookmarked = 'False' where chapter = ? and verse = ? ",(chapter,verse))
    dbcon.commit()
    dbcon.close()
def checkBookmark(chapter,verse):
    chapter = int(chapter)
    verse = int(verse)
    dbcon = sqlite3.connect("fullquranDb.db")
    dbcur = dbcon.cursor()
    dbcur.execute("Select bookmarked from quoran where chapter = ? and verse = ?",(chapter,verse))
    check, = dbcur.fetchone()
    dbcon.close()
    if check=="True":
        return True
    else:
        return False
def getAllBookmarked():
    dbcon = sqlite3.connect("fullquranDb.db")
    dbcur = dbcon.cursor()
    dbcur.execute("Select chapter,verse from quoran where bookmarked = 'True' ")
    bookmarks = dbcur.fetchall()
    dbcon.close()
    return bookmarks
