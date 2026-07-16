# SEO and Formal-Domain Launch Checklist

This document separates work that is safe to complete now from actions that require formal parish approval.

## Current safety rule

The repository default remains `noindex = true`.

The GitHub Pages review workflow explicitly builds with:

```bash
HUGO_PARAMS_NOINDEX=true
```

The formal-domain build becomes indexable only when it explicitly uses:

```bash
HUGO_BASEURL=https://triparishok.org/
HUGO_PARAMS_NOINDEX=false
```

Do not use the live values for the GitHub Pages project preview.

## Review build

```bash
rm -rf public

HUGO_BASEURL="https://triparishok.github.io/TriParishOK/" HUGO_PARAMS_NOINDEX=true hugo --gc --config hugo.toml

GITHUB_PAGES_PREFIX=/TriParishOK   python3 scripts/rewrite-gh-pages-paths.py public

python3 scripts/audit-seo.py public   --expected-base "https://triparishok.github.io/TriParishOK/"   --expect-noindex yes
```

## Formal-domain preflight without deploying

```bash
rm -rf public-live-check

HUGO_BASEURL="https://triparishok.org/" HUGO_PARAMS_NOINDEX=false hugo --gc   --config hugo.toml   --destination public-live-check

python3 scripts/audit-seo.py public-live-check   --expected-base "https://triparishok.org/"   --expect-noindex no

rm -rf public-live-check
```

This confirms that the future live build:

- does not contain `noindex`;
- uses `https://triparishok.org/` canonicals;
- produces a live robots file and sitemap;
- includes Organization and CatholicChurch structured data.

## Work requiring formal approval

1. Confirm the approved launch date and responsible parish contact.
2. Inventory the current DNS records before changing anything.
3. Preserve email-related MX, SPF, DKIM, and DMARC records.
4. Confirm whether `www.triparishok.org` should redirect to the apex domain.
5. Add the custom domain through GitHub Pages.
6. Change the deployment workflow to the formal-domain base URL.
7. Change `HUGO_PARAMS_NOINDEX` from `true` to `false`.
8. Remove the GitHub project-path rewrite step from the live deployment.
9. Add and verify the GitHub Pages CNAME configuration.
10. Make the required DNS changes using current GitHub Pages documentation.
11. Wait for the HTTPS certificate and enforce HTTPS.
12. Re-run the live SEO audit against the deployed formal domain.

## Old URL redirect preparation

Before launch, inventory indexed URLs from the current site and map each useful page to the closest new page.

Known candidates to verify include:

| Current path | Proposed destination |
| --- | --- |
| `/bulletin/` | `/bulletins/` |
| `/contact-us/` | `/contact/` |
| `/about/` | `/our-parishes/` |
| `/join-our-parish/` | `/new-here/` |

Do not redirect unrelated store, account, cart, or checkout pages to the homepage. Decide whether each should return a proper not-found response or receive a specific replacement page.

GitHub Pages does not provide ordinary server-side redirect rules. Choose and test the redirect method before DNS cutover.

## Search setup after launch

1. Create or recover the Google Search Console domain property.
2. Verify ownership through DNS.
3. Submit `https://triparishok.org/sitemap.xml`.
4. Inspect:
   - the homepage;
   - Mass and Confession;
   - St. Ann;
   - Our Lady of Perpetual Help;
   - Mother of Sorrows.
5. Request indexing only after the formal domain is stable.
6. Review indexing, mobile usability, and Core Web Vitals after Google gathers data.

## Local parish search

Before creating anything new, check for existing Google Business Profiles for all three parishes.

For each verified profile, confirm:

- official parish name;
- exact address;
- parish office phone;
- Catholic church category;
- the matching parish-page URL;
- exterior and sanctuary photos;
- accessibility and parking information;
- office hours only where staffed.

Do not list Mass times as ordinary business opening hours.

## Remaining enhancements

- Create a dedicated 1200 × 630 social-sharing image.
- Add favicons and an Apple touch icon.
- Add image width and height attributes where practical.
- Run PageSpeed Insights after the formal-domain launch.
- Ask the Archdiocese and trusted Catholic directories to link to the specific parish pages.
