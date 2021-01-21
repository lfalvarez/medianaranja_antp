from django.core.management.base import BaseCommand, CommandError
from python_graphql_client import GraphqlClient
from dj_proposals_candidates.models import Commitment
from mn_juego.models import Distrito, Propuesta, Candidatura
import numpy as np


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
              author {
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


def process_proposals_from_data(data, url):
    for assembly in data['data']['assemblies']:
        territory_id = assembly['id']
        territory_name = assembly['title']['translations'][0]['text']
        exists_territory = Distrito.objects.filter(remote_id=territory_id).exists()
        if not exists_territory:
            territory = Distrito.objects.create(remote_id=territory_id, name=territory_name)
        else:
            territory = Distrito.objects.get(remote_id=territory_id)
        proposals_component = next(filter(lambda component: component['__typename'] == 'Proposals', assembly['components']), None)
        if proposals_component:
            proposals = proposals_component['proposals']['edges']
            for p_dict in proposals:
                proposal_dict = p_dict['node']
                proposal_id = proposal_dict['id']
                proposal_exists = Propuesta.objects.filter(remote_id=proposal_id).exists()
                if not proposal_exists:
                    proposal = Propuesta.objects.create(remote_id=proposal_id,
                                                        title=proposal_dict['title'],
                                                        territory=territory,
                                                        description=proposal_dict['body'],
                                                        votes = proposal_dict['voteCount'])
                else:
                    proposal = Propuesta.objects.get(remote_id=proposal_id)
                for endorsement in p_dict['node']['endorsements']:
                    profile_path = url+endorsement['profilePath']
                    candidate_exists = Candidatura.objects.filter(profile_path=profile_path).exists()
                    if not candidate_exists:
                        candidate = Candidatura.objects.create(
                            profile_path=profile_path,
                            name=endorsement['name'],
                            img_url=url+endorsement['avatarUrl'],
                            nickname=endorsement['nickname'],
                            territory=territory
                        )
                    else:
                        candidate = Candidatura.objects.get(profile_path=profile_path)
                    
                    commitment, created_commitment = Commitment.objects.get_or_create(candidate=candidate, proposal=proposal)


def prepare_data():
    for distrito in Distrito.objects.all():
        counter = 0
        for proposal in distrito.proposals.order_by('id'):
            propuesta = Propuesta.objects.get(proposal_ptr__id=proposal.id)
            propuesta.position_in_array = counter
            propuesta.save()
            counter += 1
        counter = 0
        for candidate in distrito.candidates.order_by('id'):
            candidatura = Candidatura.objects.get(candidate_ptr__id=candidate.id)
            candidatura.position_in_array = counter
            candidatura.save()
            counter += 1


def create_matrix():
    for distrito in Distrito.objects.all():
        propuestas = Propuesta.objects.filter(territory=distrito).order_by('position_in_array')
        candidates = Candidatura.objects.filter(territory=distrito).order_by('position_in_array')
        candidates_count = candidates.count()
        proposals_count = propuestas.count()
        if not candidates_count or not proposals_count:
            continue
        matrix = np.zeros((proposals_count, candidates_count))
        for proposal in propuestas:
            for candidate in candidates:
                commitment_exists = Commitment.objects.filter(proposal=proposal, candidate=candidate).exists()
                if commitment_exists:
                    propuesta = Propuesta.objects.get(proposal_ptr__id=proposal.id)
                    candidatura = Candidatura.objects.get(candidate_ptr__id=candidate.id)
                    matrix[propuesta.position_in_array, candidatura.position_in_array] = 1
        distrito.matriz = np.vectorize(np.binary_repr)(matrix.astype(int), width=1)
        distrito.save()
        m = distrito.get_matrix()
        print('<<<', m, '>>>')


class Command(BaseCommand):
    help = 'Carga desde un endpoint con graphql'

    def add_arguments(self, parser):
        parser.add_argument('url', nargs=1, type=str)

    def handle(self, *args, **options):
        url = options['url'][0]
        api_url = "{url}/api".format(url = url)
        client = GraphqlClient(endpoint=api_url)
        data = client.execute(query=query, variables=variables)
        process_proposals_from_data(data, url)
        prepare_data()
        create_matrix()
        
