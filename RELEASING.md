# Release Process

This document explains how to create releases for notebook-parser.

## Overview

Releases are automated via GitHub Actions. When you push a version tag (e.g., `v0.1.0`), GitHub automatically:
1. Runs tests
2. Builds the package
3. Creates a GitHub release
4. Uploads distribution files (wheels and source)
5. Generates release notes from commits

## Creating a Release

### Quick Method (Automated Script)

```bash
# Make sure you're on main branch with clean working directory
git checkout main
git pull

# Run the release script with the new version
./scripts/release.sh 0.1.0

# Review the changes
git show HEAD

# Push to GitHub to trigger the release
git push && git push --tags
```

The script will:
- Update the version in `pyproject.toml`
- Create a commit with the version bump
- Create a git tag (e.g., `v0.1.0`)
- Show you the next steps

### Manual Method

If you prefer to do it manually:

```bash
# 1. Update version in pyproject.toml
# Change: version = "0.1.0"

# 2. Commit the version change
git add pyproject.toml
git commit -m "chore: bump version to 0.1.0"

# 3. Create a git tag
git tag -a v0.1.0 -m "Release v0.1.0"

# 4. Push to GitHub
git push && git push --tags
```

## Version Numbering

We follow [Semantic Versioning](https://semver.org/):

- **MAJOR** version (1.0.0): Incompatible API changes
- **MINOR** version (0.1.0): New functionality, backwards compatible
- **PATCH** version (0.0.1): Bug fixes, backwards compatible

### Examples
- `0.1.0` - Initial release with basic features
- `0.2.0` - Added new prompt types
- `0.2.1` - Fixed bug in image optimization
- `1.0.0` - Stable API, ready for production

## What Happens After Pushing a Tag

1. **GitHub Actions Workflow Triggers**
   - Workflow file: `.github/workflows/release.yml`
   - Runs on: Ubuntu (latest)

2. **Tests Run**
   - All pytest tests must pass
   - If tests fail, release is aborted

3. **Package Build**
   - Creates wheel file (`.whl`)
   - Creates source distribution (`.tar.gz`)
   - Files saved to `dist/` directory

4. **Release Created**
   - GitHub release page created automatically
   - Release notes generated from git commits
   - Built packages attached as release assets

5. **Users Can Download**
   - From GitHub Releases page
   - Install with pip from the wheel file

## Monitoring Releases

- View releases: https://github.com/13Mai13/notebook-parser/releases
- View workflow runs: https://github.com/13Mai13/notebook-parser/actions
- Check workflow status: Click on the "Actions" tab after pushing a tag

## Troubleshooting

### Release workflow failed
1. Go to Actions tab on GitHub
2. Click on the failed workflow run
3. Check the logs for errors
4. Fix the issue, delete the tag, and try again:
   ```bash
   git tag -d v0.1.0           # Delete local tag
   git push --delete origin v0.1.0  # Delete remote tag
   # Fix the issue, then create tag again
   ```

### Tests failed during release
- Fix the tests locally
- Create a new patch version
- Try the release again

### Version already exists
- Delete the existing tag (see above)
- Or bump to the next version

## Pre-release Testing

Before creating a release, test locally:

```bash
# Run tests
uv run pytest

# Build the package
uv build

# Test installation from wheel
pip install dist/notebook_parser-0.1.0-py3-none-any.whl

# Test the installed package
notebook-parser --help
```

## Next Steps After First Release

After your first successful release, consider:
1. Publishing to PyPI (see PUBLISHING.md)
2. Creating a Homebrew formula
3. Announcing the release on social media
4. Adding a changelog file
