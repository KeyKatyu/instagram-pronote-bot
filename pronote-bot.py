import pronotepy, schedule, time, datetime, re
from pronotepy.ent import YOUR_ENT_HERE
from instagrapi import Client
from PIL import Image, ImageFont, ImageDraw

client = pronotepy.Client('https://PRONOTE_URL_LIKE_THAT.index-education.net/pronote/eleve.html',
                          username='YOUR_PRONOTE_USERNAME_HERE',
                          password='AND_YOUR_PASSWORD',
                          ent=YOUR_ENT_HERE)
instagram = Client()
instagram.login("YOUR_INSTA_ACCOUNT_USERNAME_HERE", "AND_YOUR_INSTA_PASSWORD")
thread = instagram.direct_threads(1)[0]

grades_already_published = []
canceled_lessons_already_published = []

def getIfThereIsANewNote():
    for grade in client.current_period.grades:
        if grade.comment not in grades_already_published:
            instagram.direct_send("🆕 NOUVELLE NOTE 🆕\n" +
                "\n➡️ " + grade.subject.name + " ⬅️"
                + "\n" + grade.comment 
                + "\n\nNote ➕ " + grade.max 
                + "\nNote ➖ " + grade.min 
                + "\nCoefficient ✖️ " + grade.coefficient
                + "\nMoyenne de la classe ⭐ " + grade.average,
                thread_ids=[thread.id])
            print("NOUVELLE NOTE DÉTECTÉE : message envoyé !")
            grades_already_published.append(grade.comment)

    print("- Vérif. NN : " + datetime.datetime.now().strftime("%d/%m/%Y à %Hh %Mm %Ss"))
    client.keep_alive()
    
def getIfThereIsAnAbsentProfessor():
    listOfLessons = client.lessons(datetime.date.today(), datetime.date.today() + datetime.timedelta(days=5))
    for lesson in listOfLessons:
        if lesson.status == "Prof. absent" and lesson.subject.name + " " + lesson.start.strftime('Le %d/%m/%Y à %H:%M') not in canceled_lessons_already_published and lesson.teacher_name != "IF YOU WANT TO EXCLUDE SOME TEACHER OF THE CHECK":
            instagram.direct_send("🚫 PROF. ABSENT 🚫\n" +
                "\n➡️ " + lesson.subject.name + " ⬅️"
                + "\n\n🧍 " + lesson.teacher_name
                + "\n🔥 " + lesson.status
                + "\n📅 " + lesson.start.strftime('Le %d/%m/%Y à %H:%M'),
                thread_ids=[thread.id])
            print("PROFESSEUR ABSENT DÉTECTÉ : message envoyé !")
            canceled_lessons_already_published.append(lesson.subject.name + " " + lesson.start.strftime('Le %d/%m/%Y à %H:%M'))

    print("- Vérif. PA : " + datetime.datetime.now().strftime("%d/%m/%Y à %Hh %Mm %Ss"))
    client.keep_alive()

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
        if(len(food) > 20):
            modified = replacenth(food, " ", "\n", check_spaces(food))
            menu_text += "\n- " + modified
        else:
            menu_text += "\n- " + food

    image_editable = ImageDraw.Draw(menu_image)
    image_editable.text((550,470), title_text, (255, 255, 255), font=title_font)
    image_editable.text((35,630), menu_text, (255, 255, 255), font=menu_font)
    menu_image.save("bot/menu_results/" + datetime.datetime.now().strftime("%d%m%Y") + ".jpg")

    instagram.photo_upload_to_story('bot/menu_results/' + datetime.datetime.now().strftime("%d%m%Y") + ".jpg")
    print("CANTINE : menu du jour publié !")

if client.logged_in:
    for grade in client.current_period.grades:
        grades_already_published.append(grade.comment)

    listOfLessons = client.lessons(datetime.date.today(), datetime.date.today() + datetime.timedelta(days=5))
    for lesson in listOfLessons:
        if lesson.status == "Prof. absent" and lesson.subject.name + " " + lesson.start.strftime('Le %d/%m/%Y à %H:%M') not in canceled_lessons_already_published and lesson.teacher_name != "IF YOU WANT TO EXCLUDE SOME TEACHER OF THE CHECK":
            canceled_lessons_already_published.append(lesson.subject.name + " " + lesson.start.strftime('Le %d/%m/%Y à %H:%M'))

    print("PRONOTEBOT - Démarré le " + datetime.datetime.now().strftime("%d/%m/%Y à %Hh %Mm %Ss"))
    schedule.every(HERE_YOU_CAN_EDIT_THE_SCHEDULE).minutes.do(getIfThereIsANewNote)
    schedule.every(AND_HERE_TOO_I_PRECISE_IN_MINUTES_BTW).minutes.do(getIfThereIsAnAbsentProfessor)
    schedule.every().monday.at("THE HOUR SCHEDULE IN FORMAT HH:MM").do(retrieveCanteenMenuInStory)
    schedule.every().tuesday.at("10:35").do(retrieveCanteenMenuInStory)
    schedule.every().wednesday.at("LIKE THAT").do(retrieveCanteenMenuInStory)
    schedule.every().thursday.at("DO YOU UNDERSTAND ?").do(retrieveCanteenMenuInStory)
    schedule.every().friday.at("xd").do(retrieveCanteenMenuInStory)
else:
    print("Un problème est survenu lors de la connexion à l'ENT.")
    exit()

while 1:
    schedule.run_pending()
    time.sleep(1)
