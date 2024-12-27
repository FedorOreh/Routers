from aiogram import Router, F
from aiogram.types import Message, LabeledPrice, PreCheckoutQuery, ContentType
from aiogram.filters import Command, CommandStart
from aiogram import Bot
from config import TOKEN, PAYMENTS_TOKEN

bot = Bot(token=TOKEN)

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    await bot.delete_message(message.from_user.id, message.message_id)
    await bot.send_message(message.from_user.id, 'Привет!')

PRICE = LabeledPrice(label='Buying', amount=100*100)

@router.message(Command('buy'))
async def buy(message: Message):
    await bot.send_invoice(title='Test Invoice Router',
                           chat_id=message.from_user.id,
                           currency='rub',
                           description='Test Invoice',
                           start_parameter='bot',
                           payload='top',
                           prices=[PRICE],
                           provider_token=PAYMENTS_TOKEN)

@router.pre_checkout_query()
async def preCheck(precheckout: PreCheckoutQuery):
    await bot.answer_pre_checkout_query(precheckout.id, ok=True)

@router.message(F.successful_payment)
async def success(message: Message):
    payment_info = message.successful_payment
    print(payment_info)
    await bot.send_message(message.from_user.id, 'You successfully buy this item!')