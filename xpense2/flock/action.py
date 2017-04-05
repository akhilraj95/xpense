import secret
from models import User,Currency
import urllib2,json

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

def total(expense_list,trackObj):
    try:
        currency_list = Currency.objects.all()
        total = {}
        for curr in currency_list:
            total[curr.abbr] = 0
        for expense in expense_list:
            total[expense.currency.abbr]+=expense.amount
        total = {key: value for key, value in total.items()
             if value is not 0}
        target_curr = str(trackObj.budget_currency.abbr)
        target_value = 0
        perc_spent = 0
        if target_curr in total.keys():
            target_value = total[target_curr]

        #check if there is a budget
        if trackObj.budget != 0:
            #converting all currencies to budget currency
            target_value = 0
            symbols = total.keys()
            rates = getconversionrates(target_curr,symbols)
            target_value = 0
            for key, value in total.items():
                if key==target_curr:
                    target_value+=value
                else:
                    target_value+= round(value/rates[key],2)

            perc_spent = round((target_value/trackObj.budget)*100,2)
        return total,target_value,perc_spent
    except:
        raise

def getconversionrates(to_curr,from_curr_list):
    if to_curr in from_curr_list:
        from_curr_list.remove(to_curr)
    from_curr_list_str = ','.join(from_curr_list)
    API_string = 'http://api.fixer.io/latest?base='+to_curr+'&symbols='+from_curr_list_str
    response = urllib2.urlopen(API_string).read()
    pjson = json.loads(response)
    return pjson['rates']
