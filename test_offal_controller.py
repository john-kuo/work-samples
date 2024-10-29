import pytest
from unittest.mock import MagicMock, patch
from offal_controller import OffalController, DataService

@pytest.fixture
def controller():
    return OffalController()

@pytest.fixture
def mock_data_service():
    return MagicMock(spec=DataService)

def test_init_scope(controller):
    assert controller.scope is not None

def test_authenticated_user(controller):
    assert controller.scope['user'] is not None
    assert controller.scope['user'].is_authenticated()

@pytest.mark.parametrize("callback_type,expected_result", [
    ("success", {"result": {"id": 2}}),
    ("error", "Request Failed")
])
def test_fetch_offals(controller, mock_data_service, callback_type, expected_result):
    controller.data_service = mock_data_service
    mock_data_service.fetch.side_effect = lambda cb: cb[callback_type](expected_result)

    controller.init()

    mock_data_service.fetch.assert_called_once()
    if callback_type == "success":
        assert controller.scope['offal_list'] == expected_result
    else:
        assert controller.scope['error'] == expected_result

@pytest.mark.parametrize("callback_type,expected_result", [
    ("success", {"result": {"id": 2}}),
    ("error", "Request Failed")
])
def test_create_offal(controller, mock_data_service, callback_type, expected_result):
    controller.data_service = mock_data_service
    mock_data_service.create.side_effect = lambda data, cb: cb[callback_type](expected_result)

    controller.scope['new_offal'] = {"id": 1, "animal": "dog"}
    controller.scope['offal_list'] = [{"animal": "cat"}]
    controller.create_offal()

    assert controller.scope['new_offal']['animal'] == "cat"
    assert not controller.scope['show_modal']['create']
    mock_data_service.create.assert_called_once()
    if callback_type == "error":
        assert controller.scope['error'] == expected_result

@pytest.mark.parametrize("callback_type,expected_result", [
    ("success", {"result": {"id": 2}}),
    ("error", "Request Failed")
])
def test_update_offal(controller, mock_data_service, callback_type, expected_result):
    controller.data_service = mock_data_service
    mock_data_service.update.side_effect = lambda id, data, cb: cb[callback_type](expected_result)

    controller.update_offal()

    mock_data_service.update.assert_called_once()
    if callback_type == "error":
        assert controller.scope['error'] == expected_result

@pytest.mark.parametrize("callback_type,expected_result", [
    ("success", {"result": {"id": 2}}),
    ("error", "Request Failed")
])
def test_delete_offal(controller, mock_data_service, callback_type, expected_result):
    controller.data_service = mock_data_service
    mock_data_service.remove.side_effect = lambda id, cb: cb[callback_type](expected_result)

    controller.delete_offal_with_id()

    mock_data_service.remove.assert_called_once()
    assert not controller.scope['show_modal']['delete']
    if callback_type == "error":
        assert controller.scope['error'] == expected_result

@pytest.mark.parametrize("dialog_type", ["create", "delete", "update"])
def test_open_dialog(controller, dialog_type):
    getattr(controller, f"open_{dialog_type}_offal_dialog")()
    assert controller.scope['show_modal'][dialog_type]

@pytest.mark.parametrize("dialog_type", ["create", "delete", "update"])
def test_close_dialog(controller, dialog_type):
    getattr(controller, f"close_{dialog_type}_offal_dialog")()
    assert not controller.scope['show_modal'][dialog_type]

if __name__ == "__main__":
    pytest.main()