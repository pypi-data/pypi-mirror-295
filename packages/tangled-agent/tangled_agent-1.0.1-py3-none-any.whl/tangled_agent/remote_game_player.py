"""
This module provides the RemoteGamePlayer class, which manages a player's interaction with a remote game server.
"""

from __future__ import annotations

import json
import os
import time
from typing import Union
import requests
import jwt

from tangled_game_client import ApiException, MakeMoveRequest, JoinGameRequest
from tangled_game_engine import Game, GameAgentBase, GamePlayerBase

from .connection.api_connection import ConnectionClient
from .connection.auth0_handler import Auth0DeviceAuthorization

class RemoteGamePlayer(GamePlayerBase):
    """
    Represents a player in a remote game, providing methods to authenticate, join a game,
    make moves, and synchronize the game state with a remote server.

    Attributes:
        player (GameAgentBase): The agent representing the player.
        game (Game): The local game instance used to mirror the remote game state.
        game_spec (dict): Specifications of the game (e.g., number of vertices, edges).
        host_url (str): The URL of the remote game server.
        token (dict): Authentication tokens for the remote game server.
        game_id (str): The ID of the game on the remote server.
        join_token (str): The token used to join the game.
        player_index (int): The index of the player in the game.
    """
    
    player: GameAgentBase
    game: Game
    game_spec: dict

    host_url : str = None
    token: dict = None
    game_id: str = None
    join_token: str = None
    player_index: int = None

    @property
    def access_token(self):
        if self.token:
            return self.token.get('access_token')
        return None
    
    @property
    def id_token(self):
        if self.token:
            return self.token.get('id_token')
        return None
    
    def __init__(self, player: GameAgentBase, game_id: str, host_url: str, player_index: int = 0, agent_name: str = "default", force_new_credentials: bool = False):

        self.host_url = host_url
        self.game_id = game_id
        self.player = player
        self.player_index = player_index

        # Get the authentication token
        self.authenticate(force_new_credentials)

        # Use auth token to set player ID
        player.id = self.get_user_id(self.access_token) + f".{agent_name}"

        # Test login
        self.__test_token_and_login()
        
        # Make a local game client to mirror remote game state
        self.game = Game()
        self.game.create_game()

    def authenticate(self, force_new_credentials: bool = False):
        """
        Authenticate the user with Auth0
        Save this authentication so we don't have to regenerate it every time
        """

        # Load authentication token from .env.auth file
        def load_auth_token() -> Union[dict, None]:
            token_file = None
            if os.path.isfile('.env.auth'):
                with open('.env.auth', 'r') as file:
                    token_file = file.read().strip()

            if token:=is_auth_token_valid(token_file):
                return token

            return None

        # Save authentication token to .env.auth file
        def save_auth_token(auth_token: dict):
            with open('.env.auth', 'w') as file:
                token_file = {"token": auth_token, "expiration": time.time() + 3600}
                file.write(json.dumps(token_file))


        # Check if authentication token is valid. Return actual token if valid, None if not
        def is_auth_token_valid(token: str) -> Union[dict, None]:
            if token:
                try:
                    token_file = json.loads(token)
                    expiration = float(token_file['expiration'])
                    if expiration >= time.time():
                        return token_file['token']
                except Exception as e:
                    print(f"Error loading token file: {e}")
            return None

        auth0_token = load_auth_token()
        if not auth0_token or force_new_credentials:
            auth0 = Auth0DeviceAuthorization()
            auth0_token = auth0.authenticate()
            save_auth_token(auth0_token)
        
        self.token = auth0_token

            
    def play_game(self) -> dict:
        """Plays the game until it is over."""

        self.join_game()

        # Intialize the game state and wait for evenyone to join
        while True:
            # Get game state from server
            self.game.set_game_state(self.get_game_state(), validate=False)
            def validate_player_joined(id:str):
                parts = id.split('.')
                return len(parts) == 2

            if validate_player_joined(self.game.player1_id) and validate_player_joined(self.game.player2_id):
                break

        while not self.game.is_game_over():
            # Get game state from server
            new_state = self.get_game_state()

            # Update local game state
            self.game.set_game_state(new_state, validate=False)

            if self.game.is_my_turn(self.player.id):
                move = self.player.make_move(self.game)
                if move:
                    # Make the move on the server
                    self.make_move(move)
                    pass
                else:
                    print("No moves available. Ending game.")
                    break
                    
            else:
                # Wait a bit until maybe it's my turn
                time.sleep(0.5)
                
        final_state = self.game.get_game_state()
        final_score = self.get_game_score()
        p1_score = final_score.get('player1_score', None)
        p2_score = final_score.get('player2_score', None)
        winner = 1 if p1_score > p2_score else 2 if p2_score > p1_score else 0

        print(f"Game Over: {final_state=}, {final_score=}")
        print(f"Player 1: {self.game.player1_id}={p1_score}")
        print(f"Player 2: {self.game.player2_id}={p2_score}")
        print(f"Winner: {['Draw', self.game.player1_id, self.game.player2_id][winner]}")
        return {"state": final_state, "score": final_score}

    def __create_a_test_game(self) -> dict:
        """
        Create a test game for the player.
        This shouldn't be part of the final package, but is useful for testing.
        """

        with ConnectionClient(self.host_url, self.access_token) as api_instance:
            try:
                # Create a game
                create_game_request = {"player_id1": self.player.id, "player_id2": "player2", "vertex_count": self.game_spec["vertex_count"], "edges": self.game_spec["edges"]}
                api_response = api_instance.public_create_game(create_game_request, sub=self.player.id)
                print(f"The response of DefaultApi->create_game:\n{api_response}")
                return api_response.dict()
            except ApiException as e:
                print(f"Exception when calling DefaultApi->public_get_score: {e}")
                raise e
            except Exception as e:
                print(f"Exception when calling DefaultApi->public_get_score: {e}")
                raise e
            

    def join_game(self):
        """
        Set up connection to the server to join the remote game.
        Saves the player connection token and player index.
        """

        with ConnectionClient(self.host_url, self.access_token) as api_instance:
            try:
                # Join the game
                join_game_request = {"game_token": self.game_id, "player_id": self.player.id, "player_index": self.player_index}
                api_response = api_instance.join_game(join_game_request)
                print(f"The response of DefaultApi->join_game:\n{api_response}")
                self.join_token = api_response.join_token
                self.player_index = api_response.player_index
                self.player.id = api_response.player_id

            except Exception as e:
                print(f"Exception when joining game {join_game_request=}: {e}")
                raise e

    def get_game_state(self) -> dict:
        """Set up connection to the server to get the game state"""

        with ConnectionClient(self.host_url, self.access_token) as api_instance:
            try:
                print(f"Getting game state for game {self.game_id}")
                api_response = api_instance.get_game_state(self.game_id)
                print(f"The response of DefaultApi->get_game_state:\n{api_response}")
                return api_response.to_dict()["state"]
            except Exception as e:
                print(f"Exception when calling DefaultApi->get_game_state: {e}")
                raise e

    def get_game_score(self) -> dict:
        """Set up connection to the server to get the game score"""

        with ConnectionClient(self.host_url, self.access_token) as api_instance:
            try:
                print(f"Getting game score for game {self.game_id}")
                api_response = api_instance.get_score(self.game_id, "simulatedannealing")
                print(f"The response of DefaultApi->get_game_score:\n{api_response}")
                return api_response.to_dict()["score"]
            except Exception as e:
                print(f"Exception when calling DefaultApi->get_game_state: {e}")
                raise e

    def make_move(self, move: tuple[int, int, int]) -> bool:
        """Set up connection to the server to make a move"""

        with ConnectionClient(self.host_url, self.access_token) as api_instance:
            try:
                make_move_request = MakeMoveRequest(game_token=self.game_id, player_id=self.player.id, join_token=self.join_token, move=move)
                api_response = api_instance.make_move(make_move_request)
                print(f"The response of DefaultApi->make_move:\n{api_response}")
                return True
            except Exception as e:
                print(f"Exception when making a move {make_move_request=}: {e}")
                raise e

        return False
    
    def __test_token_and_login(self):
        """
        Test the login process.
        """
        print(f"Token Response: {self.token}")
        
        self.validate_token(self.access_token)
        self.validate_token(self.id_token)

        # Test login with id_token
        # Do a post to http://localhost:8080/login_user with the id_token as the Authorization header
        base_url = "http://localhost:8081"
        base_url= "https://main-service-fastapi-blue-pond-7261.fly.dev"

        while True:
            try:
                login_response = requests.post(f"{base_url}/login_user", 
                                                headers={
                                                    "Authorization": f"Bearer {self.access_token}",
                                                    "X-ID-Token": self.id_token},
                                                timeout=20)
                print(f"Login Response: {login_response.json()}")

                if login_response.status_code == 200:
                    users_response = requests.get(f"{base_url}/users", 
                                                headers={"Authorization": f"Bearer {self.access_token}"},
                                                timeout=20)
                    print(f"Users Response: {users_response.json()}")
                    break
            except requests.exceptions.Timeout:
                print("Timeout waiting for login response.")
            except requests.exceptions.ConnectionError:
                print("Connection error waiting for login response.")
            except requests.exceptions.RequestException as e:
                print("Error waiting for login response:", e)
                time.sleep(5)

    @staticmethod
    def decode_token(token: str) -> dict:
        """
        Decode a JWT token to extract claims.

        Args:
            token (str): The JWT token to decode.

        Returns:
            dict: The decoded claims.
        """
        decoded_token = jwt.decode(token, options={"verify_signature": False})
        return decoded_token
    
    def validate_token(self, token: str) -> bool:
        """
        Decode a JWT token to extract claims.

        Args:
            token (str): The JWT token to decode.

        Returns:
            dict: The decoded claims.
        """
        try:
            decoded_token = self.decode_token(token)
            print("Decoded Token:", decoded_token)
            return True
        except Exception as e:
            print(f"Error decoding token: {e}")
            return False


    @staticmethod
    def get_user_id(token: str) -> str:
        """
        Get the user ID from the token.

        Args:
            token (str): The JWT token to decode.

        Returns:
            str: The user ID.
        """
        return RemoteGamePlayer.decode_token(token).get('sub')
    
