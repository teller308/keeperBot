import logging

import gkeepapi
import keyring

from core import db
from models.gkeep_user import GKeepUser

logger = logging.getLogger(__name__)


class GKeepHandler:

    MASTER_TOKEN_NAME = 'google-keep-token'
    _instance = None

    @staticmethod
    def get_instance():
        if GKeepHandler._instance is None:
            return GKeepHandler()
        else:
            return GKeepHandler._instance

    def __init__(self) -> None:
        if self._instance is None:
            self._keep_instance = gkeepapi.Keep()
            self._active_users_ids = []
            self._cmd_list = {
                'help': self._help,
                'log_in': self._log_in,
                'log_out': self._log_out,
                'create': self._create_note,
                'read': self._read_note,
                'update': self._update_note,
                'delete': self._delete_note,
                'list': self._list_notes
            }

            self._required_login_cmd_list = (
                'create', 'read', 'update', 'delete', 'list', 'log_out')

            self._registered_users = GKeepUser.query.all()

            GKeepHandler._instance = self

        else:
            raise Exception('This class is a singleton.')

    def _new_login(self, user_id: int, email: str, password: str) -> None:
        self._keep_instance.login(email, password)
        token = self._keep_instance.getMasterToken()
        keyring.set_password(self.MASTER_TOKEN_NAME, email, token)
        self._register_new_user(user_id, email)

        return 'Logged in successfully.'

    def _resume_login(self, user_id: int, email: str) -> None:
        token = keyring.get_password(self.MASTER_TOKEN_NAME, email)
        self._keep_instance.resume(email, token)
        self._active_users_ids.append(user_id)
        return 'Welcome back.'

    def _is_user_active(self, user_id: int) -> bool:
        if user_id in self._active_users_ids:
            return True
        return False

    def _is_user_registered(self, user_id: int) -> bool:
        for user in self._registered_users:
            if user.tg_user_id == user_id:
                return True
        return False

    def _get_user_email_by_id(self, user_id: int) -> str:
        for user in self._registered_users:
            if user.tg_user_id == user_id:
                return user.email

    def _register_new_user(self, user_id: int, email: str) -> str:
        new_user = GKeepUser(tg_user_id=user_id, email=email)
        self._active_users_ids.append(user_id)
        self._registered_users.append(new_user)
        db.session.add(new_user)
        db.session.commit()
        db.session.refresh(new_user)
        return 'Successful registration.'

    def _log_in(self, *args: tuple) -> str:
        if len(args) != 3:
            return 'Please use this format:\n/log_in [email] [pass].'
        email, password, user_id = args
        try:
            if self._is_user_active(user_id):
                return 'You are already in the system.'
            elif self._is_user_registered(user_id):
                return self._resume_login(user_id, email)
            else:
                return self._new_login(user_id, email, password)
        except Exception as exc:
            msg = 'Something went wrong when try to log in. {}'.format(exc)
            logger.error(msg)
            return 'Failed to log in.'

    def _log_out(self, *args: tuple) -> str:
        user_id = args[0]
        for user in self._registered_users:
            if user.tg_user_id == user_id:
                user_to_remove = user
        self._active_users_ids.remove(user_id)
        self._registered_users.remove(user_to_remove)
        db.session.delete(user_to_remove)
        db.session.commit()

        return 'Logged out.'

    def _create_note(self, *args: tuple) -> str:
        if len(args) < 3:
            return 'Please use this format:' \
                '\n/create [note_title] [note_content].'
        name, content = args[0], ' '.join(args[1:-1])
        note = self._keep_instance.createNote(name, content)
        self._keep_instance.sync()
        return 'Created: {}'.format(note.title)

    def _read_note(self, *args: tuple) -> str:
        if len(args) != 2:
            return 'Please use this format:\n/read [note_title].'
        name, _ = args
        gnotes = self._keep_instance.find(query=name)
        content = []
        for note in gnotes:
            if note.title != '':
                content.append(note.title)
                text = note.text
                content.append(text)
                if text[-1] != '\n':
                    content.append('\n')
        if len(content) == 0:
            return 'I found nothing.'
        return ('\n').join(el for el in content)

    def _update_note(self, *args: tuple) -> str:
        if len(args) != 3:
            return 'Please use this format:' \
                '\n/update [note_title] [new_content].'
        name, content = args[0], ' '.join(args[1:-1])
        gnotes = self._keep_instance.find(query=name)
        for note in gnotes:
            note.text = content
        self._keep_instance.sync()
        return 'Updated.'

    def _delete_note(self, *args: tuple) -> str:
        if len(args) != 2:
            return 'Please use this format:\n/delete [note_title].'
        name, _ = args
        gnotes = self._keep_instance.find(query=name)
        deleted_notes = []
        for note in gnotes:
            deleted_notes.append(note.title)
            note.delete()
        self._keep_instance.sync()
        if len(deleted_notes) == 0:
            return 'No matches found with {}.'.format(name)
        return 'Cleared:\n{}'.format('\n'.join(deleted_notes))

    def _list_notes(self, *args: tuple) -> str:
        gnotes = self._keep_instance.all()
        result = '\n'.join(
            note.title for note in gnotes if note.title != '')
        if len(result) < 4096:
            return result
        return 'Result is too long.'

    def _help(self, *args: tuple) -> str:
        guide_ref = 'https://support.google.com/accounts/answer/185833?' \
            'hl=en&ctx=ch_b%2F0%2FDisplayUnlockCaptcha'
        help_text = 'To use this bot you need to get app password. ' \
            'Short guide here: {}'.format(guide_ref)
        return help_text

    def _is_command(self, recieved_data: dict) -> bool:
        if recieved_data.get('message') is not None:
            entities = recieved_data['message'].get('entities')
            if entities is not None:
                entity_type = entities[0].get('type')
                if entity_type == 'bot_command':
                    return True
        return False

    def router(self, recieved_data: dict) -> str:
        answer_dict = {}
        if recieved_data.get('message'):
            user_id = recieved_data['message']['from']['id']
            answer_dict['chat_id'] = user_id

            try:
                if self._is_command(recieved_data) is True:
                    input_data_list = recieved_data['message']['text'].split(
                        ' ')
                    input_data_list.append(user_id)

                    command = input_data_list.pop(0).replace('/', '')

                    if command in self._required_login_cmd_list:
                        if not self._is_user_active(user_id):
                            if not self._is_user_registered(user_id):
                                answer_dict['text'] = 'Please log in.'
                                return answer_dict
                            else:
                                # not active but registered user
                                email = self._get_user_email_by_id(user_id)
                                self._resume_login(user_id, email)

                    func = self._cmd_list.get(command, 'Unknown command.')
                    answer_dict['text'] = func(*input_data_list)
                else:
                    answer_dict['text'] = 'Please use a command from the list.'
                return answer_dict
            except Exception as exc:
                logger.error(exc)
                msg = 'Something went wrong in message processing'
                answer_dict['text'] = msg
                return answer_dict
