from database import setup_database
from chat import ask_zero
from notifications import get_notifications
from session import clear_session
from timing import print_stats
from episode_database import setup_episode_database

def main():

    setup_database()
    clear_session()
    setup_episode_database()

    print("=" * 50)
    print("Zero is online.")
    print("Type 'exit' to quit.")
    print("=" * 50)

    while True:

        for note in get_notifications():
            print(note)

        user = input("\nYou: ").strip()

        if not user:
            continue

        if user.lower() in ("exit", "quit", "bye"):
            print("\nZero: Goodbye, Safvan.")
            break

        result = ask_zero(user)

        if result:
            print(f"\nZero: {result['reply']}")
            
            if result["stats"] is not None: 
                print_stats(result['stats'], result['elapsed'])  # Placeholder for elapsed time

if __name__ == "__main__":
    main()