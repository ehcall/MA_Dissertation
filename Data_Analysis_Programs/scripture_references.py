import re

ref_books = ["Bible Dictionary","Guide to the Scriptures","Topical Guide","Joseph Smith Translation"]
hebrew_bible = ["Genesis","Exodus","Leviticus",'Lev\.',"Numbers","Deuteronomy","Joshua","Judges","Ruth","1 Samuel","2 Samuel",
                "1 Kings","2 Kings","1 Chronicles","2 Chronicles","Ezra","Nehemiah","Esther","Job","Psalms", "Psalm [0-9]",
                "Proverbs","Ecclesiastes","Song of Solomon","Isaiah","Jeremiah","Lamentations","Ezekiel","Daniel",
                "Hosea","Joel", "Amos","Obadiah","Jonah","Micah","Nahum","Habakkuk","Zephaniah","Haggai","Zechariah",
                "Malachi"]
new_testament = ["Matthew","Mark","Luke","John","Acts","Romans","1 Corinthians","2 Corinthians","Galatians","Ephesians",
                 "Philippians","Colossians","1 Thessalonians","2 Thessalonians","1 Timothy","2 Timothy","Titus",
                 "Philemon","Hebrews","James","1 Peter","2 Peter","1 John","2 John","3 John","Jude","Revelation"]
book_of_mormon = ["Testimony of Three Witnesses","Testimony of Eight Witnesses","1 Nephi","2 Nephi","2 Ne\.", "Jacob","Enos",
                  "Jarom","Omni","Words of Mormon","Mosiah","Alma","Helaman","3 Nephi","4 Nephi","Mormon",
                  "Ether","Moroni"]
d_and_c = ["Explanatory Introduction to the Doctrine and Covenants","Doctrine and Covenants","D&C",'D&amp;C']
pearl_of_great_price = ["Moses","Abraham","Joseph Smith—Matthew","Joseph Smith — Matthew","Joseph Smith—History",
                        "Joseph Smith — History","Articles of Faith"]

def check_book_name(line):
    for book in ref_books:
        if re.search(book, line):
            return True
    for book in hebrew_bible:
        if re.search(book, line):
            return True
    for book in new_testament:
        if re.search(book, line):
            return True
    for book in book_of_mormon:
        if re.search(book, line):
            return True
    for book in d_and_c:
        if re.search(book, line):
            return True
    for book in pearl_of_great_price:
        if re.search(book, line):
            return True
    return False

def remove_extras(line):
    line = re.sub(" ?[Ss]ee also ?",'',line)
    line = re.sub(" ?[Ss]ee ?",'',line)
    #line = re.sub("italics added",'',line)
    return line
def check_if_scripture(line):
    line = remove_extras(line)
    false_options = ['Mormon Doctrine','History of the Church','Journal of Discourses','Doctrines of Salvation',
                     'Joseph Smith Papers','New Era','Ensign','Liahona','Authorship','Revelations in Context',
                     'Messianic','Student Manual','Teachings of','First Presidency letter','Encyclopedia','Pioneer',
                     'A New Witness','josephsmithpapers','Ante-Nicene','Discourses','The Articles','Story Gems',
                     'Tullidge','James R. Clark','Conference Report','Church History and Modern Revelation','Lyndon',
                     'Robert J. Matthews','Orson Hyde','Gospel Topics']
    for f_o in false_options:
        if re.search(f_o, line):
            return False

    if check_book_name(line):
        return True
    elif re.search("verses? [0-9]",line):
        return True
    elif re.search("section heading",line):
        return True
    elif re.search("footnote",line):
        return True
    elif not re.search('[A-z]',line):
        return True
    else:

        return False

def check_scripture_phrase(quote):
    return