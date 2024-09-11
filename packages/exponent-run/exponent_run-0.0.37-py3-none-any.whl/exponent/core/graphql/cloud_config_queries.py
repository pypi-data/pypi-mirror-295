GET_CLOUD_CONFIGS_QUERY: str = """
    query {
        cloudConfigs {
            __typename
            ... on UnauthenticatedError {
                message
            }
            ... on CloudConfigs {
                configs {
                    cloudConfigUuid
                    githubOrgName
                    githubRepoName
                    repoUrl
                }
            }
        }
    }
"""

CREATE_CLOUD_CONFIG_MUTATION: str = """
    mutation CreateCloudConfig(
        $githubOrgName: String!,
        $githubRepoName: String!,
    ) {
        createCloudConfig(
            input: {
                githubOrgName: $githubOrgName,
                githubRepoName: $githubRepoName,
            }
        ) {
            __typename
            ... on UnauthenticatedError {
                message
            }
            ... on CloudConfig {
                cloudConfigUuid
                githubOrgName
                githubRepoName
                repoUrl
            }
        }
    }
"""

UPDATE_CLOUD_CONFIG_MUTATION: str = """
    mutation UpdateCloudConfig(
        $cloudConfigUuid: String!,
        $githubOrgName: String!,
        $githubRepoName: String!,
    ) {
        updateCloudConfig(
            cloudConfigUuid: $cloudConfigUuid,
            input: {
                githubOrgName: $githubOrgName,
                githubRepoName: $githubRepoName,
            }
        ) {
            __typename
            ... on UnauthenticatedError {
                message
            }
            ... on CloudConfig {
                cloudConfigUuid
                githubOrgName
                githubRepoName
                repoUrl
            }
        }
    }
"""
