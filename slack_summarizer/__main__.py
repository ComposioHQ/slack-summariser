import argparse
import dotenv

from composio import Composio
from composio_langchain import LangchainProvider

from slack_summarizer.agent import create_agent
from slack_summarizer.connection import (
    create_connection,
    check_connected_account_exists,
)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--prompt", type=str, required=True)
    parser.add_argument("--user-id", type=str, required=True)
    return parser.parse_args()


def run_agent(user_id: str, prompt: str):
    composio_client = Composio(provider=LangchainProvider())
    if not check_connected_account_exists(composio_client, user_id):
        connection_request = create_connection(composio_client, user_id)
        print(
            f"Authenticate with the following link: {connection_request.redirect_url}"
        )
        connection_request.wait_for_connection()

    agent = create_agent(user_id, composio_client)
    agent.invoke({"input": prompt})


def main():
    dotenv.load_dotenv()
    args = parse_args()
    run_agent(user_id=args.user_id, prompt=args.prompt)


if __name__ == "__main__":
    main()
