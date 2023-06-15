from matching.games import HospitalResident

from utils.data import leerlingen, mentoren


def match():
    mentor_voorkeuren = mentoren.get_voorkeuren()
    leerling_voorkeuren = leerlingen.get_voorkeuren()

    # Vul de lijst van de voorkeur voor een mentor aan,
    # dit doen we zodat de leerling het grootste voordeel heeft
    for mentor in mentor_voorkeuren:
        for leerling in leerling_voorkeuren:
            if (leerling_voorkeuren[leerling][0] == mentor
                    and leerling not in mentor_voorkeuren[mentor]):
                mentor_voorkeuren[mentor].append(leerling)
            if (leerling_voorkeuren[leerling][1] == mentor
                    and leerling not in mentor_voorkeuren[mentor]):
                mentor_voorkeuren[mentor].append(leerling)
            if (leerling_voorkeuren[leerling][2] == mentor
                    and leerling not in mentor_voorkeuren[mentor]):
                mentor_voorkeuren[mentor].append(leerling)

    # De capaciteiten van de mentoren (wordt nog vervangen door een database)
    capaciteiten = {
        "Jansen": 8,
        "Klaassen": 10,
        "Pietersen": 11,
        "Van Dam": 13
    }

    # Los de "game" op
    game = HospitalResident.create_from_dictionaries(
        leerlingen.get_voorkeuren(), mentor_voorkeuren, capaciteiten)
    match_uitkomst = game.solve()

    # Zet de mentor van de leerling in de database
    for mentor, leerling in match_uitkomst.items():
        for leerling in leerling:
            leerlingen.set_mentor(leerling, mentor)

    # Print de uitkomsten leesbaar
    print("De uitkomst is:\n")
    for mentor, leerling in match_uitkomst.items():
        print(f"{mentor}: {leerling}")

    # Controleer of de uitkomst valide is
    print(f"\nUitkomst valide: {game.check_validity()}")
    print(f"Uitkomst stabiel: {game.check_stability()}")
<<<<<<< HEAD:utils/match.py
=======


match()
>>>>>>> e0ca0224b9ee6faf53f90265b562b2b48317d8dd:match.py
