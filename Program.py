import PySimpleGUI as sg
import ezsheets

def isExist(studentID, sheet):
  return studentID in sheet.getColumn(1)

def isCheckIn(studentID, sheet):
  return sheet.getColumn(5)[sheet.getColumn(1).index(studentID)] == "TRUE"
  
def getData(col, studentID, sheet):
  return sheet.getColumn(col)[sheet.getColumn(1).index(studentID)]

def openPopUpWindow(title, txt):

  sz = 20
  if txt == "Success!":
    sz = 30

  elements = [
    [sg.Text(txt, font = ("Futura", sz))],
    [sg.Button("Back", font = ("Futura", 18))] 
  ]

  popUpLayout = [
    [sg.VPush()],
    [sg.Push(), sg.Column(elements, element_justification='c'), sg.Push()],
    [sg.VPush()]
  ]

  window = sg.Window(title, popUpLayout, modal = True, size = (400, 250))

  while True:

    event, values = window.read()

    if event == sg.WIN_CLOSED or event == "Back":
      break

  window.close()

def checkIn(studentID, sheet):
  sheet["E" + str(sheet.getColumn(1).index(studentID)+1)] = "TRUE"
  openPopUpWindow("Registration System", "Success!")
  
def openDisplayWindow(studentID, sheet):

  elements = [
    [sg.VPush()],
    [sg.Text("Student ID: " + studentID, font = ("Futura", 30))],
    [sg.Text("Name: " + getData(2, studentID, sheet), font = ("Futura", 30))],
    [sg.Text("Nickname: " + getData(3, studentID, sheet), font = ("Futura", 30))],
    [sg.Text("T-Shirt Size: " + getData(4, studentID, sheet), font = ("Futura", 30))],
    [sg.VPush()]
  ]

  displayLayout = [
    [sg.VPush()],
    [sg.Push(), sg.Column(elements, element_justification='l'), sg.Push()],
    [sg.Push(), sg.Column([[sg.Button("Check-in", font = ("Futura", 30), size = (10, 1))]], element_justification='c'), sg.Push()],
    [sg.VPush()]
  ]

  window = sg.Window("Registration System", displayLayout, modal = True, size = (800, 600))

  while True:

    event, values = window.read()

    if event == sg.WIN_CLOSED:
      break

    if event == "Check-in":
      checkIn(studentID, sheet)
      break

  window.close()
  
def main():

  sg.theme("BlueMono")

  sheetID = "1vFFBYLlZ01aLi0TNHqbWZKWJ6QIGHDp9x9Beca03CMI"
  sheet = ezsheets.Spreadsheet(sheetID)["CheckInFreshy"]

  elements = [
    [sg.Text("Enter Student ID: ", font = ("Futura", 30)), sg.InputText(size = (10, 1), font = ("Futura", 30), do_not_clear = False)],
    [sg.VPush()],
    [sg.Button("Continue", font = ("Futura", 30), size = (10, 1))]
  ]
  
  mainLayout = [
    [sg.VPush()],
    [sg.Push(), sg.Column(elements, element_justification='c'), sg.Push()],
    [sg.VPush()]
  ]

  window = sg.Window("Registration System", mainLayout, size = (800, 600))

  while True:

    event, values = window.read()

    if event == sg.WIN_CLOSED:
      break

    if event == "Continue":
      studentID = values[0]

      if isExist(studentID, sheet):

        if isCheckIn(studentID, sheet):
          openPopUpWindow("Error", "You have already checked in")

        else:
          openDisplayWindow(studentID, sheet)

      else:
        openPopUpWindow("Error", "Your student ID does not exist")

  window.close()

if __name__ == "__main__":
  main()