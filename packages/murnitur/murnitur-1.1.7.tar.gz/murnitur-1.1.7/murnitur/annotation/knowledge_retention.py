import re
import json
from murnitur.annotation.evaluation.metrics import BaseMetric
from murnitur.guard.prompt_injection import generate_response
from murnitur.main import GuardConfig


class KnowledgeRetentionMetric(BaseMetric):

    def __init__(self, threshold: int = 0.3, model: str = "gpt-4o-mini"):
        self.threshold = threshold
        self.metric = "Knowledge Retention"
        self.model = model
        self.system_prompt = """
NOTE: Only return a JSON response

Based on the given conversation log, generate a JSON object to indicate the knowledge retention score. The JSON will have 2 fields: 'score' and 'reason'.
The 'score' is strictly a float from 0 to 1. The closer to 1, the lower the knowledge retention.
The 'reason' key should provide a concise explanation for the score.

RUBRIC FOR KNOWLEDGE RETENTION:
{
    High Retention (Score: 0 to 0.3),
    Moderate Retention (Score: 0.4 to 0.6),
    Low Retention (Score: 0.7 to 1)
}

**
IMPORTANT: Please make sure to only return in JSON format, with the 'score' key strictly between 0 and 1, and the 'reason' key as a brief explanation. You don't have to be too strict.

Example JSON:
{
  "score": 0.2,
  "reason": "Clear explanations with repetition of key points, ensuring high retention."
}

===== END OF EXAMPLE ======

Given conversation log:
{{conversation_log}}

JSON:
"""

    def measure(self, test_case: list[dict]):
        dataset = str(
            [
                {"input": msg.get("input", ""), "output": msg.get("output", "")}
                for msg in test_case
            ]
        )
        inputs = [msg.get("input", "") for msg in test_case]
        outputs = [msg.get("output", "") for msg in test_case]
        prompt = self.system_prompt
        prompt = re.sub(r"{{prompt}}", dataset, prompt)
        response = json.loads(
            generate_response(
                prompt=prompt, config=GuardConfig(provider="openai", model=self.model)
            )
        )
        self.score = response.get("score", 1)
        self.success = True if self.score <= self.threshold else False
        self.reason = response.get("reason", "")
        self.inputs = inputs
        self.outputs = outputs
        return self

    async def a_measure(self, test_case: list[dict]):
        return self.measure(test_case)

    def is_successful(self):
        return self.success

    @property
    def __name__(self):
        return "Knowledge Retention"
