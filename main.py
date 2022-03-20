from ast import keyword
import sqlite3

con = sqlite3.connect("kaffe.db")
cursor = con.cursor()

def main():
    
    while True: 
        print("\n")
        print("Yo yo, velkommen til KaffeDB!")
        print("1. Skriv en kaffesmaking")
        print("2. Vis liste over brukere som har smakt flest kaffer")
        print("3. Vis liste over kaffe sortert etter hva som gir deg mest for pengene")
        print("4. Skriv inn et nøkkelord og søk etter kaffer beskrevet med det nøkkelordet")
        print("5. Vis kaffer fra Rwanda og Colombia som ikke er vaskede")
        print("6. Avslutt programmet")
        tall = int(input("Velg en option, skriv inn et tall fra 1-5:"))
        
        if(tall == 1):
            print("Test1")
            break
        
        elif(tall == 2):
            getListOverUsersWithMostTasted()
            break

        elif(tall == 3):
            getMostCoffePerPrice()
            break
        
        elif(tall == 4):
            keyword = input('hvilket nøkkelord vil du søke etter?')
            getCoffeByKeyWord(keyword)
            break
        
        elif(tall == 5):
            print("Test5")
            break

        elif(tall == 6):
            print("Takk for i dag!")
            con.close()
            break
        
        else:
            print("Ugyldig input! Tallet må være mellom 1 og 5.")

def getListOverUsersWithMostTasted():
  cursor.execute("""SELECT Bruker.Fornavn, Bruker.Etternavn, count (distinct KaffeID) as antallUnikeKafferSmakt 
                    FROM  Kaffesmaking NATURAL JOIN Bruker
                    WHERE Smaksdato LIKE '%2022'
                    GROUP BY Kaffesmaking.Epostadresse
                    ORDER BY antallUnikeKafferSmakt DESC
                    """)
  row = cursor.fetchall()
  print(row)
  #con.close()

def getMostCoffePerPrice():
  cursor.execute("""SELECT KaffeNavn, avg(Poeng) as SnittPoeng, KiloprisNOK, BrenneriNavn 
                    FROM Kaffesmaking
                    NATURAL JOIN Kaffe
                    NATURAL JOIN KaffeBrentAvBrenneri
                    NATURAL JOIN Kaffebrenneri
                    GROUP BY kaffeID
                    ORDER BY (Snittpoeng/KiloprisNOK) DESC
                    """)
  row = cursor.fetchall()
  i = 1
  #print("NR KAFFENAVN SNITTPOENG KILOPRIS(NOK) BRENNERINAVN")
  #print("-------------------------")
  for entry in row:
    print(str(i) + ".", entry)
    i = i + 1 
  #print(row)
  #con.close()

def getCoffeByKeyWord(keyword):
    keyword = "%" + keyword + "%"
    cursor.execute("""SELECT BrenneriNavn, KaffeNavn
                        FROM Kaffe 
                            NATURAL JOIN KaffeBrentAvBrenneri
                            NATURAL JOIN Kaffebrenneri
                        WHERE Kaffe.KaffeBeskrivelse LIKE :keyword

                        UNION

                        SELECT BrenneriNavn, KaffeNavn
                        FROM Kaffesmaking
                            NATURAL JOIN Kaffe
                            NATURAL JOIN KaffeBrentAvBrenneri
                            NATURAL JOIN Kaffebrenneri
                        WHERE Kaffesmaking.Smaksnotat LIKE :keyword

                    """, (keyword,))
    row = cursor.fetchall()
    if row == "[]":
        print("Det var ingen kaffer som stemte med søket ditt")
    print(row)


main()