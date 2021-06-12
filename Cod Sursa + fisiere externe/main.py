import pygame
import math
import random
from pygame import mixer

# Initializarea librariei
pygame.init()

# Initializarea paginii
screen = pygame.display.set_mode((800, 600))

# Fundal
fundal = pygame.image.load("Fundal_Spatiu.png").convert()
y = 0

# Muzica de fundal
mixer.music.load("Muzica_Fundal.wav")
mixer.music.play(-1)

# Titlul si logoul paginii
pygame.display.set_caption("Chicken Invaders")
logo = pygame.image.load("logo_31px.png")
pygame.display.set_icon(logo)

# Scor
val_scor = 0
font = pygame.font.Font('segoeui.ttf', 25)
textX = 10
textY = 6


def afis_scor(x, y):
    scor = font.render("Scor: " + str(val_scor), True, (255, 255, 255))
    screen.blit(scor, (x, y))


# Text taste volum
font_sunet = pygame.font.Font('segoeui.ttf', 12)
text_volum_X = 590
text_volum_p_Y = 25
text_volum_m_Y = 10

def afis_sunet(x, y, z):
    tasta_p = font_sunet.render("P - activeaza muzica fundal", True, (255, 255, 255))
    screen.blit(tasta_p, (x, y))
    tasta_m = font_sunet.render("M - dezactiveaza muzica fundal", True, (255, 255, 255))
    screen.blit(tasta_m, (x, z))


# Game Over
font_game_over = pygame.font.Font('segoeuib.ttf', 70)
font_scor_final = pygame.font.Font('seguisb.ttf', 22)


def game_over_text():
    game_over = font_game_over.render("GAME OVER", True, (255, 255, 255))
    scor_final = font_scor_final.render("SCOR FINAL: " + str(val_scor), True, (255, 255, 255))
    screen.blit(game_over, (200, 200))
    screen.blit(scor_final, (325, 285))


sunet_rep = 1  # Variabila ce verifica daca sunetul de final a fost pornit o singura data


def sunet_final():
    sunet_game_over = mixer.Sound("Sunet_Game_Over.wav")
    sunet_game_over.play()


# Initializarea Eroului
AvatarJucator = pygame.image.load("Naveta_64px.png")
jucatorX = 370
jucatorY = 480
jucatorX_miscare = 0


def jucator(x, y):
    screen.blit(AvatarJucator, (x, y))


# Initializarea Inamicului
AvatarInamic = []
inamicX = []
inamicY = []
inamicX_miscare = []
inamicY_miscare = []
numar_inamici = 5

for i in range(numar_inamici):
    AvatarInamic.append(pygame.image.load('Gaina_62X51px.png'))
    inamicX.append(random.randint(0, 736))
    inamicY.append(random.randint(50, 150))
    inamicX_miscare.append(1.2)
    inamicY_miscare.append(30)


def inamic(x, y, i):
    screen.blit(AvatarInamic[i], (x, y))


# Initializare Glont
AvatarGlont = pygame.image.load('glont_31px.png')
glontX = 0
glontY = 480
glontY_miscare = 10  # Viteza de miscare a glontului
glont_stare = "pregatit"


def trage_glont(x, y):
    global glont_stare
    glont_stare = "tras"
    screen.blit(AvatarGlont, (x + 17, y + 10))

# Calculeaza daca glontul ajunge la o anumita distanta fata de inamic
def inamic_lovit(inamicX, inamicY, glontX, glontY):
    distanta = math.sqrt(math.pow(glontY - inamicY, 2) + math.pow(glontX - inamicX, 2))
    if distanta <= 27:
        return True
    else:
        return False


# Baza
ruleaza = True
while ruleaza:
    # Ecranul principal
    screen.fill((0, 0, 50))
    # Fundal in pagina - miscare poza
    y_rel = y % fundal.get_rect().height
    screen.blit(fundal, (0, y_rel - fundal.get_rect().height))
    if y_rel < 600:
        screen.blit(fundal, (0, y_rel))
    y += 3  # Viteza cu care se misca imaginea din fundal

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            ruleaza = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                # Viteza de miscare a navetei la stanga
                jucatorX_miscare = -2
            if event.key == pygame.K_RIGHT:
                # Viteza de miscare a navetei la drepta
                jucatorX_miscare = 2
            if event.key == pygame.K_m:
                mixer.music.pause()
            if event.key == pygame.K_p:
                mixer.music.unpause()
            if event.key == pygame.K_SPACE:
                if glont_stare == "pregatit":
                    # Adauga sunet cand tragi
                    sunet_glont = mixer.Sound("Sunet_Laser.wav")
                    sunet_glont.play()
                    # Glontul netras preia aceeasi coordonata X ca si nava
                    glontX = jucatorX
                    trage_glont(glontX, glontY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                jucatorX_miscare = 0

    # Asigurare ca naveta nu iese din pagina
    if jucatorX <= 0:
        jucatorX = 0
    elif jucatorX >= 736:
        jucatorX = 736

    jucatorX += jucatorX_miscare

    # Miscarea inamicului
    for i in range(numar_inamici):

        # Afisarea pe ecran a textului "Game Over" (Joc terminat)
        if inamicY[i] > 420:  # Distanta pe axa Y, la care, daca ajunge inamicul, jocul se termina
            for j in range(numar_inamici):
                inamicY[j] = 2000
            game_over_text()
            mixer.music.pause()
            if sunet_rep == 1:
                sunet_final()
            sunet_rep += 1
            text_volum_X = 2000
            textY = 2000
            textX = 2000
            y +=5
            break

        # Ecuatia prin care pozitia pe axa x a inamicului creste sau scade
        inamicX[i] += inamicX_miscare[i]
        # Daca coordonata X a inamicului i este egala sau mai mica decat 0, acesta va incepe sa se miste spre dreapta si in acelasi timp se va muta in jos pe axa Y
        if inamicX[i] <= 0:
            inamicX_miscare[i] = 1.2
            inamicY[i] += inamicY_miscare[i]
        # Daca coordonata X a inamicului i este egala sau mai mare decat 736, acesta va incepe sa se miste spre stanga si in acelasi timp se va muta in jos pe axa Y
        elif inamicX[i] >= 736:
            inamicX_miscare[i] = -1.2
            inamicY[i] += inamicY_miscare[i]

        # Inamic Lovit
        lovire = inamic_lovit(inamicX[i], inamicY[i], glontX, glontY)
        if lovire:
            sunet_inamic_mort = mixer.Sound('Sunet_Gaina_Moarta.wav')
            sunet_inamic_mort.play()
            glontY = 480
            glont_stare = "pregatit"
            val_scor += 1
            # Adaugare inamic in plus la fiecare 10 inamici morti
            if val_scor % 10 == 0:
                numar_inamici += 1
                AvatarInamic.append(pygame.image.load('Gaina_62X51px.png'))
                inamicX.append(random.randint(0, 736))
                inamicY.append(random.randint(50, 150))
                inamicX_miscare.append(1.2)
                inamicY_miscare.append(30)
            inamicX[i] = random.randint(0, 736)
            inamicY[i] = random.randint(50, 150)

        inamic(inamicX[i], inamicY[i], i)

    # Miscarea Glontului
    # Daca valoarea pe axa Y a glontului devine mai mica sau egala cu 0, glontul revine la starea sa initiala
    if glontY <= 0:
        glontY = 480
        glont_stare = "pregatit"
    # Daca glontul a fost tras, apasand pe tasta SPACE, acesta va fi activat si in acelasi timp valoarea sa pe axa Y va scade
    if glont_stare == "tras":
        trage_glont(glontX, glontY)
        glontY -= glontY_miscare

    jucator(jucatorX, jucatorY)
    afis_scor(textX, textY)
    afis_sunet(text_volum_X, text_volum_p_Y, text_volum_m_Y)
    pygame.display.update()
