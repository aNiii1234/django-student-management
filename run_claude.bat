@echo off
REM Set environment variables
set ANTHROPIC_BASE_URL=https://open.bigmodel.cn/api/anthropic
set ANTHROPIC_AUTH_TOKEN=1c4e0aed3bea42ac83bace4116055fb0.cRoRUCqGFzuob3fE

REM Run claude command --dangerously-skip-permissions
@REM npx claude --dangerously-skip-permissions
npx claude --dangerously-skip-permissions