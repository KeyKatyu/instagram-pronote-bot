import pronotepy, schedule, time, datetime, re
from pronotepy.ent import your_ent
from instagrapi import Client
from instagrapi.types import StoryMention
from PIL import Image, ImageFont, ImageDraw

client = pronotepy.Client('https://pronoteurl.index-education.net/pronote/eleve.html',
                          username='pronote id',
                          password='pronote password',
                          ent=your_ent if needed)
instagram = Client()
instagram.login("insta id", "insta password")
thread = insta_thread_id

grades_already_published = []
canceled_lessons_already_published = []

def getIfThereIsANewNote():
    for grade in client.current_period.grades:
        if grade.comment + " en " + grade.subject.name not in grades_already_published:
            instagram.direct_send("🆕 NOUVELLE NOTE 🆕\n" +
                "\n➡️ " + grade.subject.name + " ⬅️"
                + "\n" + grade.comment 
                + "\n\nNote ➕ " + grade.max + "/" + grade.out_of
                + "\nNote ➖ " + grade.min + "/" + grade.out_of
                + "\nCoefficient ✖️ " + grade.coefficient
                + "\nMoyenne ⭐ " + grade.average,
                thread_ids=[thread])
            print("NOUVELLE NOTE DÉTECTÉE : message envoyé !")
            grades_already_published.append(grade.comment + " en " + grade.subject.name)

    print("-> Vérif. NN : " + datetime.datetime.now().strftime("%d/%m/%Y à %Hh %Mm %Ss"))
    
def getIfThereIsAnAbsentProfessor():
    listOfLessons = client.lessons(datetime.date.today(), datetime.date.today() + datetime.timedelta(days=5))
    for lesson in listOfLessons:
        if lesson.status == "Prof. absent" and lesson.subject.name + " " + lesson.start.strftime('Le %d/%m/%Y à %H:%M') not in canceled_lessons_already_published and lesson.teacher_name != "Teachers' names who you want to be excluded":
            instagram.direct_send("🚫 PROF. ABSENT 🚫\n" +
                "\n➡️ " + lesson.subject.name + " ⬅️"
                + "\n\n🧍 " + lesson.teacher_name
                + "\n🔥 " + lesson.status
                + "\n📅 " + lesson.start.strftime('Le %d/%m/%Y à %H:%M'),
                thread_ids=[thread])
            print("PROFESSEUR ABSENT DÉTECTÉ : message envoyé !")
            canceled_lessons_already_published.append(lesson.subject.name + " " + lesson.start.strftime('Le %d/%m/%Y à %H:%M'))

    print("-> Vérif. PA : " + datetime.datetime.now().strftime("%d/%m/%Y à %Hh %Mm %Ss"))
    
    if client.session_check():
        print("-> PRONOTE SESSION RENEWED")

def replacenth(string, sub, wanted, n):
        where = [m.start() for m in re.finditer(sub, string)][n - 1]
        before = string[:where]
        after = string[where:]
        after = after.replace(sub, wanted)
        newString = before + after
        return newString

def check_spaces(string):
    count = 0
    for i in range(0, len(string)):
        if string[i] == " ":
            count += 1
    return count

def retrieveCanteenMenuInStory():
    todayMenu = client.menus(datetime.date.today(), datetime.date.today() + datetime.timedelta(days=1))

    if not todayMenu:
        print("CANTINE : Jour férié, aucun menu publié !")
        return

    menu = []
    for starter in todayMenu[0].first_meal:
        menu.append(starter.name)

    for main in todayMenu[0].main_meal:
        menu.append(main.name)

    for side in todayMenu[0].side_meal:
        menu.append(side.name)

    for cheese in todayMenu[0].cheese:
        menu.append(cheese.name)

    for dessert in todayMenu[0].dessert:
        menu.append(dessert.name)

    menu_image = Image.open("bot/menu_patern.jpg")
    menu_font = ImageFont.truetype('bot/menu_font.ttf', 110)
    title_font = ImageFont.truetype('bot/title_font.ttf', 150)
    title_text = datetime.datetime.now().strftime("%d/%m/%Y")
    menu_text = ""
    for food in menu:
        if(len(food) > 19):
            modified = replacenth(food, " ", "\n", check_spaces(food))
            menu_text += "\n- " + modified
        else:
            menu_text += "\n- " + food

    image_editable = ImageDraw.Draw(menu_image)
    image_editable.text((550,470), title_text, (255, 255, 255), font=title_font)
    image_editable.text((35,630), menu_text, (255, 255, 255), font=menu_font)
    menu_image.save("bot/menu_results/" + datetime.datetime.now().strftime("%d%m%Y") + ".jpg")

    instagram.photo_upload_to_story('bot/menu_results/' + datetime.datetime.now().strftime("%d%m%Y") + ".jpg",
        mentions=[StoryMention(user=instagram.user_info_by_username('insta user you want to @ in the story'))])
    print("CANTINE : Menu du jour publié !")

if client.logged_in:
    for grade in client.current_period.grades:
        grades_already_published.append(grade.comment + " en " + grade.subject.name)

    listOfLessons = client.lessons(datetime.date.today(), datetime.date.today() + datetime.timedelta(days=5))
    for lesson in listOfLessons:
        if lesson.status == "Prof. absent" and lesson.subject.name + " " + lesson.start.strftime('Le %d/%m/%Y à %H:%M') not in canceled_lessons_already_published and lesson.teacher_name != "Teachers' names who you want to be excluded":
            canceled_lessons_already_published.append(lesson.subject.name + " " + lesson.start.strftime('Le %d/%m/%Y à %H:%M'))

    print("PRONOTEBOT - Démarré le " + datetime.datetime.now().strftime("%d/%m/%Y à %Hh %Mm %Ss"))
    schedule.every(15).minutes.do(getIfThereIsANewNote)
    schedule.every(15).minutes.do(getIfThereIsAnAbsentProfessor)
    schedule.every().monday.at("12:25").do(retrieveCanteenMenuInStory)
    schedule.every().tuesday.at("12:25").do(retrieveCanteenMenuInStory)
    schedule.every().wednesday.at("11:30").do(retrieveCanteenMenuInStory)
    schedule.every().thursday.at("12:25").do(retrieveCanteenMenuInStory)
    schedule.every().friday.at("11:30").do(retrieveCanteenMenuInStory)
else:
    print("Un problème est survenu lors de la connexion à l'ENT.")
    exit()

while 1:
    schedule.run_pending()
    time.sleep(1)
