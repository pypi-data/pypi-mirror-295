
# LLM AutoScoring Library

This library provides a comprehensive set of tools for evaluating the performance of Language Model (LLM) extraction processes. It includes various scoring mechanisms and an easy-to-use evaluation framework.

## Installation

```bash
pip install llm_autoscoring
```

## Usage

Here's a quick example of how to use the library:

```python
from llm_autoscoring import Evaluator, ExactMatchScorer, RegexScorer, MultiSelectScorer, OpenAIScorer

# Define scorers
scorers = {
    "name": ExactMatchScorer(),
    "date": RegexScorer(r"\d{4}-\d{2}-\d{2}"),
    "fruits": MultiSelectScorer(),
    "description": OpenAIScorer("your-api-key-here")
}

# Create evaluator
evaluator = Evaluator(scorers)

# Define reference and candidate data
references = {
    "name": "John Doe",
    "date": "2023-05-15",
    "fruits": "apple,banana,cherry",
    "description": "A tall man with brown hair"
}
candidates = {
    "name": "John Doe",
    "date": "2023-05-15",
    "fruits": "apple,cherry,date",
    "description": "A man of average height with dark hair"
}

# Evaluate
results = evaluator.evaluate(references, candidates)
print(results)
```

## Available Scorers

- `ExactMatchScorer`: Checks for exact matches between reference and candidate strings.
- `RegexScorer`: Checks if the candidate string matches a given regular expression pattern.
- `OpenAIScorer`: Uses OpenAI's API to judge the similarity between reference and candidate strings.
- `SemanticScorer`: Computes semantic similarity between reference and candidate strings using spaCy.
- `F1Scorer`: Calculates the F1 score for text comparison.
- `DateScorer`: Checks if dates match, with flexible parsing.
- `MultiSelectScorer`: Evaluates multi-select fields, providing F1 score and detailed metrics.
