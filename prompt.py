
class StarCraftII_HEP:
    def __init__(self, race, K, action_dict):
        self.race = race.lower()
        self.race_specific_prompt = {
            "protoss": "For Protoss, keep an eye on Nexus's energy to Chrono Boost important structures.",
        }
        self.race_tactics_prompt = {
            "protoss": """
            1. Zealot & STALKER tactic:
                -Key buildings: 
                    military: GATEWAY/WARPGATE (6+).
                    technolegy: CYBERNETICSCORE(1 and only 1), TWILIGHTCOUNCIL(1 and only 1, CYBERNETICSCORE needed), FORGE(1 and only 1).
                -Key technologies: 
                    Necessary: WARPGATERESEARCH(CYBERNETICSCORE needed), CHARGE(TWILIGHTCOUNCIL needed).
                    Optimal: PROTOSSGROUNDWEAPONSLEEVEL(1,2, FORGE needed), PROTOSSGROUNDARMORSLEVEL(1,2, FORGE needed), PROTOSSSHIELDSLEEVEL(1,2, FORGE needed).
                -Key forces: ZEALOT: STALKER=1:1 or 2:1, as many as possible.
                -Key timing: 
                    At 2 minutes: Complete the construction of the second NEXUS and 2 GATEWAY.
                    At 4 minutes: 3+ WARPGATE, 1 CYBERNETICSCORE built and WARPGATERESEARCH research started.
                    At 8 minutes: 6+ WARPGATE, 1 CYBERNETICSCORE, 1 TWILIGHTCOUNCIL(CYBERNETICSCORE needed) built and all necessary key technology research completed.
                -Applicable situation: 
                    Only in the first 8 minutes of the game.
            2. Carrier tactic:
                -Key buildings: 
                    military: STARGATE(6, CYBERNETICSCORE needed)
                    technolegy: CYBERNETICSCORE(1 and only 1), FLEETBEACON(1 and only 1, STARGATE and CYBERNETICSCORE needed), FORGE(1 and only 1).
                -Key technologies: 
                    Necessary:  WARPGATERESEARCH(CYBERNETICSCORE needed), PROTOSSAIRWEAPONSLEEVEL(1,2, CYBERNETICSCORE needed).
                    Optimal: PROTOSSAIRMARMORSLEEVEL(1,2, CYBERNETICSCORE needed), PROTOSSSHIELDSLEEVEL(1,2, FORGE needed), PROTOSSGROUNDARMORSLEVEL(1,2, FORGE needed).
                -Key forces: 
                    First 6 minutes, ZEALOT: STALKER=1:1, as many as possible, with little CARRIER.
                    After 6 minutes, Mainly CARRIER(STARGATE and FLEETBEACON need), with a small amount of STALKER or ZEALOT.
                -Key timing: 
                    At 2 minutes: Complete the construction of the second NEXUS and 2 GATEWAY.
                    At 6 minutes: 2 STARGATE, 1 CYBERNETICSCORE, 1 FLEETBEACON, at least 1 CARRIER in trainning.
                    At 10 minutes: 6 STARGATE, 1 CYBERNETICSCORE, 1 FLEETBEACON, 6+ CARRIER and necessary technology research completed.
                -Applicable situation: 
                    Usually after 6 minutes of the game, or enemies have air units / heavy units.
            """,
        }

        self.system_prompt = f"""
        You are an AI trained in analyzing and summarizing StarCraft II games. You understand the nuances and strategies of the {self.race} race. 
        Based on the summaries of a game, we want you to analyze the game progression in a structured way.

        1. Choose Tactic
        First, here are some tactics, you should choose one as <current tactic>:
        {self.race_tactics_prompt.get(self.race)}
        Choose one as <current tactic> based on the game time and intelligence gathered through reconnaissance.

        2. Priority Construction Analysis:
        This part is temporarily locked, to protect our results until paper be published.

        3. Conventional Construction Planning:
        This part is temporarily locked, to protect our results until paper be published.

        Decisions:
        if there is <priority> in 'Priority Construction Analysis', set 1 decision as <priority>, 1 <TRAIN PROBE> and other actions must be <EMPTY ACTION>. For example, if <priority> is BUILD NEXUS:
            <BUILD NEXUS>
            <TRAIN PROBE>
            <EMPTY ACTION>
            <EMPTY ACTION>
            <EMPTY ACTION>
        otherwise, set decisions according to 'Conventional Construction Planning', set 1 Technology item, 1~2 Economic item, 2 Military items, 1 Other item. For example, if there is no <priority>:
            <BUILD CYBERNETICSCORE> (Technology item)
            <TRAIN PROBE> (Economic item)
            <TRAIN ZEALOT> (Military item)
            <TRAIN STALKER> (Military item)
            <SCOUTING PROBE> (Other item, Scouting, Chronoboost, or Attack)
        When you have technology building and some gas storage, you should add technology study that have not been started. For example, if there is no <priority>:
            <RESEARCH PROTOSSAIRWEAPONSLEVEL1> (Technology item, or research any required but not studied technology)
            <TRAIN PROBE> (Economic item)
            <BUILD PYLON> (Economic item)
            <TRAIN ZEALOT> (Military item)
            <TRAIN STALKER> (Military item)
       If you have a lot supply left and lot resources, you can set more Military items and stop use CHRONOBOOST. For example, if there is no <priority>:
            <BUILD FLEETBEACON> (Technology item, or research any required but not studied technology)
            <TRAIN PROBE> (Economic item)
            <BUILD STARGATE> (Military item)
            <TRAIN CARRIER> (Military item)
            <TRAIN ZEALOT> (Military item)

        Lastly, consider the current situation and the analyses above, make {K} actionable and specific decisions from the action dictionary{action_dict}. This dictionary comprises four categories of actions: unit production, building construction, technology research, and other actions. Remember to align these decisions with the current stage of the game and <current tactic>, and avoid proposing actions that are not currently feasible.

        Give your analysis and decision, do not ask for other data:
        """

    def generate_prompts(self):
        if self.race == 'protoss':
            self.example_input_prompt = r"chunk0:At 01:59 game time, our current StarCraft II situation is as follows:\n\nResources:\n- Game time: 01:59\n- Worker supply: 21\n- Mineral: 215\n- Gas: 100\n- Supply left: 10\n- Supply cap: 31\n- Supply used: 21\n\nBuildings:\n- Nexus count: 1\n- Pylon count: 2\n- Gas buildings count: 1\n- Gateway count: 1\n\nUnits:\n- Probe count: 21\n\nPlanning:\n\nPlanning structure:\n- Planning gateway count: 1\n\nEnemy:\n\nUnit:\n- Enemy unittypeid.drone: 1\n\n"
            self.example_output_prompt = """
Based on the provided information, Here's a summary of the situation:

This part is temporarily locked, to protect our results until paper be published.
"""
        else:
            raise NotImplementedError
        return self.system_prompt, self.example_input_prompt, self.example_output_prompt
