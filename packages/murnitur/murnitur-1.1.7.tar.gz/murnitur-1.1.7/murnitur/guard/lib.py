import re
from typing import Union, List
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from murnitur.main import GuardConfig
from .prompt_injection import PromptInjectionDetector
from .toxicity_detection import ToxicityDetector
from .bias_detection import BiasDetector
from .hallucination_detection import HallucinationDetector

analyzer = SentimentIntensityAnalyzer()

pii_patterns = {
    "address": r"\d{1,5}\s\w{1,2}\.\s(\b\w+\b\s){1,2}\w+\.",
    "date": r"\d{1,2}/\d{1,2}/\d{4}",
    "email": r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+",
    "financial_info": r"\b(?:\d[ -]*?){13,16}\b|\b(?:credit\s*card|card|last\s+(?:four|4)\s+digits|four\s+digits|last\s+four\s+digits\s+of\s+credit\s*card|last\s+4\s+digits\s+of\s+credit\s*card)\D*?(\d{4})\b",
    "phone_number": r"(?:\+?\d{1,3})?[-.\s]?(?:\(?\d{2,4}\)?)?[-.\s]?\d{5,}",
    "ssn": r"\b\d{3}[-.\s]?\d{2}[-.\s]?\d{4}\b|\b(?:last\s+four\s+digits\s+of\s+SSN|last\s+4\s+digits\s+of\s+SSN|last\s+four\s+digits\s+of\s+social\s+security\s+number|last\s+4\s+digits\s+of\s+social\s+security\s+number)\D*?(\d{4})\b",
}


def evaluate_rule(
    value: Union[int, str], operator: str, payload_value: Union[str, int]
) -> bool:
    operators = {
        "equal": lambda x, y: x == y,
        "not_equal": lambda x, y: x != y,
        "contains": lambda x, y: y in x,
        "greater_than": lambda x, y: x > y,
        "less_than": lambda x, y: x < y,
        "greater_than_equal": lambda x, y: x >= y,
        "less_than_equal": lambda x, y: x <= y,
        "any": lambda x, y: any(item in y for item in x),
        "all": lambda x, y: all(item in y for item in x),
    }

    if isinstance(payload_value, str) and operator in (
        "greater_than",
        "less_than",
        "greater_than_equal",
        "less_than_equal",
    ):
        try:
            payload_value = int(payload_value)
        except ValueError:
            return False

    return operators[operator](payload_value, value)


def check_pii(
    payload: str, operator: str, value: Union[str, List[str]]
) -> tuple[bool, List[str]]:
    found_patterns = []

    def find_patterns(patterns: List[str]) -> List[str]:
        return [
            pattern
            for pattern in patterns
            if pattern in pii_patterns and re.findall(pii_patterns[pattern], payload)
        ]

    if operator == "contains":
        found_patterns = find_patterns(value)
        result = any(found_patterns)
    elif operator == "any":
        found_patterns = find_patterns(value)
        result = any(found_patterns)
    elif operator == "all":
        found_patterns = find_patterns(value)
        result = all(
            re.findall(pii_patterns[pattern], payload)
            for pattern in value
            if pattern in pii_patterns
        )

    return result, found_patterns


def detect_tone(payload: str, operator: str, value: Union[str, List[str]]) -> tuple[bool, list[str]]:
    tones, _ = detect(payload)
    if isinstance(value, str):
        value = [value]
    if operator == "equal" or operator == "contains" or operator == "any":
        return (any(tone in value for tone in tones), tones)
    elif operator == "not_equal":
        return (any(tone not in value for tone in tones), tones)


def detect_injection(
    payload: str, operator: str, value: Union[str, List[str]], config: GuardConfig
) -> tuple[bool, dict]:

    injection_score = PromptInjectionDetector(config=config).detect_prompt_injection(
        payload
    )
    if injection_score:
        injection_type = injection_score.get("type", "")

        if isinstance(value, str):
            value = [value]
        if operator == "equal" or operator == "contains":
            return (
                injection_type in value,
                injection_score,
            )
        elif operator == "not_equal":
            return (
                injection_type not in value,
                injection_score,
            )


def detect_toxicity(
    output: str, operator: str, value: int, config: GuardConfig
) -> tuple[bool, dict]:
    result = ToxicityDetector(config=config).detect_toxicity(output)
    res = evaluate_rule(value, operator, result.get("score", 0))
    return res, result


def detect_bias(output: str, operator: str, value: int, config: GuardConfig) -> tuple[bool, dict]:
    result = BiasDetector(config=config).detect_bias(output)
    res = evaluate_rule(value, operator, result.get("score", 0))
    return res, result


def detect_hallucination(
    output: str, contexts: list[str], operator: str, value: int, config: GuardConfig
) -> tuple[bool, dict]:
    result = HallucinationDetector(config=config).detect_hallucination(contexts, output)
    res = evaluate_rule(value, operator, result.get("score", 0))
    return res, result


def detect(text):
        sentiment = analyzer.polarity_scores(text)
        compound_score = sentiment["compound"]

        tones = []

        if compound_score >= 0.05:
            if sentiment["pos"] > 0.6:
                tones.append("joy")
            if sentiment["pos"] > 0.4:
                tones.append("love")
            if "joy" not in tones and "love" not in tones:
                tones.append("positive")
        elif compound_score <= -0.05:
            if sentiment["neg"] > 0.6:
                tones.append("anger")
            if sentiment["neg"] > 0.4:
                tones.append("annoyance")
            if sentiment["neg"] > 0.2:
                tones.append("sadness")
            if (
                "anger" not in tones
                and "annoyance" not in tones
                and "sadness" not in tones
            ):
                tones.append("negative")
        else:
            tones.append("neutral")

        return tones, sentiment
