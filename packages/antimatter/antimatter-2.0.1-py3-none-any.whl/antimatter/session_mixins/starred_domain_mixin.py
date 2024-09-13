from typing import Any, Dict, List

import antimatter_api as openapi_client
from antimatter import errors

from antimatter.session_mixins.base import BaseMixin


class StarredDomainMixin(BaseMixin):

    def _verify_call(self):
        if self.authz.auth_client.get_token_scope() != "google_oauth_token":
            raise errors.PermissionDenied("use an oauth client to access this functionality")
        return

    def list_starred_domains(self) -> List[str]:
        """
        Returns a list of starred domains for the current user
        """
        self._verify_call()
        return openapi_client.StarredDomainList.from_json(
            self.authz.get_session().list_starred_domains()
        ).domains

    def add_starred_domain(self, domain_id: str) -> None:
        """
        Adds a domain to the starred list for the current user
        """
        self._verify_call()
        self.authz.get_session().add_starred_domain(domain_id)

    def delete_starred_domain(self, domain_id: str) -> None:
        """
        Removes a domain from the starred list for the current user
        """
        self._verify_call()
        self.authz.get_session().delete_starred_domain(domain_id)
