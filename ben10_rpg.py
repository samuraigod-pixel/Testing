#!/usr/bin/env python3
"""Text-based RPG set in the Ben 10 universe with detailed character creation."""

from __future__ import annotations

import textwrap


LINE = "-" * 72


def wrap(text: str) -> str:
    return "\n".join(textwrap.wrap(text, width=72))


def prompt_choice(prompt: str, options: list[str]) -> str:
    options_lower = {opt.lower(): opt for opt in options}
    while True:
        print(prompt)
        for idx, opt in enumerate(options, start=1):
            print(f"  {idx}. {opt}")
        choice = input("Choose by number or name: ").strip()
        if not choice:
            continue
        if choice.isdigit():
            idx = int(choice)
            if 1 <= idx <= len(options):
                return options[idx - 1]
        normalized = choice.lower()
        if normalized in options_lower:
            return options_lower[normalized]
        print("Invalid choice, try again.\n")


def prompt_int(prompt: str, min_value: int, max_value: int) -> int:
    while True:
        value = input(f"{prompt} ({min_value}-{max_value}): ").strip()
        if not value.isdigit():
            print("Enter a number.")
            continue
        number = int(value)
        if min_value <= number <= max_value:
            return number
        print("Out of range. Try again.")


def prompt_yes_no(prompt: str) -> bool:
    while True:
        value = input(f"{prompt} [y/n]: ").strip().lower()
        if value in {"y", "yes"}:
            return True
        if value in {"n", "no"}:
            return False
        print("Please answer y or n.")


def intro() -> None:
    print(LINE)
    print("BEN 10: OMNITRIX CHRONICLES")
    print(LINE)
    print(wrap(
        "A strange surge of energy hits Bellwood. The Omnitrix is unstable, and "
        "only a new hero can stabilize it. Build your character, step into the "
        "Ben 10 universe, and decide what kind of legend you'll become."
    ))
    print(LINE)


def choose_background() -> dict:
    backgrounds = {
        "Plumber Cadet": {
            "description": "Trained by the Plumbers, you know protocols and tech.",
            "bonuses": {"Tech": 2, "Tactics": 1},
        },
        "Road Trip Survivor": {
            "description": "You grew up on the road and learned to improvise.",
            "bonuses": {"Agility": 1, "Willpower": 2},
        },
        "Alien Exchange Student": {
            "description": "You came to Earth to study humanity and its quirks.",
            "bonuses": {"Empathy": 2, "Knowledge": 1},
        },
        "Bellwood Athlete": {
            "description": "A local sports star with raw physical talent.",
            "bonuses": {"Strength": 2, "Stamina": 1},
        },
        "Tinkerer": {
            "description": "You build devices from scrap and curiosity.",
            "bonuses": {"Tech": 1, "Knowledge": 2},
        },
        "Mystic Apprentice": {
            "description": "You studied hidden arts and learned calm focus.",
            "bonuses": {"Willpower": 2, "Empathy": 1},
        },
    }
    print("Choose your background:")
    choice = prompt_choice("", list(backgrounds.keys()))
    details = backgrounds[choice]
    print(wrap(details["description"]))
    print(f"Bonuses: {details['bonuses']}")
    return {"name": choice, **details}


def allocate_stats() -> dict:
    stats = {
        "Strength": 3,
        "Agility": 3,
        "Stamina": 3,
        "Tech": 3,
        "Willpower": 3,
        "Knowledge": 3,
        "Empathy": 3,
        "Tactics": 3,
    }
    pool = 12
    print(LINE)
    print("Allocate your core stats.")
    print(wrap(
        "Each stat starts at 3. You have 12 points to distribute. Max 8 per stat."
    ))
    print("Stats: Strength, Agility, Stamina, Tech, Willpower, Knowledge, Empathy, Tactics")
    while pool > 0:
        print(f"\nRemaining points: {pool}")
        for name, value in stats.items():
            print(f"  {name}: {value}")
        stat_name = prompt_choice("Pick a stat to increase", list(stats.keys()))
        max_add = min(8 - stats[stat_name], pool)
        if max_add == 0:
            print("That stat is already at max.")
            continue
        add = prompt_int(f"How many points to add to {stat_name}?", 1, max_add)
        stats[stat_name] += add
        pool -= add
    return stats


def choose_quirks() -> list[str]:
    quirks = [
        "Calm Under Pressure",
        "Hotheaded",
        "Protective",
        "Curious",
        "Strategist",
        "Reckless",
        "Tech Enthusiast",
        "Alien Culture Fan",
        "Lone Wolf",
        "Team Player",
        "Quiet Observer",
        "Bold Leader",
    ]
    chosen = []
    print(LINE)
    print("Pick two personality quirks (they shape story choices).")
    while len(chosen) < 2:
        remaining = [q for q in quirks if q not in chosen]
        pick = prompt_choice("Select a quirk", remaining)
        chosen.append(pick)
        print(f"Added: {pick}")
    return chosen


def choose_starting_gear() -> list[str]:
    gear_options = [
        "Plumber Badge (access to Plumber channels)",
        "Prototype Scanner (detects alien signals)",
        "Gwen's Spellbook Copy (basic wards)",
        "Kevin's Toolkit (repair & sabotage)",
        "Max's Road Atlas (safe houses)",
        "Custom Communicator (encrypted)",
    ]
    chosen = []
    print(LINE)
    print("Choose two starting gear items:")
    while len(chosen) < 2:
        remaining = [item for item in gear_options if item not in chosen]
        pick = prompt_choice("Select gear", remaining)
        chosen.append(pick)
        print(f"Added: {pick}")
    return chosen


def choose_omnitrix_mode() -> str:
    options = [
        "Proto-Omnitrix (unstable, high risk/high reward)",
        "Calibrated Omnitrix (balanced, reliable)",
        "Custom Codon Harness (experimental, tactical boosts)",
    ]
    print(LINE)
    print("Choose your Omnitrix variant:")
    return prompt_choice("", options)


def build_character() -> dict:
    print(LINE)
    name = input("Enter your hero name: ").strip() or "Nova"
    origin = prompt_choice("Choose your origin", ["Human", "Half-Alien", "Alien"])
    print(LINE)
    background = choose_background()
    stats = allocate_stats()
    for stat, bonus in background["bonuses"].items():
        stats[stat] = min(10, stats[stat] + bonus)
    quirks = choose_quirks()
    gear = choose_starting_gear()
    omnitrix = choose_omnitrix_mode()

    print(LINE)
    print("Optional: Assign a signature move.")
    signature_move = input("Name your signature move (or press Enter to skip): ").strip()

    profile = {
        "Name": name,
        "Origin": origin,
        "Background": background["name"],
        "Quirks": quirks,
        "Gear": gear,
        "Omnitrix": omnitrix,
        "Signature Move": signature_move or "None",
        "Stats": stats,
    }
    return profile


def show_profile(profile: dict) -> None:
    print(LINE)
    print("YOUR HERO PROFILE")
    print(LINE)
    for key in ["Name", "Origin", "Background", "Omnitrix", "Signature Move"]:
        print(f"{key}: {profile[key]}")
    print("Quirks:")
    for quirk in profile["Quirks"]:
        print(f"  - {quirk}")
    print("Gear:")
    for item in profile["Gear"]:
        print(f"  - {item}")
    print("Stats:")
    for stat, value in profile["Stats"].items():
        print(f"  {stat}: {value}")


def opening_scene(profile: dict) -> None:
    print(LINE)
    print(wrap(
        f"The Omnitrix hums as {profile['Name']} watches the skyline. "
        "A shadowy drone crashes through the clouds, broadcasting a message: "
        "'All available heroes report to the Rustbucket. This is not a drill.'"
    ))
    if prompt_yes_no("Will you answer the call?"):
        print(wrap(
            "You race toward the Rustbucket, your Omnitrix glowing. The journey begins."
        ))
    else:
        print(wrap(
            "You hesitate, but the Omnitrix vibrates with urgency. Destiny won't wait."
        ))
    print(LINE)
    print("To be continued...")


def main() -> None:
    intro()
    profile = build_character()
    show_profile(profile)
    opening_scene(profile)


if __name__ == "__main__":
    main()
