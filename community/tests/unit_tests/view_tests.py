from rest_framework import exceptions
from rest_framework.parsers import MultiPartParser, JSONParser
from rest_framework.request import Request

from community.tests.conftests import *
from rest_framework.test import APIRequestFactory
from community.service.post_service import PostService, PostsService
from community.view.post_view import PostView, GetPostsView


class TestViewLayerValidators:
    def test_query_param_validator_with_invalid_data(self):
        pass

    def test_query_param_validator_with_valid_data(self):
        pass

    def test_path_params_validator_with_invalid_data(self):
        pass

    def test_path_params_validator_with_valid_data(self):
        pass


class TestPostView:
    PostViewPath = 'post/'
    PostsViewPath = 'posts/'

    def test_get_method_with_invalid_path_params(
            self,
            invalid_post_path_param_list
    ):
        factory = APIRequestFactory()
        request = factory.get(self.PostViewPath)

        for path_param in invalid_post_path_param_list:
            with pytest.raises(exceptions.ParseError):
                PostView().get(request, post_id=path_param)

    def test_get_method_with_valid_path_params(
            self,
            mocker,
            valid_post_path_param,
            mocked_service_response
    ):
        mocker = mocker.patch.object(PostService, "get_post")
        mocker.return_value = mocked_service_response

        factory = APIRequestFactory()
        request = factory.get(self.PostViewPath)

        response = PostView().get(request, post_id=valid_post_path_param)
        assert response

    def test_post_method_with_invalid_request_body(
            self,
            invalid_reqeust_post_body_for_method_post
    ):
        for request_body in invalid_reqeust_post_body_for_method_post:
            factory = APIRequestFactory()
            request = factory.post(self.PostViewPath, data=request_body)
            request = Request(request, parsers=[MultiPartParser()])

            with pytest.raises(exceptions.ParseError):
                PostView().post(request)

    def test_post_method_with_valid_request_body(
            self,
            mocker,
            valid_reqeust_post_body_for_method_post,
            mocked_service_response
    ):
        create_post_mocker = mocker.patch.object(PostService, "create_post")
        create_post_mocker.return_value = mocked_service_response

        for request_body in valid_reqeust_post_body_for_method_post:
            factory = APIRequestFactory()
            request = factory.post(self.PostViewPath, data=request_body)
            request = Request(request, parsers=[MultiPartParser()])

            response = PostView().post(request)
            assert response

    def test_patch_method_with_invalid_request_body_and_valid_path_param(
            self,
            invalid_reqeust_post_body_for_method_post,
            valid_post_path_param
    ):
        for request_body in invalid_reqeust_post_body_for_method_post:
            factory = APIRequestFactory()
            request = factory.patch(self.PostViewPath, data=request_body)
            request = Request(request, parsers=[MultiPartParser()])

            with pytest.raises(exceptions.ParseError):
                PostView().patch(request, post_id=valid_post_path_param)

    def test_patch_method_with_valid_request_body_and_invalid_path_params(
            self,
            valid_reqeust_post_body_for_method_post,
            invalid_post_path_param_list
    ):
        for path_param in invalid_post_path_param_list:
            for request_body in valid_reqeust_post_body_for_method_post:
                factory = APIRequestFactory()
                request = factory.patch(self.PostViewPath, data=request_body)
                request = Request(request, parsers=[MultiPartParser()])

                with pytest.raises(exceptions.ParseError):
                    PostView().patch(request, post_id=path_param)

    def test_patch_method_with_invalid_request_body_and_invalid_path_params(
            self,
            invalid_reqeust_post_body_for_method_post,
            invalid_post_path_param_list
    ):
        for path_param in invalid_post_path_param_list:
            for request_body in invalid_reqeust_post_body_for_method_post:
                factory = APIRequestFactory()
                request = factory.patch(self.PostViewPath, data=request_body)
                request = Request(request, parsers=[MultiPartParser()])

                with pytest.raises(exceptions.ParseError):
                    PostView().patch(request, post_id=path_param)

    def test_patch_method_with_valid_request_body_and_valid_path_params(
            self,
            mocker,
            valid_reqeust_post_body_for_method_post,
            valid_post_path_param,
            mocked_service_response
    ):
        get_post_user_id_mocker = mocker.patch.object(PostService, "get_post_user_id")
        get_post_user_id_mocker.return_value = None
        check_object_permissions_mocker = mocker.patch.object(PostView, "check_object_permissions")
        check_object_permissions_mocker.return_value = None
        update_post_mocker = mocker.patch.object(PostService, "update_post")
        update_post_mocker.return_value = mocked_service_response

        for request_body in valid_reqeust_post_body_for_method_post:
            factory = APIRequestFactory()
            request = factory.patch(self.PostViewPath, data=request_body)
            request = Request(request, parsers=[MultiPartParser()])

            response = PostView().patch(request, post_id=valid_post_path_param)
            assert response

    def test_delete_method_with_invalid_path_param(
            self,
            invalid_post_path_param_list
    ):
        factory = APIRequestFactory()
        request = factory.delete(self.PostViewPath)

        for path_param in invalid_post_path_param_list:
            with pytest.raises(exceptions.ParseError):
                PostView().delete(request, post_id=path_param)

    def test_delete_method_with_valid_path_param(
            self,
            mocker,
            valid_post_path_param,
            mocked_service_response
    ):
        get_post_user_id_mocker = mocker.patch.object(PostService, "get_post_user_id")
        get_post_user_id_mocker.return_value = None
        check_object_permissions_mocker = mocker.patch.object(PostView, "check_object_permissions")
        check_object_permissions_mocker.return_value = None
        delete_post_mocker = mocker.patch.object(PostService, "delete_post")
        delete_post_mocker.return_value = mocked_service_response

        factory = APIRequestFactory()
        request = factory.delete(self.PostViewPath)

        response = PostView().delete(request, post_id=valid_post_path_param)
        assert response

    def test_authentication_permission(self):
        pass

    def test_instance_permission(self):
        pass


class TestPostsView:
    PostsViewPath = 'posts/'

    def test_get_method_with_invalid_query_param(
            self,
            invalid_post_query_params_list,
    ):
        for query_param in invalid_post_query_params_list:
            factory = APIRequestFactory()
            request = factory.get(self.PostsViewPath, data=query_param, format='json')
            request = Request(request, parsers=[JSONParser()])

            with pytest.raises(exceptions.ParseError):
                GetPostsView().get(request)

    def test_get_method_with_valid_query_param(
            self,
            mocker,
            valid_post_query_params_list,
            mocked_service_response
    ):
        mocker = mocker.patch.object(PostsService, "get_posts")
        mocker.return_value = mocked_service_response

        for query_param in valid_post_query_params_list:
            factory = APIRequestFactory()
            request = factory.get(self.PostsViewPath, data=query_param, format='json')
            request = Request(request, parsers=[JSONParser()])

            response = GetPostsView().get(request)
            assert response
