import pandas as pd

def find_top_interests_pandas(csv_file, top_n=4):
    """Reads the CSV file and finds the top N interests for each participant, considering only interest values > 3."""
    df = pd.read_csv(csv_file)
    names = df['Name'].tolist()
    results = []

    for name in names:
        row = df[df['Name'] == name].iloc[0, 1:]
        filtered_row = row[row > 3]  # Only consider interest values > 3
        top_interests = filtered_row.sort_values(ascending=False).head(top_n).index.tolist()
        results.append({'Name': name, 'Top Interests': top_interests})

    return pd.DataFrame(results)

def create_topic_groups(df):
    """Creates groups of participants for each topic based on their interests."""
    topic_groups = {}
    for topic in df.columns[1:]:
        topic_groups[topic] = df.sort_values(by=topic, ascending=False)['Name'].tolist()
    return topic_groups

def assign_sessions(topic_groups, predefined_sessions, max_per_group=12):
    """Assigns topics to predefined sessions while ensuring no participant is scheduled for multiple topics in the same session."""
    sessions = {session: {topic: [] for topic in topics} for session, topics in predefined_sessions.items()}
    assigned_people = {session: set() for session in predefined_sessions.keys()}
    all_people = set()

    for session, topics in predefined_sessions.items():
        for topic in topics:
            if topic in topic_groups:
                for person in topic_groups[topic]:
                    if person not in assigned_people[session] and len(sessions[session][topic]) < max_per_group:
                        sessions[session][topic].append(person)
                        assigned_people[session].add(person)
                        all_people.add(person)

    # Ensure each person is scheduled at least once overall
    for person in df['Name']:
        if person not in all_people:
            for session, topics in predefined_sessions.items():
                for topic in topics:
                    if topic in topic_groups and person in topic_groups[topic] and len(sessions[session][topic]) < max_per_group:
                        sessions[session][topic].append(person)
                        assigned_people[session].add(person)
                        all_people.add(person)
                        break

    return sessions

def print_sessions_with_people(sessions):
    """Prints the assigned sessions with topics and assigned people."""
    for session, topics in sessions.items():
        print(f"Session {session}:")
        for topic, people in topics.items():
            print(f"  - {topic}:")
            for person in people:
                print(f"{person}")
        print("-" * 20)

def print_volunteers(df):
    """Prints the names of participants who have specified a 6 (volunteers) and the topics they volunteered for."""
    volunteers = df[df.iloc[:, 1:].eq(6).any(axis=1)]
    for index, row in volunteers.iterrows():
        name = row['Name']
        topics = row[row == 6].index.tolist()
        print(f"{name}: {', '.join(topics)}")


if __name__ == "__main__":
    csv_file_path = 'interests.csv'
    df = pd.read_csv(csv_file_path)
    predefined_sessions = {
        1: ["Hardware Development", "AI", "Software Development", "Statistical Methods", "Modeling Systems", "New physics at colliders", "How to PhD"],
        2: ["Labs", "AI", "Software Development", "Statistical Methods", "Dark Matter", "Time Management", "How to PhD"],
        3: ["FPGA Development", "AI", "Analytical Methods", "Statistical Methods", "Dark Matter", "Time Management", "Outreach"],
        4: ["Automation", "Software Development", "Analytical Methods", "Modeling Systems", "New physics at colliders", "Addressing Power Abuse", "Non-Scientific Topics"]
    }
    top_interests_df = find_top_interests_pandas(csv_file_path, top_n=4)
    if not top_interests_df.empty:
        topic_groups = create_topic_groups(df)
        sessions = assign_sessions(topic_groups, predefined_sessions)
        print_sessions_with_people(sessions)
        print("\nVolunteers:")
        print_volunteers(df)