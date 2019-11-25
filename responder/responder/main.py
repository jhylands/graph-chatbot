
class Context:
    SIMPLE = 1

def handle_simple_chat(message):
    sw = message.lower.startswith
    if sw("hi") or sw("hello"):
        return "Hi!"

#Set the chat switch as a constant for now
CHAT_SWITCH = {
    Context.SIMPLE:handle_simple_chat,
}
def respond(chat, message):
    '''
    The main function for handling the incoming messages.
    @param chat     This is a context variable holding the context of the conversation
    @param message  This it the text content of the message

    @return chat, message
    '''
    response = CHAT_SWITCH[chat.context](message)
    chat.responded()
    return chat, response


