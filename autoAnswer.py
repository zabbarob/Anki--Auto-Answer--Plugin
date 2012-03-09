#!/usr/bin/env python
from ankiqt import mw
from ankiqt.ui.main import AnkiQt
from anki.hooks import addHook, wrap
from threading import Timer

#import growlpy.Growl
#gn = growlpy.Growl.GrowlNotifier(applicationName='Anki', applicationIcon=growlpy.Growl.Image.imageFromPath('/Applications/Anki.app/Contents/Resources/anki.icns'), notifications=['autoAnswer'])
#gn.register()

def notify(str):
    print('AutoAnswer: ' + str)
    #gn.notify('autoAnswer', 'autoAnswer', str)

# configuration of plugin

secondsUntilAnswer = 9.0
#secondsIgnoringKeys = 1.0

# ignore key events for some seconds, if auto-answer executed
# NOTE this is currently not working
#
#keyPressEventHandler = mw.keyPressEvent
#
#def handleKeyPressEvents():
#    notify('handling key press events')
#    mw.keyPressEvent = keyPressEventHandler
#    replace = False
#
#def keyPressEventIgnorer(evt):
#    notify('ignoring key press events')
#    evt.accept()
#
#def replaceKeyPressEventHandler():
#    global handleKeyEventsTimer
#    handleKeyEventsTimer.cancel()
#
#    # WARNING execute next line and Faster-Keys plugin will no longer work!!!
#    mw.keyPressEvent = keyPressEventIgnorer 
#
#    handleKeyEventsTimer = Timer(secondsIgnoringKeys, handleKeyPressEvents)
#    handleKeyEventsTimer.start()
#
#handleKeyEventsTimer = Timer(secondsIgnoringKeys, handleKeyPressEvents)

# set ease button 1 as default if auto-answer executed

defaultEaseButton = AnkiQt.defaultEaseButton
replace = False

def onDefaultEaseButton(self):
    notify('onDefaultEaseButton')
    global replace
    global defaultEaseButton
    return 1 if replace else defaultEaseButton(self)

def replaceDefaultEaseButton():
    global replace
    replace = True

AnkiQt.defaultEaseButton = wrap(AnkiQt.defaultEaseButton, onDefaultEaseButton, pos="after")

# automatically press answer button

def pressAnswerButton():
    notify('pressing answer button')
    #replaceKeyPressEventHandler()
    replaceDefaultEaseButton()
    mw.mainWin.showAnswerButton.click()

pressAnswerButtonTimer = Timer(secondsUntilAnswer, pressAnswerButton)

def resetTimer():
   notify('resetting timer')
   global replace
   replace = False
   global pressAnswerButtonTimer
   pressAnswerButtonTimer.cancel()
   pressAnswerButtonTimer = Timer(secondsUntilAnswer, pressAnswerButton)
   pressAnswerButtonTimer.start()

def stopTimer():
   notify('stopping timer')
   global pressAnswerButtonTimer
   pressAnswerButtonTimer.cancel()

def onPreMoveToState(self, state):
    notify('move to state')
    if state in ["showAnswer", "editCurrentFact", "studyScreen"]:
        stopTimer()

addHook('showQuestion', resetTimer)
addHook('deckFinished', stopTimer)
addHook('deckClosed', stopTimer)
addHook('quit', stopTimer)

AnkiQt.moveToState = wrap(AnkiQt.moveToState, onPreMoveToState, pos="before")

# register plugin

mw.registerPlugin('autoAnswer', 2011100501)

