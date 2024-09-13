from dataclasses import asdict, dataclass
from typing import Any, Dict, Optional
from antimatter.auth.config.tokens import OidcToken


@dataclass
class Profile:
    """
    Profile structure, containing the name, domain ID, API key, default
    read and write contexts and token
    """

    name: str
    domain_id: str
    api_key: str
    default_read_context: Optional[str]
    default_write_context: Optional[str]
    token: Optional[OidcToken]

    @staticmethod
    def from_dict(json: Dict[str, Any]) -> "Profile":
        if json is None:
            return None
        json["oidc_token"] = OidcToken.from_dict(json["oidc_token"]) if json.get("oidc_token") else None
        return Profile(
            name=json["name"],
            domain_id=json["domain_id"],
            api_key=json["api_key"],
            default_read_context=json.get("default_read_context"),
            default_write_context=json.get("default_write_context"),
            token=json["oidc_token"],
        )

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        del d["token"]
        d["oidc_token"] = self.token.to_dict() if self.token else None
        return d
