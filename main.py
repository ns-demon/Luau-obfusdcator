# shi is js open source 
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import secrets
import uuid
import os
import random


def rand_name():
    return "_" + secrets.token_hex(10)


def generate_notes(amount=5000):
    notes = []

    words = [
        "scriptobfuscatedby1.sm_ondiscord",
        "AuroraLuauProtector",
        "AdvancedRuntimeSystem",
        "SecureExecutionModule",
        "BytecodeProcessingLayer",
        "ScriptOptimizationEngine",
        "LuauCompatibilityFramework",
        "DynamicProtectionHandler",
        "VirtualEnvironmentModule",
        "InternalCompilerSystem"
    ]

    for _ in range(amount):
        notes.append(
            "-- "
            + random.choice(words)
            + "_"
            + secrets.token_hex(32)
        )

    return "\n".join(notes)


def create_key():
    return [
        secrets.randbelow(256)
        for _ in range(32)
    ]


def encrypt(data, key):
    encrypted = []

    for i, byte in enumerate(data):
        encrypted.append(
            byte ^ key[i % len(key)]
        )

    return encrypted



def obfuscate(source, note):

    key = create_key()

    encrypted = encrypt(
        source.encode("utf-8"),
        key
    )


    data = rand_name()
    keys = rand_name()
    output = rand_name()
    index = rand_name()


    header = generate_notes()


    custom_note = ""

    if note:
        custom_note = "-- " + note + "\n\n"


    lua = f"""
{custom_note}
{header}

local {data} = {{
{",".join(map(str, encrypted))}
}}

local {keys} = {{
{",".join(map(str,key))}
}}

local {output} = ""

for {index}=1,#{data} do

    {output} =
    {output} ..
    string.char(
        bit32.bxor(
            {data}[{index}],
            {keys}[(({index}-1)%#{keys})+1]
        )
    )

end


local func, err = loadstring({output})

if not func then

    warn("Luau decode error:")
    warn(err)

else

    func()

end


{generate_notes()}
"""

    return lua



def obfuscate_button():

    source = text.get(
        "1.0",
        tk.END
    )


    if not source.strip():

        if os.path.exists("scriptinput.txt"):

            with open(
                "scriptinput.txt",
                "r",
                encoding="utf-8"
            ) as f:
                source=f.read()

        else:

            messagebox.showerror(
                "Missing Script",
                "No Lua script found."
            )

            return


    add_note = messagebox.askyesno(
        "Custom Note",
        "Add a note at the top?"
    )


    note = ""

    if add_note:

        note = simpledialog.askstring(
            "Note",
            "Enter note:"
        ) or ""


    result = obfuscate(
        source,
        note
    )


    filename = (
        "scriptobfuscatedby1.sm_ondiscord_"
        + uuid.uuid4().hex[:12]
        + ".lua"
    )


    with open(
        filename,
        "w",
        encoding="utf-8"
    ) as f:
        f.write(result)


    messagebox.showinfo(
        "Complete",
        "Saved:\n\n" +
        os.path.abspath(filename)
    )



def open_file():

    path = filedialog.askopenfilename(
        filetypes=[
            ("Lua Script","*.lua"),
            ("Text","*.txt")
        ]
    )

    if path:

        with open(
            path,
            "r",
            encoding="utf-8"
        ) as f:

            text.delete(
                "1.0",
                tk.END
            )

            text.insert(
                "1.0",
                f.read()
            )



root = tk.Tk()

root.title(
    "Aurora Luau Protector by 1.sm."
)

root.geometry(
    "900x650"
)

root.configure(
    bg="#061827"
)


title = tk.Label(
    root,
    text="Aurora Luau Protector",
    font=("Segoe UI",26,"bold"),
    fg="#4fd8ff",
    bg="#061827"
)

title.pack(
    pady=20
)


text = tk.Text(
    root,
    bg="#02090f",
    fg="#8beaff",
    insertbackground="white",
    font=("Consolas",11)
)

text.pack(
    expand=True,
    fill="both",
    padx=20,
    pady=10
)


tk.Button(
    root,
    text="Open Lua File",
    command=open_file,
    bg="#006ca8",
    fg="white"
).pack(
    pady=5
)


tk.Button(
    root,
    text="Obfuscate Script",
    command=obfuscate_button,
    bg="#009cff",
    fg="white",
    font=("Segoe UI",12,"bold")
).pack(
    pady=10
)


if os.path.exists("scriptinput.txt"):

    with open(
        "scriptinput.txt",
        "r",
        encoding="utf-8"
    ) as f:

        text.insert(
            "1.0",
            f.read()
        )


root.mainloop()
