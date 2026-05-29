Diagnose the following production issue using available data sources.

## Bug Description
{bug_description}

## Available Sources
{available_sources}

## Diagnostic Steps

1. **Information Gathering** (use tools in parallel when possible):
   - SSH: Check application logs, process status, system resources
   - CDP: Take screenshots, capture console errors, check network
   - Code: Search for error handling and related code paths

2. **Analysis**:
   - Extract error keywords and patterns from each source
   - Classify the error type (server, client, network, rendering)
   - Correlate timestamps across sources
   - Map stack traces to source code locations

3. **Root Cause**:
   - Identify the primary cause
   - Determine if it's a code bug, config issue, or infrastructure problem
   - Assess the blast radius (what else might be affected)

4. **Recommendations**:
   - Provide immediate mitigation steps
   - Suggest long-term fixes
   - Include relevant code changes if applicable

Provide your diagnosis as a structured JSON report.
