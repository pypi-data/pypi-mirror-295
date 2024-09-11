GET_CHATS_QUERY: str = """
    query Chats {
        chats {
            ... on UnauthenticatedError {
                message
            }
            ... on Chats {
                chats {
                    id
                    chatUuid
                    name
                    firstLine
                    isShared
                    isStarted
                    updatedAt # ISO datetime string
                }
            }
        }
    }
"""
