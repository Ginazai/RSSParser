import urllib.parse, urllib.request, urllib.error;
import xml.etree.ElementTree as ET;
import sqlite3;
import re;
import codecs;
import sys;
import time;

def sleepInRange(msg = "", tts = int, hmt = int):
    r = 1;
    sys.stdout.write(msg);
    while r <= hmt:
        time.sleep(tts);
        sys.stdout.write(".");
        r += 1;
    print('\n');

aw = "it's not neccesary to add the" + '".sqlite"' + "termination:" + '\n';
db = input("Name the Database (make sure you don't reuse a name from a database in the same folder or it will result in overwrite)" +
                 '\n' + aw);

def database():
    conn = sqlite3.connect(db + '.sqlite');
    cursor = conn.cursor();

    cursor.executescript('''
    CREATE TABLE IF NOT EXISTS anime (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    title TEXT UNIQUE);

    CREATE TABLE IF NOT EXISTS episode (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    anime_id INETEGER,
    title TEXT,
    desc TEXT,
    link TEXT,
    chapter INTEGER,
    minutes INTEGER, 
    seconds INTEGER);''');

    page = 'https://www.crunchyroll.com/rss/anime/popular?lang=esES';
    sleepInRange("connecting", 1, 5);
    url = urllib.request.urlopen(page).read().decode();
    xml = ET.fromstring(url);
    print(str(len(xml[0])) + " elements retrieve");
    i = 0;
    links = list();
    while i <= len(xml[0]):
        for data in xml[0]:
            next = str(data);
            next = next.split();
            if next[1] == "'item'":
                #anime Title
                anime_title = data[14].text;
                print('\n' + str(i) + " " + anime_title);
                #episode
                episode = data[15].text;
                print("episode: " + episode);
                #chapter number
                capn = data[16].text;
                print("number of episode: " + capn);
                try:
                    #retrieve Minutes and Seconds
                    lng_init = int(data[17].text);
                    min = int(lng_init/60);
                    sec = round(lng_init % 60);
                    lng = str(min) + "min:" + str(sec) + "s";
                    print("duration: " + lng);
                except:
                    min = 0;
                    sec = 0;
                    print("(no episode length data was found for: " + anime_title + ")");
                try:
                    #retrieve the description
                    desc = data[3].text;
                    desc = desc.split("/>");
                    desc = desc[2];
                    print("descriptioon: " + desc);
                except:
                    desc = "No description.";
                 #this function checks if the link belongs to the large image
                def getLink(dictionary = dict()):
                    for k, v in dictionary.items():
                        url = v;
                        if (re.search('large.jpg\Z', url)): #simple regular expression that just checks the end of the name '\Z'
                            return url;
                 #this function check whether the param is inavalid to avoid it (provisional)
                def check (list = list(), param = ""):
                    if param != None:
                        list.append(param);

                #HERE GOES A FUNCTION THAT CHECK FOR THE INDEX OF THE POSITION OF THE URL TO THEN SEARCH THE LARGE IMG AND RETRIEVE IT.
                def searchLink():
                    x = 24;
                    while x <= 30:
                        link = data[x].attrib;
                        link = getLink(link);
                        x +=1;
                        if link == None:
                            continue;
                        else:
                            return link;
                #try to get the link. Since i cant be sure that it is gonna fid it 100% of the time it has except
                try:
                    link1 = searchLink();
                    print("link: " + link1);
                except:
                      pass;

                #inserting in a database to get data in place.
                cursor.execute('''INSERT OR IGNORE INTO anime (title) VALUES (?)''', (anime_title,));
                cursor.execute('''SELECT id FROM anime WHERE title = ?''', (anime_title,));
                anime_id = cursor.fetchone()[0];  
            
                #DO NOT UNCOMMENT. This suppose to verify wether the episode is already in, but instead it retrieve less values which traduce in less data. 
                #
                #try:
                    #cursor.execute('SELECT title FROM episode WHERE anime_id = ? AND title = ?', (anime_id, episode));
                    #et = cursor.fetchone()[0];
                    #if (et == episode): continue;
                #except:
                    #pass; #4. get out if it's not the case

                cursor.execute('''INSERT INTO episode (anime_id, title, desc, link, chapter, minutes, seconds) VALUES
                (?, ?, ?, ?, ?, ?, ?)''', (anime_id, episode, desc, link1, capn, min, sec));
                sys.stdout.write("inserting...\n");
                conn.commit();
            i += 1;
    print("Database successfully created.");


def jsParse(js = "", animejs = ""):
    if (js == None): js = 'NoName';
    if (animejs == None): animejs = 'anime';
    conn = sqlite3.connect(db + '.sqlite');
    cursor = conn.cursor();

    fhand = codecs.open(js + '.js', 'w', 'utf-8');
    animeh = codecs.open(animejs + '.js', 'w', 'utf-8');
    fhand.write('popular = [\n');
    animeh.write('animes = [\n');

    animes = dict();
    cursor.execute("SELECT * FROM anime");
    for element in cursor:
        anime_id = element[0];
        name = element[1];
        animes[anime_id] = name;
        f_out = ('[' + '"' + name + '"' + '],\n');
        animeh.write(f_out);
    cursor.execute("SELECT * FROM episode");
    for row in cursor:
        internal_id = row[1];

        episode_name = str(row[2]);
        image = str(row[4]);
        episode_num = str(row[7]);
        minutes = str(row[5]);
        seconds = str(row[6]);
        desc = str(row[3]);

        anime_title = animes[internal_id];
        print("Anime title: " + anime_title);
        print("episode: " + episode_name);
        print("description: " + desc);
        print("link: " + image);
        print("number of cha: " + str(episode_num));
        print("min: " + str(minutes));
        print("sec: " + str(seconds));

        output = ("[" + '"' + anime_title + '"' + ", " + '"' + episode_name + '"' + ", " +
                  '"' + episode_num + '"' + ", " + '"' + image + '"' + ", " + minutes + ", " +
                  seconds + ", " + "'" + desc + "'" + "],\n");
        fhand.write(output);
    fhand.write("]");
    animeh.write("]");

database();
sleepInRange("\nStarting JS creation", 1, 3);
jsn = input("\n(Leave this field empty will autoassign a name. If you restart the program again without give a name the second time it will result in rewritte the js. It is not necessary ad the" + '".js"' + "termination)" + 
            "\nName the JS file:\n");
animejsn = input('\nYou can also name the anime js:' + '\n');
jsParse(jsn, animejsn);
