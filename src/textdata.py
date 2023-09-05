class TextData():
    filename = ""
    conversations = []

class Conversation():
    conversationId = ""
    dialog = []
    choices = []

class Dialog():
    actorId = ""
    sentences = []
    afterDialogAnimationClip = []

class Sentence():
    text = ""
    fontIndex = 0
    portraitInde = 0
    animationClip = ""

class Choice():
    choiceText = ""
    