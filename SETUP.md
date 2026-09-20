# Set up your profile

This package is customized for Aman and assumes the GitHub username `aman36yt`.
If that username has changed, replace it in README.md and the script default.

1. Create a PUBLIC GitHub repository with exactly your username as its name:
   `aman36yt/aman36yt`. If it already exists, use the existing repository.
2. Extract this ZIP. Put the CONTENTS of `aman-github-profile` in the repository
   root. README.md must be at the root, alongside assets, scripts, and .github.
   Do not upload the ZIP itself. Include the hidden `.github` directory.
3. Commit and push those files. Your profile displays the README automatically.
4. In the repository, open Actions → Update profile → Run workflow.
   The statistics placeholders are replaced with live public GitHub data.
   The workflow also runs weekly. No personal access token is required.

## What is included

- Original terminal-style SVG banner with an animated cursor.
- Dark and light SVG assets, selected by the viewer's color scheme.
- Personalized biography, skills, and project table.
- Two qualitative skill/focus cards (no invented skill ratings).
- Locally generated GitHub statistics and language cards.
- Python standard-library generator and GitHub Actions workflow.

The source reference only supplied a README, not its SVG files or scripts.
These are new assets inspired by that layout, not a copy of the original artwork.

## Statistics definitions

Public repositories: all repositories owned by the account, including forks.
Stars: stars received by owned non-fork public repositories.
Followers: the public follower count.
Languages: number of owned non-fork public repositories whose PRIMARY language
matches each language; top five shown. This is not code-byte percentage or skill.
No commit or streak totals are claimed. Data is fetched before rewriting cards;
API failures preserve the previous cards and fail the workflow.

## Editing

Edit README.md for biography, project links, and social links. LinkedIn and
Instagram links were omitted because no verified URLs were provided.
Edit scripts/generate.py for banner text, skill cards, colors, and layouts.
Run `python scripts/generate.py` to regenerate initial placeholder assets.
Run `python scripts/generate.py --fetch --username aman36yt` for current data.

Typing animation, stack icons, and the project badge use external image services.
The banner, skill cards, and statistics are stored in the repository itself.

## Troubleshooting

Missing images: keep the assets folder beside README.md with the same filenames.
No stats update: manually run the workflow and inspect its log. Repository or
organization policies and branch protection may prevent the workflow from
pushing. Allow the workflow's intended write access or commit generated assets
manually; do not disable unrelated protection rules.
Scheduled workflows can be delayed or disabled for inactive repositories.
If GitHub shows an old image, append a new query string such as `?v=2` to its path.

GitHub profile README documentation:
https://docs.github.com/en/account-and-profile/how-tos/profile-customization/managing-your-profile-readme

Validation: all bundled SVGs parse as XML and all local README image paths exist.
Live GitHub Actions execution must be performed in your own repository.
