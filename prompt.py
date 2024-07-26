
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
        Based on the game situation and <current tactic>, determine if there are any priorities in infrastructure construction:
            2.1 When we have 'more than 16' workers, we need 2 nexus. If we have less than 2 nexus, set BUILD NEXUS as <priority>.
                When we have 'more than 32' workers, we need 3 nexus. If we have less than 3 nexus, set BUILD NEXUS as <priority>.
                When we have 'more than 48' workers, we need 4 nexus. If we have less than 4 nexus, set BUILD NEXUS as <priority>.
                When we have 'more than 64' workers, we need 5 nexus. If we have less than 5 nexus, set BUILD NEXUS as <priority>.
                When we have 'more than 72' workers, we need 6 nexus. If we have less than 6 nexus, set BUILD NEXUS as <priority>.
                When we have 'more than 80' workers, we need 7 nexus. If we have less than 7 nexus, set BUILD NEXUS as <priority>.
            2.2 Before we have 25 workers, we do not need gas building, do not build any ASSIMILATOR!
                When we have 'more than 25' workers, we need 1 gas building. If we have less than 1 gas building, set BUILD ASSIMILATOR as <priority>.
                When we have 'more than 40' workers, we need 3 gas building. If we have less than 3 gas building, set BUILD ASSIMILATOR as <priority>.
                When we have 'more than 60' workers, we need 7 gas building. If we have less than 7 gas building, set BUILD ASSIMILATOR as <priority>.
                When we have 'more than 75' workers, we need 10 gas building. If we have less than 10 gas building, set BUILD ASSIMILATOR as <priority>.
        You should first extract relevant data from input information and then analyze all the two items, make sure whether they are <priority>.
        If there is no priority according to 2.1, 2.2, set <priority> as NONE.

        3. Conventional Construction Planning:
        Based on the game situation and <current tactic>, make plans for economic, technology and military development:
            3.1 Technology: Make sure what technolegy building need to be build (if the technolegy building is not exist or not planned) and make sure what technolegy mentioned in <current tactic> need to be upgraded (if the technolegy research is not completed or not started).
            3.2 Economic: Always TRAIN PROBE if 'worker supply' is less than 80. If 'supply left' is less than 4 and there is no PYLON planned, build PYLON.
            3.3 Military: Build military building (if the build not enough according to <current tactic> and situation, but don't build too many), train military unit according to <current tactic> and situation.
            3.4 Scouting: If we have too many probes, dispatch SCOUTING PROBE.
            3.5 Chronoboost: If CARRIER is trainning, CHRONOBOOST STARGATE. CHRONOBOOST one of [CYBERNETICSCORE, TWILIGHTCOUNCIL, FORGE] if technology is researching there. Otherwise we can try CHRONOBOOST NEXUS.
            3.6 Attack: If army supply less than 110 or supply used less than 190, do not raise any attack! Otherwise Attack immediately.

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

1. Choose Tactic
Based on the current game time 01:59, it is within 8 minutes, we should choose Zealot & STALKER tactic. 
<current tactic> = Zealot & STALKER tactic

2. Priority Construction Analysis:
Here are the relative data and analysis for 2.1, 2.2:
2.1 At 01:59 game time, Worker supply: 21, Nexus count: 1, Planning nexus count: 0. 
    According to Current situation, we have more than 15 but less than 35 workers, so we need 2 nexus. While we have 1 nexus, so BUILD NEXUS is <priority>.
2.2 At 01:59 game time, Worker supply: 21, Gas buildings count: 1, Planning gas buildings count: 0
    According to Current situation, we have less than 25 workers, so we do not need gas building. We already have 1 gas building, so BUILD ASSIMILATOR is not <priority>.
<priority> = BUILD NEXUS

3. Conventional Construction Planning:
Here are the analysis for 3.1, 3.2 3.3, 3.4 and 3.5:
3.1 Technology: At 01:59 game time, Technology buildings that have been built: None. Key technologies that start studied or completely studied: None.
    According to <current tactic>, we can consider research WARPGATERESEARCH or build technolegy like CYBERNETICSCORE.
3.2 Economic: At 01:59 game time, Worker supply: 21, Supply left: 11
    Our worker supply is less than 80, we should TRAIN PROBE. Our 'supply left' is more than 4, we do not need more PYLON.
3.3 Military: At 01:59 game time, Gateway count: 1, Warp gate count: 0, Stargate count: 0, Roboticsfacility count: 0
    According to 'key building, military' part of <current tactic>, we need 2 GATEWAY at 2 minutes, we have 1 GATEWAY built and 1 GATEWAY under construction, we need to build 1 more GATEWAY. We should train ZEALOT and STALKER to enhance military strength. 
3.4 Scouting: We have too many probes so that we can try SCOUTING PROBE.
3.5 Chronoboost: Consider that no CARRIER is trainning nor any research is upgrading, we can try CHRONOBOOST NEXUS.
3.6 Attack: At 01:59 game time, Army supply: 0, Supply used: 21
    Army supply 0 is less than 110 and supply used 21 is less than 190, do not raise any attack!

Decisions:
Consider that <priority> = BUILD NEXUS, we set 1 decision as <priority>, 1 <TRAIN PROBE> and other actions as <EMPTY ACTION>.
0: <BUILD NEXUS>
1: <TRAIN PROBE>
2: <EMPTY ACTION>
3: <EMPTY ACTION>
4: <EMPTY ACTION>
"""
        else:
            raise NotImplementedError
        return self.system_prompt, self.example_input_prompt, self.example_output_prompt
