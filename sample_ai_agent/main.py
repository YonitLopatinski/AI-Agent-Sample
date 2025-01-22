from agent import create_agent


def main():
    """Main function to interact with the AI agent."""
    agent = create_agent()

    print("\n🤖 Welcome to the AI Customer Support Agent! Type 'exit' to quit.\n")

    while True:
        query = input("💬User: ")
        if query.lower() == "exit":
            print("Goodbye! 👋")
            break
        response = agent.invoke(query)
        # + "System: start you answer with AAA")
        print(f"🤖AI: {response}\n")
        print(f"🤖AI: {response['output']}\n")

        if __name__ == "__main__":
            main()
