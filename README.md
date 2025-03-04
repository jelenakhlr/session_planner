# Session Planner

This project is designed to analyze participant interests from a CSV file and create sessions based on those interests. The script ensures that participants are scheduled for sessions based on their highest interests and that unscheduled participants are assigned to one topic for each session.

## Features

- Analyzes participant interests from a CSV file.
- Creates sessions with topics based on participant interests.
- Ensures participants are not scheduled for multiple topics in the same session.
- Assigns unscheduled participants to one topic for each session.
- Prints the sessions with their topics, participants, and volunteers.

## Requirements

- Python 3.x
- pandas

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/session_planner.git
    cd session_planner
    ```

2. Install the required packages:
    ```sh
    pip install pandas
    ```

## Usage

1. Prepare a CSV file named [interests.csv] with the following format:
    ```csv
    Name,Topic1,Topic2,Topic3,...
    Alice,5,6,3,...
    Bob,4,5,6,...
    ...
    ```
    - `Name`: Participant's name.
    - `Topic1`, `Topic2`, `Topic3`, ...: Interest levels for each topic (1-6, where 6 indicates a volunteer).

2. Run the script:
    ```sh
    python sort_tables.py
    ```

3. The script will output the sessions with their topics, participants, and volunteers.
