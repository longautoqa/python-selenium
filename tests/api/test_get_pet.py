import allure

from src.api.pet.pet_api import PetApi
from src.api.pet.pet_assertions import PetAssertions
from test_data.factories.pet_data_factory import create_random_pet_body
from src.api.libs.utils.schema_validator import SchemaValidator

pet_api = PetApi()

@allure.story('Get pet API')
class TestGetPet:
  @allure.testcase('https://diceus.atlassian.net/browse/TC-10')
  def test_get_pet(self):
    # Create new pet
    payload = create_random_pet_body()
    create_pet_res = pet_api.create_pet(payload)
    PetAssertions.assert_pet_created_successfully(create_pet_res)
    # Get created pet
    pet_id = PetAssertions.get_pet_id(create_pet_res)
    get_pet_res = pet_api.get_pet(pet_id)
    SchemaValidator.validate_response(get_pet_res, 'pet.json')

  @allure.testcase('https://diceus.atlassian.net/browse/TC-11')
  def test_get_a_non_existing_pet(self):
    get_pet_res = pet_api.get_pet(9999999999999)
    PetAssertions.status_not_found(get_pet_res.status_code)
    PetAssertions.is_equal('Pet not found', get_pet_res.json()['message'])
