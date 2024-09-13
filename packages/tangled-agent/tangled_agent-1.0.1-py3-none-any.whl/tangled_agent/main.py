"""
Main entry point for the Tangled agent game playing tools.
"""

from __future__ import annotations

import importlib
import sys
import configargparse
from tangled_game_engine import GameAgentBase, Game
from .basic_game import play_local_game, play_remote_game


def import_agent(agent_name: str) -> GameAgentBase:
    """
    Dynamically import a class from a string specification in the format 'module_name.ClassName'.
    
    Args:
        agent_name (str): The module and class name as a single string.
    
    Returns:
        type: The class type that was dynamically imported.
    """
    try:
        # Split the input into module and class
        print(f"Importing {agent_name}")
        module_name, class_name = agent_name.rsplit('.', 1)
        print(f"Importing module {module_name} and class {class_name}")

        # Import the module
        module = importlib.import_module(module_name)

        # Get the class from the module
        clazz = getattr(module, class_name)
        if not issubclass(clazz, GameAgentBase):
            raise ValueError(f"Class '{class_name}' is not a subclass of GameAgentBase.")
        
        return clazz
    except (ImportError, AttributeError, ValueError) as e:
        raise ImportError(f"Could not import class {agent_name}. Ensure it exists and is correctly specified (e.g. module_name.ClassName).") from e
    

def setup_args() -> configargparse.ArgParser:
    """
    Set up handling of command-line arguments.
    """

    description = """
Play a game of Tangled with one or two custom agents, either for local testing
 or for online play."""
    
    epilog = """
Run this program with the --help flag to see the full list of options.
"""

    usage = """
Local game: 
    python -m tangled-agent --agent your_agent.YourAgentClass
Remote game: 
    python -m tangled-agent --game-id <game-id> --agent your_agent.YourAgentClass [--player-index 1] [--new-credentials]

Or you can use a configuration file (e.g. config.ini) with the following format:

```config.ini
[DEFAULT]
agent = your_agent.YourAgentClass
agent_2 = your_agent.OtherAgentClass
vertex_count = 5
game-id = <game-id>
host = <game-host>
new-credentials = False
```

or a combination of both:

    python -m tangled_agent:main --config config.ini --game_id <game-id> --host <game-host> --new-credentials

If a game-id is provided, the script will connect to the remote game server and join the game as either player 1 or 2 using the specified GameAgent subclass.
"""

    parser = configargparse.ArgParser(description=description,
                                        epilog=epilog,
                                        usage=usage,
                                        default_config_files=['config.ini'])

    

    parser.add('--config', is_config_file=True, help='Path to the configuration file.')
    parser.add_argument('--game-id', type=str, default=None, help='The ID of the game to connect to for a remote game.')
    parser.add_argument('--host', type=str, default='https://game-service-fastapi-blue-pond-7261.fly.dev', help='The host URL for the remote game server.')
    parser.add_argument('--new-credentials', action='store_true', help='Force new credentials.')
    parser.add_argument('--agent-class', type=str, default="tangled_agent.RandomRandyAgent", help='The qualified name of the game agent class (module.ClassName) to use.')
    parser.add_argument('--agent-class-2', type=str, default=None, help='The qualified name of the game agent class (module.ClassName) to use for player 2 (local game only).')
    parser.add_argument('--agent-name', type=str, default="default", help="The name of the logged in user's agent-id to join the game as (e.g. default).")
    parser.add_argument('--player-index', type=int, default=0, help='The index of the player to be in the game (0=no preference, 1 or 2).')
    parser.add_argument('--vertex-count', type=int, default=0, help='The number of vertices in the game (default edges are all possible combinations).')
    parser.add_argument('--game-spec', type=str, default=None, help='A JSON-formatted array of pairs (e.g. [[0,1],[0,2],...]) representing the game specification as edges. Vertex count will default to max index in the edge list+1.')
    parser.add_argument('--generate-agent', action='store_true', help='Generate an example agent class in agent-example.py.')
    return parser


example_agent = '''
from __future__ import annotations

from typing import Tuple
from tangled_agent import GameAgentBase, Game, Vertex, Edge

class ExampleAgent(GameAgentBase):
    """
    Example agent class for playing the Snowdrop Quantum Tangled game.
    Implement the make_move method to make a move in the game.
    Use the game object to get the current game state and legal moves.
    Generate a move as a tuple of (move_type, move_index, move_state).
        move_type (int): The type of move to make (e.g. Game.MoveType.EDGE.value).
        move_index (int): The index of the move to make (e.g. the edge index).
        move_state (int): The state of the move to make (e.g. Game.Edge.State.FM).
    Valid move_type:
        Game.MoveType.EDGE.value: Set the state of an edge.
        Game.MoveType.VERTEX.value: Claim a vertex (once per player per game)
        Game.MoveType.QUIT.value: Quit the game.
    Valid move_state:
        For Game.MoveType.EDGE move:
            Game.Edge.State.NEITHER.value: Set the edge to have no preferred state.
            Game.Edge.State.FM.value: Set the edge to prefer a feromagnetic state.
            Game.Edge.State.NFM.value: Set the edge to prefer a non-feromagnetic state.
        For Game.MoveType.VERTEX move:
            Game.Vertex.State.P1.value: Claim the vertex for player 1.
            Game.Vertex.State.P2.value: Claim the vertex for player 2.
    """

    def make_move(self, game: Game) -> Tuple[int, int, int]:
        """
        Make a random legal move in the game.
        """
        import random

        legal_moves = game.get_legal_moves(self.id)

        # Look at the details and state of the game.
        state = game.get_game_state()

        if not legal_moves or (len(legal_moves) == 1 and legal_moves[0][0] == Game.MoveType.QUIT.value):
            print("No legal moves available. Game must be over.")
            return None

        while True:
            move = random.choice(legal_moves)
            if move[0] != Game.MoveType.QUIT.value:
                break

        return move
    

'''

def main():
    """
    Main entry point for the script.
    Get the command-line arguments and start the game.
    """
    global args

    if args.generate_agent:
        print("Generating example agent class in agent-example.py")
        import os
        if os.path.exists("agent-example.py"):
            print("File agent-example.py already exists. Exiting without overwriting.")
            exit(1)

        with open("agent-example.py", "w") as f:
            f.write(example_agent)
            exit(0)

    # Create an agent from the class from a string
    agent_class = import_agent(args.agent_class)

    agent_name = args.agent_name

    if args.game_id is not None:

        # Create the agent to play the game. The player ID should match one of the players in the game.
        player = agent_class()

        print(f"Game ID: {args.game_id}")
        print(f"Host: {args.host}")
        print(f"Force New Credentials: {args.new_credentials}")
        print(f"Player Index: {args.player_index}")
        print(f"Agent Name: {agent_name}")

        play_remote_game(args.game_id, args.host, player, player_index=args.player_index, agent_name=agent_name, force_new_credentials=args.new_credentials)
    else:
        # Create an agent from the class from a string
        agent_class2 = import_agent(args.agent_class_2) if args.agent_class_2 else None

        # Create two agents with names (e.g. RandomRandyAgent("player1"))
        player1 = agent_class(agent_class.__name__)
        player2 = agent_class2(agent_class2.__name__) if agent_class2 else agent_class(agent_class.__name__ + "_2")

        # Make a game specification if we have a game spec
        if args.vertex_count >= 2 and args.game_spec:
            game_spec = {"vertex_count": args.vertex_count, "edges": args.game_spec}
        elif args.game_spec:
            game_spec = {"vertex_count": max([max(edge) for edge in args.game_spec])+1, "edges": args.game_spec}
        else:
            if args.vertex_count < 2:
                # Default to 3 vertices if no vertex count is specified
                print("No vertex count specified. Defaulting to 3 vertex game.")
                args.vertex_count = 3
            game_spec = {"vertex_count": args.vertex_count, "edges": [[i, j] for i in range(args.vertex_count-1) for j in range(i+1, args.vertex_count)]}

        print(f"Game Specification: {game_spec}")
        game = Game()
        game.create_game(game_spec["vertex_count"], game_spec["edges"])

        # Play a local game with the two agents
        play_local_game(player1, player2, game)


args = setup_args().parse_args()

if __name__ == "__main__":
    main()

