#!/usr/bin/env bash
# vLLM API test script

HOST="${HOST:-localhost}"
PORT="${PORT:-8000}"
BASE_URL="http://${HOST}:${PORT}"
MODEL="${MODEL:-Qwen/Qwen2.5-14B-Instruct}"

PASS=0
FAIL=0

echo "Testing vLLM server at ${BASE_URL}"
echo "Model: ${MODEL}"
echo "========================================"

test_endpoint() {
    local name="$1"
    local cmd="$2"

    echo -ne "\n${name}... "
    if eval "$cmd" 2>&1; then
        ((PASS++))
    else
        ((FAIL++))
    fi
}

# Test 1: List models
test_endpoint "[1/10] List models" \
    "curl -sf '${BASE_URL}/v1/models' | jq -e '.data'"

# Test 2: Basic completions
test_endpoint "[2/10] Basic completions" \
    "curl -sf -X POST '${BASE_URL}/v1/completions' \
      -H 'Content-Type: application/json' \
      -d '{\"model\": \"${MODEL}\", \"prompt\": \"Hello\", \"max_tokens\": 10}' | jq -e '.choices'"

# Test 3: Batch completions
test_endpoint "[3/10] Batch completions" \
    "curl -sf -X POST '${BASE_URL}/v1/completions' \
      -H 'Content-Type: application/json' \
      -d '{\"model\": \"${MODEL}\", \"prompt\": [\"Once\", \"In\"], \"max_tokens\": 10}' | jq -e '.choices'"

# Test 4: Chat completions
test_endpoint "[4/10] Chat completions" \
    "curl -sf -X POST '${BASE_URL}/v1/chat/completions' \
      -H 'Content-Type: application/json' \
      -d '{\"model\": \"${MODEL}\", \"messages\": [{\"role\": \"user\", \"content\": \"Hi\"}], \"max_tokens\": 10}' | jq -e '.choices'"

# Test 5: Sampling parameters
test_endpoint "[5/10] Sampling parameters" \
    "curl -sf -X POST '${BASE_URL}/v1/chat/completions' \
      -H 'Content-Type: application/json' \
      -d '{\"model\": \"${MODEL}\", \"messages\": [{\"role\": \"user\", \"content\": \"Hi\"}], \"max_tokens\": 10, \"temperature\": 0.9, \"top_p\": 0.95}' | jq -e '.choices'"

# Test 6: Streaming
test_endpoint "[6/10] Streaming" \
    "curl -sf -X POST '${BASE_URL}/v1/chat/completions' \
      -H 'Content-Type: application/json' \
      -d '{\"model\": \"${MODEL}\", \"messages\": [{\"role\": \"user\", \"content\": \"Hi\"}], \"stream\": true, \"max_tokens\": 10}' | grep -q 'data:'"

# Test 7: Logprobs
test_endpoint "[7/10] Logprobs" \
    "curl -sf -X POST '${BASE_URL}/v1/completions' \
      -H 'Content-Type: application/json' \
      -d '{\"model\": \"${MODEL}\", \"prompt\": \"Hello\", \"max_tokens\": 5, \"logprobs\": 5}' | jq -e '.choices[0].logprobs'"

# Test 8: Stop sequences
test_endpoint "[8/10] Stop sequences" \
    "curl -sf -X POST '${BASE_URL}/v1/completions' \
      -H 'Content-Type: application/json' \
      -d '{\"model\": \"${MODEL}\", \"prompt\": \"1.\", \"max_tokens\": 20, \"stop\": [\"3.\"]}' | jq -e '.choices'"

# Test 9: Echo
test_endpoint "[9/10] Echo" \
    "curl -sf -X POST '${BASE_URL}/v1/completions' \
      -H 'Content-Type: application/json' \
      -d '{\"model\": \"${MODEL}\", \"prompt\": \"Hello\", \"max_tokens\": 5, \"echo\": true}' | jq -e '.choices'"

# Test 10: Multiple completions
test_endpoint "[10/10] Multiple completions (n=2)" \
    "curl -sf -X POST '${BASE_URL}/v1/completions' \
      -H 'Content-Type: application/json' \
      -d '{\"model\": \"${MODEL}\", \"prompt\": \"Hi\", \"max_tokens\": 10, \"n\": 2}' | jq -e '.choices | length == 2'"

echo -e "\n========================================"
echo "Results: ${PASS} passed, ${FAIL} failed"

if [ $FAIL -gt 0 ]; then
    exit 1
fi
