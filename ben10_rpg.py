#!/usr/bin/env python3
"""Text-based RPG set in the Ben 10 universe with detailed character creation."""

from __future__ import annotations

import textwrap


LINE = "-" * 72
VERSION = "1.0"


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
    print(f"BEN 10: OMNITRIX CHRONICLES (Version {VERSION})")
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

def choose_origin() -> dict:
    origins = {
        "Human": {
            "description": "Earth-born with a knack for adapting to chaos.",
            "bonuses": {"Willpower": 1, "Tactics": 1},
            "feature": "Adaptive: reroll one failed check per session.",
        },
        "Half-Alien": {
            "description": "Mixed heritage grants unusual resilience and insight.",
            "bonuses": {"Stamina": 1, "Empathy": 1},
            "feature": "Hybrid Instinct: resistance to fatigue effects.",
        },
        "Alien": {
            "description": "A visitor to Earth with unique biology and perspective.",
            "bonuses": {"Knowledge": 1, "Tech": 1},
            "feature": "Outworlder: gain advantage on alien-tech checks.",
        },
    }
    print("Choose your origin:")
    choice = prompt_choice("", list(origins.keys()))
    details = origins[choice]
    print(wrap(details["description"]))
    print(f"Bonus: {details['bonuses']} | Feature: {details['feature']}")
    return {"name": choice, **details}


def choose_stat_profile() -> dict:
    profiles = {
        "Rookie (base 2, pool 10, cap 7)": {"base": 2, "pool": 10, "cap": 7},
        "Standard (base 3, pool 12, cap 8)": {"base": 3, "pool": 12, "cap": 8},
        "Heroic (base 4, pool 14, cap 9)": {"base": 4, "pool": 14, "cap": 9},
        "Custom": {"base": 3, "pool": 12, "cap": 8},
    }
    print(LINE)
    print("Choose your stat allocation profile.")
    choice = prompt_choice("", list(profiles.keys()))
    if choice != "Custom":
        return profiles[choice]
    base = prompt_int("Custom base value per stat", 1, 5)
    pool = prompt_int("Custom points to distribute", 4, 20)
    cap = prompt_int("Custom per-stat cap", max(base + 2, 5), 10)
    return {"base": base, "pool": pool, "cap": cap}


def allocate_stats() -> dict:
    profile = choose_stat_profile()
    stats = {
        "Strength": profile["base"],
        "Agility": profile["base"],
        "Stamina": profile["base"],
        "Tech": profile["base"],
        "Willpower": profile["base"],
        "Knowledge": profile["base"],
        "Empathy": profile["base"],
        "Tactics": profile["base"],
    }
    pool = profile["pool"]
    cap = profile["cap"]
    print(LINE)
    print("Allocate your core stats.")
    print(wrap(
        f"Each stat starts at {profile['base']}. You have {pool} points to "
        f"distribute. Max {cap} per stat."
    ))
    print("Stats: Strength, Agility, Stamina, Tech, Willpower, Knowledge, Empathy, Tactics")
    while pool > 0:
        print(f"\nRemaining points: {pool}")
        for name, value in stats.items():
            print(f"  {name}: {value}")
        stat_name = prompt_choice("Pick a stat to increase", list(stats.keys()))
        max_add = min(cap - stats[stat_name], pool)
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


def choose_focuses() -> list[str]:
    focuses = [
        "Leadership",
        "Engineering",
        "Survival",
        "Investigation",
        "Diplomacy",
        "Stealth",
        "Athletics",
        "First Aid",
        "Alien Lore",
        "Driving",
    ]
    chosen = []
    print(LINE)
    print("Choose two focus skills to define your specialties.")
    while len(chosen) < 2:
        remaining = [focus for focus in focuses if focus not in chosen]
        pick = prompt_choice("Select a focus", remaining)
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


def choose_alien_roster() -> list[str]:
    aliens = {
        "Heatblast": "Pyrokinetic alien with ranged fire control.",
        "Four Arms": "Heavy-hitter with immense strength and grappling power.",
        "XLR8": "Super-speed scout with rapid strikes.",
        "Diamondhead": "Crystal armor and projectile control.",
        "Grey Matter": "Genius-level intellect and small size.",
        "Cannonbolt": "Rolling tank form with impact damage.",
        "Wildvine": "Plant-based control with entangling vines.",
        "Upgrade": "Tech-merging alien that enhances devices.",
        "Ripjaws": "Aquatic predator with underwater dominance.",
        "Ghostfreak": "Phasing stealth alien with eerie mobility.",
    }
    chosen = []
    print(LINE)
    print("Select three starting aliens for your Omnitrix playlist.")
    while len(chosen) < 3:
        remaining = [name for name in aliens.keys() if name not in chosen]
        pick = prompt_choice("Choose an alien", remaining)
        chosen.append(pick)
        print(wrap(f"{pick}: {aliens[pick]}"))
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
    origin = choose_origin()
    print(LINE)
    background = choose_background()
    stats = allocate_stats()
    for stat, bonus in {**background["bonuses"], **origin["bonuses"]}.items():
        stats[stat] = min(10, stats[stat] + bonus)
    quirks = choose_quirks()
    focuses = choose_focuses()
    gear = choose_starting_gear()
    aliens = choose_alien_roster()
    omnitrix = choose_omnitrix_mode()

    print(LINE)
    print("Optional: Assign a signature move.")
    signature_move = input("Name your signature move (or press Enter to skip): ").strip()

    profile = {
        "Name": name,
        "Origin": origin,
        "Background": background["name"],
        "Quirks": quirks,
        "Focuses": focuses,
        "Gear": gear,
        "Aliens": aliens,
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
        value = profile[key]
        if isinstance(value, dict):
            value = value["name"]
        print(f"{key}: {value}")
    print(f"Origin Feature: {profile['Origin']['feature']}")
    print("Quirks:")
    for quirk in profile["Quirks"]:
        print(f"  - {quirk}")
    print("Gear:")
    for item in profile["Gear"]:
        print(f"  - {item}")
    print("Focus Skills:")
    for focus in profile["Focuses"]:
        print(f"  - {focus}")
    print("Starting Aliens:")
    for alien in profile["Aliens"]:
        print(f"  - {alien}")
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
