from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivymd.app import MDApp
from kivy.graphics import Color
from functools import partial
from kivy.clock import  Clock

import socket
import logging
import json

class ClientInterface:
    def __init__(self,idplayer='X'):
        self.idplayer=idplayer
        #self.server_address=('192.168.63.182',6666)
        self.server_address=('192.168.194.234',6666)

    def send_command(self,command_str=""):
        global server_address
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(self.server_address)
        logging.warning(f"connecting to {self.server_address}")
        try:
            logging.warning(f"sending message ")
            sock.sendall(command_str.encode())
            # Look for the response, waiting until socket is done (no more data)
            data_received="" #empty string
            while True:
                #socket does not receive all data at once, data comes in part, need to be concatenated at the end of process
                data = sock.recv(16)
                if data:
                    #data is not empty, concat with previous content
                    data_received += data.decode()
                    if "\r\n\r\n" in data_received:
                        break
                else:
                    # no more data, stop the process by break
                    break
            # at this point, data_received (string) will contain all data coming from the socket
            # to be able to use the data_received as a dict, need to load it using json.loads()
            hasil = json.loads(data_received)
            logging.warning("data received from server:")
            return hasil
        except:
            logging.warning("error during data receiving")
            return False

    def set_location(self,lokasi):
        player = self.idplayer
        command_str=f"set_location {player} {lokasi}"
        print(command_str)
        hasil = self.send_command(command_str)
        print(hasil)
        if (hasil['status']=='OK'):
            return True
        else:
            return False

    def get_location(self):
        command_str=f"get_location"
        hasil = self.send_command(command_str)
        print(hasil)
        if (hasil['status']=='OK'):
            lokasi = hasil['location']
            return lokasi

    def get_last_turn(self):
        command_str=f"get_last_turn"
        hasil = self.send_command(command_str)
        print(hasil)
        if (hasil['status']=='OK'):
            lokasi = hasil['last_turn']
            return lokasi
            
    def reset(self):
        command_str=f"reset"
        hasil = self.send_command(command_str)

class MyApp(MDApp):
    idplayer = "X"
    title = idplayer
    client_interface = ClientInterface(idplayer)
    def refresh(self,callback):
        # Keep Track of win or lose
        self.winner = False
        self.turn = self.arr = self.client_interface.get_last_turn()
        self.arr = self.client_interface.get_location()
        
        for nomor in range(1,9):
            self.btn[int(nomor)].text = ""
            self.btn[int(nomor)].disabled = False
        
        for nomor in self.arr[0]:
            self.btn[int(nomor)].text = "X"
            self.btn[int(nomor)].disabled = True
        
        for nomor in self.arr[1]:
            self.btn[int(nomor)].text = "O"
            self.btn[int(nomor)].disabled = True
            
        # Define Who's turn it is
        if self.turn == 'O':
            self.score.text = "O's Turn!"
        if self.turn == 'X':
            self.score.text = "X's Turn!"
        
        self.win()
            
            
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "BlueGray"
        
        root = FloatLayout()
        self.gridl = GridLayout(size_hint = (.5, .5),pos_hint = {'center_x': .5, 'center_y': .7},cols = 3,rows = 3)
        self.score = Label(font_size="32sp",text="X GOES FIRST!",halign="center",pos_hint={"center_y": .3})
        self.resets = Button(size_hint = (.2, .05),text="Restart The Game",pos_hint={'center_x': .5, 'center_y': .15},on_release=self.restart)
        
        root.add_widget(self.gridl)
        root.add_widget(self.score)
        root.add_widget(self.resets)
        
        self.btn = []
        for i in range(0,9):
            self.btn.append(Button(text="",font_size="45sp"))
            self.btn[-1].bind(on_release=partial(self.presser,i))
            self.gridl.add_widget(self.btn[-1])
        Clock.schedule_interval(self.refresh,1)
        return root
        
    def presser(self,nomor,*kwargs):
        if self.turn != self.idplayer:
            return self
        if self.turn == "X":
            self.arr[0].append(nomor)
            self.client_interface.set_location((json.dumps(self.arr[0])).replace(" ",""))
        else:
            self.arr[1].append(nomor)
            self.client_interface.set_location((json.dumps(self.arr[1])).replace(" ",""))
    def restart(self,*kwargs):
        self.client_interface.reset()

    # No Winner
    def no_winner(self):
        if self.winner == False and \
        self.btn[0].disabled == True and \
        self.btn[1].disabled == True and \
        self.btn[2].disabled == True and \
        self.btn[3].disabled == True and \
        self.btn[4].disabled == True and \
        self.btn[5].disabled == True and \
        self.btn[6].disabled == True and \
        self.btn[7].disabled == True and \
        self.btn[8].disabled == True:
            self.score.text = "IT'S A TIE!!"

    def win(self):
        # Across
        if self.btn[0].text != "" and self.btn[0].text == self.btn[1].text and self.btn[1].text == self.btn[2].text:
            self.end_game(self.btn[0], self.btn[1], self.btn[2])

        if self.btn[3].text != "" and self.btn[3].text == self.btn[4].text and self.btn[4].text == self.btn[5].text:
            self.end_game(self.btn[3], self.btn[4], self.btn[5])

        if self.btn[6].text != "" and self.btn[6].text == self.btn[7].text and self.btn[7].text == self.btn[8].text:
            self.end_game(self.btn[6], self.btn[7], self.btn[8])
        # Down
        if self.btn[0].text != "" and self.btn[0].text == self.btn[3].text and self.btn[3].text == self.btn[6].text:
            self.end_game(self.btn[0], self.btn[3], self.btn[6])

        if self.btn[1].text != "" and self.btn[1].text == self.btn[4].text and self.btn[4].text == self.btn[7].text:
            self.end_game(self.btn[1], self.btn[4], self.btn[7])

        if self.btn[2].text != "" and self.btn[2].text == self.btn[5].text and self.btn[5].text == self.btn[8].text:
            self.end_game(self.btn[2], self.btn[5], self.btn[8])

        # Diagonal 
        if self.btn[0].text != "" and self.btn[0].text == self.btn[4].text and self.btn[4].text == self.btn[8].text:
            self.end_game(self.btn[0], self.btn[4], self.btn[8])

        if self.btn[2].text != "" and self.btn[2].text == self.btn[4].text and self.btn[4].text == self.btn[6].text:
            self.end_game(self.btn[2], self.btn[4], self.btn[6])
        self.no_winner()
        # End The Game
    def end_game(self, a,b,c):
        self.winner = True
        a.color = "red"
        b.color = "red"
        c.color = "red"

        # Disable the buttons
        self.disable_all_buttons()

        # Set Label for winner
        self.score.text = f"{a.text} Wins!"

    def disable_all_buttons(self):
        # Disable The Buttons
        for i in range(0,9):
            self.btn[i].disabled = True

if __name__ == '__main__':
    MyApp().run()