from flask import Flask, jsonify, request
from typing import Dict, Any, Callable

app = Flask(__name__)

class DataService:
    def __init__(self):
        self.offal_list = []

    def fetch(self, callback: Dict[str, Callable]):
        try:
            callback['success'](self.offal_list)
        except Exception as e:
            callback['error'](str(e))

    def create(self, new_offal: Dict[str, Any], callback: Dict[str, Callable]):
        try:
            self.offal_list.append(new_offal)
            callback['success'](self.offal_list)
        except Exception as e:
            callback['error'](str(e))

    def remove(self, offal_id: int, callback: Dict[str, Callable]):
        try:
            self.offal_list = [offal for offal in self.offal_list if offal['id'] != offal_id]
            callback['success'](self.offal_list)
        except Exception as e:
            callback['error'](str(e))

    def update(self, offal_id: int, updated_offal: Dict[str, Any], callback: Dict[str, Callable]):
        try:
            for i, offal in enumerate(self.offal_list):
                if offal['id'] == offal_id:
                    self.offal_list[i] = updated_offal
                    break
            callback['success'](self.offal_list)
        except Exception as e:
            callback['error'](str(e))

class OffalController:
    def __init__(self):
        self.data_service = DataService()
        self.scope = {
            'offal_list': {},
            'new_offal': {},
            'offal_to_update': {},
            'offal_to_delete': {},
            'show_modal': {
                'create': False,
                'update': False,
                'delete': False
            },
            'error': None
        }

    def init(self):
        self.data_service.fetch(self.callbacks['fetch_offal'])

    def delete_offal_with_id(self):
        self.data_service.remove(self.scope['offal_to_delete']['id'], self.callbacks['remove_offal'])

    def create_offal(self):
        self.scope['new_offal']['animal'] = self.scope['offal_list'][0]['animal']
        self.scope['show_modal']['create'] = False
        self.data_service.create(self.scope['new_offal'], self.callbacks['create_offal'])

    def update_offal(self):
        self.data_service.update(self.scope['offal_to_update']['id'], self.scope['offal_to_update'], self.callbacks['update_offal'])

    def open_delete_offal_dialog(self, offal_to_delete):
        self.scope['offal_to_delete'] = offal_to_delete
        self.scope['show_modal']['delete'] = True

    def close_delete_offal_dialog(self):
        self.scope['show_modal']['delete'] = False

    def open_create_offal_dialog(self):
        self.scope['show_modal']['create'] = True

    def close_create_offal_dialog(self):
        self.scope['show_modal']['create'] = False

    def open_edit_offal_dialog(self, offal_to_edit):
        self.scope['offal_to_update'] = offal_to_edit
        self.scope['show_modal']['update'] = True

    def close_edit_offal_dialog(self):
        self.scope['show_modal']['update'] = False

    callbacks = {
        'fetch_offal': {
            'success': lambda data: setattr(OffalController, 'scope', {'offal_list': data}),
            'error': lambda: setattr(OffalController, 'scope', {'error': "Request Failed"})
        },
        'create_offal': {
            'success': lambda data: (
                setattr(OffalController, 'scope', {'offal_list': data}),
                OffalController.data_service.fetch(OffalController.callbacks['fetch_offal'])
            ),
            'error': lambda: setattr(OffalController, 'scope', {'error': "Request Failed"})
        },
        'remove_offal': {
            'success': lambda data: (
                setattr(OffalController, 'scope', {'offal_list': data}),
                OffalController.data_service.fetch(OffalController.callbacks['fetch_offal']),
                setattr(OffalController, 'scope', {'show_modal': {'delete': False}})
            ),
            'error': lambda: setattr(OffalController, 'scope', {'error': "Request Failed"})
        },
        'update_offal': {
            'success': lambda data: (
                setattr(OffalController, 'scope', {'offal_list': data}),
                OffalController.data_service.fetch(OffalController.callbacks['fetch_offal']),
                setattr(OffalController, 'scope', {'show_modal': {'update': False}})
            ),
            'error': lambda: setattr(OffalController, 'scope', {'error': "Request Failed"})
        }
    }

# Flask routes to handle API requests
@app.route('/api/offal', methods=['GET', 'POST', 'PUT', 'DELETE'])
def handle_offal():
    controller = OffalController()
    if request.method == 'GET':
        controller.init()
    elif request.method == 'POST':
        controller.create_offal()
    elif request.method == 'PUT':
        controller.update_offal()
    elif request.method == 'DELETE':
        controller.delete_offal_with_id()
    return jsonify(controller.scope)

if __name__ == '__main__':
    app.run(debug=True)