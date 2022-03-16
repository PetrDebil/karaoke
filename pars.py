import time
import os
import json

def sindex_main_page(name_song):  # создает и заполяет html файл пести
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(executable_path="D:\\program\\chromedriver.exe", options=options)
    url = "https://genius.com/"
    try:
        driver.get(url=url)
        time.sleep(0.5)
        song_name_input = driver.find_element_by_tag_name("input")
        song_name_input.send_keys(name_song + Keys.ENTER)
        time.sleep(2)
        #
        song_href = driver.find_element_by_xpath("//div[@class='mini_card-thumbnail clipped_background_image--background_fill clipped_background_image']")
        song_href.click()
        time.sleep(4)
        #
        src = driver.page_source
        time.sleep(2)
        with open("index.html", 'w', encoding="utf-8") as file:
            file.write(src)
    except Exception:
        return "error"
    finally:
        driver.close()
        driver.quit()


def song_creater(name_song):
    with open("songs\\names_write_names.json", "r", encoding="utf-8") as file:
        src = file.readlines()
    for i in src:
        aname, bname = i.split('_')
        if aname == name_song:
            bname = bname[:-1]
            return bname
    sindex_main_page(name_song)
    song_name = bs4_song()
    bs4_song()
    with open("songs\\names_write_names.json", "a", encoding="utf-8") as file:
        file.write(f"{name_song.lower()}_{song_name} \n")
    return song_name


def bs4_song():  # creating  (song_name).txt
    from bs4 import BeautifulSoup
    all_text_read = []
    with open("index.html", encoding="utf-8") as file:
        src = file.read()
    soup = BeautifulSoup(src, "lxml")
    all_texts = soup.find_all("div", class_="Lyrics__Container-sc-1ynbvzw-6 jYfhrf")
    name_song = soup.find("h2", class_="TextLabel-sc-8kw9oj-0 Lyrics__Title-sc-1ynbvzw-0 hHEDka").text
    with open(f"songs\\{name_song}.txt", 'w', encoding="utf-8") as file:
        file.write("")
    for all_text in all_texts:
        all_text = str(all_text)
        zamena = ["<br>", "<br/>", "__", "___"]
        for znach in zamena:
            if znach in all_text:
                all_text = all_text.replace(f"{znach}", "_")
        soup = BeautifulSoup(all_text, "lxml")
        all_text = soup.text

        all_text = all_text.replace('_', '\n')

        s = all_text.split('\n')

        for i in s:
            st = []
            if int(len(i)) > 80:
                while int(len(i)) > 80:
                    st.append(i[:int(len(i)) // 2])
                    i = i.replace(i[:int(len(i)) // 2], '')
                st.append(i)
                for _ in st:
                    all_text_read.append(_)
            else:
                k = i
                all_text_read.append(k)
    try:
        all_text_read.remove('')
    except Exception:
        pass
    for i in all_text_read:
        if 'Текст песни' in i:
            all_text_read.remove(i)
    with open(f"songs\\{name_song}.txt", 'a', encoding="utf-8") as file:
        for i in all_text_read:
            file.write(i + "\n")
    return name_song

def main_menu():
    import tkinter
    try:
        os.mkdir("songs")
        with open("songs\\names_write_names.json", "w", encoding="utf-8") as file:
            file.write('')
    except Exception:
        pass

    def clicked():
        name_song = txt.get()
        name_song = song_creater(name_song)
        lbl.destroy()
        txt.destroy()
        btn.destroy()
        time.sleep(0.5)
        with open(f"songs\\{name_song}.txt", encoding="utf-8") as file:
            src = file.read()



        lxl = tkinter.Label(window, text=f"{name_song}", font="Arial 25", bd=50, width=100)
        lxl.grid(column=0, row=0)
        all_text = src.split('\n')
        def next_():
            k = 3
            s = ''
            for i in range(k - 1):
                s = all_text[i] + '\n' + all_text[i + 1] + '\n' + all_text[i + 2] + '\n' + all_text[i + 3] + '\n\n'
                all_text.remove(all_text[i])
            sng.configure(text=s)

        time.sleep(0.5)
        sng = tkinter.Label(window, text='', font="Arial 14", bd=50, width=100)
        sng.grid(column=0, row=1)
        btnn = tkinter.Button(window, text="next", command=next_, font="Arial 23", width=20, bd=5)
        btnn.grid(column=0, row=2)

    window = tkinter.Tk()
    window.title("Караоке Владика")
    window.geometry('1920x1080')
    lbl = tkinter.Label(window, text="Введите название песни", font="Arial 25", bd=50, width=100)
    lbl.grid(column=0, row=0)
    txt = tkinter.Entry(window, width=50, font="Arial 25", bd=3)
    txt.grid(column=0, row=1)
    btn = tkinter.Button(window, text="Поиск песни", command=clicked, font="Arial 23", width=20, bd=5)
    btn.grid(column=0, row=2)

    window.mainloop()


def main():
    main_menu()


if __name__ == "__main__":
    main()
