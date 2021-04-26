"""

This GUI queries users on which garden they prefer, and whether they like, dislike, or are
neutral about each garden.

"""

import tkinter as tk
import json
import os
import pprint
import numpy as np
from numpy.random import default_rng
rng = default_rng()
import image_generation
import matplotlib.pyplot as plt

class Application(tk.Frame):
    def __init__(self, master=None):
        # super init and pack
        super().__init__(master)
        self.master = master
        self.pack()
        # all widget creation
        # subframes creation
        self.leftsubframe = tk.Frame(self)
        self.rightsubframe = tk.Frame(self)
        self.bottomsubframe = tk.Frame(self)

        self.leftbuttonssubframe = tk.Frame(self.leftsubframe)
        self.rightbuttonssubframe = tk.Frame(self.rightsubframe)

        # button creation and options setting
        # button commands
        self.prefer_left_command = lambda event=None: self.register_prefer_input("left")
        self.prefer_right_command = lambda event=None: self.register_prefer_input("right")
        self.left_like_command = lambda event=None: self.register_ordinal_input("left", "like")
        self.left_neutral_command = lambda event=None: self.register_ordinal_input("left", "neutral")
        self.left_dislike_command = lambda event=None: self.register_ordinal_input("left", "dislike")
        self.right_like_command = lambda event=None: self.register_ordinal_input("right", "like")
        self.right_neutral_command = lambda event=None: self.register_ordinal_input("right", "neutral")
        self.right_dislike_command = lambda event=None: self.register_ordinal_input("right", "dislike")

        # buttons
        self.p = tk.IntVar()
        self.lo = tk.IntVar()
        self.ro = tk.IntVar()
        self.response_to_int = {'like':1, 'neutral':2, 'dislike':3}

        self.radio_integers = [self.p, self.lo, self.ro]
        self.preferleft = tk.Radiobutton(self.leftbuttonssubframe, text='Prefer Left (E)',
                                    command=self.prefer_left_command, variable=self.p, value=1)
        self.preferright = tk.Radiobutton(self.rightbuttonssubframe, text='Prefer Right (I)',
                                     command=self.prefer_right_command, variable=self.p, value=2)

        self.leftlike = tk.Radiobutton(self.leftbuttonssubframe, text='Like (F)',
                                  command=self.left_like_command, variable=self.lo, value=1)
        self.leftneutral = tk.Radiobutton(self.leftbuttonssubframe, text='Neutral (D)',
                                     command=self.left_neutral_command, variable=self.lo, value=2)
        self.leftdislike = tk.Radiobutton(self.leftbuttonssubframe, text='Dislike (S)',
                                     command=self.left_dislike_command, variable=self.lo, value=3)

        self.rightlike = tk.Radiobutton(self.rightbuttonssubframe, text='Like (J)',
                                   command=self.right_like_command, variable=self.ro, value=1)
        self.rightneutral = tk.Radiobutton(self.rightbuttonssubframe, text='Neutral (K)',
                                      command=self.right_neutral_command, variable=self.ro, value=2)
        self.rightdislike = tk.Radiobutton(self.rightbuttonssubframe, text='Dislike (L)',
                                      command=self.right_dislike_command, variable=self.ro, value=3)

        self.list_of_input_buttons = [self.preferleft, self.preferright, self.leftlike,
                                      self.leftneutral, self.leftdislike, self.rightlike,
                                      self.rightneutral, self.rightdislike]
        self.clear = tk.Button(self.bottomsubframe, text="Clear (X)",
                               command=self.clear_command)
        self.submit = tk.Button(self.bottomsubframe, text="Submit (Spacebar)",
                                command=self.submit_command, state="disabled")
        self.quit = tk.Button(self.bottomsubframe, text="Quit",
                              command=self.master.destroy)

        master.bind('e', self.prefer_left_command)
        master.bind('i', self.prefer_right_command)
        master.bind('f', self.left_like_command)
        master.bind('d', self.left_neutral_command)
        master.bind('s', self.left_dislike_command)
        master.bind('j', self.right_like_command)
        master.bind('k', self.right_neutral_command)
        master.bind('l', self.right_dislike_command)
        master.bind('x', self.clear_command)
        master.bind('<space>', self.submit_command)

        # image creation: using image_generation.py
        self.old_left_image = tk.PhotoImage(file="~/Downloads/sparkle_house.gif")
        self.old_right_image = tk.PhotoImage(file="~/Downloads/sparkle_house.gif")
        # image-containing label creation
        self.imagelabel = tk.Label(self)

        # all packing
        # imagelabel
        self.imagelabel.pack(side="top")
        self.leftimage, self.rightimage = image_generation.generate_random_images()
        image_generation.plot_and_show_images(self.leftimage, self.rightimage, self.imagelabel)

        # frames
        self.leftsubframe.pack(side="left", expand=True)
        self.rightsubframe.pack(side="right", expand=True)

        self.leftbuttonssubframe.pack(side="right")
        self.rightbuttonssubframe.pack(side="left")

        # input radio-buttons
        self.preferleft.pack(side="top", pady=20)
        self.preferright.pack(side="top", pady=20)

        self.leftdislike.pack(side="bottom", anchor="w")
        self.leftneutral.pack(after=self.leftdislike, side="bottom", anchor='w')
        self.leftlike.pack(after=self.leftneutral, side="bottom", anchor='w')

        self.rightdislike.pack(side="bottom", anchor="w")
        self.rightneutral.pack(after=self.rightdislike, side="bottom", anchor='w')
        self.rightlike.pack(after=self.rightneutral, side="bottom", anchor='w')

        # bottom subframe and its 3 buttons
        self.bottomsubframe.pack(side="bottom")

        self.clear.pack(side="left")
        self.submit.pack(after=self.clear, side="left")
        self.quit.pack(after=self.submit, side="left")

        # data storage instance variables.
        # preferrecords is a list of dictionaries: "left" is left image name, "right"
        # is right image name, and "preference" is left or right.
        # ordinalrecords is an array of dictionaries: "image" is image name, "rating" is
        # either "dislike," "like," or "neutral. these will be written to ~/alphagarden_data.txt
        # after submit is pressed.
        self.preferinput = ""
        self.leftordinalinput = ""
        self.rightordinalinput = ""

        # These 2 blocks will raise an error if there is data in alphagarden_preference_data.txt
        # or alphagarden_ordinal_data.txt that is not valid JSON. If there is valid JSON, it will
        # load the data into preferrecords/ordinalrecords. If there is no files named
        # alphagarden_preference_data or alphagarden_ordinal_data.txt, it will create one.
        try:
            with open('alphagarden_preference_data.txt') as infile:
                self.preferrecords = json.load(infile)
        except json.decoder.JSONDecodeError:
            if os.path.getsize('alphagarden_preference_data.txt') == 0:
                self.preferrecords = {"data": []}
            else:
                raise
        except FileNotFoundError:
            with open('alphagarden_preference_data.txt', 'w'):
                self.preferrecords = {"data": []}
        try:
            with open('alphagarden_ordinal_data.txt') as infile:
                self.ordinalrecords = json.load(infile)
        except json.decoder.JSONDecodeError:
            if os.path.getsize('alphagarden_ordinal_data.txt') == 0:
                self.ordinalrecords = {"data": []}
            else:
                raise
        except FileNotFoundError:
            with open('alphagarden_ordinal_data.txt', 'w'):
                self.ordinalrecords = {"data": []}


        # booleans representing whether input was registered
        self.registeredpreferinput = False
        self.registeredleftordinalinput = False
        self.registeredrightordinalinput = False

    # button commands
    def register_prefer_input(self, response):
        self.preferinput = response
        self.registeredpreferinput = True

        if response == 'left':
            self.p.set(1)
        else:
            self.p.set(2)
        # check if submit can be ungrayed
        if self.ready_to_submit():
            self.enable_submit()



    def register_ordinal_input(self, image, response):
        if image == "left":
            self.leftordinalinput = response
            self.registeredleftordinalinput = True
            self.lo.set(self.response_to_int[response])
        elif image == "right":
            self.rightordinalinput = response
            self.registeredrightordinalinput = True
            self.ro.set(self.response_to_int[response])
        else:
            print("ERROR: invalid value for 'response'")

        # check if submit can be ungrayed
        if self.ready_to_submit():
            self.enable_submit()

    def clear_command(self, event=None):
        # clear out inputs
        self.leftordinalinput = ""
        self.rightordinalinput = ""
        self.preferinput = ""

        self.registeredpreferinput = False
        self.registeredleftordinalinput = False
        self.registeredrightordinalinput = False

        for int in self.radio_integers:
            int.set(0)
        # gray out submit button + make unresponsive
        self.submit["state"] = "disabled"

    def submit_command(self, event=None):
        # print("registered submit command!")

        # submit inputs to records
        if self.ready_to_submit():
            # Todo: find better str representation of images
            self.ordinal_input_to_records("L", self.leftordinalinput)
            self.ordinal_input_to_records("R", self.rightordinalinput)
            self.prefer_input_to_records(self.preferinput)
            self.input_to_json()
            # pick new images from acquisition function
            self.leftimage, self.rightimage = image_generation.generate_random_images()
            image_generation.plot_and_show_images(self.leftimage, self.rightimage, self.imagelabel)

            # clear_command
            self.clear_command()
        """
        else:
            print("ERROR: Not ready to submit!")
        """


    def prefer_input_to_records(self, response):
        # Todo: find suitable names for images
        self.preferrecords["data"].append({"left": "L", "right": "R",
                                           "preference": response})
        pass

    def ordinal_input_to_records(self, image, response):
        # Todo: find suitable names for images
        self.ordinalrecords["data"].append({"image": image, "rating": response})
        pass

    # returns true if we are ready to submit, false otherwise
    def ready_to_submit(self):
        return bool(self.registeredpreferinput and self.registeredrightordinalinput
                    and self.registeredleftordinalinput)

    # ungrays submit + makes responsive
    def enable_submit(self):
        self.submit["state"] = "normal"

    # puts input to long term storage in json
    def input_to_json(self):
        with open('alphagarden_preference_data.txt', 'w') as outfile:
            json.dump(self.preferrecords, outfile, indent=4)
        with open('alphagarden_ordinal_data.txt', 'w') as outfile:
            json.dump(self.ordinalrecords, outfile, indent=4)


root = tk.Tk()
app = Application(master=root)
app.mainloop()
