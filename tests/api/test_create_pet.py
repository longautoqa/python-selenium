import pytest
import allure

from src.api.pet.pet_api import PetApi
from src.api.pet.pet_assertions import PetAssertions
from src.api.pet.types import PetStatus
from src.utils.randomize import rand_unique_str, random_image_url
from src.api.libs.utils.schema_validator import SchemaValidator

from test_data.factories.pet_data_factory import (
  create_random_pet_body,
  create_pet_with_status,
  create_pet_with_tags,
  create_pet_with_photo_urls
)

pet_api = PetApi()

@allure.story('Create pet API')
class TestCreatePet:
  @allure.testcase('https://diceus.atlassian.net/browse/TC-01')
  def test_create_pet_with_all_fields(self):
    # Create new pet
    payload = create_random_pet_body()
    create_pet_res = pet_api.create_pet(payload)
    PetAssertions.assert_pet_created_successfully(create_pet_res)    
    # Get created pet
    pet_id = PetAssertions.get_pet_id(create_pet_res)
    get_pet_res = pet_api.get_pet(pet_id)

  @pytest.mark.parametrize('status', [PetStatus.AVAILABLE, PetStatus.PENDING, PetStatus.SOLD])
  @allure.testcase('https://diceus.atlassian.net/browse/TC-02')
  def test_create_pet_with_different_status(self, status):
    # Create new pet
    payload = create_pet_with_status(status)
    create_pet_res = pet_api.create_pet(payload)
    PetAssertions.assert_pet_created_successfully(create_pet_res)
    PetAssertions.assert_pet_status(create_pet_res, status)
    SchemaValidator.validate_response(create_pet_res, 'pet.json')
    # Get created pet
    pet_id = PetAssertions.get_pet_id(create_pet_res)
    get_pet_res = pet_api.get_pet(pet_id)
    PetAssertions.is_equal(status, PetAssertions.get_pet_status(get_pet_res))
    SchemaValidator.validate_response(get_pet_res, 'pet.json')

  @allure.testcase('https://diceus.atlassian.net/browse/TC-03')
  def test_create_pet_with_only_name(self):
    # Create new pet
    pet_name = rand_unique_str('pet_name')
    create_pet_res = pet_api.create_pet({ 'name': pet_name })
    PetAssertions.assert_pet_created_successfully(create_pet_res)    
    PetAssertions.is_equal(pet_name, PetAssertions.get_pet_name(create_pet_res))
    # Get created pet
    pet_id = PetAssertions.get_pet_id(create_pet_res)
    get_pet_res = pet_api.get_pet(pet_id)
    PetAssertions.is_equal(pet_name, PetAssertions.get_pet_name(get_pet_res))
    PetAssertions.is_equal([], PetAssertions.get_photo_urls(get_pet_res))
    PetAssertions.is_equal([], PetAssertions.get_pet_tags(get_pet_res))

  @allure.testcase('https://diceus.atlassian.net/browse/TC-04')
  def test_create_pet_with_any_status(self):
    # Create new pet
    random_status = rand_unique_str('status')
    payload = create_random_pet_body({ 'status': random_status })
    create_pet_res = pet_api.create_pet(payload)
    PetAssertions.assert_pet_created_successfully(create_pet_res)
    PetAssertions.assert_pet_status(create_pet_res, random_status)
    # Get created pet
    pet_id = PetAssertions.get_pet_id(create_pet_res)
    get_pet_res = pet_api.get_pet(pet_id)
    PetAssertions.is_equal(random_status, PetAssertions.get_pet_status(get_pet_res))

  @pytest.mark.parametrize('tags',
    [
      [],
      [{'name': rand_unique_str('tag')}],
      [{'name': rand_unique_str('tag')}, {'name': rand_unique_str('tag')}],
    ],
    ids=['no tag', 'single tag', 'multi tags']
  )
  @allure.testcase('https://diceus.atlassian.net/browse/TC-05')
  def test_create_pet_with_tags(self, tags):
    # Create new pet
    payload = create_pet_with_tags(tags)
    create_pet_res = pet_api.create_pet(payload)
    expected_tag_names = [tag['name'] for tag in tags]
    PetAssertions.assert_pet_tag_names(create_pet_res, expected_tag_names)
    # Get created pet
    pet_id = PetAssertions.get_pet_id(create_pet_res)
    get_pet_res = pet_api.get_pet(pet_id)
    PetAssertions.is_equal(expected_tag_names, PetAssertions.extract_tag_names(get_pet_res))

  @pytest.mark.parametrize('images',
    [
      [],
      [random_image_url()],
      [random_image_url(), random_image_url()],
    ],
    ids=['no image', 'single image', 'multi images']
  )
  @allure.testcase('https://diceus.atlassian.net/browse/TC-06')
  def test_create_pet_with_photo_url(self, images):
    # Create new pet
    payload = create_pet_with_photo_urls(images)
    create_pet_res = pet_api.create_pet(payload)
    PetAssertions.assert_pet_photo_urls(create_pet_res, images)
    # Get created pet
    pet_id = PetAssertions.get_pet_id(create_pet_res)
    get_pet_res = pet_api.get_pet(pet_id)
    PetAssertions.is_equal(images, PetAssertions.get_photo_urls(get_pet_res))
