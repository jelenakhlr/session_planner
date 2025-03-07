import pandas as pd
import random

def find_top_interests_pandas(csv_file):
    """(Same as before)"""
    try:
        df = pd.read_csv(csv_file)
        names = df['Name'].tolist()
        results = []

        for name in names:
            row = df[df['Name'] == name].iloc[0, 1:]
            top_5 = row.sort_values(ascending=False).head(5).index.tolist()
            results.append({'Name': name, 'Top Interests': top_5})

        return pd.DataFrame(results)

    except FileNotFoundError:
        print(f"Error: File not found at {csv_file}")
        return pd.DataFrame()
    except Exception as e:
        print(f"An error occurred: {e}")
        return pd.DataFrame()

def create_topic_groups(interests_df):
    """(Same as before)"""
    topic_groups = {}
    if not interests_df.empty:
        for index, row in interests_df.iterrows():
            name = row['Name']
            for topic in row['Top Interests']:
                if topic not in topic_groups:
                    topic_groups[topic] = []
                topic_groups[topic].append(name)
    return topic_groups

def assign_sessions_optimized(topic_groups, max_iterations=1000):
    """(Same as before)"""
    all_topics = list(topic_groups.keys())
    num_sessions = 4
    best_sessions = None
    best_happiness = float('-inf')

    for _ in range(max_iterations):
        sessions = {i: [] for i in range(1, num_sessions + 1)}
        assigned_people = {i: set() for i in range(1, num_sessions + 1)}
        random.shuffle(all_topics)

        for topic in all_topics:
            assigned = False
            for session_num in range(1, num_sessions + 1):
                valid = True
                for person in topic_groups[topic]:
                    if person in assigned_people[session_num]:
                        valid = False
                        break
                if valid:
                    sessions[session_num].append(topic)
                    for person in topic_groups[topic]:
                        assigned_people[session_num].add(person)
                    assigned = True
                    break

        happiness = calculate_happiness(sessions, topic_groups)

        if happiness > best_happiness:
            best_happiness = happiness
            best_sessions = sessions

    return best_sessions

def calculate_happiness(sessions, topic_groups):
    """(Same as before)"""
    happiness = 0
    assigned_people = {i: set() for i in range(1, 5)}
    for session_num, topics in sessions.items():
        for topic in topics:
            for person in topic_groups[topic]:
                if person not in assigned_people[session_num]:
                    happiness += 1
                    assigned_people[session_num].add(person)
    return happiness

def print_sessions_with_people(sessions, topic_groups):
    """
    Prints the assigned sessions with topics and assigned people.

    Args:
        sessions (dict): A dictionary of sessions and their assigned topics.
        topic_groups (dict): A dictionary of topics and their associated names.
    """
    for session_num, topics in sessions.items():
        print(f"Session {session_num}:")
        for topic in topics:
            print(f"- Group: {topic} -")
            for person in topic_groups[topic]:
                print(f"{person}")
        print("-" * 20)

def print_volunteers(df):
    """
    Prints the names of participants who have specified a 6 (volunteers) and the topics they volunteered for.

    Args:
        df (pd.DataFrame): DataFrame containing participant names and interests.
    """
    volunteers = df[df.iloc[:, 1:] == 6].dropna(how='all')
    for index, row in volunteers.iterrows():
        name = row['Name']
        topics = row[row == 6].index.tolist()
        print(f"{name} volunteered for: {', '.join(topics)}")

if __name__ == "__main__":
    csv_file_path = 'interests.csv'
    top_interests_df = find_top_interests_pandas(csv_file_path)
    if not top_interests_df.empty:
        topic_groups = create_topic_groups(top_interests_df)
        sessions = assign_sessions_optimized(topic_groups)
        print_sessions_with_people(sessions, topic_groups)
        print("\nVolunteers:")
        print_volunteers(pd.read_csv(csv_file_path))