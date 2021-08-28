
TYPE, WHO, YES_OR_NO = 0, 1, 2

def is_murder(who): return ['is_murder', who, True]
def is_innocent(who): return ['is_murder', who, False]
def said_true(who): return ['said', who, True]
def said_false(who): return ['said', who, False]

def straight_claim(murders: set, innocents: set, claim: list):
    if claim[YES_OR_NO]:
        murders.add(claim[WHO])
    else:
        innocents.add(claim[WHO])

    return murders, innocents

def negate(claim) -> list:
    return [claim[TYPE], claim[WHO], not claim[YES_OR_NO]]

def find_murder(murders: set, innocents: set, claims: dict, lair: str):
    for who, claim in claims.items():
        if who == lair:
            claim = negate(claim)

        if claim[TYPE] == 'is_murder':
            murders, innocents = straight_claim(murders, innocents, claim)
        elif claim[TYPE] == 'said':
            murders, innocents = straight_claim(
                murders,
                innocents,
                claims[claim[WHO]] if claim[YES_OR_NO] else negate(claims[claim[WHO]]))
        else:
            raise f'unknown type {claim[TYPE]}'

    return murders, innocents

def check_lair(claims: dict) -> str:
    for lair in claims.keys():
        murders, innocents = find_murder(set([lair]), set(), claims, lair)
        if len(murders) == 1 and len(set(murders) & set(innocents)) == 0:
            return murders.pop()
    
    return None

print('''Late Wittgenstein

Wittgenstein has been murdered. The culprit is one of either Friedrich Nietzsche, Lou Andreas-Salomé, Karl Marx or Ludwig Feuerbach. They make the following statements. You have been correctly informed that guilty person always lies, and everyone else tells the truth.

Nietzsche: Salomé is the culprit.
Salomé: Marx is innocent.
Feuerbach: Salomé’s statement is true.
Marx: Nietzsche’s statement is false.

Who killed Wittgenstein?''')

N = 'Nietzsche'
S = 'Salomé'
F = 'Feuerbach'
M = 'Marx'

murder = check_lair(claims = {
    S: is_innocent(M),
    F: said_true(S),
    M: said_false(N),
    N: is_murder(S)})

print('The murder is: ', murder)
