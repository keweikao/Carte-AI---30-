#!/bin/bash
set -e

echo "🚀 Starting Final P1 Automation Test..."

# 1. Backend Smoke Test
echo "\n[1/4] Running Backend Smoke Test (DiningAgent)..."
if python3 test_ai_quick_start.py; then
    echo "✅ Backend Smoke Test Passed"
else
    echo "❌ Backend Smoke Test Failed"
    exit 1
fi

# 2. Frontend Lint
echo "\n[2/4] Running Frontend Lint..."
cd frontend
if npm run lint; then
    echo "✅ Frontend Lint Passed"
else
    echo "❌ Frontend Lint Failed"
    exit 1
fi

# 3. Frontend Unit Tests
echo "\n[3/4] Running Frontend Unit Tests..."
if npm run test; then
    echo "✅ Frontend Unit Tests Passed"
else
    echo "❌ Frontend Unit Tests Failed"
    exit 1
fi

# 4. Frontend Build Test
echo "\n[4/4] Running Frontend Build..."
if npm run build; then
    echo "✅ Frontend Build Passed"
else
    echo "❌ Frontend Build Failed"
    exit 1
fi

echo "\n🎉 All P1 Tests Passed! Ready for Social Media Promotion."
