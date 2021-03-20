import urllib.request
import json
import random
import pygame.mixer
from jogo_forca.settings import SPECIAL_CHARS, DROWNING_SOUND_FX, GAME_OVER_SOUND_FX, WIN_OVER_SOUND_FX, DESENHO_FORCA, LIFE, TEXT_GO, TEXT_YW, URL

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
        word += '"'
        for letter in word:
            if letter not in SPECIAL_CHARS:
                t += letter
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
    resp = urllib.request.urlopen(URL).read()
    data = json.loads(resp.decode('utf-8'))

    return data['value']['joke'].split()


def sortea(seq):
    return random.choice(seq)


# Imprime o desenho da FORCA correspondente ao número de letras erradas e as
# letras certas até o momento.
def desenha(erros):
    print(DESENHO_FORCA[erros])
    print(LIFE[erros])


# Recebe como parâmetro uma string com todas as letras já tentadas (certas +
# erradas). Devolve uma letra minúscula que não foi tentada antes. Faz
# consistência se a pessoa digitou uma letra e não um número ou caractere
# especial ou mesmo se não digitou nada.
def chute_feio(letras, alfabeto):
    nc = ''
    for letter in alfabeto:
        if letter not in letras:
            nc += letter
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
    for letter in p:
        if letter not in lc:
            return False
    return True


def tocar_som(som):
    s = sound.Sound(som)
    espera_tocar(s.play())


def main():
    while True:
        palavra = sortea(tirar_caracteres(carregaJoke()))
        for letter in palavra:
            print("-", end="")
        certas, erradas = '', ''
        while True:
            letter = input("\nChute uma letra: ").lower()
            if letter in SPECIAL_CHARS:
                print("\nSó letras!")
            elif letter not in chute_feio(certas + erradas, letters):
                print("\nEssa letra já foi!")
            else:
                if letter in palavra:
                    certas += letter
                else:
                    erradas += letter
            if len(erradas) > 6:
                print(TEXT_GO)
                print(f"\nPalavra Sorteada: {palavra}")
                tocar_som(GAME_OVER_SOUND_FX)
                break
            else:
                desenha(len(erradas))
            print(f"\nErradas: {erradas}")
            for letter in palavra:
                if letter in certas:
                    print(letter, end="")
                else:
                    print("-", end="")
            if len(erradas) == 6:
                tocar_som(DROWNING_SOUND_FX)
            if win(certas, palavra):
                print("\nParabéns ^^, você acaba de salvar mais um pai de família de Zé Palito!!")
                print(TEXT_YW)
                tocar_som(WIN_OVER_SOUND_FX)
                break
        if not novamente():
            break


if __name__ == '__main__':
    main()
