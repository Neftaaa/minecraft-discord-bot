from src.functions.embeds_builders import convert_server_data_dict

standard_server_data = {"motd": {"clean": ["test:", "Réussi!"]},
                        "players": {"online": 5, "max": 20},
                        "version": "1.20.2"}

monoline_server_data = {"motd": {"clean": ["test"]},
                        "players": {"online": 5, "max": 20},
                        "version": "1.20.2"}


class TestClass:

    def test_should_standard_convert(self):
        standard_convert = convert_server_data_dict(standard_server_data)
        assert standard_convert == {'final_motd': 'test:\nRéussi!',
                                    'max_player_count': 20,
                                    'online_player_count': 5,
                                    'version': '1.20.2'}

    def test_should_mono_convert(self):
        monoline_convert = convert_server_data_dict(monoline_server_data)
        assert monoline_convert == {'final_motd': 'test',
                                    'max_player_count': 20,
                                    'online_player_count': 5,
                                    'version': '1.20.2'}