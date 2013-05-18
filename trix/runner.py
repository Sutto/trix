import argparse
from .config import defaults, Configuration
from .environment import Environment
from .game import readPieces
import trix.agent

parser = argparse.ArgumentParser(description="Trix configuration information")
parser.add_argument('-c', '--config', dest='config_file', help='A configuration file to read details from', nargs='?')
parser.add_argument('-a', '--agent', dest='agent', help='The name of the agent ot use', nargs='?', default=defaults.agent, type=str, choices=trix.agent.ValidAgents)
parser.add_argument('-w', '--width', dest='width', help='The width of the tetrist board', default=defaults.width, type=int)
parser.add_argument('-b', '--buffer', dest='buffer', help='The size of the buffer', default=defaults.buffer, type=int)
parser.add_argument('input_file', help='The file to read input from')
parser.add_argument('output_file', help='The file to write output to')

def main(argv):
    parsed_arguments = parser.parse_args(argv[1:])
    configuration = Configuration()
    configuration.merge(parsed_arguments)
    # Now, build the environment.
    pieces      = readPieces(configuration.input_file)
    environment = Environment(configuration, pieces)
    agent_type  = trix.agent.from_name(configuration.agent)
    agent       = agent_type(environment)
    agent.run()

if __name__ == '__main__':
  import sys
  main(sys.argv)