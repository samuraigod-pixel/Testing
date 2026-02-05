#!/usr/bin/env python3
"""Text-based RPG set in the Ben 10 universe with detailed character creation."""

from __future__ import annotations

import textwrap


LINE = "-" * 72
VERSION = "1.0"


class GameUI:
    def __init__(self) -> None:
        self.width = 72

    def divider(self) -> None:
        print(LINE)

    def title(self, text: str) -> None:
        self.divider()
        print(text)
        self.divider()

    def section(self, text: str) -> None:
        print()
        print(text.upper())
        self.divider()

    def wrap(self, text: str) -> str:
        return "\n".join(textwrap.wrap(text, width=self.width))

    def pause(self) -> None:
        input("\nPress Enter to continue...")

    def menu(self, title: str, options: list[str]) -> str:
        self.section(title)
        return prompt_choice("", options)


UI = GameUI()


def wrap(text: str) -> str:
    return UI.wrap(text)


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
    UI.title(f"BEN 10: OMNITRIX CHRONICLES (Version {VERSION})")
    print(wrap(
        "A strange surge of energy hits Bellwood. The Omnitrix is unstable, and "
        "only a new hero can stabilize it. Build your character, step into the "
        "Ben 10 universe, and decide what kind of legend you'll become."
    ))
    UI.divider()


def choose_background() -> dict:
    backgrounds = {
        "Plumber Cadet": {
            "description": "Trained by the Plumbers, you know protocols and tech.",
            "bonuses": {"Tech": 2, "Tactics": 1},
            "subtypes": [
                "Field Operations",
                "Tech Response",
                "Recon Specialist",
            ],
        },
        "Road Trip Survivor": {
            "description": "You grew up on the road and learned to improvise.",
            "bonuses": {"Agility": 1, "Willpower": 2},
            "subtypes": [
                "Rustbucket Mechanic",
                "Campfire Storyteller",
                "Emergency Navigator",
            ],
        },
        "Alien Exchange Student": {
            "description": "You came to Earth to study humanity and its quirks.",
            "bonuses": {"Empathy": 2, "Knowledge": 1},
            "subtypes": [
                "Cultural Ambassador",
                "Linguistics Adept",
                "Curiosity Seeker",
            ],
        },
        "Bellwood Athlete": {
            "description": "A local sports star with raw physical talent.",
            "bonuses": {"Strength": 2, "Stamina": 1},
            "subtypes": [
                "Track Star",
                "Combat Sports",
                "Team Captain",
            ],
        },
        "Tinkerer": {
            "description": "You build devices from scrap and curiosity.",
            "bonuses": {"Tech": 1, "Knowledge": 2},
            "subtypes": [
                "Gadgeteer",
                "Salvage Engineer",
                "Prototype Tester",
            ],
        },
        "Mystic Apprentice": {
            "description": "You studied hidden arts and learned calm focus.",
            "bonuses": {"Willpower": 2, "Empathy": 1},
            "subtypes": [
                "Ward Keeper",
                "Runes Scholar",
                "Astral Seeker",
            ],
        },
    }
    UI.section("Choose your background")
    choice = prompt_choice("", list(backgrounds.keys()))
    details = backgrounds[choice]
    print(wrap(details["description"]))
    print(f"Bonuses: {details['bonuses']}")
    subtype = prompt_choice("Select a background specialty", details["subtypes"])
    return {"name": choice, "subtype": subtype, **details}

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
    UI.section("Choose your origin")
    choice = prompt_choice("", list(origins.keys()))
    details = origins[choice]
    print(wrap(details["description"]))
    print(f"Bonus: {details['bonuses']} | Feature: {details['feature']}")
    if choice == "Alien":
        subspecies = prompt_choice(
            "Select your alien lineage",
            ["Galvan", "Tetramand", "Pyronite", "Kineceleran", "Petrosapien"],
        )
    elif choice == "Half-Alien":
        subspecies = prompt_choice(
            "Select your mixed heritage",
            ["Anodite", "Osmosian", "Lenopan", "Vulpimancer", "Loboan"],
        )
    else:
        subspecies = prompt_choice(
            "Select your human upbringing",
            ["Bellwood Local", "Rural Traveler", "City Techie", "Coastal Nomad"],
        )
    return {"name": choice, "subspecies": subspecies, **details}


def choose_stat_profile() -> dict:
    profiles = {
        "Rookie (base 2, pool 10, cap 7)": {"base": 2, "pool": 10, "cap": 7},
        "Standard (base 3, pool 12, cap 8)": {"base": 3, "pool": 12, "cap": 8},
        "Heroic (base 4, pool 14, cap 9)": {"base": 4, "pool": 14, "cap": 9},
        "Custom": {"base": 3, "pool": 12, "cap": 8},
    }
    UI.section("Choose your stat allocation profile")
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
    UI.section("Pick two personality quirks (they shape story choices)")
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
    UI.section("Choose two focus skills to define your specialties")
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
    UI.section("Choose two starting gear items")
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
    UI.section("Select three starting aliens for your Omnitrix playlist")
    while len(chosen) < 3:
        remaining = [name for name in aliens.keys() if name not in chosen]
        pick = prompt_choice("Choose an alien", remaining)
        chosen.append(pick)
        print(wrap(f"{pick}: {aliens[pick]}"))
    return chosen


def choose_goal() -> str:
    goals = [
        "Stabilize the Omnitrix",
        "Find a missing Plumber",
        "Protect Bellwood",
        "Redeem a former rival",
        "Recover lost alien tech",
        "Prove yourself to the Plumbers",
    ]
    UI.section("Choose your personal goal")
    return prompt_choice("", goals)


def choose_flaw() -> str:
    flaws = [
        "Overconfident",
        "Impulsive",
        "Distrustful",
        "Stubborn",
        "Easily Distracted",
        "Too Protective",
    ]
    UI.section("Choose one core flaw (for drama)")
    return prompt_choice("", flaws)


def choose_ally() -> str:
    allies = [
        "Plumber Handler",
        "Classmate Sidekick",
        "Alien Pen Pal",
        "Underground Fixer",
        "Family Mentor",
        "Rival Turned Friend",
    ]
    UI.section("Choose a key ally")
    return prompt_choice("", allies)


def apply_blake_walker_cheats(profile: dict) -> dict:
    if profile["Name"].lower() != "blake walker":
        return profile
    UI.section("Blake Walker cheat options unlocked")
    cheat_options = [
        "Max out all stats to 10",
        "Gain all focus skills",
        "Gain all starting gear",
        "Unlock every starting alien",
        "Double your background and origin bonuses",
        "Add a legendary Omnitrix perk",
    ]
    chosen = []
    while True:
        print("Select cheat options (choose as many as you want).")
        remaining = [option for option in cheat_options if option not in chosen]
        remaining.append("Finish cheat selection")
        pick = prompt_choice("", remaining)
        if pick == "Finish cheat selection":
            break
        chosen.append(pick)
        print(f"Added: {pick}")

    if "Max out all stats to 10" in chosen:
        for stat in profile["Stats"]:
            profile["Stats"][stat] = 10
    if "Gain all focus skills" in chosen:
        profile["Focuses"] = [
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
    if "Gain all starting gear" in chosen:
        profile["Gear"] = [
            "Plumber Badge (access to Plumber channels)",
            "Prototype Scanner (detects alien signals)",
            "Gwen's Spellbook Copy (basic wards)",
            "Kevin's Toolkit (repair & sabotage)",
            "Max's Road Atlas (safe houses)",
            "Custom Communicator (encrypted)",
        ]
    if "Unlock every starting alien" in chosen:
        profile["Aliens"] = [
            "Heatblast",
            "Four Arms",
            "XLR8",
            "Diamondhead",
            "Grey Matter",
            "Cannonbolt",
            "Wildvine",
            "Upgrade",
            "Ripjaws",
            "Ghostfreak",
        ]
    if "Double your background and origin bonuses" in chosen:
        combined = {}
        for source in (profile["Background Bonuses"], profile["Origin Bonuses"]):
            for stat, bonus in source.items():
                combined[stat] = combined.get(stat, 0) + bonus
        for stat, bonus in combined.items():
            profile["Stats"][stat] = min(10, profile["Stats"][stat] + bonus)
    if "Add a legendary Omnitrix perk" in chosen:
        profile["Omnitrix Perk"] = "Legendary Sync: once per chapter, evolve an alien."
    profile["Cheats Enabled"] = chosen
    return profile


def choose_omnitrix_mode() -> str:
    options = [
        "Proto-Omnitrix (unstable, high risk/high reward)",
        "Calibrated Omnitrix (balanced, reliable)",
        "Custom Codon Harness (experimental, tactical boosts)",
    ]
    UI.section("Choose your Omnitrix variant")
    return prompt_choice("", options)


def build_player_profile(profile: dict) -> dict:
    derived = {
        "Health": 20 + profile["Stats"]["Stamina"] * 2,
        "Energy": 10 + profile["Stats"]["Willpower"],
        "Resolve": 5 + profile["Stats"]["Empathy"],
        "Credits": 50 + profile["Stats"]["Tactics"] * 5,
    }
    profile["Resources"] = derived
    profile["Experience"] = 0
    profile["Level"] = 1
    return profile


def build_skill_list(profile: dict) -> dict:
    stats = profile["Stats"]
    skills = {
        "Brawl": stats["Strength"] + profile["Level"],
        "Athletics": stats["Agility"] + profile["Level"],
        "Endurance": stats["Stamina"] + profile["Level"],
        "Engineering": stats["Tech"] + profile["Level"],
        "Focus": stats["Willpower"] + profile["Level"],
        "Research": stats["Knowledge"] + profile["Level"],
        "Empathy": stats["Empathy"] + profile["Level"],
        "Tactics": stats["Tactics"] + profile["Level"],
    }
    profile["Skills"] = skills
    return profile


def build_abilities(profile: dict) -> dict:
    origin = profile["Origin"]["name"]
    base_abilities = {
        "Human": ["Adaptive Push (reroll a check)"],
        "Half-Alien": ["Hybrid Instinct (ignore fatigue once)"],
        "Alien": ["Outworlder Insight (alien tech advantage)"],
    }
    omnitrix_boon = {
        "Proto-Omnitrix (unstable, high risk/high reward)": "Overclock Shift",
        "Calibrated Omnitrix (balanced, reliable)": "Stabilized Shift",
        "Custom Codon Harness (experimental, tactical boosts)": "Tactical Shift",
    }
    abilities = list(base_abilities.get(origin, []))
    abilities.append(omnitrix_boon.get(profile["Omnitrix"], "Omnitrix Shift"))
    profile["Abilities"] = abilities
    return profile


def build_world() -> dict:
    return {
        "Bellwood": {
            "desc": "Home streets, familiar faces, and hidden threats.",
            "connections": ["Rustbucket", "Plumber HQ", "Downtown", "Lake Park"],
        },
        "Rustbucket": {
            "desc": "Max's RV and the team's mobile base.",
            "connections": ["Bellwood", "Plumber HQ"],
        },
        "Plumber HQ": {
            "desc": "Secure hub for Plumber operations and intel.",
            "connections": ["Rustbucket", "Bellwood", "Null Void Gate"],
        },
        "Downtown": {
            "desc": "Crowded city center with tech shops and chaos.",
            "connections": ["Bellwood", "Lake Park"],
        },
        "Lake Park": {
            "desc": "Quiet trails hiding strange energy readings.",
            "connections": ["Bellwood", "Downtown"],
        },
        "Null Void Gate": {
            "desc": "A volatile portal to the Null Void.",
            "connections": ["Plumber HQ"],
        },
    }


def random_event_table() -> list[dict]:
    return [
        {
            "name": "Drone Ambush",
            "summary": "A rogue drone attacks, forcing a quick response.",
            "effect": lambda state: state["Resources"].__setitem__(
                "Energy", max(0, state["Resources"]["Energy"] - 2)
            ),
        },
        {
            "name": "Plumber Tip",
            "summary": "A tip gives you a tactical advantage.",
            "effect": lambda state: state["Resources"].__setitem__(
                "Resolve", state["Resources"]["Resolve"] + 1
            ),
        },
        {
            "name": "Omnitrix Glitch",
            "summary": "The Omnitrix flickers, draining energy.",
            "effect": lambda state: state["Resources"].__setitem__(
                "Energy", max(0, state["Resources"]["Energy"] - 3)
            ),
        },
        {
            "name": "Civilian Rescue",
            "summary": "You help civilians, earning goodwill.",
            "effect": lambda state: state["Resources"].__setitem__(
                "Credits", state["Resources"]["Credits"] + 10
            ),
        },
        {
            "name": "Alien Artifact",
            "summary": "You find a strange artifact buzzing with power.",
            "effect": lambda state: state["Resources"].__setitem__(
                "Energy", state["Resources"]["Energy"] + 1
            ),
        },
    ]


def roll_event_index(seed: int, size: int) -> int:
    return seed % size


def resolve_random_event(state: dict, location: str) -> None:
    events = random_event_table()
    seed = state["Experience"] + state["Resources"]["Energy"] + len(location)
    event = events[roll_event_index(seed, len(events))]
    UI.section(f"Random Event: {event['name']}")
    print(wrap(event["summary"]))
    event["effect"](state)
    print("Event resolved.")


def show_player_profile(profile: dict) -> None:
    UI.section("Player Profile")
    print(f"Level: {profile['Level']} | XP: {profile['Experience']}")
    for name, value in profile["Resources"].items():
        print(f"{name}: {value}")
    print("Abilities:")
    for ability in profile["Abilities"]:
        print(f"  - {ability}")
    print("Skills:")
    for skill, value in profile["Skills"].items():
        print(f"  {skill}: {value}")


def show_location(world: dict, current: str) -> None:
    UI.section(f"Location: {current}")
    print(wrap(world[current]["desc"]))
    print("Connections:")
    for idx, dest in enumerate(world[current]["connections"], start=1):
        print(f"  {idx}. {dest}")


def choose_location(world: dict, current: str) -> str:
    options = world[current]["connections"]
    return prompt_choice("Travel to:", options)


def choose_training(profile: dict) -> None:
    training = [
        ("Sparring", "Brawl"),
        ("Obstacle Course", "Athletics"),
        ("Tech Lab", "Engineering"),
        ("Meditation", "Focus"),
        ("Research Session", "Research"),
        ("Tactical Briefing", "Tactics"),
    ]
    UI.section("Training")
    options = [name for name, _ in training]
    choice = prompt_choice("Choose training", options)
    for name, skill in training:
        if name == choice:
            profile["Skills"][skill] += 1
            profile["Experience"] += 5
            print(f"{skill} increases to {profile['Skills'][skill]}.")
            print("You gain 5 XP.")
            break


def rest(profile: dict) -> None:
    UI.section("Rest")
    profile["Resources"]["Energy"] = min(
        15, profile["Resources"]["Energy"] + 3
    )
    profile["Resources"]["Resolve"] = min(
        10, profile["Resources"]["Resolve"] + 2
    )
    print("You take a breather and recover energy.")


def apply_level_up(profile: dict) -> None:
    while profile["Experience"] >= 20 * profile["Level"]:
        profile["Experience"] -= 20 * profile["Level"]
        profile["Level"] += 1
        profile["Resources"]["Health"] += 4
        profile["Resources"]["Energy"] += 1
        for skill in profile["Skills"]:
            profile["Skills"][skill] += 1
        print(f"Level up! You reached level {profile['Level']}.")


def play_game(profile: dict) -> None:
    world = build_world()
    current_location = "Bellwood"
    turn = 1
    while True:
        UI.title(f"Turn {turn}: {current_location}")
        show_location(world, current_location)
        show_player_profile(profile)
        action = UI.menu(
            "Choose an action",
            ["Travel", "Investigate (random event)", "Train", "Rest", "End Adventure"],
        )
        if action == "Travel":
            current_location = choose_location(world, current_location)
        elif action == "Investigate (random event)":
            resolve_random_event(profile, current_location)
            profile["Experience"] += 3
        elif action == "Train":
            choose_training(profile)
        elif action == "Rest":
            rest(profile)
        else:
            UI.section("Adventure Ended")
            print("Thanks for playing!")
            break
        apply_level_up(profile)
        turn += 1


def build_character() -> dict:
    print(LINE)
    name = input("Enter your hero name: ").strip() or "Nova"
    origin = choose_origin()
    print(LINE)
    background = choose_background()
    stats = allocate_stats()
    combined_bonuses = {}
    for source in (background["bonuses"], origin["bonuses"]):
        for stat, bonus in source.items():
            combined_bonuses[stat] = combined_bonuses.get(stat, 0) + bonus
    for stat, bonus in combined_bonuses.items():
        stats[stat] = min(10, stats[stat] + bonus)
    quirks = choose_quirks()
    focuses = choose_focuses()
    gear = choose_starting_gear()
    aliens = choose_alien_roster()
    omnitrix = choose_omnitrix_mode()
    goal = choose_goal()
    flaw = choose_flaw()
    ally = choose_ally()

    print(LINE)
    print("Optional: Assign a signature move.")
    signature_move = input("Name your signature move (or press Enter to skip): ").strip()

    profile = {
        "Name": name,
        "Origin": origin,
        "Origin Bonuses": origin["bonuses"],
        "Background": background["name"],
        "Background Specialty": background["subtype"],
        "Background Bonuses": background["bonuses"],
        "Quirks": quirks,
        "Focuses": focuses,
        "Gear": gear,
        "Aliens": aliens,
        "Omnitrix": omnitrix,
        "Signature Move": signature_move or "None",
        "Goal": goal,
        "Flaw": flaw,
        "Ally": ally,
        "Stats": stats,
    }
    profile = apply_blake_walker_cheats(profile)
    profile = build_player_profile(profile)
    profile = build_skill_list(profile)
    profile = build_abilities(profile)
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
    print(f"Origin Lineage: {profile['Origin']['subspecies']}")
    print(f"Origin Feature: {profile['Origin']['feature']}")
    print(f"Background Specialty: {profile['Background Specialty']}")
    print(f"Goal: {profile['Goal']}")
    print(f"Flaw: {profile['Flaw']}")
    print(f"Key Ally: {profile['Ally']}")
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
    if "Omnitrix Perk" in profile:
        print(f"Omnitrix Perk: {profile['Omnitrix Perk']}")
    if "Cheats Enabled" in profile:
        print("Cheats Enabled:")
        for cheat in profile["Cheats Enabled"]:
            print(f"  - {cheat}")
    show_player_profile(profile)


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
    if prompt_yes_no("Start the adventure now?"):
        play_game(profile)


if __name__ == "__main__":
    main()
