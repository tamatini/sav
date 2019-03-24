import unittest
from sav_depot.services.client_service import ClientList
from unittest.mock import patch, Mock


def creer_client(ID, Nom, Prénom):
    client = Mock()
    client.client_id = ID
    client.nom_client = Nom
    client.prenom_client = Prénom

    return client


class TestClientService(unittest.TestCase):

    EXPECTED_CLIENT_LIST = [
        {'ID': 1, 'Nom': 'TEAHUI', 'Prénom': 'Tamatini'}
    ]

    @patch('sav_depot.services.client_service')
    def test_get_all_client(self, client_mock):
        client_mock.query.all.return_value = [creer_client(
            f['ID'], f['Nom'], f['Prénom']) for f in self.EXPECTED_CLIENT_LIST]
        client = ClientList()
        self.assertEqual(client.get(), self.EXPECTED_CLIENT_LIST)
