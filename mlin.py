from time import sleep

from logika import (
    broj_figura_na_ploci,
    generiraj_poteze,
    odaberi_potez_ai,
    protivnik,
    primijeni_potez,
)
from modeli import Potez, Stanje
from konstante import (
    BROJ_FIGURA,
    IGRAC_O,
    IGRAC_X,
    PRAZNO,
    POZICIJE_PO_BROJU,
    BROJEVI_PO_POZICIJI,
    KOORDINATE,
    VEZE,
)


def prikazi_plocu(ploca):
    platno = [[" " for i in range(35)] for j in range(7)]

    for prva, druga in VEZE:
        x1, y1 = KOORDINATE[prva - 1]
        x2, y2 = KOORDINATE[druga - 1]
        if y1 == y2:
            for x in range(min(x1, x2) + 3, max(x1, x2)):
                platno[y1][x] = "_"
        else:
            for y in range(min(y1, y2) + 1, max(y1, y2)):
                platno[y][x1] = "|"

    for pozicija in range(len(KOORDINATE)):
        x, y = KOORDINATE[pozicija]          
        tekst = f"{ploca[pozicija]}{BROJEVI_PO_POZICIJI[pozicija]:02d}"
        platno[y][x:x + len(tekst)] = tekst
        
    print("\n".join("".join(red).rstrip() for red in platno))
    print("X/O = figura igrača, - = prazno polje")


def unesi_poziciju(poruka, dopustene, natrag = False):
    while True:
        unos = input(poruka).strip().lower()
        if unos == "q":
            return None
        if natrag and unos == "b":
            return "NATRAG"
        try:
            broj_polja = int(unos) - 1
        except ValueError:
            print("Unesite broj polja ili q za izlaz.")
            continue
        if not 0 <= broj_polja < len(POZICIJE_PO_BROJU):
            print("Odabrano polje nije dopušteno.")
            continue
        pozicija = POZICIJE_PO_BROJU[broj_polja]
        if pozicija not in dopustene:
            print("Odabrano polje nije dopušteno.")
            continue
        return pozicija


def unesi_potez(stanje, igrac):
    potezi = generiraj_poteze(stanje, igrac)
    if not potezi:
        return None

    postavljeni = stanje.x if igrac == IGRAC_X else stanje.o
    if postavljeni < BROJ_FIGURA:
        moguca_odredista = {potez.odrediste for potez in potezi}
        odrediste = unesi_poziciju("Odaberite prazno polje za postavljanje (1-24, q za izlaz): ", moguca_odredista)
        if odrediste is None:
            return None
        moguci_potezi = [potez for potez in potezi if potez.odrediste == odrediste]
    else:
        while True:
            moguca_polazista = {potez.polaziste for potez in potezi if potez.polaziste is not None}
            polaziste = unesi_poziciju("Odaberite svoju figuru (polja 1-24, q za izlaz): ", moguca_polazista)
            if polaziste is None:
                return None
            moguca_odredista = {potez.odrediste for potez in potezi if potez.polaziste == polaziste}
            odrediste = unesi_poziciju("Odaberite odredišno polje (1-24, q za izlaz, b za povratak na odabir figure): ", moguca_odredista, natrag=True)
            if odrediste is None:
                return None
            if odrediste == "NATRAG":
                print("Povratak na odabir figure")
                continue
            moguci_potezi = [potez for potez in potezi if potez.polaziste == polaziste and potez.odrediste == odrediste]
            break

    moguce_zrtve = [potez.zrtva for potez in moguci_potezi if potez.zrtva is not None]
    if moguce_zrtve:
        zrtva = unesi_poziciju("Odaberite protivničku figuru za uklanjanje (1-24): ", set(moguce_zrtve))
        if zrtva is None:
            return None
        return next(potez for potez in moguci_potezi if potez.zrtva == zrtva)
    return moguci_potezi[0]


def opisi_potez(potez: Potez):
    if potez.polaziste is None:
        opis = f"postavlja figuru na {BROJEVI_PO_POZICIJI[potez.odrediste]}"
    else:
        opis = f"premješta figuru s {BROJEVI_PO_POZICIJI[potez.polaziste]} na {BROJEVI_PO_POZICIJI[potez.odrediste]}"

    if potez.zrtva is not None:
        opis += f" i uklanja protivničku figuru s {BROJEVI_PO_POZICIJI[potez.zrtva]}"
        
    return opis


def pokreni_igru():
    print("Dobrodošli u igru Mlin!\nCilj igre: svesti protivnika na manje od 3 figure ili ga potpuno blokirati tako da nema nijedan mogući potez." + 
          "\n\nIgra se odvija u dvije glavne faze:\nFaza postavljanja:\n" +
          "Svaki igrač ima ukupno 9 figura koje naizmjenično postavlja na prazna polja na ploči." +
          " Ako složite tri svoje figure u niz (vodoravno ili okomito), ostvarili ste mlin i možete ukloniti jednu protivničku figuru s ploče.\n" +
          "\nFaza pomicanja:\n" + 
          "Nakon što su sve figure postavljene, igrači ih pomiču na susjedna slobodna polja " +
          "povezana linijama.\n" + 
          "\nPravilo 3 figure: Kada igraču preostanu samo 3 figure, njegova pravila kretanja se mijenjaju:" + 
          " figure više nisu ograničene na susjedna polja, već mogu skakati na bilo koje prazno polje na ploči.\n\n"
    )
    while True:
        ljudski_igrac = input("Odaberite svoju boju/znak (X ili O; X igra prvi): ").strip().upper()
        if ljudski_igrac in (IGRAC_X, IGRAC_O):
            break
        print("Odaberite X ili O.")

    igrac_ai = protivnik(ljudski_igrac)
    stanje = Stanje(tuple(PRAZNO for i in range(24)), 0, 0)
    na_potezu = IGRAC_X
    ponavljanja = {(stanje, na_potezu): 1}
    broj_poteza = 0

    print(f"\nVi igrate kao {ljudski_igrac}, umjetna inteligencija kao {igrac_ai}.")
    print("Za završetak igre unesite q.")

    while broj_poteza < 200:
        svi_postavljeni = stanje.x == BROJ_FIGURA and stanje.o == BROJ_FIGURA
        prikazi_plocu(stanje.ploca)

        if svi_postavljeni and broj_figura_na_ploci(stanje.ploca, na_potezu) < 3:
            print(f"Pobijedio je igrač {protivnik(na_potezu)}.")
            return

        potezi = generiraj_poteze(stanje, na_potezu)
        if not potezi:
            print(f"Igrač {na_potezu} nema dopuštenih poteza.")
            print(f"Pobijedio je igrač {protivnik(na_potezu)}.")
            return

        if na_potezu == ljudski_igrac:
            print(f"Vaš je potez ({na_potezu}).")
            potez = unesi_potez(stanje, na_potezu)
            if potez is None:
                print("Igra je prekinuta.")
                return
        else:
            print("Umjetna inteligencija razmišlja...")
            potez = odaberi_potez_ai(stanje, igrac_ai)
            sleep(1)  
            if potez is None:
                print("Umjetna inteligencija nema dopuštenih poteza.")
                return
            print(f"Umjetna inteligencija {opisi_potez(potez)}")

        stanje = primijeni_potez(stanje, potez, na_potezu)
        broj_poteza += 1
        na_potezu = protivnik(na_potezu)
        kljuc_stanja = (stanje, na_potezu)
        ponavljanja[kljuc_stanja] = ponavljanja.get(kljuc_stanja, 0) + 1
        if ponavljanja[kljuc_stanja] >= 3:
            prikazi_plocu(stanje.ploca)
            print("Neriješeno: isto stanje ponovilo se tri puta.")
            return

    prikazi_plocu(stanje.ploca)
    print("Neriješeno: dosegnuto je ograničenje broja poteza.")


if __name__ == "__main__":
    pokreni_igru()
