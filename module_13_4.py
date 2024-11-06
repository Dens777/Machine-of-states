from aiogram import Bot,Dispatcher,executor,types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State,StatesGroup
from aiogram.dispatcher import FSMContext
import asyncio

api ='8056937450:AAGiDrgxJroFEBkyTQT2ck3oTKTiIhRKnvI'
bot =Bot(token=api)
db =Dispatcher(bot,storage=MemoryStorage())

class UserState(StatesGroup):
    weight = State()
    growth = State()
    age = State()

@db.message_handler(text='Calories')
async def set_age(message):
    await message.answer('Введите свой возраст:')
    await UserState.age.set()


@db.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer('Введите свой рост:')
    await UserState.growth.set()


@db.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer('Введите свой вес:')
    await UserState.weight.set()


@db.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    calories = (10 * int(data["weight"])) + (6.25 * int(data["growth"])) - (5 * int(data["age"])) + 5
    await message.answer(f"Калорий для оптимального похудения {calories}")

    await state.finish()



if __name__=='__main__':
    executor.start_polling(db,skip_updates=True)