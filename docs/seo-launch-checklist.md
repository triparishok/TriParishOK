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

python3 scripts/audit-seo.py public   --expected-base "https://triparishok.github.io/TriParishOK/"   --expect-noindex yes

python3 scripts/audit-internal-links.py public   --expected-base "https://triparishok.github.io/TriParishOK/"
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
8. Confirm the internal-link audit passes with the formal-domain base URL.
9. Add and verify the GitHub Pages CNAME configuration.
10. Make the required DNS changes using current GitHub Pages documentation.
11. Wait for the HTTPS certificate and enforce HTTPS.
12. Re-run the live SEO audit against the deployed formal domain.

## Old URL redirect preparation

The WordPress sitemap was inventoried on July 21, 2026. Useful parish URLs receive Hugo alias pages so old bookmarks and search results reach the closest replacement after cutover.

| Current path | Destination | Disposition |
| --- | --- | --- |
| `/bulletin/` | `/bulletins/` | Alias added |
| `/about/` | `/our-parishes/` | Alias added |
| `/join-our-parish/` | `/new-here/` | Alias added |
| `/adult-ed-scripture-study/` | `/faith-formation/` | Alias added |
| `/prolife/` | `/catholic-links/` | Alias added |
| `/vocations/` | `/catholic-links/` | Alias added |
| `/contact/` | `/contact/` | Path preserved |
| `/events/` | `/events/` | Path preserved; MinistryPlatform integration pending |
| `/becoming-catholic/` | `/becoming-catholic/` | Path preserved |
| `/forms/` | `/forms/` | Path preserved |
| `/catholic-links/` | `/catholic-links/` | Path preserved |

The following obsolete WordPress, store, and unrelated template URLs intentionally receive no homepage redirect: `/hello-world/`, `/testimonials/`, `/shop/`, `/checkout/`, `/my-account/`, `/cart/`, `/services/`, `/projects/`, `/map/`, `/category/uncategorized/`, `/author/admin/`, and the `ae_global_templates` query URLs. After cutover they should resolve as not found rather than being misrepresented as equivalent parish content.

GitHub Pages does not provide ordinary server-side redirect rules. Hugo aliases are client-side compatibility pages, not HTTP 301 responses. Confirm each alias works on the formal domain after cutover.

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

- Dedicated 1200 × 630 social-sharing artwork is complete.
- Favicons and an Apple touch icon are complete.
- Explicit image width and height attributes are complete for rendered content images.
- The GitHub Pages review build scored 100 for Performance, Accessibility, and Best Practices on both mobile and desktop. Re-run PageSpeed Insights after the formal-domain launch.
- Replace temporary parish-building photographs when the approved official photographs arrive. The topical AI-generated header artwork is separately identified in `data/page_headers.yaml` and may remain until better approved photography is available.
- MinistryPlatform user-login widget passed a live whitelist test on the GitHub Pages review origin on July 22, 2026. Giving, event, update, prayer, and support widgets still require their exact approved embed snippets or configuration identifiers before implementation.
- Correct and verify Google Business Profiles and request corrections to stale Archdiocesan directory information.
- Ask the Archdiocese and trusted Catholic directories to link to the specific parish pages.
