import allure

from src.api.pet.pet_api import PetApi
from src.api.pet.pet_assertions import PetAssertions
from test_data.factories.pet_data_factory import create_random_pet_body

pet_api = PetApi()

@allure.story('Delete pet API')
class TestDeletePet:
  @allure.testcase('https://diceus.atlassian.net/browse/TC-07')
  def test_delete_a_pet(self):
    # Create new pet
    payload = create_random_pet_body()
    create_pet_res = pet_api.create_pet(payload)
    PetAssertions.assert_pet_created_successfully(create_pet_res)    
    # Get a pet_id
    pet_id = PetAssertions.get_pet_id(create_pet_res)
    # Delete a pet
    del_pet_res = pet_api.delete_pet(pet_id)
    PetAssertions.status_ok(del_pet_res)
    PetAssertions.is_equal(str(pet_id), del_pet_res.json()['message'])
    # Get deleted pet
    get_deleted_pet_res = pet_api.get_pet(pet_id)
    PetAssertions.status_not_found(get_deleted_pet_res)
    PetAssertions.is_equal('Pet not found', get_deleted_pet_res.json()['message'])

  @allure.testcase('https://diceus.atlassian.net/browse/TC-08')
  def test_delete_pet_with_invalid_id(self):
    del_pet_res = pet_api.delete_pet('random_str')
    PetAssertions.status_not_found(del_pet_res.status_code)
    PetAssertions.contains_text(del_pet_res.json()['message'], 'random_str')

  @allure.testcase('https://diceus.atlassian.net/browse/TC-09')
  def test_delete_a_non_existent_pet(self):
    del_pet_res = pet_api.delete_pet(9999999999999)
    PetAssertions.status_not_found(del_pet_res.status_code)
