from operator import index
import PySimpleGUI as sg
import ezsheets

def isExist(studentID, sheet):
    return studentID in sheet.getColumn(1)

def isCheckIn(studentID, sheet):
    return sheet.getColumn(5)[sheet.getColumn(1).index(studentID)] == "TRUE"

def getData(studentID, sheet, col):
    return sheet.getColumn(col)[sheet.getColumn(1).index(studentID)]

def PopUpWindow(title, txt):

    sz = 20
    if txt == "Success!":
        sz = 30

    popUpElements = [
        [sg.Text(txt, font = ("Futura", sz))],
        [sg.Button("Back", font = ("Futura", 18), key = "-Back-")] 
    ]

    popUpLayout = [
        [sg.VPush()],
        [sg.Push(), sg.Column(popUpElements, element_justification='c'), sg.Push()],
        [sg.VPush()]
    ]

    window = sg.Window(title, popUpLayout, modal = True, size = (400, 250))

    while True:

        event, values = window.read()

        if event == sg.WIN_CLOSED or event == "-Back-":
            break

    window.close()

def checkIn(studentID, sheet):
    sheet["E" + str(sheet.getColumn(1).index(studentID)+1)] = "TRUE"
    PopUpWindow("Registration System", "Success!")

def BaanWindow(sheet):
    
    BaanElements = [
        [sg.Text("Enter No. and Baan: ", font = ("Futura", 30)), sg.InputText(size = (10, 1), font = ("Futura", 30), do_not_clear = False)],
        [sg.Text("Nickname: ", font = ("Futura", 30), key = "-NICKNAME-")],
        [sg.Text("Baan: ", font = ("Futura", 30), key = "-BAAN-")],
        [sg.VPush()],
        
    ]
    BaanLayout = [
        [sg.VPush()],
        [sg.Push(), sg.Column(BaanElements, element_justification = 'l'), sg.Push()],
        [sg.Push(), sg.Column([[sg.Button("Update", font = ("Futura", 30), size = (10, 1), key = "-UPDATE-", bind_return_key = True)]], element_justification = 'l'), sg.Push()],
        [sg.VPush()]
    ]

    window = sg.Window("Registration System", BaanLayout, size = (800, 600))

    while True:

        event, values = window.read()

        if event == sg.WIN_CLOSED:
            break

        try:
            no, baan = values[0].split(" ")
        except:
            continue

        no = ('0' * (3 - len(no))) + no

        if event == "-UPDATE-":
            if no in sheet.getColumn(2):
                window["-NICKNAME-"].update("Nickname: " + sheet.getColumn(4)[sheet.getColumn(2).index(no)])
                window["-BAAN-"].update("Baan: " + str(baan))
                sheet["G" + str(sheet.getColumn(2).index(no)+1)] = baan
    
    window.close()


def DisplayWindow(studentID, sheet, isStaff):
    
    if isStaff:
        displayElements = [
            [sg.VPush()],
            [sg.Text("Student ID: " + studentID, font = ("Futura", 30))],
            [sg.Text("Name: " + getData(studentID, sheet, 2), font = ("Futura", 30))],
            [sg.Text("Nickname: " + getData(studentID, sheet, 3), font = ("Futura", 30))],
            [sg.Text("Position: " + getData(studentID, sheet, 4), font = ("Futura", 30))],
            [sg.VPush()]
        ]
    else:
        displayElements = [
            [sg.VPush()],
            [sg.Text("No. : " + getData(studentID, sheet, 2), font = ("Futura", 30))],
            [sg.Text("Student ID: " + studentID, font = ("Futura", 30))],
            [sg.Text("Name: " + getData(studentID, sheet, 3), font = ("Futura", 30))],
            [sg.Text("Nickname: " + getData(studentID, sheet, 4), font = ("Futura", 30))],
            [sg.Text("T-Shirt Size: " + getData(studentID, sheet, 6), font = ("Futura", 30))],
            [sg.VPush()]
        ]
    displayLayout = [
        [sg.VPush()],
        [sg.Push(), sg.Column(displayElements, element_justification='l'), sg.Push()],
        [sg.Push(), sg.Column([[sg.Button("Check-in", font = ("Futura", 30), size = (10, 1), key = "-CheckIn-")]], element_justification = 'c'), sg.Push()],
        [sg.VPush()]
    ]

    window = sg.Window("Registration System", displayLayout, size = (800, 600))
    
    while True:

        event, values = window.read()

        if event == sg.WIN_CLOSED:
            break

        if event == "-CheckIn-":
            checkIn(studentID, sheet)
            break
        
    window.close()

def SearchWindow(sheet, isStaff = True):

    searchElements = [
        [sg.Text("Enter Student ID: ", font = ("Futura", 30)), sg.InputText(size = (10, 1), font = ("Futura", 30), do_not_clear = False)],
        [sg.VPush()],
        [sg.Button("Continue", font = ("Futura", 30), size = (10, 1), key = "-Continue-")]
    ]
    searchLayout = [
        [sg.VPush()],
        [sg.Push(), sg.Column(searchElements, element_justification='c'), sg.Push()],
        [sg.VPush()]
    ]

    window = sg.Window("Registration System", searchLayout, size = (800, 600))

    while True:

        event, values = window.read()

        if event == sg.WINDOW_CLOSED:
            break

        if event == "-Continue-":
            studentID = values[0]

            if len(studentID) == 10 and isExist(studentID, sheet):

                if isCheckIn(studentID, sheet):
                    PopUpWindow("Registration System", "You have already checked in")

                else:
                    window.hide()
                    DisplayWindow(studentID, sheet, isStaff)
                    window.un_hide()
            
            else:
                PopUpWindow("Registration System", "Your student ID does not exist")
    
    window.close()

def FreshmenWindow(sheet):

    freshmenElements = [
        [sg.Text("Please select operation", font = ("Futura", 30))],
        [sg.Text(" ", font = ("Futura", 30))],
        [sg.Button("Check In", font = ("Futura", 30), size = (20, 1), key = "-CHECKIN-")],
        [sg.Button("Baan", font = ("Futura", 30), size = (20, 1), key = "-BAAN-")]
    ]
    freshmenLayout = [
        [sg.VPush()],
        [sg.Push(), sg.Column(freshmenElements, element_justification = "c"), sg.Push()],
        [sg.VPush()]
    ]

    window = sg.Window("Registration System", freshmenLayout, size = (800, 600))

    while True:
        
        event, values = window.read()

        if event == sg.WIN_CLOSED:
            break

        if event == "-CHECKIN-":
            window.hide()
            SearchWindow(sheet, False)
            window.un_hide()
        
        if event == "-BAAN-":
            window.hide()
            BaanWindow(sheet)
            window.un_hide()

    window.close()

def main():

    sg.theme("LightBrown")

    sheetID = "1vFFBYLlZ01aLi0TNHqbWZKWJ6QIGHDp9x9Beca03CMI"
    sheet = ezsheets.Spreadsheet(sheetID)

    mainElements = [
        [sg.Text("Please select type of participant", font = ("Futura", 30))],
        [sg.Text(" ", font = ("Futura", 30))],
        [sg.Button("Staff", font = ("Futura", 30), size = (20, 1), key = "-Staff-")],
        [sg.Button("Freshmen", font = ("Futura", 30), size = (20, 1), key = "-Freshmen-")]
    ]
    mainLayout = [
        [sg.VPush()],
        [sg.Push(), sg.Column(mainElements, element_justification = "c"), sg.Push()],
        [sg.VPush()]
    ]

    window = sg.Window("Registration System", mainLayout, size = (800, 600))

    while True:

        event, values = window.read()

        if event == sg.WIN_CLOSED:
            break

        if event == "-Staff-":
            window.hide()
            SearchWindow(sheet["CheckInStaff"])
            window.un_hide()

        if event == "-Freshmen-":
            window.hide()
            FreshmenWindow(sheet["CheckInFreshmen"])
            window.un_hide()
            
    
    window.close()


if __name__ == "__main__":
    main()
