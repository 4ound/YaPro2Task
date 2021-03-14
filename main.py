from flask import Flask, request
from flask_restplus import Api, Resource, fields
from db import InMemoryDb

flask_app = Flask(__name__)
app = Api(app=flask_app,
          version="1.0",
          title="Notes service",
          ordered=True)
db = InMemoryDb()

name_space = app.namespace('notes', description='Notes APIs')

note_model = app.model(
    'Замтека без id',
    {
        'title': fields.String(
            required=True,
            description="Заголовок заметки",
            help="Если заголовок не указан - то вместо него вернутся первые N символов текста заметки"
        ),
        'content': fields.String(required=True, description="Описание заметки", help="Не может быть пустым")
    }
)

note_with_id_model = app.model(
    'Заметка с id',
    {
        'id': fields.Integer(required=True, description="Идентифкатор заметки", help=""),
        'title': fields.String(
            required=True,
            description="Заголовок заметки",
            help="Если заголовок не указан - то вместо него вернутся первые N символов текста заметки"
        ),
        'content': fields.String(required=True, description="Текст заметки", help="Не может быть пустым")
    }
)


@name_space.route("/")
class NotesClass(Resource):
    @name_space.doc(params={'query': 'Фильтрующий запрос'})
    @name_space.response(200, 'Возвращает список заметок', note_with_id_model)
    def get(self):
        """
        Получение списка всех заметок.
        Если задан фильтр, то список фильтруется в соответствии с ним (запрос содержится в наименовании (title) или в
        тексте заметки (content)))
        Если заголовок не указан - то вместо него возвращать первые N символов текста заметки,
        где N - число, задаваемое в конфигурационном файле
        """
        query = request.args.get('query')

        return db.get_notes(query)

    @name_space.response(200, 'Возвращает созданную заметку', note_with_id_model)
    @name_space.response(400, 'Переданы неверные аргументы')
    @name_space.expect(note_model)
    def post(self):
        """
        Добавление заметки
        C возможностью указания заголовка (title) и текста заметки (content)
        Заголовок - не обязательный параметр

        """
        title = request.json.get('title')
        content = request.json.get('content')
        if content:
            return db.add_note(title, content)
        else:
            return None, 400


@name_space.route("/<int:id>")
@app.doc(params={'id': 'Идентификатор заметки'})
class NotesClass(Resource):
    @name_space.response(200, 'Заметка найдена и удалена', note_with_id_model)
    @name_space.response(400, 'Замтека не найдена')
    @name_space.expect(note_model)
    def put(self, id):
        """
        Редактирование заметки по ее идентификатору
        Для редактирования доступны: заголовок, текст заметки
        """
        title = request.json.get('title')
        content = request.json.get('content')
        note = db.modify_note(id, title, content)
        if note:
            return note.get()
        else:
            return None, 400

    @name_space.response(200, 'Заметка найдена и удалена')
    @name_space.response(400, 'Замтека не найдена')
    def delete(self, id):
        """
        Удаление заметки по ее идентификатору
        """
        is_deleted = db.delete(id)
        if is_deleted:
            return None, 200
        else:
            return None, 400

    @name_space.response(200, 'Заметка найдена и удалена')
    @name_space.response(400, 'Замтека не найдена')
    def get(self, id):
        """
        Получение заметки по ее идентификатору
        Если заголовок не указан - то вместо него возвращать первые N символов текста заметки, где N - число, задаваемое в конфигурационном файле
        """
        note = db.get_note(id)
        if note:
            return note.get(), 200
        else:
            return None, 400


if __name__ == '__main__':
    flask_app.run(debug=True)
