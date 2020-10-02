import feedparser;
import sqlite3;
import urllib.request, urllib.parse, urllib.error;
import codecs;
import sys;
import time;

def load(msg = "", t = int, hmt = int):
    i = 0;
    sys.stdout.write(msg);
    while i < hmt:
        sys.stdout.write('.');
        time.sleep(t);
        i +=1;

db = input('\nCreate a Database (keep in mind that reuse names or leave empty fields will not make any changes if the default or especified database exists and it will add all new content if the page is updated)\n');
if (db == None or db == ""): db = 'myDatabase';
web = input('(skip for default)The program would work at it best only with the "Popular Animes" from crunchyroll RSS, but you can try whatever you wish:\n');
if (web == "" or web == None): web = "https://www.crunchyroll.com/rss/anime/popular?lang=enEN";

def searchData():
    load("connecting", 1, 3);
    page = web;
    url = urllib.request.urlopen(page).read().decode();
    feedp = feedparser.parse(url);

    con = sqlite3.connect(db + '.sqlite');
    cursor = con.cursor();

    cursor.executescript('''
    CREATE TABLE IF NOT EXISTS anime (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    anime_title TEXT UNIQUE);

    CREATE TABLE IF NOT EXISTS episode (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    anime_id INTEGER,
    episode_title TEXT,
    desc TEXT,
    image TEXT,
    chapter TEXT,
    minutes INTEGER,
    seconds INTEGER,
    link TEXT);''');
    
    i = len(feedp.entries);
    j = 0;

    for line in feedp.entries[0]:
        print(line);


    while j < i:
        title_position = feedp.entries[j].title;
        title_position = title_position.strip();
        elements = title_position.split(" - ");

        try:
            anime = elements[0];
            episode = elements[1];
            chap_name = elements[2];

            desc = feedp.entries[j].description;
            d = desc.split("/>");
            descrip = d[2];

            lng = feedp.entries[j].crunchyroll_duration;
            c = int(lng); 
            min = int(c/60);
            sec = round(c%60);

            video_link = feedp.entries[j].link;
            thu = feedp.entries[j].media_thumbnail[0];
            thumb = thu['url']; 
        except:
            pass;

        print('\n'+str(j + 1)+'. inserting:');
        print(anime + ' ' + episode);
        print(chap_name + ': ');
        print(descrip);
        print('and it resources: \n' + video_link + '\n' + thumb);
        print('duration: ' + str(min) + 'min:' + str(sec)  + 's\n');

        
        cursor.execute('INSERT OR IGNORE INTO ANIME (anime_title) VALUES (?)', (anime,));
        cursor.execute('SELECT id FROM anime WHERE anime_title = ?', (anime,));
        anime_id = cursor.fetchone()[0];

        try:
            cursor.execute('SELECT episode_title FROM episode WHERE anime_id = ? AND episode_title = ?', (anime_id, chap_name));
            found = cursor.fetchone()[0];
            print("\n######################| " + found + " was already in |######################");
            j += 1;
            if (j == i): print('\nNo changes have been made.');
            continue;
        except:
            pass

        cursor.execute('''INSERT INTO episode (anime_id, episode_title, desc, image, chapter, minutes, seconds, link) VALUES
                      (?, ?, ?, ?, ?, ?, ?, ?)''', (anime_id, chap_name, descrip, thumb, episode, min, sec, video_link));


        j +=1;
        print(anime + " inserted.");
        con.commit();
        continue;
    cursor.close();
    con.close();


def confirm(quest = "", default = ""):
    param = input(quest);
    if (param == "0"):
        param = default;
    return param;


def createJs():
    con = sqlite3.connect(db + '.sqlite');
    cursor = con.cursor();

    cursor.execute('''SELECT anime_title, episode_title, desc, image, link, chapter, minutes, seconds 
                  FROM episode INNER JOIN anime ON anime.id = episode.anime_id''');

    defv =  "popular_anime_re";

    ep_db = confirm('\n(Enter to skip, 0 to skip all) Give a name to your ".js" file, it will contain the episodes data (leave the fill empty or assign a name from an existing ".js" in the same folder results in overwrite):\n', defv);
    if (defv == ep_db):
        an_db = "anime";
        en = 'popular';
        an = 'animes';
    else:
        ep_db = ep_db;
        if (ep_db == ""): ep_db = defv;
        an_db = input('\n(Enter to skip) Give a name to your anime database, as you can assume it save only the existing animes:\n');
        if (an_db == ""): an_db = "anime";
        en = input('\n(Enter to skip) Alternativly you can give a name for each data container (i.e. animes = []).\nOnly the name is needed:\n');
        if (en == ""): en = 'popular';
        an = input('\n(Enter to skip) Anime data container: \n');
        if (an == ""): an = 'animes';

    fh = codecs.open('../Web/resource/'+ ep_db + '.js', 'w', 'utf-8');
    af = codecs.open('../Web/resource/'+ an_db + '.js', 'w', 'utf-8');
    fh.write(en + ' = [\n');
    af.write(an + ' = [\n');

    i = -1;
    check = list();
    for row in cursor:
        is_in = True;
        anime = row[0];

        if not anime in check:
            check.append(anime);
            is_in = False;
            i += 1;

        pre_ep = row[1];
        episode_ti = pre_ep.replace('"', "'");

        predesc = row[2].replace('"', "'");
        predesc = predesc.replace("\n", " ");
        desc = predesc;

        img_link = row[3];
        vid_link = row[4];
        num_chap = row[5];
        min = row[6];
        sec = row[7];

        print(anime);
        print(episode_ti);
        print(desc);
        print(img_link);
        print(vid_link);
        print(num_chap);
        print(min);
        print(sec);

        epout = ("[" + '"' + anime + '"' +", " + '"' + episode_ti + '"' + ", " +
                 '"' + num_chap + '"' + ", "+ '"' + img_link + '"' + ", " + str(min) + ", " + str(sec) + ", " + '"' +
                 desc + '"' + ', ' + '"' + vid_link + '"' + "],\n");
        fh.write(epout);

        if (is_in == False): 
            anout = ("[" + '"' + check[i] + '"' + "],\n")
            af.write(anout);

    fh.write(']');
    af.write(']');
    con.commit();
    cursor.close();
    con.close();



i = 0;
while i < 1:
    print('\nWhat would you like to do with this database?\n');
    ans = input('1: Create it and process it\n2: Only create it\n3: only process it (keep it mind this option assume that the structure is identical to what this program produce)\n');
    if (ans == '1'):
        searchData();
        createJs();
        i += 1;
    elif (ans == '2'):
        searchData();
        i += 1;
    elif (ans == '3'):
        createJs();
        i += 1;
    else:
        print('Invalid argument');