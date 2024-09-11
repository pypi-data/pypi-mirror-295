"""
SPDX-License-Identifier: Apache-2.0
Copyright Contributors to the ODPi Egeria project.

Runtime manager is a view service that supports user interaction with the running platforms.

"""
import asyncio

from requests import Response

from pyegeria import Client, max_paging_size, body_slimmer


class RuntimeManager(Client):
    """
    Client to issue Runtime status requests.

    Attributes:

        view_server : str
                Name of the server to use.
        platform_url : str
            URL of the server platform to connect to
        user_id : str
            The identity of the user calling the method - this sets a default optionally used by the methods
            when the user doesn't pass the user_id on a method call.
        user_pwd: str
            The password associated with the user_id. Defaults to None
        token: str, optional
            Bearer token

    Methods:

    """

    def __init__(
        self,
        view_server: str,
        platform_url: str,
        user_id: str,
        user_pwd: str = None,
        token: str = None,
    ):
        Client.__init__(self, view_server, platform_url, user_id, user_pwd, token=token)
        self.cur_command_root = f"{platform_url}/servers/"
        self.platform_guid = "44bf319f-1e41-4da1-b771-2753b92b631a"  # this is platform @ 9443 from the core content archive
        self.default_platform_name = (
            "Default Local OMAG Server Platform"  # this from the core content archive
        )
        self.view_server = view_server

    async def _async_connect_to_cohort(
        self,
        server_guid: str,
        cohort_name: str,
    ) -> None:
        """A new server needs to register the metadataCollectionId for its metadata repository with the other servers
        in the open metadata repository. It only needs to do this once and uses a timestamp to record that the
        registration event has been sent. If the server has already registered in the past, it sends a
        reregistration request.  Async version.

        https://egeria-project.org/concepts/cohort-member/

        Parameters
        ----------
        server_guid : str
            Identity of the server to act on.
        cohort_name : str
            Name of the cohort to join

        Returns
        -------
           None

        Raises
        ------
        InvalidParameterException
        PropertyServerException
        UserNotAuthorizedException

        """

        url = (
            f"{self.platform_url}/servers/{self.view_server}/api/open-metadata/runtime-manager/cohort-members/"
            f"{server_guid}/cohorts/{cohort_name}/connect"
        )
        await self._async_make_request("GET", url)
        return

    def connect_to_cohort(
        self,
        server_guid: str,
        cohort_name: str,
    ) -> None:
        """A new server needs to register the metadataCollectionId for its metadata repository with the other servers
        in the open metadata repository. It only needs to do this once and uses a timestamp to record that the
        registration event has been sent. If the server has already registered in the past, it sends a
        reregistration request.

        https://egeria-project.org/concepts/cohort-member/

        Parameters
        ----------
        server_guid: str
           Identity of the server to act on.
        cohort_name: str
            Name of the cohort to join

        Returns
        -------
           None

        Raises
        ------
        InvalidParameterException
        PropertyServerException
        UserNotAuthorizedException

        """
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._async_connect_to_cohort(server_guid, cohort_name))
        return

    async def _async_disconnect_from_cohort(
        self,
        server_guid: str,
        cohort_name: str,
    ) -> None:
        """Disconnect communications from a specific cohort.  Async version.
            https://egeria-project.org/concepts/cohort-member/
        Parameters
        ----------
        server_guid : str
            Identity of the server to act on.
        cohort_name : str
            Name of the cohort to join

        Returns
        -------
           None

        Raises
        ------
        InvalidParameterException
        PropertyServerException
        UserNotAuthorizedException

        """

        url = (
            f"{self.platform_url}/servers/{self.view_server}/api/open-metadata/runtime-manager/cohort-members/"
            f"{server_guid}/cohorts/{cohort_name}/disconnect"
        )
        await self._async_make_request("GET", url)
        return

    def disconnect_from_cohort(
        self,
        server_guid: str,
        cohort_name: str,
    ) -> None:
        """Disconnect communications from a specific cohort.
            https://egeria-project.org/concepts/cohort-member/
        Parameters
        ----------
        server_guid: str
           Identity of the server to act on.
        cohort_name: str
            Name of the cohort to join

        Returns
        -------
           None

        Raises
        ------
        InvalidParameterException
        PropertyServerException
        UserNotAuthorizedException

        """
        loop = asyncio.get_event_loop()
        loop.run_until_complete(
            self._async_disconnect_from_cohort(server_guid, cohort_name)
        )
        return

    async def _async_unregister_from_cohort(
        self,
        server_guid: str,
        cohort_name: str,
    ) -> None:
        """Unregister from a specific cohort and disconnect from cohort communications.  Async version.
            https://egeria-project.org/concepts/cohort-member/
        Parameters
        ----------
        server_guid : str
            Identity of the server to act on.
        cohort_name : str
            Name of the cohort to join

        Returns
        -------
           None

        Raises
        ------
        InvalidParameterException
        PropertyServerException
        UserNotAuthorizedException

        """

        url = (
            f"{self.platform_url}/servers/{self.view_server}/api/open-metadata/runtime-manager/cohort-members/"
            f"{server_guid}/cohorts/{cohort_name}/unregister"
        )
        await self._async_make_request("GET", url)
        return

    def unregister_from_cohort(
        self,
        server_guid: str,
        cohort_name: str,
    ) -> None:
        """Unregister from a specific cohort and disconnect from cohort communications.
            https://egeria-project.org/concepts/cohort-member/

        Parameters
        ----------
        server_guid: str
           Identity of the server to act on.
        cohort_name: str
            Name of the cohort to join

        Returns
        -------
           None

        Raises
        ------
        InvalidParameterException
        PropertyServerException
        UserNotAuthorizedException

        """
        loop = asyncio.get_event_loop()
        loop.run_until_complete(
            self._async_disconnect_from_cohort(server_guid, cohort_name)
        )
        return

    async def _async_refresh_config(
        self,
        server_guid: str,
        gov_engine_name: str,
    ) -> None:
        """Request that the governance engine refresh its configuration by calling the metadata server. This request is
            useful if the metadata server has an outage, particularly while the governance server is initializing.
            This request just ensures that the latest configuration is in use.  Async version.

            https://egeria-project.org/concepts/governance-engine-definition/

        Parameters
        ----------
        server_guid : str
            Identity of the server to act on.
        gov_engine_name : str
            Name of the governance engine to refresh.

        Returns
        -------
           None

        Raises
        ------
        InvalidParameterException
        PropertyServerException
        UserNotAuthorizedException

        """

        url = (
            f"{self.platform_url}/servers/{self.view_server}/api/open-metadata/runtime-manager/engine-hosts/"
            f"{server_guid}/governance_engines/{gov_engine_name}/refresh-config"
        )
        await self._async_make_request("GET", url)
        return

    def refresh_config(
        self,
        server_guid: str,
        gov_engine_name: str,
    ) -> None:
        """Request that the governance engine refresh its configuration by calling the metadata server. This request is
            useful if the metadata server has an outage, particularly while the governance server is initializing.
            This request just ensures that the latest configuration is in use.

            https://egeria-project.org/concepts/governance-engine-definition/

        Parameters
        ----------
        server_guid : str
            Identity of the server to act on.
        gov_engine_name : str
            Name of the governance engine to refresh.

        Returns
        -------
           None

        Raises
        ------
        InvalidParameterException
        PropertyServerException
        UserNotAuthorizedException

        """
        loop = asyncio.get_event_loop()
        loop.run_until_complete(
            self._async_refresh_config(server_guid, gov_engine_name)
        )
        return

    async def _async_get_platforms_by_name(
        self,
        filter: str = None,
        view_server: str = None,
        effective_time: str = None,
        start_from: int = 0,
        page_size: int = max_paging_size,
    ) -> str | list:
        """Returns the list of platforms with a particular name. The name is specified in the filter.  Async version.
         Parameters
         ----------
        filter : str, opt
             Filter specifies the display name or qualified name of the platforms to return information for. If the
             value is None, we will default to the default_platform_name that comes from the core content pack.

         view_server : str, optional
            The name of the view_server to get governance engine summaries from. If not provided, the default view_server name
            will be used.

         start_from : int, optional
            The index from which to start fetching the engine actions. Default is 0.

         page_size : int, optional
            The maximum number of engine actions to fetch in a single request. Default is `max_paging_size`.

         Returns
         -------
         Response
            A lit of json dict with the platform reports.

         Raises
         ------
         InvalidParameterException
         PropertyServerException
         UserNotAuthorizedException

        """
        if view_server is None:
            view_server = self.view_server

        if filter is None:
            filter = self.default_platform_name

        url = (
            f"{self.platform_url}/servers/{view_server}/api/open-metadata/runtime-manager/platforms/by-name?"
            f"startFrom={start_from}&pageSize={page_size}"
        )
        if effective_time is not None:
            body = {"filter": filter, "effectiveTime": effective_time}
        else:
            body = {"filter": filter}

        response = await self._async_make_request("POST", url, body)

        return response.json().get("elementList", "No platforms found")

    def get_platforms_by_name(
        self,
        filter: str = None,
        view_server: str = None,
        effective_time: str = None,
        start_from: int = 0,
        page_size: int = max_paging_size,
    ) -> str | list:
        """Returns the list of platforms with a particular name. The name is specified in the filter.

        Parameters
        ----------
        filter : str, opt
            Filter specifies the display name or qualified name of the platforms to return information for. If the
            value is None, we will default to the default_platform_name that comes from the core content pack.

        view_server : str, optional
           The name of the view_server to get governance engine summaries from. If not provided, the default view_server name
           will be used.

        start_from : int, optional
           The index from which to start fetching the engine actions. Default is 0.


        page_size : int, optional
           The maximum number of engine actions to fetch in a single request. Default is `max_paging_size`.

        Returns
        -------
        Response
           A lit of json dict with the platform reports.

        Raises
        ------
        InvalidParameterException
        PropertyServerException
        UserNotAuthorizedException
        """
        loop = asyncio.get_event_loop()
        response = loop.run_until_complete(
            self._async_get_platforms_by_name(
                filter, view_server, effective_time, start_from, page_size
            )
        )
        return response

    async def _async_get_platforms_by_type(
        self,
        filter: str = None,
        view_server: str = None,
        effective_time: str = None,
        start_from: int = 0,
        page_size: int = max_paging_size,
    ) -> str | list:
        """Returns the list of platforms with a particular deployed implementation type.  The value is specified in
        the filter. If it is null, or no request body is supplied, all platforms are returned.  Async version.

        Parameters
        ----------
        filter : str, opt
            Filter specifies the kind of deployed implementation type of the platforms to return information for.
            If the value is None, we will default to the "OMAG Server Platform".

        view_server : str, optional
               The name of the view_server to get governance engine summaries from. If not provided, the default view_server name
               will be used.

        start_from : int, optional
               The index from which to start fetching the engine actions. Default is 0.

        page_size : int, optional
           The maximum number of engine actions to fetch in a single request. Default is `max_paging_size`.

        Returns
        -------
        Response
           A lit of json dict with the platform reports.

        Raises
        ------
        InvalidParameterException
        PropertyServerException
        UserNotAuthorizedException

        """
        if view_server is None:
            view_server = self.view_server

        if filter is None:
            filter = "OMAG Server Platform"

        url = (
            f"{self.platform_url}/servers/{view_server}/api/open-metadata/runtime-manager/platforms/"
            f"by-deployed-implementation-type?startFrom={start_from}&pageSize={page_size}"
        )

        if effective_time is not None:
            body = {"filter": filter, "effectiveTime": effective_time}
        else:
            body = {"filter": filter}

        response = await self._async_make_request("POST", url, body)
        return response.json().get("elements", "No platforms found")

    def get_platforms_by_type(
        self,
        filter: str = None,
        view_server: str = None,
        effective_time: str = None,
        start_from: int = 0,
        page_size: int = max_paging_size,
    ) -> str | list:
        """Returns the list of platforms with a particular deployed implementation type.  The value is specified in
        the filter. If it is null, or no request body is supplied, all platforms are returned.

        Parameters
        ----------
        filter : str, opt
            Filter specifies the kind of deployed implementation type of the platforms to return information for.
            If the value is None, we will default to the "OMAG Server Platform".

        view_server : str, optional
           The name of the view_server to get governance engine summaries from. If not provided, the default view_server name
           will be used.

        start_from : int, optional
           The index from which to start fetching the engine actions. Default is 0.


        page_size : int, optional
           The maximum number of engine actions to fetch in a single request. Default is `max_paging_size`.

        Returns
        -------
        Response
           A lit of json dict with the platform reports.

        Raises
        ------
        InvalidParameterException
        PropertyServerException
        UserNotAuthorizedException

        """
        loop = asyncio.get_event_loop()
        response = loop.run_until_complete(
            self._async_get_platforms_by_type(
                filter, view_server, effective_time, start_from, page_size
            )
        )
        return response

    async def _async_get_platform_templates_by_type(
        self,
        filter: str = None,
        view_server: str = None,
        effective_time: str = None,
        start_from: int = 0,
        page_size: int = max_paging_size,
    ) -> str | list:
        """Returns the list of platform templates for a particular deployed implementation type.  The value is
        specified in the filter. If it is null, or no request body is supplied, all platforms are returned.
        Async version.

        Parameters
        ----------
        filter : str, opt
            Filter specifies the kind of deployed implementation type of the platforms to return information for.
            If the value is None, we will default to the "OMAG Server Platform".

        view_server : str, optional
               The name of the view_server to get governance engine summaries from. If not provided, the default view_server name
               will be used.

        start_from : int, optional
               The index from which to start fetching the engine actions. Default is 0.

        page_size : int, optional
           The maximum number of engine actions to fetch in a single request. Default is `max_paging_size`.

        Returns
        -------
        Response
           A lit of json dict with the platform reports.

        Raises
        ------
        InvalidParameterException
        PropertyServerException
        UserNotAuthorizedException

        """
        if view_server is None:
            view_server = self.view_server

        if filter is None:
            filter = "OMAG Server Platform"

        url = (
            f"{self.platform_url}/servers/{view_server}/api/open-metadata/runtime-manager/platforms/"
            f"by-deployed-implementation-type?startFrom={start_from}&pageSize={page_size}&getTemplates=true"
        )

        if effective_time is not None:
            body = {"filter": filter, "effectiveTime": effective_time}
        else:
            body = {"filter": filter}

        response = await self._async_make_request("POST", url, body)
        return response.json().get("elements", "No platforms found")

    def get_platform_templates_by_type(
        self,
        filter: str = None,
        view_server: str = None,
        effective_time: str = None,
        start_from: int = 0,
        page_size: int = max_paging_size,
    ) -> str | list:
        """Returns the list of platform templates with a particular deployed implementation type.  The value is
        specified in the filter. If it is null, or no request body is supplied, all platforms are returned.

        Parameters
        ----------
        filter : str, opt
            Filter specifies the kind of deployed implementation type of the platforms to return information for.
            If the value is None, we will default to the "OMAG Server Platform".

        view_server : str, optional
           The name of the view_server to get governance engine summaries from. If not provided, the default view_server name
           will be used.

        start_from : int, optional
           The index from which to start fetching the engine actions. Default is 0.


        page_size : int, optional
           The maximum number of engine actions to fetch in a single request. Default is `max_paging_size`.

        Returns
        -------
        Response
           A lit of json dict with the platform reports.

        Raises
        ------
        InvalidParameterException
        PropertyServerException
        UserNotAuthorizedException

        """
        loop = asyncio.get_event_loop()
        response = loop.run_until_complete(
            self._async_get_platforms_by_type(
                filter, view_server, effective_time, start_from, page_size
            )
        )
        return response

    async def _async_get_platform_report(
        self, platform_guid: str = None, view_server: str = None
    ) -> str | list:
        """Returns details about the running platform. Async version.

        Parameters
        ----------
        platform_guid : str
            The unique identifier for the platform.

        view_server : str, optional
           The name of the view_server to get governance engine summaries from. If not provided, the default view_server name
           will be used.

        Returns
        -------
        Response
           A json dict with the platform report.

        Raises
        ------
        InvalidParameterException
        PropertyServerException
        UserNotAuthorizedException

        """
        if view_server is None:
            view_server = self.view_server

        url = f"{self.platform_url}/servers/{view_server}/api/open-metadata/runtime-manager/platforms/{platform_guid}/report"

        response = await self._async_make_request("GET", url)

        return response.json().get("element", "No platforms found")

    def get_platform_report(
        self, platform_guid: str = None, view_server: str = None
    ) -> str | list:
        """Returns details about the running platform.

        Parameters
        ----------
        platform_guid : str
            The unique identifier for the platform.

        view_server : str, optional
           The name of the view_server to get governance engine summaries from. If not provided, the default view_server name
           will be used.


        Returns
        -------
        Response
           A json dict with the platform report.

        Raises
        ------
        InvalidParameterException
        PropertyServerException
        UserNotAuthorizedException

        """
        loop = asyncio.get_event_loop()
        response = loop.run_until_complete(
            self._async_get_platform_report(platform_guid, view_server)
        )
        return response

    async def _async_get_platform_by_guid(
        self,
        platform_guid: str = None,
        view_server: str = None,
        effective_time: str = None,
    ) -> str | list:
        """Returns details about the platform's catalog entry (asset). Async version.

        Parameters
        ----------
        filter : str, opt
            Filter specifies the kind of deployed implementation type of the platforms to return information for.
            If the value is None, we will default to the "OMAG Server Platform".

        view_server : str, optional
           The name of the view_server to get governance engine summaries from. If not provided, the default view_server name
           will be used.

        start_from : int, optional
           The index from which to start fetching the engine actions. Default is 0.


        page_size : int, optional
           The maximum number of engine actions to fetch in a single request. Default is `max_paging_size`.

        Returns
        -------
        Response
           A lit of json dict with the platform reports.

        """
        if view_server is None:
            view_server = self.view_server

        url = f"{self.platform_url}/servers/{view_server}/api/open-metadata/runtime-manager/platforms/{platform_guid}"

        if effective_time is not None:
            body = {"effectiveTime": effective_time}
            response = await self._async_make_request("POST", url, body)

        else:
            response = await self._async_make_request("POST", url)

        return response.json().get("elements", "No platforms found")

    def get_platform_by_guid(
        self,
        platform_guid: str = None,
        view_server: str = None,
        effective_time: str = None,
    ) -> str | list:
        """Returns details about the platform's catalog entry (asset).

        Parameters
        ----------
        filter : str, opt
            Filter specifies the kind of deployed implementation type of the platforms to return information for.
            If the value is None, we will default to the "OMAG Server Platform".

        view_server : str, optional
           The name of the view_server to get governance engine summaries from. If not provided, the default view_server name
           will be used.

        start_from : int, optional
           The index from which to start fetching the engine actions. Default is 0.


        page_size : int, optional
           The maximum number of engine actions to fetch in a single request. Default is `max_paging_size`.

        Returns
        -------
        Response
           A lit of json dict with the platform reports.

        Raises
        ------
        InvalidParameterException
        PropertyServerException
        UserNotAuthorizedException

        """
        loop = asyncio.get_event_loop()
        response = loop.run_until_complete(
            self._async_get_platforms_by_guid(
                platform_guid, view_server, effective_time
            )
        )
        return response

    async def _async_get_server_by_guid(
        self, server_guid: str, view_server: str = None, effective_time: str = None
    ) -> str | dict:
        """Returns details about the server's catalog entry (asset). Async version.

        Parameters
        ----------
        server_guid : str
            The unique identifier for the platform.

        view_server : str, optional
           The name of the view_server to get governance engine summaries from. If not provided, the default view_server name
           will be used.

        Returns
        -------
        Response
           A lit of json dict with the platform reports.

        Raises
        ------
        InvalidParameterException
        PropertyServerException
        UserNotAuthorizedException

        """
        if view_server is None:
            view_server = self.view_server

        url = f"{self.platform_url}/servers/{view_server}/api/open-metadata/runtime-manager/software-servers/{server_guid}"

        if effective_time is not None:
            body = {"effectiveTime": effective_time}
            response = await self._async_make_request("POST", url, body)

        else:
            response = await self._async_make_request("POST", url)

        return response.json().get("elements", "No view_server found")

    def get_server_by_guid(
        self, server_guid: str, view_server: str = None, effective_time: str = None
    ) -> str | dict:
        """Returns details about the platform's catalog entry (asset).

        Parameters
        ----------
        server_guid : str
            The unique identifier for the platform.

        view_server : str, optional
           The name of the view_server to get governance engine summaries from. If not provided, the default view_server name
           will be used.

        Returns
        -------
        Response
           A lit of json dict with the platform reports.

        Raises
        ------
        InvalidParameterException
        PropertyServerException
        UserNotAuthorizedException

        """
        loop = asyncio.get_event_loop()
        response = loop.run_until_complete(
            self._async_get_server_by_guid(server_guid, view_server, effective_time)
        )
        return response

    async def _async_get_servers_by_name(
        self,
        filter: str,
        view_server: str = None,
        effective_time: str = None,
        start_from: int = 0,
        page_size: int = max_paging_size,
    ) -> str | list:
        """Returns the list of servers with a particular name.  The name is specified in the filter. Async version.

        Parameters
        ----------
        filter : str, opt
            Filter specifies the kind of deployed implementation type of the platforms to return information for.
            If the value is None, we will default to the "OMAG Server Platform".

        view_server : str, optional
           The name of the view_server to get governance engine summaries from. If not provided, the default view_server name
           will be used.

        start_from : int, optional
           The index from which to start fetching the engine actions. Default is 0.


        page_size : int, optional
           The maximum number of engine actions to fetch in a single request. Default is `max_paging_size`.

        Returns
        -------
        Response
           A lit of json dict with the platform reports.

        Raises
        ------
        InvalidParameterException
        PropertyServerException
        UserNotAuthorizedException

        """
        if view_server is None:
            view_server = self.view_server

        url = (
            f"{self.platform_url}/servers/{view_server}/api/open-metadata/runtime-manager/software-servers/by-name?"
            f"startFrom={start_from}&pageSize={page_size}"
        )

        if effective_time is None:
            body = {"filter": filter}
        else:
            body = {"filter": filter, "effective_time": effective_time}
        response = await self._async_make_request("POST", url, body)

        return response.json().get("elements", "No platforms found")

    def get_servers_by_name(self, filter: str, view_server: str = None) -> str | list:
        """Returns the list of servers with a particular name.  The name is specified in the filter.

        Parameters
        ----------
        filter : str, opt
            Filter specifies the kind of deployed implementation type of the platforms to return information for.
            If the value is None, we will default to the "OMAG Server Platform".

        view_server : str, optional
           The name of the view_server to get governance engine summaries from. If not provided, the default view_server name
           will be used.

        start_from : int, optional
           The index from which to start fetching the engine actions. Default is 0.


        page_size : int, optional
           The maximum number of engine actions to fetch in a single request. Default is `max_paging_size`.

        Returns
        -------
        Response
           A lit of json dict with the platform reports.

        Raises
        ------
        InvalidParameterException
        PropertyServerException
        UserNotAuthorizedException

        """
        loop = asyncio.get_event_loop()
        response = loop.run_until_complete(
            self._async_get_servers_by_name(filter, view_server)
        )
        return response

    async def _async_get_servers_by_dep_impl_type(
        self,
        filter: str = "*",
        view_server: str = None,
        effective_time: str = None,
        start_from: int = 0,
        page_size: int = max_paging_size,
    ) -> str | list:
        """Returns the list of servers with a particular deployed implementation type. The value is specified
        in the filter. If it is null, or no request body is supplied, all servers are returned.
        Async version.

        Parameters
        ----------
        filter : str, opt
            Filter specifies the kind of deployed implementation type of the platforms to return information for.
            If the value is None, we will default to the "OMAG Server Platform".

        view_server : str, optional
           The name of the view_server to get governance engine summaries from. If not provided, the default view_server name
           will be used.

        start_from : int, optional
           The index from which to start fetching the engine actions. Default is 0.


        page_size : int, optional
           The maximum number of engine actions to fetch in a single request. Default is `max_paging_size`.

        Returns
        -------
        Response
           A lit of json dict with the platform reports.

        Raises
        ------
        InvalidParameterException
        PropertyServerException
        UserNotAuthorizedException

        """
        if view_server is None:
            view_server = self.view_server

        if filter == "*":
            filter = None

        url = (
            f"{self.platform_url}/servers/{view_server}/api/open-metadata/runtime-manager/software-servers/"
            f"by-deployed-implementation-type?startFrom={start_from}&pageSize={page_size}"
        )

        body = body_slimmer({"filter": filter, "effective_time": effective_time})

        response = await self._async_make_request("POST", url, body)

        return response.json().get("elements", "No platforms found")

    def get_servers_by_dep_impl_type(
        self,
        filter: str = "*",
        view_server: str = None,
        effective_time: str = None,
        start_from: int = 0,
        page_size: int = max_paging_size,
    ) -> str | list:
        """Returns the list of servers with a particular deployed implementation type.
        The value is specified in the filter. If it is null, or no request body is supplied,
        all servers are returned.

        Parameters
        ----------
        filter : str, opt
            Filter specifies the kind of deployed implementation type of the platforms to return information for.
            If the value is None, we will default to the "OMAG Server Platform".

        view_server : str, optional
           The name of the view_server to get governance engine summaries from. If not provided, the default view_server name
           will be used.

        start_from : int, optional
           The index from which to start fetching the engine actions. Default is 0.


        page_size : int, optional
           The maximum number of engine actions to fetch in a single request. Default is `max_paging_size`.

        Returns
        -------
        Response
           A lit of json dict with the platform reports.

        Raises
        ------
        InvalidParameterException
        PropertyServerException
        UserNotAuthorizedException

        """
        loop = asyncio.get_event_loop()
        response = loop.run_until_complete(
            self._async_get_servers_by_dep_impl_type(
                filter, view_server, effective_time, start_from, page_size
            )
        )
        return response

    async def _async_get_server_templates_by_dep_impl_type(
        self,
        filter: str = "*",
        view_server: str = None,
        effective_time: str = None,
        start_from: int = 0,
        page_size: int = max_paging_size,
    ) -> str | list:
        """Returns the list of view_server templates with a particular deployed implementation type.   The value is
        specified in the filter. If it is null, or no request body is supplied, all servers are returned.
        Async version.

        Parameters
        ----------
        filter : str, opt
            Filter specifies the kind of deployed implementation type of the platforms to return information for.
            If the value is None, we will default to the "OMAG Server Platform".

        view_server : str, optional
           The name of the view_server to get governance engine summaries from. If not provided, the default view_server name
           will be used.

        start_from : int, optional
           The index from which to start fetching the engine actions. Default is 0.


        page_size : int, optional
           The maximum number of engine actions to fetch in a single request. Default is `max_paging_size`.

        Returns
        -------
        Response
           A lit of json dict with the platform reports.

        Raises
        ------
        InvalidParameterException
        PropertyServerException
        UserNotAuthorizedException

        """
        if view_server is None:
            view_server = self.view_server

        if filter == "*":
            filter = None

        url = (
            f"{self.platform_url}/servers/{view_server}/api/open-metadata/runtime-manager/software-servers/"
            f"by-deployed-implementation-type?startFrom={start_from}&pageSize={page_size}&getTemplates=true"
        )

        body = body_slimmer({"filter": filter, "effective_time": effective_time})

        response = await self._async_make_request("POST", url, body)

        return response.json().get("elements", "No platforms found")

    def get_server_templates_by_dep_impl_type(
        self,
        filter: str = "*",
        view_server: str = None,
        effective_time: str = None,
        start_from: int = 0,
        page_size: int = max_paging_size,
    ) -> str | list:
        """Returns the list of view_server templates with a particular deployed implementation type.
        The value is specified in the filter. If it is null, or no request body is supplied,
        all servers are returned.

        Parameters
        ----------
        filter : str, opt
            Filter specifies the kind of deployed implementation type of the platforms to return information for.
            If the value is None, we will default to the "OMAG Server Platform".

        view_server : str, optional
           The name of the view_server to get governance engine summaries from. If not provided, the default view_server name
           will be used.

        start_from : int, optional
           The index from which to start fetching the engine actions. Default is 0.


        page_size : int, optional
           The maximum number of engine actions to fetch in a single request. Default is `max_paging_size`.

        Returns
        -------
        Response
           A lit of json dict with the platform reports.

        Raises
        ------
        InvalidParameterException
        PropertyServerException
        UserNotAuthorizedException

        """
        loop = asyncio.get_event_loop()
        response = loop.run_until_complete(
            self._async_get_server_templates_by_dep_impl_type(
                filter, view_server, effective_time, start_from, page_size
            )
        )
        return response

    async def _async_get_server_by_guid(
        self,
        server_guid: str = None,
        view_server: str = None,
        effective_time: str = None,
    ) -> str | list:
        """Returns details about the server's catalog entry (asset). Async version.

        Parameters
        ----------
        filter : str, opt
            Filter specifies the kind of deployed implementation type of the platforms to return information for.
            If the value is None, we will default to the "OMAG Server Platform".

        view_server : str, optional
           The name of the view_server to get governance engine summaries from. If not provided, the default view_server name
           will be used.

        start_from : int, optional
           The index from which to start fetching the engine actions. Default is 0.


        page_size : int, optional
           The maximum number of engine actions to fetch in a single request. Default is `max_paging_size`.

        Returns
        -------
        Response
           A lit of json dict with the platform reports.

        Raises
        ------
        InvalidParameterException
        PropertyServerException
        UserNotAuthorizedException

        """
        if view_server is None:
            view_server = self.view_server

        url = f"{self.platform_url}/servers/{view_server}/api/open-metadata/runtime-manager/software-servers/{server_guid}"

        if effective_time is not None:
            body = {"effectiveTime": effective_time}
            response = await self._async_make_request("POST", url, body)

        else:
            response = await self._async_make_request("POST", url)

        return response.json().get("element", "No servers found")

    def get_server_by_guid(
        self,
        server_guid: str = None,
        view_server: str = None,
        effective_time: str = None,
    ) -> str | list:
        """Returns details about the server's catalog entry (asset). Async version.

        Parameters
        ----------
        filter : str, opt
            Filter specifies the kind of deployed implementation type of the platforms to return information for.
            If the value is None, we will default to the "OMAG Server Platform".

        view_server : str, optional
           The name of the view_server to get governance engine summaries from. If not provided, the default view_server name
           will be used.

        start_from : int, optional
           The index from which to start fetching the engine actions. Default is 0.


        page_size : int, optional
           The maximum number of engine actions to fetch in a single request. Default is `max_paging_size`.

        Returns
        -------
        Response
           A lit of json dict with the platform reports.

        """
        loop = asyncio.get_event_loop()
        response = loop.run_until_complete(
            self._async_get_server_by_guid(server_guid, view_server, effective_time)
        )
        return response

    async def _async_get_server_report(
        self, server_guid: str = None, view_server: str = None
    ) -> str | list:
        """Returns details about the running server. Async version.

        Parameters
        ----------
        server_guid: str
            Identity of the view_server to report on.

        view_server : str, optional
           The name of the view_server to get governance engine summaries from. If not provided, the default view_server name
           will be used.


        Returns
        -------
        Response
           A list of json dict with the platform reports.

        Raises
        ------
        InvalidParameterException
        PropertyServerException
        UserNotAuthorizedException

        """
        if view_server is None:
            view_server = self.view_server

        url = f"{self.platform_url}/servers/{view_server}/api/open-metadata/runtime-manager/software-servers/{server_guid}/report"

        response = await self._async_make_request("GET", url)

        return response.json().get("elements", "No view_server found")

    def get_server_report(
        self, server_guid: str = None, view_server: str = None
    ) -> str | list:
        """Returns details about the running server.

        Parameters
        ----------
        server_guid: str
            Identity of the view_server to report on.

        view_server : str, optional
           The name of the view_server to get governance engine summaries from. If not provided, the default view_server name
           will be used.

        Returns
        -------
        Response
           A list of json dict with the platform reports.

        Raises
        ------
        InvalidParameterException
        PropertyServerException
        UserNotAuthorizedException

        """
        loop = asyncio.get_event_loop()
        response = loop.run_until_complete(
            self._async_get_server_report(server_guid, view_server)
        )
        return response

    async def _async_add_archive_file(
        self,
        archive_file: str,
        server_guid: str,
        view_server: str = None,
        time_out: int = 60,
    ) -> None:
        """Add a new open metadata archive to running OMAG Server's repository.
            An open metadata archive contains metadata types and instances.  This operation loads an open metadata archive
            that is stored in the named file.  It can be used with OMAG servers that are of type Open Metadata Store.
            Async version.

            https://egeria-project.org/concepts/open-metadata-archives/

        Parameters
        ----------
        archive_file: str
            Open metadata archive file to load.
        server_guid: str
            GUID of the view_server to load the file into.
        view_server : str, optional
           The name of the view view_server to work with. If not provided, the default view_server name
           will be used.
        time_out: int, optional
           Time out for the rest call.

        Returns
        -------
        Response
          None

        Raises
        ------
        InvalidParameterException
        PropertyServerException
        UserNotAuthorizedException

        """
        if view_server is None:
            view_server = self.view_server

        url = f"{self.platform_url}/servers/{view_server}/api/open-metadata/runtime-manager/omag-servers/{server_guid}/instance/load/open-metadata-archives/file"

        await self._async_make_request(
            "POST-DATA", url, archive_file, time_out=time_out
        )
        return

    def add_archive_file(
        self,
        archive_file: str,
        server_guid: str,
        view_server: str = None,
        time_out: int = 60,
    ) -> None:
        """Add a new open metadata archive to running OMAG Server's repository.
            An open metadata archive contains metadata types and instances.  This operation loads an open metadata archive
            that is stored in the named file.  It can be used with OMAG servers that are of type Open Metadata Store.

            https://egeria-project.org/concepts/open-metadata-archives/

        Parameters
        ----------
        archive_file: str
            Open metadata archive file to load.
        server_guid: str
            GUID of the view_server to load the file into.
        view_server : str, optional
           The name of the view view_server to work with. If not provided, the default view_server name
           will be used.

        Returns
        -------
        Response
           None

        Raises
        ------
        InvalidParameterException
        PropertyServerException
        UserNotAuthorizedException

        """

        loop = asyncio.get_event_loop()
        loop.run_until_complete(
            self._async_add_archive_file(
                archive_file, server_guid, view_server, time_out
            )
        )
        return

    #
    #   Activate
    #

    async def _async_activate_with_stored_config(
        self, server_guid: str, view_server: str = None
    ) -> None:
        """Activate the Open Metadata and Governance (OMAG) view_server using the configuration document stored for this
        server. Async Version

        Parameters
        ----------
        server_guid: str
            Identity of the view_server to activate.

        view_server : str, optional
           The name of the view_server to get governance engine summaries from. If not provided, the default view_server name
           will be used.

        Returns
        -------
        None


        Raises
        ------
        InvalidParameterException
        PropertyServerException
        UserNotAuthorizedException

        """
        pass

    def activate_with_stored_config(
        self, server_guid: str, view_server: str = None
    ) -> None:
        """Activate the Open Metadata and Governance (OMAG) server using the configuration document stored for this
        server. Async Version

        Parameters
        ----------
        server_guid: str
            Identity of the server to activate.

        view_server : str, optional
           The name of the view_server to get governance engine summaries from. If not provided, the default view_server name
           will be used.

        Returns
        -------
        None


        Raises
        ------
        InvalidParameterException
        PropertyServerException
        UserNotAuthorizedException

        """
        pass


if __name__ == "__main__":
    print("Main-Runtime Manager")
