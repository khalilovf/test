import allure
import pytest
from http_api.api_methods import api_sender
from config.testconfig import TestConfig


@allure.severity(allure.severity_level.CRITICAL)
class TestSmokeSuite:
    test_host = TestConfig.host
    users_path = TestConfig.users_path
    register_path = TestConfig.register_path
    login_path = TestConfig.login_path
    test_user = TestConfig.user_id

    @pytest.mark.parametrize('url, path, test_data', [(test_host, users_path, test_user)], scope="session")
    @allure.testcase('find one user')
    def test_get_one_user(self, url, path, test_data):
        get_one_user_result_json, request = api_sender(url, 200, 'GET', path + '/' + str(test_data))
        assert test_data == get_one_user_result_json.get('data').get('id')  # finded user == our hardcoded user

    @pytest.mark.parametrize('url, path', [(test_host, users_path)], scope="session")
    @allure.testcase('get list of all users')
    def test_get_users_list(self, url, path):
        get_all_users_result_json, request = api_sender(url, 200, 'GET', path)
        users_per_page = get_all_users_result_json.get('per_page')  # count users
        users_list_len = len(get_all_users_result_json.get('data'))  # check users per page number
        assert users_per_page == users_list_len
        avatar_url = get_all_users_result_json['data'][0].get('avatar')
        api_sender(avatar_url, 200, 'GET', '')  # check that avatar from response is available

    @pytest.mark.parametrize('url, path, test_data', [(test_host, users_path, '{"name": "dows","job": "fuuu"}')],
                             scope="session")
    @allure.testcase('create user and find him')
    @pytest.mark.xfail(reason='service is not creating users, so they cant be found')
    def test_post_create_user(self, url, path, test_data):
        with allure.step('create user'):
            create_user_result_json, request = api_sender(url, 201, 'POST', path, test_data)
            created_user_id = create_user_result_json.get('id')
        with allure.step('find created user with id: ' + created_user_id):
            find_created_user_json, request2 = api_sender(url, 404, 'GET', path + '/' + created_user_id)  # 404 - its ok
            assert created_user_id == find_created_user_json.get('id')
