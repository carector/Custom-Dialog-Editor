class TextData():
    filename = ""
    conversations = []

class Conversation():
    conversationId = ""
    dialog = []
    choices = []

class Dialog():
    actorId = ""
    portrait = 0
    sentences = []
    afterDialogAnimationClip = []

class Sentence():
    text = ""
    fontIndex = 0
    portraitIndex = 0
    animationClip = ""

class Choice():
    choiceText = ""
