написание логики на python требует совершенно волшебного склада ума
например, это – неправильный код:
```
def errorHandle(update: Update, context: CallbackContext):
    error = context.error
    error = exceptions.SentException(error)
    
    try:
        update.message.reply_markdown_v2(error.sentMessage)
    except Exception:
        update.message.reply_markdown_v2('Some exception has thrown\.\r\nNEED TO MAINTENANCE THE BOT')
    finally:
        print(error)
```
– и нужно писать вот так:
```
def errorHandle(update: Update, context: CallbackContext):
    error = context.error
    error = exceptions.SentException(error)
    
    try:
        sentMessage = error.sentMessage
    except Exception:
        sentMessage = 'Some exception has thrown\.\r\nNEED TO MAINTENANCE THE BOT'
    finally:
        update.message.reply_markdown_v2(sentMessage)
        print(error)
```
– вынеся в блок except код, в котором однозначно есть только одно условие возникновения ошибки, тип которой ты указал после слова except.
  
и забыть про эту ерунду просто так нельзя, потому что все дефолтные библиотеки языка поражены трай-кетчами, так что if-else структуры нарушат эту так называемую eafp-гармонию.