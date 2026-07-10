# Bulletin Workflow

The public website uses one file for the current bulletin:

static/bulletins/current-bulletin.pdf

The public link is:

/bulletins/current-bulletin.pdf

When the parish office replaces that file with the newest bulletin, the website link stays the same.

## Weekly Steps

1. Save the newest bulletin PDF.
2. Rename it exactly: current-bulletin.pdf
3. Replace the existing file in: static/bulletins/
4. Update the bulletin date in: data/bulletin.yaml
5. Preview the Bulletins page.
6. Confirm the View Current Bulletin button opens the correct PDF.

## Important Rule

The weekly bulletin is the source of truth for parish schedules, announcements, and office information.

Key information like Mass times, Confession times, office hours, and urgent schedule changes should also appear as normal website text, not only inside the PDF.
