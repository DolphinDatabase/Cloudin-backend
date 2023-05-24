#!/bin/bash

# Change this regex pattern to match your Jira card ID format
JIRA_CARD_ID_PATTERN="[A-Z]+-[0-9]+"

# Extract the commit message
COMMIT_MSG_FILE=$(mktemp)
trap "rm -f $COMMIT_MSG_FILE" EXIT
git log --format=%B -n 1 "$1" >"$COMMIT_MSG_FILE"

# Check if the commit message contains a Jira card ID
grep -qE "$JIRA_CARD_ID_PATTERN" "$COMMIT_MSG_FILE"
GREP_EXIT_CODE=$?

if [[ $GREP_EXIT_CODE -ne 0 ]]; then
    echo "ERROR: Commit message must contain a Jira card ID (e.g., ABC-123)."
    exit 1
fi