import re
import json
import os
import requests
import murnitur
from concurrent.futures import ThreadPoolExecutor
from typing import TypedDict, Optional, List, Literal, Union, Any, Callable, Dict, Tuple
from murnitur.guard.bias_detection import BiasDetector
from murnitur.guard.hallucination_detection import HallucinationDetector
from murnitur.guard.prompt_injection import PromptInjectionDetector
from murnitur.guard.toxicity_detection import ToxicityDetector
from murnitur.main import GuardConfig, TracedSpan
from .lib import (
    check_pii,
    detect_tone,
    detect_injection,
    detect_toxicity,
    detect_bias,
    detect_hallucination,
    pii_patterns,
    detect,
)

Value = Union[str, int, List[str]]

default_config: GuardConfig = {
    "murnitur_key": None,
    "provider": "openai",
    "model": "gpt-4o-mini",
    "group": None,
    "api_key": None,
    "base_url": None,
    "headers": {},
}


class Payload(TypedDict):
    input: Optional[str]
    output: Optional[str]
    contexts: Optional[list[str]]


CustomMetricFunction = Callable[[Payload], Tuple[bool, Optional[str]]]

# A registry to hold custom metric functions
custom_metric_registry: Dict[str, CustomMetricFunction] = {}


class Rule(TypedDict):
    metric: Literal[
        "pii",
        "input_pii",
        "toxicity",
        "input_tone",
        "tone",
        "bias",
        "prompt_injection",
        "ctx_adherence",
        "custom",
    ]
    operator: Optional[
        Literal[
            "equal",
            "not_equal",
            "contains",
            "greater_than",
            "less_than",
            "greater_than_equal",
            "less_than_equal",
            "any",
            "all",
        ]
    ]
    value: Value


class Action(TypedDict):
    type: Literal["OVERRIDE", "FLAG"]
    fallback: str


class RuleSet(TypedDict):
    rules: List[Rule]
    action: Action


class Response:
    def __init__(
        self,
        text: str,
        triggered: bool,
        rule: Optional[Rule] = None,
        verdict: Optional[Any] = None,
    ) -> None:
        self.text = text
        self.triggered = triggered
        self.rule = rule
        self.verdict = verdict


class Guard:
    executor = ThreadPoolExecutor(max_workers=5)

    @staticmethod
    def register_custom_metric(name: str, func: CustomMetricFunction):
        """
        Registers a custom metric function.

        Args:
            name (str): The name of the custom metric.
            func (Callable[[dict, Optional[dict]], bool]): The function to evaluate the custom metric.
        """
        custom_metric_registry[name] = func

    @staticmethod
    def send_interception_to_backend(data, api_key: str):
        if api_key is not None:
            try:
                response = requests.post(
                    "https://api.murnitur.ai/api/interceptions",
                    json=data,
                    headers={"x-murnix-trace-token": api_key},
                )
                response.raise_for_status()
            except requests.RequestException as e:
                print(f"Failed to send interception: {e}")

    @staticmethod
    def __preprocess_rules(rulesets: List[RuleSet]) -> list[RuleSet]:
        processed_rules = []

        for ruleset in rulesets:
            processed_rules.append(
                {
                    "rules": [
                        {
                            "metric": rule["metric"],
                            "operator": rule.get("operator", "contains"),
                            "value": (
                                rule["value"]
                                if isinstance(rule["value"], list)
                                else [rule["value"]]
                            ),
                        }
                        for rule in ruleset["rules"]
                    ],
                    "action": ruleset["action"],
                }
            )
        return processed_rules

    # @staticmethod
    # def shield(
    #     payload: Payload, rulesets: List[RuleSet], config: Optional[GuardConfig] = None
    # ) -> Response:
    #     with murnitur.tracer(name="Shield") as trace:
    #         trace.set_metadata(
    #             {
    #                 "input": json.dumps(payload),
    #             }
    #         )
    #         """
    #         Shields the payload based on provided rulesets.

    #         Args:
    #             payload (dict): The input data to be checked.
    #             rulesets (list): A list of rules defining how to check the payload.\n
    #             config:
    #                 murnitur_key (str): API key for Murnitur services.
    #                 group (str, optional): Group name for categorization. Default is "untitled".
    #                 openai_key (str, optional): API key for OpenAI services.
    #                 model (str, optional): Model for OpenAI services. Default is "gpt-4o-mini"

    #         Returns:
    #             Response: Response message after applying the rules.
    #         """
    #         try:

    #             if config is None:
    #                 config = default_config
    #             else:
    #                 for key, value in default_config.items():
    #                     if key not in config:
    #                         config[key] = value
    #             preprocessed_rulesets = Guard.__preprocess_rules(rulesets)
    #             return_value: Response = None
    #             for ruleset in preprocessed_rulesets:
    #                 action_type = ruleset["action"]["type"]
    #                 fallback = ruleset["action"]["fallback"]

    #                 for rule in ruleset["rules"]:
    #                     metric = rule["metric"]
    #                     operator = rule.get("operator", "contains")
    #                     rule_value = rule["value"]

    #                     if metric == "custom":
    #                         custom_function = custom_metric_registry.get(rule_value[0])
    #                         if custom_function:
    #                             result = custom_function(payload)
    #                             if not isinstance(result, Tuple):
    #                                 raise Exception(
    #                                     f"Result of {rule_value[0]} must be a Tuple."
    #                                 )
    #                             triggered, text = result
    #                             if triggered:
    #                                 submit_interception(
    #                                     payload,
    #                                     fallback,
    #                                     action_type,
    #                                     rule,
    #                                     ruleset,
    #                                     metric,
    #                                     config["group"],
    #                                     config["murnitur_key"],
    #                                     trace,
    #                                     rulesets,
    #                                     result,
    #                                 )
    #                                 return Response(
    #                                     (
    #                                         fallback
    #                                         if action_type == "OVERRIDE"
    #                                         else f"Message flagged: {fallback}"
    #                                     ),
    #                                     True,
    #                                     rule,
    #                                     result,
    #                                 )
    #                             else:
    #                                 return_value = Response(text, False)

    #                     elif metric in ("pii", "input_pii"):
    #                         pii_value = payload.get(
    #                             "output" if metric == "pii" else "input", ""
    #                         )
    #                         pii_found, pii = check_pii(pii_value, operator, rule_value)
    #                         if pii_found:
    #                             submit_interception(
    #                                 payload,
    #                                 fallback,
    #                                 action_type,
    #                                 rule,
    #                                 ruleset,
    #                                 metric,
    #                                 config["group"],
    #                                 config["murnitur_key"],
    #                                 trace,
    #                                 rulesets,
    #                                 pii,
    #                             )
    #                             return Response(
    #                                 (
    #                                     fallback
    #                                     if action_type == "OVERRIDE"
    #                                     else f"Message flagged: {fallback}"
    #                                 ),
    #                                 True,
    #                                 rule,
    #                                 pii,
    #                             )
    #                         else:
    #                             return_value = Response(pii_value, False)
    #                     elif metric in ("tone", "input_tone"):
    #                         tone_value = payload.get(
    #                             "output" if metric == "tone" else "input", ""
    #                         )
    #                         tone_detected, tones = detect_tone(
    #                             tone_value, operator, rule_value
    #                         )
    #                         if tone_detected:
    #                             submit_interception(
    #                                 payload,
    #                                 fallback,
    #                                 action_type,
    #                                 rule,
    #                                 ruleset,
    #                                 metric,
    #                                 config["group"],
    #                                 config["murnitur_key"],
    #                                 trace,
    #                                 rulesets,
    #                                 tones,
    #                             )
    #                             return Response(
    #                                 (
    #                                     fallback
    #                                     if action_type == "OVERRIDE"
    #                                     else f"Message flagged: {fallback}"
    #                                 ),
    #                                 True,
    #                                 rule,
    #                                 tones,
    #                             )
    #                         else:
    #                             return_value = Response(tone_value, False)
    #                     elif metric == "prompt_injection":
    #                         input_value = payload.get("input", "")
    #                         found_injection, verdict = detect_injection(
    #                             input_value, operator, rule_value, config
    #                         )
    #                         if found_injection:
    #                             submit_interception(
    #                                 payload,
    #                                 fallback,
    #                                 action_type,
    #                                 rule,
    #                                 ruleset,
    #                                 metric,
    #                                 config["group"],
    #                                 config["murnitur_key"],
    #                                 trace,
    #                                 rulesets,
    #                                 verdict,
    #                             )
    #                             return Response(
    #                                 (
    #                                     fallback
    #                                     if action_type == "OVERRIDE"
    #                                     else f"Message flagged: {fallback}"
    #                                 ),
    #                                 True,
    #                                 rule,
    #                                 verdict,
    #                             )
    #                         else:
    #                             return_value = Response(input_value, False)
    #                     elif metric == "toxicity":
    #                         output_value = payload.get("output", "")
    #                         toxicity_detected, verdict = detect_toxicity(
    #                             output_value, operator, rule_value[0], config
    #                         )
    #                         if toxicity_detected:
    #                             submit_interception(
    #                                 payload,
    #                                 fallback,
    #                                 action_type,
    #                                 rule,
    #                                 ruleset,
    #                                 metric,
    #                                 config["group"],
    #                                 config["murnitur_key"],
    #                                 trace,
    #                                 rulesets,
    #                                 verdict,
    #                             )
    #                             return Response(
    #                                 (
    #                                     fallback
    #                                     if action_type == "OVERRIDE"
    #                                     else f"Message flagged: {fallback}"
    #                                 ),
    #                                 True,
    #                                 rule,
    #                                 verdict,
    #                             )
    #                     elif metric == "bias":
    #                         output_value = payload.get("output", "")
    #                         bias_detected, verdict = detect_bias(
    #                             output_value, operator, rule_value[0], config
    #                         )
    #                         if bias_detected:
    #                             submit_interception(
    #                                 payload,
    #                                 fallback,
    #                                 action_type,
    #                                 rule,
    #                                 ruleset,
    #                                 metric,
    #                                 config["group"],
    #                                 config["murnitur_key"],
    #                                 trace,
    #                                 rulesets,
    #                                 verdict,
    #                             )
    #                             return Response(
    #                                 (
    #                                     fallback
    #                                     if action_type == "OVERRIDE"
    #                                     else f"Message flagged: {fallback}"
    #                                 ),
    #                                 True,
    #                                 rule,
    #                                 verdict,
    #                             )
    #                     elif metric == "ctx_adherence":
    #                         output_value = payload.get("output", "")
    #                         contexts = payload.get("contexts", [])
    #                         hallucination_detected, verdict = detect_hallucination(
    #                             output_value, contexts, operator, rule_value[0], config
    #                         )
    #                         if hallucination_detected:
    #                             submit_interception(
    #                                 payload,
    #                                 fallback,
    #                                 action_type,
    #                                 rule,
    #                                 ruleset,
    #                                 metric,
    #                                 config["group"],
    #                                 config["murnitur_key"],
    #                                 trace,
    #                                 rulesets,
    #                                 verdict,
    #                             )
    #                             return Response(
    #                                 (
    #                                     fallback
    #                                     if action_type == "OVERRIDE"
    #                                     else f"Message flagged: {fallback}"
    #                                 ),
    #                                 True,
    #                                 rule,
    #                                 verdict,
    #                             )

    #             return return_value or Response(
    #                 payload.get("output", payload.get("input", "")), False
    #             )

    #         except Exception as e:
    #             raise e

    @staticmethod
    def shield(
        payload: Payload, rulesets: List[RuleSet], config: Optional[GuardConfig] = None
    ) -> Response:
        """
        Shields the payload based on provided rulesets.

        Args:
            payload (dict): The input data to be checked.
            rulesets (list): A list of rules defining how to check the payload.\n
            config:
                murnitur_key (str): API key for Murnitur services.
                group (str, optional): Group name for categorization. Default is "untitled".
                openai_key (str, optional): API key for OpenAI services.
                model (str, optional): Model for OpenAI services. Default is "gpt-4o-mini"

        Returns:
            Response: Response message after applying the rules.
        """
        with murnitur.tracer(name="Shield") as trace:
            trace.set_metadata({"input": json.dumps(payload)})

            try:
                config = Guard._merge_config(config)
                preprocessed_rulesets = Guard.__preprocess_rules(rulesets)
                return Guard._apply_rulesets(
                    payload, preprocessed_rulesets, config, trace
                )
            except Exception as e:
                print(f"Error in shield: {e}")
                raise e

    @staticmethod
    def _merge_config(config: Optional[GuardConfig]) -> GuardConfig:
        """Merge the user config with the default config"""
        config = config or {}
        for key, value in default_config.items():
            config.setdefault(key, value)
        return config

    @staticmethod
    def _apply_rulesets(
        payload: Payload, rulesets: List[RuleSet], config: GuardConfig, trace
    ) -> Response:
        """Applies rulesets to the payload and returns a response."""
        return_value = None
        for ruleset in rulesets:
            action_type, fallback = (
                ruleset["action"]["type"],
                ruleset["action"]["fallback"],
            )

            for rule in ruleset["rules"]:
                metric = rule["metric"]
                handler = Guard._get_handler(metric)

                if handler:
                    response = handler(
                        payload,
                        rule,
                        ruleset,
                        config,
                        trace,
                        action_type,
                        fallback,
                        rulesets,
                    )
                    if response:
                        return response

                return_value = Response(
                    payload.get("output", payload.get("input", "")), False
                )

        return return_value or Response(
            payload.get("output", payload.get("input", "")), False
        )

    @staticmethod
    def _get_handler(metric: str):
        """Returns the appropriate handler based on the metric."""
        handlers = {
            "custom": Guard._handle_custom,
            "pii": Guard._handle_pii,
            "input_pii": Guard._handle_pii,
            "tone": Guard._handle_tone,
            "input_tone": Guard._handle_tone,
            "prompt_injection": Guard._handle_prompt_injection,
            "toxicity": Guard._handle_toxicity,
            "bias": Guard._handle_bias,
            "ctx_adherence": Guard._handle_ctx_adherence,
        }
        return handlers.get(metric)

    @staticmethod
    def _handle_custom(
        payload, rule, ruleset, config, trace, action_type, fallback, rulesets
    ):
        """Handle custom metric"""
        custom_function = custom_metric_registry.get(rule["value"][0])
        if custom_function:
            triggered, text = custom_function(payload)
            if triggered:
                return Guard._submit_interception_and_respond(
                    payload,
                    fallback,
                    action_type,
                    rule,
                    ruleset,
                    "custom",
                    config,
                    trace,
                    rulesets,
                    {"triggered": triggered, "text": fallback},
                )
        return None

    @staticmethod
    def _handle_pii(
        payload, rule, ruleset, config, trace, action_type, fallback, rulesets
    ):
        """Handle PII detection"""
        pii_value = payload.get("output" if rule["metric"] == "pii" else "input", "")
        pii_found, pii = check_pii(
            pii_value, rule.get("operator", "contains"), rule["value"]
        )
        if pii_found:
            return Guard._submit_interception_and_respond(
                payload,
                fallback,
                action_type,
                rule,
                ruleset,
                rule["metric"],
                config,
                trace,
                rulesets,
                pii,
            )
        return None

    @staticmethod
    def _handle_tone(
        payload, rule, ruleset, config, trace, action_type, fallback, rulesets
    ):
        """Handle tone detection"""
        tone_value = payload.get("output" if rule["metric"] == "tone" else "input", "")
        tone_detected, tones = detect_tone(
            tone_value, rule.get("operator", "contains"), rule["value"]
        )
        if tone_detected:
            return Guard._submit_interception_and_respond(
                payload,
                fallback,
                action_type,
                rule,
                ruleset,
                rule["metric"],
                config,
                trace,
                rulesets,
                tones,
            )
        return None

    @staticmethod
    def _handle_prompt_injection(
        payload, rule, ruleset, config, trace, action_type, fallback, rulesets
    ):
        """Handle prompt injection detection"""
        input_value = payload.get("input", "")
        found_injection, verdict = detect_injection(
            input_value, rule.get("operator", "contains"), rule["value"], config
        )
        if found_injection:
            return Guard._submit_interception_and_respond(
                payload,
                fallback,
                action_type,
                rule,
                ruleset,
                rule["metric"],
                config,
                trace,
                rulesets,
                verdict,
            )
        return None

    @staticmethod
    def _handle_toxicity(
        payload, rule, ruleset, config, trace, action_type, fallback, rulesets
    ):
        """Handle toxicity detection"""
        output_value = payload.get("output", "")
        toxicity_detected, verdict = detect_toxicity(
            output_value, rule.get("operator", "contains"), rule["value"][0], config
        )
        if toxicity_detected:
            return Guard._submit_interception_and_respond(
                payload,
                fallback,
                action_type,
                rule,
                ruleset,
                rule["metric"],
                config,
                trace,
                rulesets,
                verdict,
            )
        return None

    @staticmethod
    def _handle_bias(
        payload, rule, ruleset, config, trace, action_type, fallback, rulesets
    ):
        """Handle bias detection"""
        output_value = payload.get("output", "")
        bias_detected, verdict = detect_bias(
            output_value, rule.get("operator", "contains"), rule["value"][0], config
        )
        if bias_detected:
            return Guard._submit_interception_and_respond(
                payload,
                fallback,
                action_type,
                rule,
                ruleset,
                rule["metric"],
                config,
                trace,
                rulesets,
                verdict,
            )
        return None

    @staticmethod
    def _handle_ctx_adherence(
        payload, rule, ruleset, config, trace, action_type, fallback, rulesets
    ):
        """Handle hallucination/context adherence detection"""
        output_value = payload.get("output", "")
        contexts = payload.get("contexts", [])
        hallucination_detected, verdict = detect_hallucination(
            output_value,
            contexts,
            rule.get("operator", "contains"),
            rule["value"][0],
            config,
        )
        if hallucination_detected:
            return Guard._submit_interception_and_respond(
                payload,
                fallback,
                action_type,
                rule,
                ruleset,
                rule["metric"],
                config,
                trace,
                rulesets,
                verdict,
            )
        return None

    @staticmethod
    def _submit_interception_and_respond(
        payload,
        fallback,
        action_type,
        rule,
        ruleset,
        metric,
        config,
        trace,
        rulesets,
        result,
    ):
        """Helper to submit interception and return response"""
        submit_interception(
            payload,
            fallback,
            action_type,
            rule,
            ruleset,
            metric,
            config["group"],
            config["murnitur_key"],
            trace,
            rulesets,
            result,
        )
        return Response(
            fallback if action_type == "OVERRIDE" else f"Message flagged: {fallback}",
            True,
            rule,
            result,
        )

    @staticmethod
    def probe(
        payload: Payload,
        metric: Literal[
            "pii",
            "input_pii",
            "toxicity",
            "input_tone",
            "tone",
            "bias",
            "prompt_injection",
            "ctx_adherence",
        ],
        config: Optional[GuardConfig] = None,
    ):
        """
        Probes the payload for specific metrics without requiring predefined rulesets and actions.

        The `probe` function allows direct querying of the Murnitur Shield's capabilities, enabling
        users to check for specific metrics such as PII, tone, prompt injection, toxicity, bias,
        or context adherence in the given payload. This function provides a more flexible and
        immediate way to leverage Murnitur Shield's functionality without setting up complete
        rulesets and actions. Unlike the `shield` function, `probe` does not trigger any actions
        based on the results; it simply returns the findings.

        Args:
            payload (Payload): The input data to be checked, structured as a dictionary.
            metric (str): The specific metric to probe in the payload. Supported metrics include:
                          - "pii": Checks for personally identifiable information in the output.
                          - "input_pii": Checks for personally identifiable information in the input.
                          - "tone": Detects the tone of the output.
                          - "input_tone": Detects the tone of the input.
                          - "prompt_injection": Identifies prompt injection attacks in the input.
                          - "toxicity": Detects toxic language in the output.
                          - "bias": Detects biased language in the output.
                          - "ctx_adherence": Checks adherence to the given context in the output.
            config (Optional[GuardConfig]): Optional configuration settings for the Murnitur Shield.
                                            If not provided, default configuration will be used.

        Returns:
            (tuple[bool, List[str]] | list | None): The findings

        Example:
            ## Probing for input tone
            payload = {"input": "I am very frustrated with this situation."}
            result = Guard.probe(payload, 'input_tone')

            ## Example output: ['annoyance', 'sadness']
        """
        if config is None:
            config = default_config
        else:
            for key, value in default_config.items():
                if key not in config:
                    config[key] = value
        if metric in ["pii", "input_pii"]:
            values = [
                "email",
                "ssn",
                "address",
                "phone_number",
                "date",
                "financial_info",
            ]
            found_patterns = find_patterns(
                values, payload.get("output" if metric == "pii" else "input", "")
            )
            return any(found_patterns), found_patterns
        elif metric in ["tone", "input_tone"]:
            tones, _ = detect(
                payload.get("output" if metric == "tone" else "input", "")
            )
            return tones
        elif metric == "prompt_injection":
            return PromptInjectionDetector(config=config).detect_prompt_injection(
                payload.get("input", "")
            )
        elif metric == "bias":
            return BiasDetector(config=config).detect_bias(payload.get("output", ""))
        elif metric == "toxicity":
            return ToxicityDetector(config=config).detect_toxicity(
                payload.get("output", "")
            )
        elif metric == "ctx_adherence":
            return HallucinationDetector(config=config).detect_hallucination(
                payload.get("contexts", []), payload.get("output", "")
            )


def submit_interception(
    payload,
    fallback,
    action_type,
    rule,
    ruleset,
    metric,
    group=None,
    murnitur_key=None,
    trace: TracedSpan = None,
    rulesets: list[RuleSet] = [],
    verdict=None,
):
    """
    Submits an interception to the backend for processing asynchronously.

    Args:
        payload (dict): The input data to be intercepted.
        fallback (str): The fallback message.
        action_type (str): The action type, e.g., "OVERRIDE".
        rule (dict): The rule that triggered the interception.
        ruleset (dict): The ruleset containing the rule.
        group (str, optional): Group name for categorization. Default is None.
        murnitur_key (str, optional): API key for Murnitur services. Default is None.

    Returns:
        Future: A future object representing the execution of the interception.
    """
    group = group or "untitled"

    interception_data = {
        "group": group,
        "interception": {
            "input": payload.get("input"),
            "output": payload.get("output"),
            "metric": metric,
            "response": (
                fallback
                if action_type == "OVERRIDE"
                else f"Message flagged: {fallback}"
            ),
            "rule": rule,
            "action": ruleset["action"],
            "verdict": verdict,
        },
    }

    if trace:
        trace.__shield__(
            rules=rulesets,
            rule={
                **rule,
                "action": ruleset["action"],
            },
            triggered=True,
            response=interception_data["interception"]["response"],
        )
        trace.set_result(
            json.dumps({"output": interception_data["interception"]["response"]})
        )

    return Guard.executor.submit(
        Guard.send_interception_to_backend,
        data=interception_data,
        api_key=os.getenv("MURNITUR_API_KEY", murnitur_key),
    )


def find_patterns(patterns: List[str], payload: str) -> List[str]:
    return [
        pattern
        for pattern in patterns
        if pattern in pii_patterns and re.findall(pii_patterns[pattern], payload)
    ]
