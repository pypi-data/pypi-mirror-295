import json, logging
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError


class Slack:
    def __init__(self, token):
        self.client = WebClient(token=token)

    def get_user_name(self, user_id):
        try:
            result = self.client.users_info(user=user_id)
            user = result.get("user", {})
            
            # Try to get real_name directly from user
            real_name = user.get("real_name")
            
            # If not found, try to get it from user's profile
            if not real_name:
                profile = user.get("user_profile", {})
                real_name = profile.get("real_name")
            
            return real_name or "Unknown"  # Return "Unknown" if real_name is None or empty
        except Exception as e:
            logging.error(f"Error getting user info: {e}")
            return "Unknown"

    def fetch_thread_replies(self, channel_id, thread_ts):
        try:
            result = self.client.conversations_replies(channel=channel_id, ts=thread_ts)
            return result["messages"][1:]
        except SlackApiError as e:
            logging.error(f"Error fetching thread replies: {e}")
            return []

    def process_message(self, msg, is_reply=False, thread_ts=None):
        user_name = self.get_user_name(msg["user"])
        return {
            "type": "reply" if is_reply else "message",
            "user": user_name,
            "user_id": msg["user"],
            "text": msg["text"],
            "timestamp": msg["ts"],
            "thread_ts": thread_ts,
            "reactions": [
                {"name": reaction["name"], "count": reaction["count"]}
                for reaction in msg.get("reactions", [])
            ],
            "attachments": msg.get("attachments", []),
            "files": [
                {
                    "name": file.get("name"),
                    "filetype": file.get("filetype"),
                    "url_private": file.get("url_private")
                }
                for file in msg.get("files", [])
            ]
        }

    def conversation_fetch_and_process_chunk(self, conversation_id, conversation_type, oldest=None, latest=None, next_cursor=None, limit=1000):
        try:
            params = {
                "channel": conversation_id,
                "limit": limit,
            }
            if oldest:
                params["oldest"] = oldest
            if latest:
                params["latest"] = latest
            if next_cursor:
                params["cursor"] = next_cursor

            result = self.client.conversations_history(**params)
            messages = result["messages"]
            processed_messages = []

            for msg in messages:
                processed_msg = self.process_message(msg)
                if "thread_ts" in msg and msg["thread_ts"] == msg["ts"]:
                    replies = self.fetch_thread_replies(conversation_id, msg["ts"])
                    processed_msg["replies"] = [
                        self.process_message(reply, is_reply=True, thread_ts=msg["ts"])
                        for reply in replies
                    ]
                processed_messages.append(processed_msg)

            conversation_info = self.client.conversations_info(channel=conversation_id)["channel"]
            chunk_data = {
                "conversation_id": conversation_id,
                "conversation_name": conversation_info.get("name", "Direct Message"),
                "conversation_type": conversation_type,
                "is_private": conversation_info.get("is_private", True), # Default to True for DMs
                "messages": processed_messages,
            }

            next_cursor = result["response_metadata"]["next_cursor"] if result["has_more"] else None

            return json.dumps(chunk_data, indent=2), next_cursor

        except SlackApiError as e:
            logging.error(f"Error fetching messages: {e}")
            return None, None

    def channel_fetch_and_process(self, channel_id, oldest=None, latest=None, limit=1000):
        try:
            all_messages = []
            next_cursor = None

            while True:
                params = {
                    "channel": channel_id,
                    "limit": limit,  # Slack allows up to 1000 messages per request
                }
                if oldest:
                    params["oldest"] = oldest
                if latest:
                    params["latest"] = latest
                if next_cursor:
                    params["cursor"] = next_cursor

                result = self.client.conversations_history(**params)
                messages = result["messages"]

                for msg in messages:
                    processed_msg = self.process_message(msg)

                    if "thread_ts" in msg and msg["thread_ts"] == msg["ts"]:
                        replies = self.fetch_thread_replies(channel_id, msg["ts"])
                        processed_msg["replies"] = [
                            self.process_message(reply, is_reply=True, thread_ts=msg["ts"])
                            for reply in replies
                        ]

                    all_messages.append(processed_msg)

                if not result["has_more"]:
                    break

                next_cursor = result["response_metadata"]["next_cursor"]

            all_messages.reverse()  # Chronological order

            channel_info = self.client.conversations_info(channel=channel_id)["channel"]
            output = {
                "channel_id": channel_id,
                "channel_name": channel_info["name"],
                "is_private": channel_info.get("is_private", True), # Default to True for DMs
                "messages": all_messages,
            }

            return json.dumps(output, indent=2)

        except SlackApiError as e:
            logging.error(f"Error fetching messages: {e}")
            return json.dumps({"error": str(e)})

    def get_all_channels(self):
        try:
            channels = []
            cursor = None
            while True:
                result = self.client.conversations_list(types="public_channel,private_channel", cursor=cursor)
                channels.extend([{"id": channel["id"], "name": channel["name"]} for channel in result["channels"]])
                cursor = result["response_metadata"].get("next_cursor")
                if not cursor:
                    break
            return channels
        except SlackApiError as e:
            logging.error(f"Error fetching channels: {e}")
            return []


    def get_all_dms(self):
        try:
            dms = []
            cursor = None
            while True:
                result = self.client.conversations_list(types="im", cursor=cursor)
                dms.extend([{"id": dm["id"], "name": self.get_user_name(dm["user"])} for dm in result["channels"]])
                cursor = result["response_metadata"].get("next_cursor")
                if not cursor:
                    break
            return dms
        except SlackApiError as e:
            logging.error(f"Error fetching DMs: {e}")
            return []
        
    def get_all_mpims(self):
        try:
            mpims = []
            cursor = None
            while True:
                result = self.client.conversations_list(types="mpim", cursor=cursor)
                mpims.extend([{"id": mpim["id"], "name": mpim["name"]} for mpim in result["channels"]])
                cursor = result["response_metadata"].get("next_cursor")
                if not cursor:
                    break
            return mpims
        except SlackApiError as e:
            logging.error(f"Error fetching MPIMs: {e}")
            return []

