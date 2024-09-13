from datetime import datetime
from typing import Any, List, Optional, Callable

import requests
from pytz import UTC
from .errors import ResponseError
from .webhook import Webhook, WebhookEvent
from .types import ParticipantType, Conversation, Attachment

API_BASE_URL = "https://api.gradient-labs.ai"
USER_AGENT = "Gradient Labs Python"


class Client:

    def __init__(
        self,
        *,
        api_key: str,
        signing_key: Optional[str] = None,
        base_url: str = API_BASE_URL,
        timeout: int = None,
    ):
        self.api_key = api_key
        self.base_url = base_url
        self.timeout = timeout
        self.signing_key = signing_key

    @classmethod
    def localize(cls, timestamp: datetime) -> str:
        return UTC.localize(timestamp).strftime("%Y-%m-%dT%H:%M:%S.%fZ")

    def assign_conversation(
        self,
        *,
        conversation_id: str,
        participant_type: ParticipantType,
        assignee_id: Optional[str] = None,
        timestamp: Optional[datetime] = None,
    ) -> None:
        """Assigns a conversation to the given participant."""
        body = {"assignee_type": participant_type}
        if assignee_id:
            body["assignee_id"] = assignee_id
        if timestamp:
            body["timestamp"] = self.localize(timestamp)
        _ = self._put(
            f"conversations/{conversation_id}/assignee",
            body,
        )

    def finish_conversation(
        self, *, conversation_id: str, timestamp: Optional[datetime] = None
    ) -> None:
        """Finishes the conversation"""
        body = {}
        if timestamp is not None:
            body["timestamp"] = self.localize(timestamp)
        _ = self._put(
            f"conversations/{conversation_id}/finish",
            body,
        )

    def read_conversation(self, *, conversation_id: str) -> Conversation:
        """Retrieves the conversation"""
        body = self._get(
            f"conversations/{conversation_id}",
            {},
        )
        return Conversation.from_dict(body)

    def start_conversation(
        self,
        *,
        conversation_id: str,
        customer_id: str,
        channel: str,
        created: Optional[datetime] = None,
        metadata: Optional[Any] = None,
    ) -> Conversation:
        """Starts a conversation."""
        body = {
            "id": conversation_id,
            "customer_id": customer_id,
            "channel": channel,
        }
        if metadata is not None:
            body["metadata"] = metadata
        if created is not None:
            body["created"] = self.localize(created)
        rsp = self._post(
            "conversations",
            body,
        )
        return Conversation.from_dict(rsp)

    def add_message(
        self,
        *,
        message_id: str,
        conversation_id: str,
        body: str,
        participant_id: str,
        participant_type: ParticipantType,
        created: Optional[datetime] = None,
        attachments: List[Attachment] = None,
    ) -> None:
        """Adds a message to a conversation."""
        body = {
            "id": message_id,
            "body": body,
            "participant_id": participant_id,
            "participant_type": participant_type,
        }
        if created is not None:
            body["created"] = self.localize(created)
        if attachments is not None and len(attachments) != 0:
            body["attachments"] = [a.to_dict() for a in attachments]

        _ = self._post(
            f"conversations/{conversation_id}/messages",
            body,
        )

    def add_resource(
        self,
        *,
        conversation_id: str,
        name: str,
        data: Any,
    ) -> None:
        """Attaches a resource to the conversation."""
        _ = self._put(
            f"conversations/{conversation_id}/resources/{name}",
            data,
        )

    def upsert_hand_off_target(self, *, hand_off_target_id: str, name: str) -> None:
        """Inserts or updates a hand-off target."""
        _ = self._post(
            f"hand-off-targets",
            {
                "id": hand_off_target_id,
                "name": name,
            },
        )

    def parse_webhook(self, payload: str, signature_header: str) -> WebhookEvent:
        return Webhook.parse_event(
            payload=payload,
            signature_header=signature_header,
            signing_key=self.signing_key,
        )

    def _post(self, path: str, body: Any):
        return self._api_call(requests.post, path, body)

    def _put(self, path: str, body: Any):
        return self._api_call(requests.put, path, body)

    def _get(self, path: str, body: Any):
        return self._api_call(requests.get, path, body)

    def _api_call(self, request_func: Callable, path: str, body: Any):
        url = f"{self.base_url}/{path}"
        rsp = request_func(
            url,
            json=body,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}",
                "User-Agent": USER_AGENT,
            },
            timeout=self.timeout,
        )
        if rsp.status_code < 200 or rsp.status_code > 299:
            raise ResponseError(rsp)
        if len(rsp.content) != 0:
            return rsp.json()
