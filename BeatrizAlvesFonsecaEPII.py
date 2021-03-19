import urllib.request
import json
import random
import pygame.mixer

forca0 = '''
    +-----+
    |     |
          |
          |
          |
          |
============
'''

forca1 = '''
    +-----+
    |     |
    O     |
          |
          |
          |
============
'''

forca2 = '''
    +-----+
    |     |
    O     |
    |     |
          |
          |
============
'''

forca3 = '''
    +-----+
    |     |
   _O     |
    |     |
          |
          |
============
'''

forca4 = '''
    +-----+
    |     |
   _O_    |
    |     |
          |
          |
============
'''

forca5 = '''
    +-----+
    |     |
   _O_    |
    |     |
   /      |
          |
============
'''

forca6 = '''
    +-----+
    |     |
   _O_    |
    |     |
   / \    |
          |
============
'''

textGO = '''
 ___     _     _   _   __    __         __  __
|       / |   / | / | |     |  | \   | |   | _|
|  _   /__|  /  |/  | |--   |  |  \  | |-- | \
|___| /   | /   |   | |__   |__|   \_| |__ |  \\
'''

textYW = '''
     __                   ___
\ | |  | |  |   \   |   |  |  |\  | | |
 \| |  | |  |    \  |\  |  |  | \ | | |
  | |__| |__|     \_| \_| _|_ |  \| o o
'''

desenho_forca = [forca0, forca1, forca2, forca3, forca4, forca5, forca6]
life = '[OOOOOO]|[OOOOO ]|[OOOO  ]|[OOO   ]|[OO    ]|[O     ]|[      ]'.split('|')

letters = 'a á ã e é i í o ó õ u ú b c ç d f g h j k l m n p q r s t v w x y z'.split()

sound = pygame.mixer
sound.init()


def espera_tocar(canal):
    while canal.get_busy():
        pass


# Função para tirar carecteres especiais
def tirar_caracteres(lista):
    nlista = []
    for word in lista:
        t = ''
        for l in word:
            if l not in "!@#$%¨&*()`´^~[]{}'/*\|_-=+, .:;<>" and l not in '"':
                t += l
        if t not in nlista and len(t) > 3:
            nlista.append(t.lower())
    return nlista

# Retorna uma palavra sorteada, que tenha pelo menos quatro letras da seguinte
# forma:
    # a) você pedirá para o usuário digitar uma palavra única
    # b) você irá acessar todas as frases recentes do Twitter que contenham essa
    # palavra
    # c) irá eliminar as palavras com menos de quatro letras ou repetidas
    # d) irá sortear uma palavra entre as que sobraram. Para facilitar suponha
    # inglês ou pt-br como línguas permitidas


# Função para carregar lista com as palavras da piada
def carregaJoke():
    url = 'http://api.icndb.com/jokes/random?limitTo=[nerdy]'

    resp = urllib.request.urlopen(url).read()
    data = json.loads(resp.decode('utf-8'))

    return data['value']['joke'].split()


def sortea(seq):
    return random.choice(seq)


# Imprime o desenho da FORCA correspondente ao número de letras erradas e as
# letras certas até o momento.
def desenha(erros):
    print(desenho_forca[erros])
    print(life[erros])


# Recebe como parâmetro uma string com todas as letras já tentadas (certas +
# erradas). Devolve uma letra minúscula que não foi tentada antes. Faz
# consistência se a pessoa digitou uma letra e não um número ou caractere
# especial ou mesmo se não digitou nada.
def chute_feio(letras, alfabeto):
    nc = ''
    for l in alfabeto:
        if l not in letras:
            nc += l
    return nc


# Pergunta se a pessoa quer jogar de novo e retorna True ou False. Você deverá
# aceitar letras maiúsculas ou minúsculas na resposta.
def novamente():
    resp = input("\nDeseja jogar novamente? S/Y(sim/yes), N(não/no)").lower()
    if resp == 'n':
        return False
    elif resp == 's' or resp == 'y':
        return True
    return novamente()


# Retorna True caso todas as letras da palavra sorteada estejam na string certas.
def win(lc, p):
    for l in p:
        if l not in lc:
            return False
    return True


def tocar_som(som):
    s = sound.Sound(som)
    espera_tocar(s.play())


def main():
    while True:
        palavra = sortea(tirar_caracteres(carregaJoke()))
        for l in palavra:
            print("-", end = "")
        certas, erradas = '', ''
        while True:
            l = input("\nChute uma letra: ").lower()
            if l in "!@#$%¨&*()`´^~[]{}'/*\|_-=+, .:;<>" or l in '"':
                print("\nSó letras!")
            elif l not  in chute_feio(certas + erradas, letters):
                print("\nEssa letra já foi!")
            else:
                if l in palavra:
                    certas += l
                else:
                    erradas += l
            if len(erradas) > 6:
                print(textGO)
                print("\nPalavra Sorteada: %s" %palavra)
                tocar_som("sound_source/SonicTheHedgehog3MusicGameOver.wav")
                break
            else:
                desenha(len(erradas))
            print("\nErradas: %s" %erradas)
            for l in palavra:
                if l in certas:
                    print(l, end = "")
                else:
                    print("-", end = "")
            if len(erradas) == 6:
                tocar_som("sound_source/SonicTheHedgehog15Drowning.wav")
            if win(certas, palavra):
                print("\nParabéns ^^, você acaba de salvar mais um pai de família de Zé Palito!!")
                print(textYW)
                tocar_som("sound_source/SonicTheHedgehog131Up.wav")
                break
        if not novamente():
            break


if __name__ == '__main__':
    main()
