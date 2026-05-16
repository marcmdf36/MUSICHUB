from agent.memory import get_history

for song in get_history():
    print(f"{song['recommended_date']} | {song['artist']} - {song['title']} ({song['genre']})")