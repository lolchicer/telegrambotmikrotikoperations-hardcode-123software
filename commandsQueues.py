from telegram import Update
from telegram.ext import CallbackContext


async def a(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("a")


async def b(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("b")


async def c(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("c")


async def d(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("d")
