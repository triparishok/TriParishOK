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

## Still required

Do not invent widget markup or identifiers. Obtain and test the exact approved embed code or configuration for:

- giving;
- events;
- parish updates;
- prayer requests;
- support requests.

Test each widget first on the GitHub Pages review origin, then again on `https://triparishok.org/` before launch exposure.
