"""Сommon handlers and registration"""
import os
from io import BytesIO


from aiogram import types
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher import FSMContext
import requests

from home_parser.parser import check_status
from keyboards import set_link_keyboard
from messages import MESSAGES
from messages.sender import send_messages
from states import Form
from home_parser import MyHomeParser
from utils import get_var, logging


class CommonHandlers:
    """Сommon handlers"""

    async def start_command(message: types.Message) -> None:
        """
        Handler of the /start command

        Args:
            message (types.Message): Instance of the Message class.
        """
        await message.bot.send_message(
            message.chat.id,
            MESSAGES['start'].format(message.from_user.username),
            reply_markup=set_link_keyboard
        )
        
        # Add the user ID to the environment variable
        if (not os.environ.get('USER_IDS')):
            logging.warning("# os.environ.get('USER_IDS')!")
            user_ids = []
        else:
            user_ids = os.environ.get('USER_IDS').split(',')

        if str(message.chat.id) not in user_ids:
            user_ids.append(str(message.chat.id))
            os.environ['USER_IDS'] = ','.join(user_ids)
            await message.answer("Let's get started!🔥")
        
    async def show_all(message: types.Message) -> None:
        """
        Handler of the /start command

        Args:
            message (types.Message): Instance of the Message class.
        """
        await message.answer(MESSAGES['fetching'])
        os.environ['HOMES_URL'] = ""

        ## todo: remove after testing
        # url = os.environ.get('URL')
        # if not url:
        #     logging.warning("# not var_val!")
        #     return
        #
        # p = MyHomeParser(url)
        #
        # if p.status == 200:
        #     logging.debug(f'status code: {p.status}')
        # else:
        #     logging.warning(
        #         f'Oh shit... We have a problem, status code: {p.status}')
        #     return

        if not (url := get_var('URL')): return
        p = MyHomeParser(url)
        if not check_status(p): return

        p.get_cards()
        p.get_homes_url_and_images()
        p.save_to_env()

        if not len(p.homes_url):
            return

        send_messages(p, message)

        ##~^ todo: remove after testing
        # for i, var_val in enumerate(p.homes_url):
        #     # msg = f"**[{p.description['title'][i]}]({var_val})** - \n*${p.description['price'][i]}*     {p.description['square'][i]}     {p.description['stairs'][i]} \n{p.description['address'][i]}"
        #     msg = get_msg_txt(p, var_val, i)
        #     image_url = p.description['image_url'][i]
        #
        #     # Download the image and sends it
        #     response = requests.get(image_url)
        #     user_ids = os.environ.get('USER_IDS', '').split(',')
        #     if not user_ids:
        #         logging.error('Users ID is not founded')
        #         continue
        #
        #     for user_id in user_ids:
        #         try:
        #             logging.info(f'# send_photo {user_id = }')
        #             image_bytes_copy = BytesIO(response.content)
        #             image_bytes_copy.seek(0)
        #             await message.bot.send_photo(user_id, photo=image_bytes_copy, caption=msg, parse_mode="Markdown")
        #         except Exception as e:
        #             logging.exception('Sending msg error')

    async def help_command(message: types.Message) -> None: 
        """
        Handler of the /help command

        Args:
            message (types.Message): Instance of the Message class.
        """
        await message.answer("We'll be there soon 🆘")
    
    async def show_link(message: types.Message) -> None: 
        """
        Handler of the /help command

        Args:
            message (types.Message): Instance of the Message class.
        """
        url = os.environ.get('URL')
        await message.answer(url)
        
    async def cancel_command(message: types.Message, state: FSMContext) -> None: 
        current_state = await state.get_state()
        if current_state is None:
            return
        else:
            await state.finish()
            await message.answer(MESSAGES['cancel'])

    async def set_link(message: types.Message) -> None:
        await Form.url.set()
        await message.answer(
                MESSAGES['set_link']
        )

    async def update_link(message: types.Message, state: FSMContext) -> None:
        async with state.proxy() as data:
            data['var_val'] = message.text
        # Save the URL to an environment variable
        os.environ['URL'] = message.text
        logging.debug(f"set new {os.environ['URL'] = }")
        os.environ['HOMES_URL'] = ""
        await state.finish()
        await message.answer(
            MESSAGES['link_updated']
            )

def register_client_handlers(dp: Dispatcher) -> None:
    """
    Registration of common handlers

    Args:
        dp (Dispatcher): Instance of the Dispatcher class.
    """
    dp.register_message_handler(CommonHandlers.start_command, commands=['start'])
    dp.register_message_handler(CommonHandlers.help_command, commands=['help'])
    dp.register_message_handler(CommonHandlers.set_link, commands=['set_link'])
    dp.register_message_handler(CommonHandlers.show_all, commands=['show'])
    dp.register_message_handler(CommonHandlers.set_link,  lambda message: message.text in ['Задать ссылку для поиска', 'Обновить ссылку для поиска'])
    dp.register_message_handler(CommonHandlers.show_link,  lambda message: message.text  == 'Посмотреть заданную ссылку')
    dp.register_message_handler(CommonHandlers.show_link,  commands=['show_link'])
    dp.register_message_handler(CommonHandlers.cancel_command, commands=['cancel'], state='*')
    dp.register_message_handler(CommonHandlers.update_link, state=Form.url)