# MinistryPlatform Widget Test Record

## Successful GitHub Pages whitelist test

Date: July 22, 2026

Test origin: `https://triparishok.github.io`

Test page path: `/TriParishOK/widget-retest/` (temporary, unlinked, and removed immediately after testing)

Code tested:

```html
<script id="MPWidgets" src="https://mp.archokc.org/widgets/dist/MPWidgets.js"></script>
<mpp-user-login></mpp-user-login>
```

Results:

- The MinistryPlatform script loaded.
- The `mpp-user-login` custom element rendered a visible **Login** control.
- Selecting **Login** opened the Archdiocese of Oklahoma City login page.
- The login page offered password login, one-time code, password reset, account creation, and language selection.
- The previous permitted-URL/connection failure did not recur.
- Signed-out console messages stating that no token was available and the user was not authenticated were expected and did not prevent the widget from working.

The temporary public test page was removed, and the cleanup GitHub Pages deployment completed successfully.

## Approved production widget set

The Archdiocese supplied the complete approved widget set:

- user login;
- event finder;
- event details;
- event checkout.

The event pages use the current site base URL automatically, so their return links work on the GitHub Pages review site and will change to `https://triparishok.org/` with the approved formal-domain build.

Giving remains linked to St. Ann's Realm giving page. Prayer/support requests use the parish contact path, and parish updates use the bulletin and official social-media paths. No additional MinistryPlatform widgets are pending.

Test the event flow on the GitHub Pages review origin after deployment, then test it again on `https://triparishok.org/` during formal launch verification.
