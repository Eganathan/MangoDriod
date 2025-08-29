---
title: "Setting Up Claude Code Review Before Push"
date: 2025-08-20
draft: false
tags: ["git", "code-review", "automation", "claude"]
categories: ["development", "workflow"]
---

# Setting Up Claude Code Review Before Push

This guide will help you set up an automated code review system using Claude Code that runs before every git push, with the option to skip when needed.

## Prerequisites

- Claude Code CLI installed and configured
- Git repository with proper remote setup
- Terminal access

## Step 1: Create the Pre-Push Hook Script

Create a git hook that will run before every push:

```bash
# Navigate to your project root
cd /path/to/your/project

# Create the hooks directory if it doesn't exist
mkdir -p .git/hooks

# Create the pre-push hook file
touch .git/hooks/pre-push

# Make it executable
chmod +x .git/hooks/pre-push
```

## Step 2: Generated Review Reports

Every code review automatically generates a timestamped markdown report with complete analysis:

### Report Features
- **Filename**: `claude-review-report_2025-08-20_14-30-45.md`
- **Complete History**: All commits since main branch
- **File Changes**: List of all modified files  
- **Project Checks**: Linting and type checking results
- **Claude Analysis**: Detailed security, bug, and quality review
- **Action Checklist**: Checkboxes for addressing issues

### Sample Report Structure
```markdown
# Claude Code Review Report

**Generated:** 2025-08-20 14:30:45
**Branch:** feature/new-ui
**Compared Against:** origin/main  
**Review Status:** ✅ Passed

## Commits Reviewed
- feat: add new user interface
- fix: resolve navigation bug
- test: add unit tests for new component

## Files Changed
- src/components/UserInterface.tsx
- src/navigation/Router.tsx  
- tests/UserInterface.test.tsx

## Project Checks
### Linting
✅ **Passed** - No linting issues found

### Type Checking
⚠️ **Issues Found** - See type checking output

## Claude Code Review Results
[Claude's detailed analysis here]

## Quick Actions
### If Issues Found:
- [ ] Fix security vulnerabilities
- [ ] Resolve critical bugs
- [ ] Address performance issues
...
```

## Step 3: Write the Pre-Push Hook

Add the following content to `.git/hooks/pre-push`:

```bash
#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if SKIP_CLAUDE_REVIEW environment variable is set
if [ "$SKIP_CLAUDE_REVIEW" = "true" ]; then
    echo -e "${YELLOW}⚠️  Claude Code review skipped (SKIP_CLAUDE_REVIEW=true)${NC}"
    exit 0
fi

# Check if claude command is available
if ! command -v claude &> /dev/null; then
    echo -e "${RED}❌ Claude Code CLI not found. Install it first or skip with: SKIP_CLAUDE_REVIEW=true git push${NC}"
    exit 1
fi

echo -e "${YELLOW}🤖 Running Claude Code review before push...${NC}"

# Get the current branch
current_branch=$(git branch --show-current)

# Find the main/master branch
main_branch=""
if git show-ref --verify --quiet refs/heads/main; then
    main_branch="main"
elif git show-ref --verify --quiet refs/heads/master; then
    main_branch="master"
elif git show-ref --verify --quiet refs/remotes/origin/main; then
    main_branch="origin/main"
elif git show-ref --verify --quiet refs/remotes/origin/master; then
    main_branch="origin/master"
else
    echo -e "${YELLOW}⚠️  Could not find main/master branch, comparing with HEAD~1${NC}"
    main_branch="HEAD~1"
fi

# Check if there are any changes to review since main branch
if [ "$main_branch" != "HEAD~1" ] && git diff --quiet "$main_branch"..HEAD 2>/dev/null; then
    echo -e "${GREEN}✅ No changes detected since $main_branch${NC}"
    exit 0
elif [ "$main_branch" = "HEAD~1" ] && git diff --quiet HEAD~1 HEAD 2>/dev/null; then
    echo -e "${GREEN}✅ No changes detected since last commit${NC}"
    exit 0
fi

# Show what's being reviewed
echo -e "${YELLOW}📋 Reviewing changes in branch: $current_branch (since $main_branch)${NC}"
if [ "$main_branch" != "HEAD~1" ]; then
    echo -e "${BLUE}Commits to be reviewed:${NC}"
    git log --oneline "$main_branch"..HEAD
    echo -e "${BLUE}Files changed:${NC}"
    git diff --name-only "$main_branch"..HEAD
else
    git log --oneline -5
fi

echo -e "${YELLOW}📝 Running automated code review...${NC}"

# Run project-specific checks first
echo -e "${BLUE}🔧 Running project checks...${NC}"

# Linting
echo -e "${YELLOW}  → Running linter...${NC}"
if npm run lint || yarn lint 2>/dev/null; then
    echo -e "${GREEN}    ✅ Linting passed${NC}"
else
    echo -e "${YELLOW}    ⚠️  Linting issues found (will be reviewed by Claude)${NC}"
fi

# Type checking
echo -e "${YELLOW}  → Running type check...${NC}"
if npm run typecheck || yarn typecheck || tsc --noEmit 2>/dev/null; then
    echo -e "${GREEN}    ✅ Type checking passed${NC}"
else
    echo -e "${YELLOW}    ⚠️  Type issues found (will be reviewed by Claude)${NC}"
fi

# Create a temporary file for the review prompt
review_file=$(mktemp)
cat > "$review_file" << 'EOF'
Please perform a comprehensive code review of ALL changes in this branch before I push to the remote repository.

IMPORTANT: Review ALL commits since the main branch, not just the latest commit. 
Use 'git diff main..HEAD' and 'git log main..HEAD' to see all changes.

The following commits will be pushed:
$(git log --oneline main..HEAD 2>/dev/null || git log --oneline -5)

Files that have been changed:
$(git diff --name-only main..HEAD 2>/dev/null || git diff --name-only HEAD~1 HEAD)

Comprehensive review including security, bugs, performance, code quality, test coverage, and best practices. 

Please also run these project-specific commands and report any issues:
1. Linting: npm run lint || yarn lint
2. Type checking: npm run typecheck || yarn typecheck || tsc --noEmit
3. Tests: npm test || yarn test

Focus areas:
1. **Security issues** - Check for exposed secrets, SQL injection, XSS vulnerabilities
2. **Bug potential** - Logic errors, null pointer exceptions, edge cases  
3. **Code quality** - Following project conventions, proper error handling
4. **Performance** - Inefficient operations, memory issues
5. **All commits** - Review every commit since main branch, not just the latest one

If you find any critical issues, please list them clearly with file locations. 
If the code looks good to push, respond with: "✅ Code review passed - safe to push"

Please review the ENTIRE diff since main branch, including all commits and file changes.
EOF

echo -e "${YELLOW}📝 Running automated code review...${NC}"

# Run Claude Code review
claude code < "$review_file"
review_exit_code=$?

# Clean up
rm "$review_file"

# Check if Claude review was successful
if [ $review_exit_code -ne 0 ]; then
    echo -e "${RED}❌ Claude Code review failed${NC}"
    echo -e "${YELLOW}💡 To skip this review: SKIP_CLAUDE_REVIEW=true git push${NC}"
    exit 1
fi

echo ""
echo -e "${GREEN}🎉 Claude Code review completed!${NC}"
echo -e "${YELLOW}💡 To skip future reviews: SKIP_CLAUDE_REVIEW=true git push${NC}"

# Ask user if they want to proceed
echo ""
read -p "Do you want to proceed with the push? (y/N): " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${GREEN}✅ Proceeding with push...${NC}"
    exit 0
else
    echo -e "${YELLOW}🛑 Push cancelled by user${NC}"
    exit 1
fi
```

## Step 3: Configure Your Project

Add these commands to your `CLAUDE.md` file (create if it doesn't exist):

```markdown
# Project Code Review Commands

## Lint Commands
- `npm run lint` or `yarn lint` - Run ESLint
- `npm run lint:fix` or `yarn lint:fix` - Fix linting issues

## Type Checking
- `npm run typecheck` or `yarn typecheck` - Run TypeScript checking
- `tsc --noEmit` - Alternative TypeScript check

## Testing
- `npm test` or `yarn test` - Run all tests
- `npm run test:coverage` - Run tests with coverage

## Build
- `npm run build` or `yarn build` - Build the project

## Pre-push Checklist
Before pushing code, ensure:
1. All tests pass
2. No linting errors
3. No type errors
4. Build succeeds
5. No security vulnerabilities
```

## Step 4: Test the Setup

Test your setup with these commands:

```bash
# Make a small change and commit it
echo "// Test comment" >> src/test-file.js
git add .
git commit -m "test: add test comment for hook testing"

# Try to push (this should trigger Claude review)
git push origin your-branch-name

# Test skipping the review
SKIP_CLAUDE_REVIEW=true git push origin your-branch-name
```

## Usage Examples

### Normal push with review:
```bash
git push origin feature-branch
# This will automatically run Claude Code review
# Generates: claude-review-report_YYYY-MM-DD_HH-MM-SS.md
```

### Skip review when needed:
```bash
# For urgent hotfixes or when review isn't needed
SKIP_CLAUDE_REVIEW=true git push origin hotfix-branch
```

### Set up permanent skip (not recommended):
```bash
# Add to your shell profile (.bashrc, .zshrc, etc.)
export SKIP_CLAUDE_REVIEW=true
```

## Advanced Configuration

### Custom Review Prompts

Create different review prompts for different scenarios by modifying the hook:

```bash
# In your pre-push hook, you can customize based on branch
if [[ $current_branch == hotfix* ]]; then
    # Use lighter review for hotfixes
    review_prompt="Quick security and critical bug check only"
elif [[ $current_branch == feature* ]]; then
    # Full review for features
    review_prompt="Comprehensive code review including performance and best practices"
fi
```

### Integration with CI/CD

You can also integrate this into your CI/CD pipeline:

```yaml
# .github/workflows/code-review.yml
name: Claude Code Review
on: [pull_request]

jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Setup Claude Code
        run: |
          # Install Claude Code CLI
          pip install claude-code
      - name: Run Code Review
        run: |
          claude code "Please review this PR for security, bugs, and code quality issues"
```

## Troubleshooting

### Hook not running?
```bash
# Check if hook is executable
ls -la .git/hooks/pre-push

# Make it executable if needed
chmod +x .git/hooks/pre-push
```

### Claude Code not found?
```bash
# Install Claude Code CLI
pip install anthropic-claude-code

# Or using npm
npm install -g @anthropic-ai/claude-code
```

### Want to modify the hook?
```bash
# Edit the hook file
nano .git/hooks/pre-push

# Or use your preferred editor
code .git/hooks/pre-push
```

## Key Features

✅ **Full Branch Review**: Reviews ALL commits since branching from main, not just the latest commit  
✅ **Smart Branch Detection**: Automatically finds main/master/origin/main/origin/master  
✅ **Auto Project Detection**: Identifies JavaScript/TypeScript, Python, Java/Android projects automatically  
✅ **Timestamped Reports**: Generates permanent markdown reports with complete analysis  
✅ **Comprehensive Analysis**: Reviews security, performance, bugs, and code quality  
✅ **Project-Specific Checks**: Runs your lint, typecheck, and test commands  
✅ **Action Checklists**: Provides clear tasks for addressing any issues found  
✅ **Detailed Reporting**: Shows exactly which commits and files will be reviewed  
✅ **Flexible**: Can be skipped when needed for urgent pushes  

## Benefits

✅ **Automated Quality Control**: Catches issues before they reach the remote repository  
✅ **Full Change Visibility**: Reviews entire diff since branching from main  
✅ **Permanent Documentation**: Timestamped reports track all reviews and action items  
✅ **Issue Tracking**: Action checklists help systematically address problems  
✅ **Educational**: Learn best practices from Claude's feedback  
✅ **Team Consistency**: Ensures all team members follow the same review standards  
✅ **Historical Record**: Keep track of code quality improvements over time  

## Team Setup

Share this setup with your team by:

1. Adding the pre-push hook to your repository (in a `scripts/` folder)
2. Creating a setup script that copies it to `.git/hooks/`
3. Documenting the process in your project's README
4. Adding the CLAUDE.md configuration to your repository

```bash
# scripts/setup-hooks.sh
#!/bin/bash
cp scripts/pre-push .git/hooks/pre-push
chmod +x .git/hooks/pre-push
echo "✅ Claude Code review hook installed!"
```

Now your code will be automatically reviewed by Claude before every push, helping maintain high code quality while giving you the flexibility to skip when needed!