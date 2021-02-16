import os
from python_graphql_client import GraphqlClient
from dj_proposals_candidates.create_proposals_from_data import process_proposals_from_data
from zappa.asynchronous import task

query = """
{

  assemblies {
    id
    title {
      translations {
        text
      }
    }
    components {
      __typename
      ... on Proposals {
        id
        name {
          translations {
            text
          }
        }
        proposals(first: 1000) {
          edges {
            node {
              id
              title
              state
              body
              voteCount
              endorsements {
                profilePath
                avatarUrl
                nickname
                name
              }
            }
          }
        }
      }
    }
  }
}
"""
variables = {}


@task
def get_from_api():
    url = os.environ.get('REMOTE_SERVER')
    api_url = "{url}/api".format(url=url)
    client = GraphqlClient(endpoint=api_url)
    data = client.execute(query=query, variables=variables)
    process_proposals_from_data(data, url)