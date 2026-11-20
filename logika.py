from modeli import Potez, Stanje

from konstante import (
    BROJ_FIGURA,
    IGRAC_O,
    IGRAC_X,
    PRAZNO,
    MLINOVI,
    SUSJEDI
)

def protivnik(igrac):
    return IGRAC_O if igrac == IGRAC_X else IGRAC_X


def broj_figura_na_ploci(ploca, igrac):
    return ploca.count(igrac)


def je_u_mlinu(ploca, pozicija, igrac):
    return any(
        pozicija in mlin and all(ploca[polje] == igrac for polje in mlin)
        for mlin in MLINOVI
    )


def moguce_zrtve(ploca, igrac):
    zrtve = []
    
    for pozicija in range(len(ploca)):
        figura = ploca[pozicija] 
        
        if figura == igrac and not je_u_mlinu(ploca, pozicija, igrac):
            zrtve.append(pozicija)
                
    if not zrtve:
        zrtve = [pozicija for pozicija in range(len(ploca)) if ploca[pozicija] == igrac]
    return zrtve


def generiraj_poteze(stanje, igrac):
    ploca = stanje.ploca
    postavljeni = stanje.x if igrac == IGRAC_X else stanje.o
    prazna_polja = [pozicija for pozicija in range(len(ploca)) if ploca[pozicija] == PRAZNO]
    potezi= []

    if postavljeni < BROJ_FIGURA:
        moguca_kretanja = [(None, odrediste) for odrediste in prazna_polja]
    else:
        polazista = [pozicija for pozicija in range(len(ploca)) if ploca[pozicija] == igrac]
        moguca_kretanja = []
        for polaziste in polazista:
            if len(polazista) == 3:
                odredista = prazna_polja
            else:
                odredista = [susjed for susjed in SUSJEDI[polaziste] if ploca[susjed] == PRAZNO]
            moguca_kretanja.extend((polaziste, odrediste_poteza) for odrediste_poteza in odredista)

    for polaziste, odrediste in moguca_kretanja:
        nova_ploca = list(ploca)
        if polaziste is not None:
            nova_ploca[polaziste] = PRAZNO
        nova_ploca[odrediste] = igrac
        nova_ploca_t = tuple(nova_ploca)

        stvoren_mlin = any(
            odrediste in mlin and all(nova_ploca_t[polje] == igrac for polje in mlin)
            for mlin in MLINOVI
        )
        if stvoren_mlin:
            zrtve = moguce_zrtve(nova_ploca_t, protivnik(igrac))
            if zrtve:
                potezi.extend(Potez(polaziste, odrediste, zrtva) for zrtva in zrtve)
            else:
                potezi.append(Potez(polaziste, odrediste, None))
        else:
            potezi.append(Potez(polaziste, odrediste, None))

    return potezi


def primijeni_potez(stanje: Stanje, potez: Potez, igrac: str):
    x = stanje.x
    o = stanje.o
    nova_ploca = list(stanje.ploca)

    if potez.polaziste is None:
        if igrac == IGRAC_X:
            x += 1
        else:
            o += 1
    else:
        nova_ploca[potez.polaziste] = PRAZNO

    nova_ploca[potez.odrediste] = igrac
    if potez.zrtva is not None:
        nova_ploca[potez.zrtva] = PRAZNO

    return Stanje(tuple(nova_ploca), x, o)


def broj_mogucih_pomaka(ploca, igrac) -> int:
    figure = [pozicija for pozicija in range(len(ploca)) if ploca[pozicija] == igrac]
    prazna_polja = [pozicija for pozicija in range(len(ploca)) if ploca[pozicija] == PRAZNO]
    if len(figure) == 3:
        return len(figure) * len(prazna_polja)
    return sum(ploca[susjed] == PRAZNO for pozicija in figure for susjed in SUSJEDI[pozicija])


def bodovi_za_mlin(broj_figura, prazno_mjesta, ukupno_fig_igraca, protivnik_figure):
    if broj_figura == 3:
        if protivnik_figure <= 4:
            return 1500  
        return 800        
    elif broj_figura == 2 and prazno_mjesta == 1:
        if ukupno_fig_igraca == 3:
            return 350  
        return 160      
    return 0


def procijeni_stanje(stanje: Stanje, igrac_ai: str):
    ploca = stanje.ploca
    postavljeni_x = stanje.x
    postavljeni_o = stanje.o
    igrac_drugi = protivnik(igrac_ai)
    
    figure_ai = broj_figura_na_ploci(ploca, igrac_ai)
    figure_drugi = broj_figura_na_ploci(ploca, igrac_drugi)
    
    postavljeni_ai = postavljeni_x if igrac_ai == IGRAC_X else postavljeni_o
    postavljeni_drugi = postavljeni_o if igrac_ai == IGRAC_X else postavljeni_x

    if postavljeni_ai == BROJ_FIGURA and postavljeni_drugi == BROJ_FIGURA:
        if figure_ai < 3:
            return -99999
        if figure_drugi < 3:
            return 99999

    tezina_materijala = 100 if (figure_ai == 3 or figure_drugi == 3) else 30
    rezultat = (figure_ai - figure_drugi) * tezina_materijala

    for mlin in MLINOVI:
        figure_u_mlinu_ai = sum(ploca[polje] == igrac_ai for polje in mlin)
        figure_u_mlinu_drugi = sum(ploca[polje] == igrac_drugi for polje in mlin)
        prazna_u_mlinu = sum(ploca[polje] == PRAZNO for polje in mlin)
        
        rezultat += bodovi_za_mlin(figure_u_mlinu_ai, prazna_u_mlinu, figure_ai, figure_drugi)
        rezultat -= bodovi_za_mlin(figure_u_mlinu_drugi, prazna_u_mlinu, figure_drugi, figure_ai)

    if postavljeni_ai == BROJ_FIGURA and postavljeni_drugi == BROJ_FIGURA:
        mobilnost_ai = broj_mogucih_pomaka(ploca, igrac_ai)
        mobilnost_drugi = broj_mogucih_pomaka(ploca, igrac_drugi)

        if mobilnost_drugi == 0 and figure_drugi > 3:
            return 99999
        if mobilnost_ai == 0 and figure_ai > 3:
            return -99999
            
        rezultat += (mobilnost_ai - mobilnost_drugi) * 10

    return rezultat


def minimax(stanje: Stanje, na_potezu: str, igrac_ai: str, dubina: int, alfa: int, beta: int):
    if stanje.x == BROJ_FIGURA and stanje.o == BROJ_FIGURA:
        figure_na_ploci = broj_figura_na_ploci(stanje.ploca, na_potezu)
        if figure_na_ploci < 3:
            return -100000 - dubina

    potezi = generiraj_poteze(stanje, na_potezu)
    if not potezi:
        return -100000 - dubina
    
    if dubina == 0:
        return procijeni_stanje(stanje, igrac_ai)

    rangirani_potezi = []
    for potez in potezi:
        novo_stanje = primijeni_potez(stanje, potez, na_potezu)
        procjena = procijeni_stanje(novo_stanje, igrac_ai)
        rangirani_potezi.append((procjena, novo_stanje))
    rangirani_potezi.sort(key=lambda zapis: zapis[0],reverse=na_potezu == igrac_ai)

    if na_potezu == igrac_ai:
        najbolja_vrijednost = -1000000
        for i, novo_stanje in rangirani_potezi:
            vrijednost = minimax(
                novo_stanje,
                protivnik(na_potezu),
                igrac_ai,
                dubina - 1,
                alfa,
                beta,
            )
            najbolja_vrijednost = max(najbolja_vrijednost, vrijednost)
            alfa = max(alfa, najbolja_vrijednost)
            if beta <= alfa:
                break
        return najbolja_vrijednost

    najbolja_vrijednost = 1000000
    for i, novo_stanje in rangirani_potezi:
        vrijednost = minimax(
            novo_stanje,
            protivnik(na_potezu),
            igrac_ai,
            dubina - 1,
            alfa,
            beta,
        )
        najbolja_vrijednost = min(najbolja_vrijednost, vrijednost)
        beta = min(beta, najbolja_vrijednost)
        if beta <= alfa:
            break
    return najbolja_vrijednost


def odaberi_potez_ai(stanje: Stanje, igrac_ai: str):
    potezi = generiraj_poteze(stanje, igrac_ai)
    if not potezi:
        return None

    postavljeni = stanje.x if igrac_ai == IGRAC_X else stanje.o
    if postavljeni < BROJ_FIGURA:
        dubina = 2
    elif broj_figura_na_ploci(stanje.ploca, igrac_ai) == 3:
        dubina = 3
    else:
        dubina = 4

    najbolji_potez = potezi[0]
    najbolja_vrijednost = -1000000

    for potez in potezi:
        novo_stanje = primijeni_potez(stanje, potez, igrac_ai)

        vrijednost = minimax(
            novo_stanje,
            protivnik(igrac_ai),
            igrac_ai,
            dubina - 1,
            -1000000,
            1000000,
        )

        if vrijednost > najbolja_vrijednost:
            najbolja_vrijednost = vrijednost
            najbolji_potez = potez
    return najbolji_potez
