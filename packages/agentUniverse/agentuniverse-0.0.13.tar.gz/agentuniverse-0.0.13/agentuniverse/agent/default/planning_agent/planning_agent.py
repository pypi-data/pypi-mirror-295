# !/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Time    : 2024/3/15 11:40
# @Author  : heji
# @Email   : lc299034@antgroup.com
# @FileName: planning_agent.py
"""Planning agent module."""
from langchain.output_parsers.json import parse_json_markdown

from agentuniverse.agent.agent import Agent
from agentuniverse.agent.input_object import InputObject


class PlanningAgent(Agent):
    """Planning Agent class."""

    def input_keys(self) -> list[str]:
        """Return the input keys of the Agent."""
        return ['input']

    def output_keys(self) -> list[str]:
        """Return the output keys of the Agent."""
        return ['output']

    def parse_input(self, input_object: InputObject, agent_input: dict) -> dict:
        """Agent parameter parsing.

        Args:
            input_object (InputObject): input parameters passed by the user.
            agent_input (dict): agent input preparsed by the agent.
        Returns:
            dict: agent input parsed from `input_object` by the user.
        """
        agent_input['input'] = input_object.get_data('input')
        agent_input['expert_framework'] = input_object.get_data('expert_framework')
        self.agent_model.profile.setdefault('prompt_version', 'default_planning_agent.cn')
        return agent_input

    def parse_result(self, planner_result: dict) -> dict:
        """Planner result parser.

        Args:
            planner_result(dict): Planner result
        Returns:
            dict: Agent result object.
        """
        output = planner_result.get('output')
        output = parse_json_markdown(output)
        planner_result['framework'] = output['framework']
        planner_result['thought'] = output['thought']
        return planner_result
