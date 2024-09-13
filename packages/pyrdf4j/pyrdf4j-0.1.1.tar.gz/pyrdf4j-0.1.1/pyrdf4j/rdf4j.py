import json
import sys
import traceback
from http import HTTPStatus

import requests

from pyrdf4j.api_repo import APIRepo
from pyrdf4j.constants import DEFAULT_QUERY_RESPONSE_MIME_TYPE, DEFAULT_RESPONSE_TRIPLE_MIME_TYPE
from pyrdf4j.errors import URINotReachable, TerminatingError, BulkLoadError, \
    CreateRepositoryAlreadyExists, CreateRepositoryError, DropRepositoryError
from pyrdf4j.server import Server, Transaction
from pyrdf4j.repo_types import repo_config_factory


class RDF4J:
    """
    High level API to the RDF4J
    """

    def __init__(self, rdf4j_base=None, api=APIRepo):

        self.server = Server(rdf4j_base)
        self.api_class = api
        self.apis = {}

    def get_api(self, repo_id, repo_uri=None):
        if repo_id in self.apis:
            pass
        else:
            self.apis[repo_id] = self.api_class(self.server, repo_id, repo_uri=repo_uri)
        return self.apis[repo_id]

    def bulk_load_from_uri(
            self,
            repo_id,
            target_uri,
            content_type,
            clear_repository=False,
            repo_uri=None,
            auth=None,
            base_uri=None,
    ):
        """
        Load the triple_data from the harvest uri
        and push it into the triplestore
        :param repo_id:
        :param target_uri:
        :param content_type:
        :return:
        """

        # Load the triple_data from the harvest target_uri
        try:
            response = requests.get(target_uri)
        except requests.exceptions.ConnectionError as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            # todo: Logger
            print("GET termiated due to error %s %s" % (exc_type, exc_value))
            for line in traceback.format_tb(exc_traceback):
                print("Traceback:%s" % line[:-1])
            raise URINotReachable(
                'Database not reachable. Tried GET on {uri}'.format(uri=target_uri))
        if response.status_code != HTTPStatus.OK:
            raise URINotReachable(response.content)
        triple_data = response.content

        api = self.get_api(repo_id, repo_uri=repo_uri)

        if clear_repository:
            return api.replace_triple_data_in_repo(triple_data, content_type, auth=auth, base_uri=base_uri)

        #        response = self.create_repository(repo_id, auth=auth)
        #        if response.status_code == HTTPStatus.CONFLICT:
        #            if b'REPOSITORY EXISTS' in response.content:
        #                pass
        #        elif response.status_code != HTTPStatus.OK:
        #            raise TerminatingError

        return api.add_triple_data_to_repo(triple_data, content_type, auth=auth, base_uri=base_uri)

    def graph_from_uri(self,
                       repository_id,
                       target_uri,
                       content_type,
                       repo_type='memory',
                       repo_label=None,
                       auth=None,
                       overwrite=False,
                       accept_existing=True,
                       clear_repository=False,
                       **kwargs):
        """
        :param repository_id:
        :param uri:
        :param content_type:
        :param clear_repository:
        :return:
        """
        self.create_repository(repository_id, accept_existing=accept_existing, repo_type=repo_type,
                               repo_label=repo_label, auth=auth, overwrite=overwrite, **kwargs)
        response = self.bulk_load_from_uri(
            repository_id, target_uri, content_type, clear_repository=clear_repository, auth=auth)
        return response

    def create_repository(self,
                          repo_id,
                          repo_type='memory',
                          repo_label=None,
                          auth=None,
                          overwrite=False,
                          accept_existing=False,
                          **kwargs):
        """
        :param repo_id: ID of the repository to create
        :param repo_type: (Optional) Configuration template
            type name of the server (see repo_types.py)
        :param repo_label: (Optional) Label for the repository
        :param auth: (Optional) user credentials for authentication
            in form of a HTTPBasicAuth instance (testing only)
        :param overwrite: (Optional) If overwrite is enabled an existing
            server will be overwritten (testing only). Use with care!
        :param kwargs: Parameters for the Configuration template
        :return:
        """
        if repo_label is None:
            repo_label = repo_id

        repo_config = repo_config_factory(
            repo_type,
            repo_id=repo_id,
            repo_label=repo_label,
            **kwargs)

        api = self.get_api(repo_id)

        response = api.create_repository(repo_config, auth=auth)

        try:
            if response.status_code in [HTTPStatus.NO_CONTENT]:
                return response
            elif response.status_code == HTTPStatus.CONFLICT:
                msg = str(response.status_code) + ': ' + str(response.content)
                raise CreateRepositoryAlreadyExists(msg)
            else:
                msg = str(response.status_code) + ': ' + str(response.content)
                raise CreateRepositoryError(msg)

        except CreateRepositoryAlreadyExists:
            if overwrite:
                api.drop_repository(auth=auth)
                api.create_repository(repo_config, auth=auth)
            elif accept_existing:
                pass
            else:
                raise CreateRepositoryAlreadyExists(msg)

        return response

    def drop_repository(self, repo_id, accept_not_exist=False, auth=None):
        """
        :param repo_id: ID of the repository to drop
        :return: response
        :raises: DropRepositoryError if operation fails
        """

        api = self.get_api(repo_id)

        response = api.drop_repository(auth=auth)
        if response.status_code in [HTTPStatus.NO_CONTENT]:
            return response
        elif response.status_code in [HTTPStatus.NOT_FOUND]:
            if accept_not_exist:
                return response
        msg = str(response.status_code) + ': ' + str(response.content)
        raise DropRepositoryError(msg)

    def move_data_between_repositorys(
            self,
            target_repository,
            source_repository,
            auth=None,
            repo_type='memory'):
        """
        :param target_repository:
        :param source_repository:
        :param auth:
        :return:
        """
        self.create_repository(source_repository,
                               accept_existing=True,
                               auth=auth,
                               repo_type=repo_type)
        self.create_repository(target_repository,
                               accept_existing=True,
                               auth=auth,
                               repo_type=repo_type)

        api_source = self.get_api(source_repository)
        triple_data = api_source.query_repository("CONSTRUCT {?s ?o ?p} WHERE {?s ?o ?p}",
                                                  auth=auth,
                                                  mime_type=DEFAULT_RESPONSE_TRIPLE_MIME_TYPE)
        api_target = self.get_api(target_repository)
        response = api_target.add_triple_data_to_repo(
            triple_data,
            DEFAULT_RESPONSE_TRIPLE_MIME_TYPE,
            auth=auth)

        return response

    def get_turtle_from_query(self, repo_id, query, auth=None):
        """
        :param repository:
        :param query:
        :return:
        """
        mime_type = 'text/turtle'
        triple_data = self.get_triple_data_from_query(
            repo_id,
            query,
            mime_type=mime_type,
            auth=auth)
        return triple_data

    def get_triple_data_from_query(
            self,
            repo_id,
            query,
            mime_type=None,
            auth=None,
            repo_uri=None):
        """
        :param repo_id:
        :param query:
        :param mime_type:
        :return:
        """
        api = self.get_api(repo_id, repo_uri=repo_uri)

        if mime_type is None:
            mime_type = DEFAULT_RESPONSE_TRIPLE_MIME_TYPE

        return api.query_repository(query, mime_type=mime_type, auth=auth)

    def empty_repository(self, repository, auth=None):
        """
        :param repository:
        :return:
        """
        # self.create_repository(repository, auth=auth)
        api = self.get_api(repository)
        return api.empty_repository(auth=auth)

    def query_repository(self, repo_id, query, auth=None):
        api = self.get_api(repo_id)

        res = api.query_repository(query, auth=auth)

        json_data = json.loads(res)

        return json_data

    def add_data_to_repo(
            self,
            repo_id,
            triple_data,
            content_type,
            repo_uri=None,
            auth=None):

        api = self.get_api(repo_id, repo_uri=repo_uri)

        return api.add_triple_data_to_repo(triple_data, content_type, auth=auth)
