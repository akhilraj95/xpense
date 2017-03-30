import secret
from models import User
#FlockOS
from pyflock import FlockClient, verify_event_token
from pyflock import Message, SendAs, Attachment, Views, WidgetView, HtmlView, ImageView, Image, Download, Button, OpenWidgetAction, OpenBrowserAction, SendToAppAction


def appInstall(pjson):
    try:
        userId = pjson['userId']
        token = pjson['token']
        u = User(userId = userId, token=token)
        u.save()
    except:
        raise

def appUninstall(pjson):
    try:
        userId = pjson['userId']
        User.objects.get(userId=userId).delete()
    except:
        raise

def sendMessage(chat_id,userId,message):
    try:
        user = User.objects.get(userId=userId)
        flock_client = FlockClient(token=user.token, app_id=secret.getAppID)
        send_as_xpense = SendAs(name='Xpense', profile_image='https://pbs.twimg.com/profile_images/1788506913/HAL-MC2_400x400.png')
        send_as_message = Message(to=chat_id,text=message,send_as=send_as_xpense)
        flock_client.send_chat(send_as_message)
    except:
        raise
