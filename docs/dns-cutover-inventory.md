# triparishok.org DNS Cutover Inventory

Recorded July 21, 2026. This is a public-record snapshot for the July 30 website launch. It does not replace an export or screenshot of the complete DNS zone from the domain provider.

## Current provider and website routing

| Record | Current value | Launch treatment |
| --- | --- | --- |
| Nameservers | `ns53.domaincontrol.com`, `ns54.domaincontrol.com` | Preserve unless a separate, approved migration is planned |
| Apex A | `198.12.232.179` | Old website server; replace only during the approved GitHub Pages cutover |
| Apex AAAA | None found | Do not add unless GitHub's current instructions require it |
| `www` CNAME | `triparishok.org` | Review during cutover so `www` reaches the approved canonical domain |
| CAA | None found | No action required solely for launch |

## Email records — preserve

| Record | Current value |
| --- | --- |
| MX | `0 mx1-usg1.ppe-hosted.com` |
| MX | `0 mx2-usg1.ppe-hosted.com` |
| MX | `0 mx3-usg1.ppe-hosted.com` |
| SPF TXT | `v=spf1 include:_spf-usg1.ppe-hosted.com include:secureserver.net ~all` |
| Microsoft verification TXT | `NETORG18107623.onmicrosoft.com` |

No public DMARC record was found at `_dmarc.triparishok.org`. No record was found under the common DKIM selectors checked (`selector1`, `selector2`, `default`, `google`, and `k1`). This is an email-security follow-up, not a reason to invent or add records during the website cutover. Confirm the mail provider's intended DKIM and DMARC configuration separately.

## Before changing DNS

1. Export or screenshot the complete DNS zone in GoDaddy.
2. Confirm that the three MX records, both apex TXT records, and every mail-related CNAME/TXT record remain untouched.
3. Confirm whether both `triparishok.org` and `www.triparishok.org` should work, with the apex domain remaining canonical.
4. Add the custom domain in GitHub Pages and follow GitHub's current DNS values exactly.
5. Do not enable the indexable production build until the custom domain, HTTPS certificate, and internal links are verified.

## After changing DNS

Verify:

- the apex and `www` site addresses;
- HTTPS and certificate validity;
- incoming and outgoing parish email;
- MX, SPF, Microsoft verification, and any provider-confirmed DKIM/DMARC records;
- the live sitemap, robots file, canonical URLs, and internal links.

