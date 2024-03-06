from datetime import datetime, timedelta

# Elokuvateatterin salit, joista on tallessa salin nimi (avain) sekä
# paikkojen määrä, rivien määrä ja paikkojen rivillä määrä (arvotuple).
salit = {"1": (90, 9, 10), "2": (81, 9, 9), "3": (56, 7, 8)}

# tulostaa alkuvalikon
def main():
    print("Elokuvateatterin varausjärjestelmä\n\nTervetuloa! Miten voimme auttaa tänään?\n")
    while True:
        valinta = input("1. Selaa elokuvia ja varaa lippuja\n2. Kirjaudu sisään ylläpitäjänä\n0. Poistu\n")
        if valinta == "0":
            exit()
        elif valinta == "1":
            selaa_elokuvia()
        elif valinta == "2":
            tarkasta_salasana()
        else:
            print("Valitse jokin annetuista vaihtoehdoista jatkaaksesi.")

# Mikäli halutaan kirjautua sisään ylläpitäjänä, kysytään salasanaa. Kolmen
# väärän salasanan jälkeen ohjelma lopetetaan.
def tarkasta_salasana():
    laskuri = 0
    while laskuri <= 2:
        salasana = input("Anna salasana: ")
        if salasana == "admin":
            avaa_yllapitajan_jarjestelma()
            return
        else:
            print("Salasana ei kelpaa.")
            laskuri += 1
    print("Annoit väärän salasanan 3 kertaa. Lopetetaan ohjelma. Soronoo!")
    exit()

# tulostaa ylläpitäjän valikon
def avaa_yllapitajan_jarjestelma():
    print("\nTervetuloa, admin!")
    while True:
        print("1. Lisää elokuvia ohjelmistoon\n2. Lisää näytöksiä\n3. Tarkastele varauksia\n4. Kirjaudu ulos\n")
        valinta = input("Valintasi: ")
        if valinta == "1":
            lisaa_elokuva()
        elif valinta == "2":
            lisaa_naytos()
        elif valinta == "3":
            tarkastele_varauksia()
        elif valinta == "4":
            print("Kirjaudutaan ulos ja palataan päävalikkoon...\n")
            return
        else:
            print("Valitse jokin annetuista vaihtoehdoista jatkaaksesi.")

# Avataan tiedosto, josta varaukset löytyvät, ja tulostetaan löydetty
# tieto haluttuun muotoon.
def tarkastele_varauksia():
    varaukset = []
    with open("varaukset.csv") as t:
        eka = True
        for rivi in t:
            if eka:
                eka = False
                continue
            tiedot = rivi.strip().split(",")
            asiakas = etsi_asiakas(tiedot[0])
            naytos = etsi_naytos(tiedot[1])
            paikka = f"Paikka: {tiedot[2]}"
            varaukset.append(asiakas+"\n"+naytos+paikka+"\n")
    print("Löytyneet varaukset:\n")
    for varaus in varaukset:
        print(varaus)
    print()

# Avataan asiakasrekisterin sisältävä tiedosto ja palautetaan
# sähköpostiosoitteen perusteella löytyvä asiakas muotoiltuna merkkijonona.
# Mikäli asiakasta ei löydy, palautetaan tyhjä merkkijono.
def etsi_asiakas(sposti: str) -> str:
    with open("asiakkaat.csv") as t:
        for rivi in t:
            if sposti == rivi.split(",")[0]:
                nimi = rivi.strip().split(",")[1]
                return f"Varaaja: {nimi} ({sposti})"
        return ""

#Avataan näytökset sisältävä tiedosto ja etsitään näytöksen id:n perusteella
#haluttu näytös ja palautetaan halutut tiedot muotoiltuna merkkijonona.
#Mikäli näytöstä ei löydy, palautetaan tyhjä merkkijono.
def etsi_naytos(id: str) -> str:
    with open("naytokset.csv") as t:
        for rivi in t:
            if id == rivi.split(",")[0]:
                tiedot = rivi.strip().split(",", 5)
                del tiedot[-1]
                return f"Näytöksen tiedot: {tiedot[1]}, sali {tiedot[2]}, {tiedot[3]} klo {tiedot[4]} "
    return ""

# Lisätään käyttäjän syötteiden perusteella uusi elokuva ohjelmiston
# sisältävään tiedostoon.
def lisaa_elokuva():
    print("Lisätään uusi elokuva ohjelmistoon.")
    elokuva = ""
    nimi = input("Elokuvan nimi: ")
    while True:
        kesto = input("Elokuvan kesto (h:min): ")
        try:
            h = kesto.split(":")[0]
            min = kesto.split(":")[1]
            break
        except:
            ("Anna elokuvan kesto pyydetyssä muodossa (h:min)")
    ikaraja = input("Elokuvan ikäraja: ")
    elokuva += nimi+","
    elokuva += kesto+","
    elokuva += ikaraja+"\n"
    print(f"Lisätäänkö {nimi}, kesto {h}h {min}min, ikäraja {ikaraja} ohjelmistoon? Hyväksy painamalla enter, peru antamalla mikä tahansa muu merkki: ")
    if input("Valintasi: ") == "":
        with open("ohjelmisto.csv", "a") as t:
            t.write(elokuva)
        print("Elokuva lisättiin ohjelmistoon onnistuneesti! Palataan ylläpitäjän valikkoon.\n")
    else:
        return

# Lisätään käyttäjän syötteiden perusteella uusi näytös näytökset sisältävään
# tiedostoon.
def lisaa_naytos():
    print("Valitse näytöksen elokuva:\n")
    ohjelmisto = sorted(hae_elokuvat())
    for elokuva in ohjelmisto:
        print(elokuva[0])
    elokuva_loydetty = False
    while elokuva_loydetty == False:
        valinta = input("Anna elokuvan nimi (tai poistu painamalla enter): ")
        if valinta == "":
            return
        for elokuva in ohjelmisto:
            if valinta == elokuva[0]:
                elokuva_loydetty = True
                kesto = elokuva[1]
                break
        if elokuva_loydetty == False:
            print("Anna ohjelmistosta löytyvä elokuva.")
    while True:
        alkamisaika = anna_alkamisaika()
        aika_str = alkamisaika[1]
        alkamisaika = alkamisaika[0]
        while True:
            sali = input("Anna salin numero (1, 2 tai 3): ")
            if sali != "1" and sali != "2" and sali != "3":
                print("Valitse jokin saleista 1, 2 tai 3.\n")
                continue
            else:
                break
        if tarkasta_onko_sali_vapaa(sali, kesto, alkamisaika):
            print("kukkuluuruu")
            with open("naytokset.csv") as t:
                sisalto = t.readlines()
                id = (sisalto[-1].split(","))[0]
                if int(id)+1 < 10:
                    id = "00"+str(int(id)+1)
                elif 9 < int(id)+1 < 100:
                    id = "0"+str(int(id)+1)
            with open("naytokset.csv", "a") as t:
                t.write(id+","+valinta+","+sali+","+aika_str+"\n")
            print("Näytös lisätty!\n")
            return
        else:
            print("Sali on varattu valitsemanasi ajankohtana. Valitse toinen sali tai aika.")

# Muutetaan käyttäjän syötteenä antamat päivä- ja aikatiedot datetime-olioksi
# ja str-olioksi ja palautetaan ne.   
def anna_alkamisaika():
    while True:
        pvm = input("Anna päivämäärä muodossa dd.mm.yyyy (esim. 02.02.2022): ")
        klo = input("Anna kellonaika muodossa hh:mm (esim. 18:30): ")
        pvmklo = pvm+","+klo
        try:
            alkamisaika = datetime.strptime(pvmklo, "%d.%m.%Y,%H:%M")
            return (alkamisaika, pvmklo)
        except:
            print("Anna päivämäärä ja kellonaika pyydetyssä muodossa.")

# Tarkastetaan parametreina annettujen tietojen perusteella, onko valitussa
# salissa samaan aikaan käynnissä toinen elokuva.    
def tarkasta_onko_sali_vapaa(sali: str, kesto: str, alkamisaika: datetime):
    vartti = timedelta(minutes=15)
    kesto_dt = timedelta(hours=int(kesto.split(":")[0]), minutes=int(kesto.split(":")[1]))
    loppumisaika = alkamisaika + kesto_dt + vartti
    alkamisaika -= vartti
    with open("naytokset.csv") as t:
        for rivi in t:
            rivi = rivi.split(",")
            if rivi[2] == sali:
                elokuvan_kesto = hae_elokuvan_kesto(rivi[1])
                alku = datetime.strptime(rivi[3]+rivi[4].strip(), "%d.%m.%Y%H:%M")
                loppu = alku + elokuvan_kesto + vartti
                alku -= vartti
                if alkamisaika <= alku <= loppumisaika or alku <= alkamisaika <= loppu or alkamisaika <= loppu <= loppumisaika:
                    return False
    return True

# Haetaan annetun elokuvan kesto timedelta-objektina.
def hae_elokuvan_kesto(elokuvan_nimi: str):
    ohjelmisto = hae_elokuvat()
    for elokuva in ohjelmisto:
        if elokuvan_nimi == elokuva[0]:
            aika = elokuva[1].split(":")
            return timedelta(hours=int(aika[0]), minutes=int(aika[1]))

# Avaa ohjelmiston sisältävän tiedoston ja palauttaa ohjelmistossa olevat elokuvat
# ja niiden tiedot.
def hae_elokuvat():
    ohjelmisto = []
    with open("ohjelmisto.csv")as t:
        for rivi in t:
            rivi = rivi.strip("\n")
            elokuva = rivi.split(",")
            ohjelmisto.append(elokuva)
    del ohjelmisto[0]
    return ohjelmisto

# Listataan ohjelmiston elokuvat, listataan valitun elokuvan näytökset ja tehdään
# varaus valintojen perusteella.
def selaa_elokuvia():
    elokuvat = sorted(hae_elokuvat())
    print("Valitse elokuva:\n")
    for elokuva in (elokuvat):
        print(f"{elokuva[0]}, kesto {elokuva[1]}, ikäraja {elokuva[2]}")
    print("\nMikäli haluat varata lippuja, valitse elokuva.\nPalataksesi päävalikkoon paina enter.")
    while True:
        valinta = input("Anna elokuvan nimi: ")
        print()
        if valinta == "":
            return
        for elokuva in elokuvat:
            if valinta == elokuva[0]:
                naytokset = etsi_naytokset(valinta)
                muotoillut = muotoile_naytokset(naytokset)
                for i, naytos in enumerate(muotoillut, start=1):
                    print(f"{i}. {naytos}")
                print("Mikäli haluat varata lippuja, valitse näytös.\nPalataksesi päävalikkoon paina enter.")
                while True:
                    valittu_naytos = input("Valitse haluamasi näytös: ")
                    if valittu_naytos == "":
                        return
                    try:
                        valittu_naytos_int = int(valittu_naytos)
                        break
                    except ValueError:
                        print("Anna valintasi numerona.")
                for j in range(len(naytokset)):
                    if int(valittu_naytos)-1 == j:
                        tee_varaus(naytokset[j][0])
                        return
        else:
            print("Valitsemaasi elokuvaa ei ole ohjelmistossa.")              
    
# Etsitään näytökset sisältävästä tiedostosta annetun elokuvan kaikki näytökset.
def etsi_naytokset(elokuvan_nimi: str):
    naytokset = []
    with open("naytokset.csv") as t:
        for rivi in t:
            rivi = rivi.strip("\n")
            naytos = rivi.split(",")
            if elokuvan_nimi == naytos[1]:
                naytokset.append(naytos)           
    return naytokset

# Palautetaan parametrina annetusta näytökset sisältävästä listasta luettavampi
# versio.
def muotoile_naytokset(naytokset: list):
    muotoillut = []
    for naytos in naytokset:
        naytos_str = f"{naytos[1]}, {naytos[3]} klo {naytos[4]}, sali {naytos[2]}"
        muotoillut.append(naytos_str)
    return muotoillut

# Haetaan parametrina annetun näytöksen varatut paikat.
def hae_varatut_paikat(naytos_id: str) -> list:
    with open("naytokset.csv") as t:
        for rivi in t:
            rivi = rivi.strip("\n")
            naytos = rivi.split(",")
            if str(naytos_id) == naytos[0]:
                return list(naytos[5:])

#Tulostaa salin vapaat ja varatut paikat ja palauttaa salin nimen.
def tulosta_sali(naytos_id: str):
    with open("naytokset.csv") as t:
        for rivi in t:
            rivi = rivi.strip("\n")
            naytos = rivi.split(",")
            if naytos_id == naytos[0]:
                sali = naytos[2]
    for s in salit:
        if sali in s:
            riveja = int(salit[sali][1])
            paikkoja_rivilla = int(salit[sali][2])
    k = 1
    varatut = [int(i) for i in hae_varatut_paikat(naytos_id)]
    for i in range(riveja):
        for j in range(paikkoja_rivilla):
            if k in varatut:
                print(" x",end=" ")
            else:
                if k < 10:
                    print("",k,end=" ")
                else:
                    print(k, end=" ")
            k+=1
        print()
    return sali

# Tehdään paikkavaraus parametrina annettuun näytökseen.
def tee_varaus(naytos_id):
    sali = tulosta_sali(naytos_id)
    varatut = hae_varatut_paikat(naytos_id)
    while True:
        paikkavalinta = input("Valitse paikka (tai poistu painamalla enter): ")
        if paikkavalinta == "":
            return
        if paikkavalinta in varatut:
            print("Valitsemasi paikka on valiettavasti varattu. Valitse toinen paikka.")
        elif int(paikkavalinta) < 1 or int(paikkavalinta) > salit[sali][0]:
            print("Valitsemaasi paikkaa ei löydy kyseisestä salista.")
        else:
            print("Luodaan varaus. Täytä pyydetyt tiedot jatkaaksesi.")
            sposti = luo_kayttaja()
            with open("varaukset.csv", "a") as t:
                t.write(sposti+","+naytos_id+","+paikkavalinta+"\n")
            lisaa_varattu_paikka(naytos_id, paikkavalinta)
            print("Paikka on varattu onnistuneesti!")
            break

# Otetaan talteen näytökset sisältävän tiedoston sisältö ja kirjoitetaan tiedosto
# uudestaan lisätyllä paikkavarauksella.   
def lisaa_varattu_paikka(naytos_id: str, paikka: str):
    muokatut = []
    with open("naytokset.csv") as t:
        for rivi in t:
            tiedot = rivi.strip().split(",")
            if tiedot[0] == naytos_id:
                tiedot.append(paikka)
            muokatut.append(",".join(tiedot)+"\n")
    with open("naytokset.csv", "w") as t:
        for rivi in muokatut:
            t.write(rivi)

# Tarkastetaan, onko käyttäjän antamalla sähköpostilla jo asiakas ja mikäli ei,
# luodaan uusi.
def luo_kayttaja():
    sposti = input("Anna sähköpostiosoitteesi (esimerkki@esim.fi): ")
    if etsi_asiakas(sposti) != "":
        pass
    else:
        nimi = input("Anna nimesi: ")
        with open("asiakkaat.csv", "a") as t:
            t.write(sposti+","+nimi+"\n")
    return sposti


main()