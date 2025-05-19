import csv
import os
from datetime import datetime
import matplotlib.pyplot as plt

DATA_FILE = 'mood_log.csv'

# Mapping: user input number → (emoji, mood level)
MOOD_OPTIONS = {
    '1': ('😄', 3),
    '2': ('😊', 2),
    '3': ('😐', 1),
    '4': ('☹️', 0),
}

def init_data_file():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Date', 'Emoji', 'Note'])

def log_mood():
    date_str = datetime.now().strftime('%Y-%m-%d')
    print("\nHow do you feel today?")
    for num, (emoji, _) in MOOD_OPTIONS.items():
        print(f"{num}. {emoji}")

    choice = input("Enter the number corresponding to your mood: ").strip()
    if choice not in MOOD_OPTIONS:
        print("Invalid choice. Please try again.")
        return

    emoji, _ = MOOD_OPTIONS[choice]
    note = input("Optional note: ").strip()

    with open(DATA_FILE, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([date_str, emoji, note])

    print("✅ Mood logged!")

def plot_moods():
    if not os.path.exists(DATA_FILE):
        print("No mood data found.")
        return

    dates, moods, notes = [], [], []
    emoji_to_level = {emoji: level for _, (emoji, level) in MOOD_OPTIONS.items()}
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            dates.append(row['Date'])
            moods.append(emoji_to_level.get(row['Emoji'], 1))  # default to neutral
            notes.append(row['Note'])

    if not dates:
        print("No mood data to plot.")
        return

    plt.figure(figsize=(10, 5))
    plt.plot(dates, moods, marker='o', linestyle='-', linewidth=2, color='#6A5ACD')

    # Add emoji annotations at each point
    for i, (x, y) in enumerate(zip(dates, moods)):
        emoji = list(emoji_to_level.keys())[list(emoji_to_level.values()).index(y)]
        plt.text(x, y + 0.1, emoji, fontsize=16, ha='center')

    plt.ylim(-0.5, 3.5)
    plt.yticks([0, 1, 2, 3], ['☹️', '😐', '🙂', '😄'], fontsize=12)
    plt.xticks(rotation=45, fontsize=10)
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Mood Level', fontsize=12)
    plt.title('Mood Over Time', fontsize=14, weight='bold', pad=15)
    plt.grid(visible=True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.gca().set_facecolor('#F9F9F9')  # Light background
    plt.show()

def main():
    init_data_file()
    while True:
        print("\n=== Emoji Mood Tracker ===")
        print("1. Log today's mood")
        print("2. Show mood chart")
        print("3. Exit")
        choice = input("> ").strip()
        if choice == '1':
            log_mood()
        elif choice == '2':
            plot_moods()
        elif choice == '3':
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please choose 1, 2, or 3.")

if __name__ == "__main__":
    main()
