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