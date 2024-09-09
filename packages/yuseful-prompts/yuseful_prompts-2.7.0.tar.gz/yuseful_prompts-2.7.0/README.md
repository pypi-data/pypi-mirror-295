# yuseful_prompts

## what is this ?

This is a simple python package that uses `ollama` with prompts I'm finding useful for my own projects.

## pre requisites

- `ollama` installed with a model of your chosing referenced in as the `DEFAULT_MODEL` in `yuseful_prompts/useful_prompts.py`

## test

- `python3 -m pytest -v ./yuseful_prompts/test_useful_prompts.py`

### benchmark

Here are a few SLMs I've tested on September 1st latest commit:

- `hermes3`      => 45/45 tests correct in  145.81s
- `gemma2:9b`    => 45/45 tests correct in  210.54s
- `llama3.1`     => 44/45 tests correct in  139.47s
- `mistral-nemo` => 44/45 tests correct in  253.18s
- `llama3.1:70b` => 43/45 tests correct in 1167.93s
- `qwen2:7b`     => 41/45 tests correct in  134.13s
- `phi3.5`       => 32/45 tests correct in  164.38s
