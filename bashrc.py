import discord
from colorama import Fore
import consts
import sqlite3

#  base de donnée sqlite
# name=Color
# machine=Color
# dir=Color
# prompt=Color
# title=Title of the window

def init_bd():
    conn = sqlite3.connect("bashrc.db")
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS bashrc (user_id PRIMARY KEY NOT NULL, name TEXT, machine TEXT, dir TEXT, prompt TEXT, title TEXT, Use_VT TEXT)")
    conn.commit()
    conn.close()

def init_bashrc(user_id: int):
    """SQlite """
    conn = sqlite3.connect("bashrc.db")
    c = conn.cursor()
    c.execute("SELECT * FROM bashrc WHERE user_id=?", (user_id,))
    data = c.fetchone()
    if(data is None):
        c.execute("INSERT INTO bashrc VALUES (?, ?, ?, ?, ?, ?, ?)", (user_id, "BLACK", "BLACK", "BLACK", "BLACK", "Terminal", "False"))
        conn.commit()
        conn.close()
    else:
        conn.close()


def del_bashrc(user_id: int):
    """SQlite """
    conn = sqlite3.connect("bashrc.db")
    c = conn.cursor()
    c.execute("DELETE FROM bashrc WHERE user_id=?", (user_id,))
    conn.commit()
    conn.close()

def have_bashrc(user_id: int):
    """SQLite"""
    conn = sqlite3.connect("bashrc.db")
    c = conn.cursor()
    c.execute("SELECT * FROM bashrc WHERE user_id=?", (user_id,))
    data = c.fetchone()
    if(data is None):
        conn.close()
        return False
    else:
        conn.close()
        return True

def change_value(user_id: str, key: str, value: str):
    """SQLite"""
    conn = sqlite3.connect("bashrc.db")
    c = conn.cursor()
    c.execute(f"UPDATE bashrc SET {key}=? WHERE user_id=?", (value, str(user_id)))
    conn.commit()
    conn.close()
    

def verif_color(color: str):
    if(color in consts.COLOR):
        return True
    else:
        return False
    

# Change value

def change_name_color(user_id: str, color: str):
    try:
        if(verif_color(color) and have_bashrc(user_id)):
            change_value(user_id, "name", color)
        else:
            return False
        return True
    except:
        return False

def change_machine_color(user_id: int, color: str):
    try:
        if(verif_color(color) and have_bashrc(user_id)):
            change_value(user_id, "machine", color)
        else:
            return False
        return True
    except:
        return False

def change_dir_color(user_id: int, color: str):
    try:
        if(verif_color(color) and have_bashrc(user_id)):
            change_value(user_id, "dir", color)
        else:
            return False
        return True
    except:
        return False

def change_prompt_color(user_id: int, color: str):
    try:
        if(verif_color(color) and have_bashrc(user_id)):
            change_value(user_id, "prompt", color)
        else:
            return False
        return True
    except:
        return False

def change_title(user_id: int, title: str):
    try:
        if(have_bashrc(user_id)):
            change_value(user_id, "title", title)
        else:
            return False
        return True
    except:
        return False

def change_use_vt(user_id: int, value: str):
    try:
        if(have_bashrc(user_id)):
            change_value(user_id, "Use_VT", value)
        else:
            return False
        return True
    except:
        return False

# Get value

def get_value(user_id: int, value: str):
    """SQLite"""
    v = {
        "name": 0,
        "machine": 1,
        "dir": 2,
        "prompt": 3,
        "title": 4,
        "Use_VT": 5
    }
    conn = sqlite3.connect("bashrc.db")
    c = conn.cursor()
    c.execute("SELECT name, machine, dir, prompt, title, Use_VT FROM bashrc WHERE user_id=?", (user_id,))
    data = c.fetchone()
    if(data is None):
        conn.close()
        return False
    else:
        conn.close()
        return data[v[value]]

def get_name_color(user_id: int):
    return get_value(user_id, "name")

def get_machine_color(user_id: int):
    return get_value(user_id, "machine")

def get_dir_color(user_id: int):
    return get_value(user_id, "dir")

def get_prompt_color(user_id: int):
    return get_value(user_id, "prompt")

def get_title(user_id: int):
    return get_value(user_id, "title")

def get_use_vt(user_id: int):
    return get_value(user_id, "Use_VT")

# Generate a bashrc

def genere_bashrc(user_id: int) -> str:
    #name_color = get_name_color(user_id)
    #machine_color = get_machine_color(user_id)
    #dir_color = get_dir_color(user_id)
    #prompt_color = get_prompt_color(user_id)

    color_name = consts.COLOR[get_name_color(user_id)]
    color_machine = consts.COLOR[get_machine_color(user_id)]
    color_directory = consts.COLOR[get_dir_color(user_id)]
    following_text = consts.COLOR[get_prompt_color(user_id)]

    title = get_title(user_id)
    if(get_use_vt(user_id) == "True"):
        use_vt = "test -e /home/infoetu/valentin.thuillier.etu/bashrc && . /home/infoetu/valentin.thuillier.etu/bashrc"
    else:
        use_vt = "# test -e /home/infoetu/valentin.thuillier.etu/bashrc && . /home/infoetu/valentin.thuillier.etu/bashrc"
    return f"""# Generated by BasteRC 
test -e /home/public/admin/bashrc && . /home/public/admin/bashrc
{use_vt}

PS1=\"\\[\\e[32m\\][\\[\\e[m\\]\\[\\e[{color_name}m\\]\\u\\[\\e[m\\]\\[\\e[33m\\]@\\[\\e[m\\]\\[\\e[{color_machine}m\\]\\h\\[\\e[m\\]:\\[\\e[{color_directory}m\\]\\w\\[\\e[m\\]\\[\\e[32m\\]]\\[\\e[m\\]\\[\\e[{following_text}m\\]\\$\[\\e[{following_text}m\\] \"
echo -en "\\033]0;{title}\\007"
"""