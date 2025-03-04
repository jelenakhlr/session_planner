import pandas as pd
import random

def analyze_interest(df):
    """
    Analyzes participant interests from a DataFrame.

    Args:
        df (pd.DataFrame): DataFrame containing participant names and interests.

    Returns:
        dict: A dictionary where keys are topics and values are dictionaries containing lists of 'highest_interest' and 'volunteers'.
    """
    topics = df.columns[1:]  # Exclude 'Name' column
    results = {}
    for topic in topics:
        highest_interest = []
        volunteers = []
        max_interest = df[topic].max()
        if max_interest == 6:  # 6 indicates volunteer
            volunteers = df[df[topic] == 6]['Name'].tolist()
            highest_interest = df[df[topic] == 5]['Name'].tolist() #if there are volunteers, consider 5 as the highest interest.
        else:
            highest_interest = df[df[topic] == max_interest]['Name'].tolist()
            volunteers = []
        results[topic] = {'highest_interest': highest_interest, 'volunteers': volunteers}
    return results



def create_sessions(results, num_sessions=4, max_topics_per_session=7, df=None):
    """
    Creates sessions with relaxed constraints, minimizing conflicts and scheduling unscheduled participants.

    Args:
        results (dict): Dictionary from analyze_interest.
        num_sessions (int): Number of sessions.
        max_topics_per_session (int): Maximum topics per session.
        df (pd.DataFrame): Original DataFrame for unscheduled participant lookup.

    Returns:
        dict: Dictionary representing the sessions and their topics with participants.
    """
    sessions = {f"Session {i+1}": {} for i in range(num_sessions)}
    topics = list(results.keys())
    random.shuffle(topics)

    session_index = 0
    while topics:
        topic = topics.pop(0)
        participants = results[topic]['highest_interest'] + results[topic]['volunteers']
        volunteers = results[topic]['volunteers']

        session_participants = set() #keep track of participants in current session.
        for t_data in sessions[f"Session {session_index + 1}"].values():
            session_participants.update(t_data['participants'])

        valid_participants = [p for p in participants if p not in session_participants] #remove duplicates in current session.
        valid_volunteers = [v for v in volunteers if v in valid_participants]

        if len(sessions[f"Session {session_index + 1}"]) < max_topics_per_session and valid_participants:
            sessions[f"Session {session_index + 1}"][topic] = {
                'participants': valid_participants,
                'volunteers': valid_volunteers,
            }
            session_index = (session_index + 1) % num_sessions #move to next session.
        else:
            topics.append(topic) #add topic back to list if session is full or no valid participants.
            session_index = (session_index + 1) % num_sessions #move to next session.

    # Schedule unscheduled participants
    scheduled_participants = set()
    for session in sessions.values():
        for data in session.values():
            scheduled_participants.update(data['participants'])

    unscheduled_participants = set(df['Name']) - scheduled_participants
    
    for participant in unscheduled_participants:
        top_interests = [] #list to store the top interests.
        for topic in results:
            interest_value = df.loc[df['Name'] == participant, topic].values[0]
            if interest_value < 6: #exclude volunteers.
                top_interests.append((interest_value, topic)) #add the interest to the list.

        top_interests.sort(key=lambda x: x[0], reverse=True) #sort the interests in descending order.
        # Schedule unscheduled participants for each session
    scheduled_participants = set()
    for session in sessions.values():
        for data in session.values():
            scheduled_participants.update(data['participants'])

    unscheduled_participants = set(df['Name']) - scheduled_participants

    for participant in unscheduled_participants:
        
        top_interests = []
        for topic in results:
            interest_value = df.loc[df['Name'] == participant, topic].values[0]
            if interest_value < 6:
                top_interests.append((interest_value, topic))

        top_interests.sort(key=lambda x: x[0], reverse=True)
        
        for session_name in sessions:
            if top_interests:
                topic_to_add = top_interests.pop(0)
                topic_to_add = topic_to_add[1] #get the topic name.
                session_participants = set()
                for t_data in sessions[session_name].values():
                    session_participants.update(t_data['participants'])

                if participant not in session_participants and len(sessions[session_name]) < max_topics_per_session:

                    if topic_to_add in sessions[session_name]:
                        sessions[session_name][topic_to_add]['participants'].append(participant)
                    else:
                        sessions[session_name][topic_to_add] = {'participants': [participant], 'volunteers': []}
            
    # Final check and scheduling for remaining unscheduled participants
    scheduled_participants = set()
    for session in sessions.values():
        for data in session.values():
            scheduled_participants.update(data['participants'])

    remaining_unscheduled = set(df['Name']) - scheduled_participants
    
    for participant in remaining_unscheduled:
        for session_name in sessions:
            session_participants = [p for data in sessions[session_name].values() for p in data['participants']]
            if participant not in session_participants:
                top_interests = []
                for topic in results:
                    interest_value = df.loc[df['Name'] == participant, topic].values[0]
                    if interest_value < 6:
                        top_interests.append((interest_value, topic))
                top_interests.sort(key=lambda x: x[0], reverse=True)
                if top_interests:
                    topic_to_add = top_interests[0][1]
                    if topic_to_add in sessions[session_name]:
                        sessions[session_name][topic_to_add]['participants'].append(participant)
                    else:
                        sessions[session_name][topic_to_add] = {'participants': [participant], 'volunteers': []}
    return sessions

def final(sessions):
    # Final group size check and splitting
    for session_name, session_data in sessions.items():
        for topic, data in list(session_data.items()):  # Use list() to avoid dictionary size change during iteration
            participants = data['participants']
            if 10 < len(participants):
                half_len = len(participants) // 2
                first_half = participants[:half_len]
                second_half = participants[half_len:]
                session_data[f"{topic} (1)"] = {'participants': first_half, 'volunteers': [v for v in data['volunteers'] if v in first_half]}
                session_data[f"{topic} (2)"] = {'participants': second_half, 'volunteers': [v for v in data['volunteers'] if v in second_half]}
                del session_data[topic]

            elif len(participants) < 3 and len(participants) > 0:
                del session_data[topic] #remove groups that are too small.

    return sessions


def print_sessions_with_participants_and_volunteers(sessions):
    """
    Prints the sessions and their topics with participants and volunteers.

    Args:
        sessions (dict): Dictionary representing the sessions.
    """
    for session, topics in sessions.items():
        print(f"{session}:")
        for topic, data in topics.items():
            print(f"  - {topic}:")
            if data['participants']:
                print("    - Participants:")
                for name in data['participants']:
                    print(f"      - {name}")
            else:
                print("    - No participants")
            if data['volunteers']:
                print("    - Volunteers:")
                for name in data['volunteers']:
                    print(f"      - {name}")
        print("-" * 20)

if __name__ == '__main__':
    df = pd.read_csv('interests.csv')
    results = analyze_interest(df)
    sessions = create_sessions(results, df=df)
    sessions = final(sessions)
    print_sessions_with_participants_and_volunteers(sessions)