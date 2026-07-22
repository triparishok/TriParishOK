# July 30 Formal-Domain Launch Runbook

This is the step-by-step checklist for moving the approved website from the GitHub Pages review address to `https://triparishok.org/`. Do not begin the cutover before July 30 or before the pastor's final approval.

## People and access needed

- Amber: GitHub repository and website verification
- Person with GoDaddy DNS access
- Parish office contact who can test parish email
- Angela or MinistryPlatform support contact if widgets are still unresolved

Do not share passwords by email or put credentials, API keys, widget tokens, or login details in this repository.

## Day before launch

1. Confirm `main` is clean and the latest GitHub review deployment passed.
2. Review the homepage, Mass and Confession, New Here, Giving, Forms, Faith Formation, Safe Environment, and all three parish pages on a phone and desktop.
3. Confirm the regular Mass and Confession schedule with the parish office.
4. Confirm every current notice has the correct start date, end date, parish, and action button.
5. Export or screenshot the complete GoDaddy DNS zone.
6. Record the current apex A record so rollback is possible: `198.12.232.179`.
7. Confirm the existing MX, SPF, Microsoft verification, and every mail-related DNS record will remain untouched.
8. Confirm the approved official parish photos have been added or consciously deferred.
9. Confirm the MinistryPlatform user-login widget still renders. Its GitHub Pages whitelist test passed on July 22, 2026. Test each additional widget separately after receiving its exact approved embed code.

## Final private preflight

Build the formal-domain version locally and require both audits to pass:

```bash
HUGO_BASEURL="https://triparishok.org/" HUGO_PARAMS_NOINDEX=false hugo --gc --config hugo.toml --destination /tmp/triparish-live-preflight
python3 scripts/audit-seo.py /tmp/triparish-live-preflight --expected-base "https://triparishok.org/" --expect-noindex no
python3 scripts/audit-internal-links.py /tmp/triparish-live-preflight --expected-base "https://triparishok.org/"
```

Do not continue if either audit reports an error.

## GitHub Pages setup

1. In the repository, open **Settings → Pages**.
2. Enter `triparishok.org` as the custom domain.
3. Save the custom domain.
4. Follow the exact DNS values GitHub displays at that time; do not rely on an old screenshot or copied instructions.
5. Keep the repository's `CNAME` file and deployment workflow consistent with `triparishok.org`.
6. Change the production workflow to use `https://triparishok.org/` and set `HUGO_PARAMS_NOINDEX=false` only in the approved launch commit.

## DNS cutover

1. In GoDaddy, change only the website-routing records required by GitHub Pages.
2. Do not alter MX or mail-related TXT/CNAME records.
3. Configure `www` according to GitHub's current instructions so it reaches the canonical apex domain.
4. Save the DNS changes and record exactly what changed.

## Verification before announcing launch

Verify all of the following:

- `https://triparishok.org/` loads over HTTPS.
- `https://www.triparishok.org/` reaches the intended canonical site.
- The browser certificate is valid and GitHub Pages allows **Enforce HTTPS**.
- Header logo, menu, footer, images, CSS, and all internal links work without `/TriParishOK/` path errors.
- Giving opens the approved St. Ann Realm page in the expected manner.
- Annual Catholic Appeal opens the Archdiocesan appeal page.
- The MinistryPlatform user login works on the formal domain. Each additional giving, event, update, prayer, or support widget works independently before it is exposed in navigation.
- Incoming and outgoing parish email still work.
- `https://triparishok.org/robots.txt` permits indexing and names the formal sitemap.
- `https://triparishok.org/sitemap.xml` contains only formal-domain URLs.
- Page source contains formal-domain canonical URLs and no `noindex` directive.
- The homepage, Mass page, and all three parish pages work on phone and desktop.

## Search setup after the site is stable

1. Verify the Google Search Console domain property through DNS.
2. Submit `https://triparishok.org/sitemap.xml`.
3. Inspect and request indexing for the homepage, Mass page, and three parish pages.
4. Update each verified Google Business Profile with its specific parish-page URL.
5. Ask the Archdiocese to correct stale directory information.
6. Run PageSpeed Insights for phone and desktop after the production cache has settled.

## Rollback plan

If the site, HTTPS, or email has a serious problem:

1. Do not delete the new GitHub deployment or repository history.
2. Restore only the website-routing DNS records to the recorded pre-launch values, including apex A `198.12.232.179` if it is still the confirmed old-site value.
3. Leave MX and mail records untouched.
4. Restore the last known-good deployment commit if the failure is in the site build rather than DNS.
5. Set the review/production build back to `noindex=true` if an incomplete build is publicly reachable.
6. Record the symptom, time, DNS values, and commit before attempting another cutover.

Do not redirect unrelated obsolete WordPress/store pages to the homepage. They should remain not found unless a genuine replacement exists.
