import allure

from src.api.pet.pet_api import PetApi
from src.api.pet.pet_assertions import PetAssertions
from test_data.factories.pet_data_factory import (
  create_random_pet_body,
  update_pet_body
)
from src.utils.randomize import rand_unique_str

pet_api = PetApi()

@allure.story('Update pet API')
class TestUpdatePet:
  @allure.testcase('https://diceus.atlassian.net/browse/TC-12')
  def test_update_pet_name(self):
    # Create new pet
    payload = create_random_pet_body()
    create_pet_res = pet_api.create_pet(payload)
    PetAssertions.assert_pet_created_successfully(create_pet_res)    
    # Get created pet
    pet_id = PetAssertions.get_pet_id(create_pet_res)
    # Update pet
    update_payload = update_pet_body(payload, { 'name': rand_unique_str('new_name') })
    update_pet_res = pet_api.update_pet(pet_id, update_payload)
    PetAssertions.status_ok(update_pet_res)
    PetAssertions.is_equal(update_payload['name'], update_pet_res.json()['name'])
    # Get updated pet
    get_pet_res = pet_api.get_pet(pet_id)
    PetAssertions.status_ok(get_pet_res)
    PetAssertions.is_equal(update_payload['name'], get_pet_res.json()['name'])