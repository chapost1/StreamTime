from use_cases.db_operation_utils.concrete import update_in_database
from typing import Dict
import pytest
from common.app_errors import AppError


@pytest.mark.asyncio
async def test_should_return_none_on_successful_update():
    class SuccessulUpdate:
        async def update(self, new_desired_state: Dict) -> None:
            return None
    
    assert await update_in_database(updatable=SuccessulUpdate(), new_desired_state={}) is None


@pytest.mark.asyncio
async def test_should_propagate_exception():
    class ExceptionalUpdate:
        async def update(self, new_desired_state: Dict) -> None:
            raise AppError()
    
    try:
        await update_in_database(updatable=ExceptionalUpdate(), new_desired_state={})
        # should not reach
        assert 2 == 1
    except AppError as ae:
        assert 1 == 1


@pytest.mark.asyncio
async def test_should_fail_if_new_desired_state_dict_is_not_given():
    class UpdateClass:
        async def update(self) -> None:
            return None
    try:
        await update_in_database(updatable=UpdateClass())
        # should not reach
        assert 2 == 1
    except TypeError:
        assert 1 == 1


@pytest.mark.asyncio
async def test_should_pass_new_desired_state_to_update_class():
    class Updatable:
        side_effect = None

        async def update(self, new_desired_state: Dict) -> None:
            self.side_effect = new_desired_state
            return None

    mock = Updatable()

    arg = {'message': 'hello world!'}
    await update_in_database(updatable=mock, new_desired_state=arg)

    assert mock.side_effect == arg
