HALT_CHAT_STREAM_MUTATION: str = """
  mutation HaltChatStream($chatUuid: String!) {
    haltChatStream(chatUuid: $chatUuid) {
      __typename
    }
  }
"""


MOVE_CHAT_TO_CLOUD_MUTATION: str = """
  mutation MoveChatToCloud($chatUuid: String!) {
    moveChatToCloud(chatUuid: $chatUuid) {
      ... on Chat {
        chatUuid
        name
      }
      ... on UnauthenticatedError {
        message
      }
      ... on ChatNotFoundError {
        message
      }
      ... on CloudSessionError {
        message
        chatUuid
      }
    }
  }
"""
