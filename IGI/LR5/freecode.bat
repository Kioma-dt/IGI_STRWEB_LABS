@echo off
title Claude Code via OmniRoute

:: OmniRoute
set ANTHROPIC_BASE_URL=http://localhost:20128/v1
set ANTHROPIC_AUTH_TOKEN=sk-71fce2eb1bc7d766-9530d7-757c324c

:: Recommended model
set ANTHROPIC_MODEL=kr/claude-sonnet-4.5

:: Reduce retries spam
set NODE_NO_WARNINGS=1

claude

pause