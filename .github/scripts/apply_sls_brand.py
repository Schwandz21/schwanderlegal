from pathlib import Path
import re

p = Path('index.html')
s = p.read_text()

canonical = '  <link rel="canonical" href="https://schwanderlegal.com/" />'
if '/assets/favicon-64.jpg' not in s:
    if canonical not in s:
        raise SystemExit('Canonical link not found')
    s = s.replace(
        canonical,
        canonical
        + '\n  <link rel="icon" type="image/jpeg" sizes="64x64" href="/assets/favicon-64.jpg?v=20260828" />'
        + '\n  <link rel="shortcut icon" href="/assets/favicon-64.jpg?v=20260828" />',
        1,
    )

og = '  <meta property="og:site_name" content="Schwander Legal Services, P.A." />'
if 'property="og:image"' not in s:
    if og not in s:
        raise SystemExit('Open Graph site-name marker not found')
    s = s.replace(
        og,
        og
        + '\n  <meta property="og:image" content="https://schwanderlegal.com/assets/sls-wordmark-header.jpg?v=20260828" />'
        + '\n  <meta property="og:image:alt" content="Schwander Legal Services, P.A. official wordmark" />',
        1,
    )


def replace_css(text, selector, replacement):
    pattern = rf'^    {re.escape(selector)} \{{.*?^    \}}'
    text, count = re.subn(pattern, replacement, text, count=1, flags=re.M | re.S)
    if count != 1:
        raise SystemExit(f'CSS selector {selector} matched {count} blocks')
    return text


s = replace_css(
    s,
    '.site-header',
    '''    .site-header {
      position: sticky;
      top: 0;
      z-index: 20;
      background: linear-gradient(90deg, #021f43 0%, #06365f 58%, #0a4677 100%);
      border-bottom: 1px solid rgba(198, 160, 81, 0.72);
      box-shadow: 0 8px 28px rgba(2, 31, 67, 0.18);
    }''',
)

s = replace_css(
    s,
    '.nav',
    '''    .nav {
      max-width: var(--max);
      margin: 0 auto;
      min-height: 102px;
      padding: 9px 22px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 28px;
    }''',
)

s = replace_css(
    s,
    '.brand',
    '''    .brand {
      display: flex;
      align-items: center;
      flex: 0 1 340px;
      min-width: 255px;
    }''',
)

marker = '''    .brand small {
      display: block;
      margin-top: -3px;
      color: var(--muted);
      font-size: 11px;
      font-weight: 800;
      letter-spacing: 0.09em;
      text-transform: uppercase;
    }'''
if '.brand-logo {' not in s:
    if marker not in s:
        raise SystemExit('Brand small marker not found')
    s = s.replace(
        marker,
        marker
        + '''

    .brand-logo {
      display: block;
      width: min(330px, 35vw);
      max-height: 86px;
      height: auto;
      object-fit: contain;
      object-position: left center;
    }''',
        1,
    )

s = replace_css(
    s,
    '.nav-links',
    '''    .nav-links {
      display: flex;
      align-items: center;
      gap: 20px;
      font-size: 14px;
      color: rgba(255, 255, 255, 0.92);
      font-weight: 700;
    }''',
)

s = replace_css(
    s,
    '.nav-links a:hover',
    '''    .nav-links a:hover {
      color: #f5d98c;
    }''',
)

old_brand = '''      <a class="brand" href="#top" aria-label="Schwander Legal Services home">
        <span class="brand-mark" aria-hidden="true">S</span>

        <span>
          Schwander Legal Services, P.A.
          <small>Delaware Refinance Closing Coverage</small>
        </span>
      </a>'''
new_brand = '''      <a class="brand" href="#top" aria-label="Schwander Legal Services, P.A. home">
        <img class="brand-logo" src="/assets/sls-wordmark-header.jpg?v=20260828" alt="Schwander Legal Services, P.A." width="560" height="161" decoding="async" />
      </a>'''
if old_brand not in s:
    raise SystemExit('Legacy header block not found')
s = s.replace(old_brand, new_brand, 1)

mobile = '''      .nav {
        min-height: 68px;
      }'''
mobile_new = '''      .nav {
        min-height: 76px;
        padding: 7px 14px;
        gap: 12px;
      }

      .brand {
        min-width: 0;
        flex: 1 1 auto;
      }

      .brand-logo {
        width: min(245px, 58vw);
        max-height: 68px;
      }'''
if mobile not in s:
    raise SystemExit('Mobile nav marker not found')
s = s.replace(mobile, mobile_new, 1)

if '<span class="brand-mark"' in s:
    raise SystemExit('Legacy generic S tile survived')
if s.count('mailto:') != 6:
    raise SystemExit('Unexpected mailto count: ' + str(s.count('mailto:')))
for required in (
    'class="brand-logo"',
    '/assets/favicon-64.jpg?v=20260828',
    '/assets/sls-wordmark-header.jpg?v=20260828',
    'Request Rate Sheet',
    'Delaware Refinance Closing Coverage for Your Existing Files',
):
    if required not in s:
        raise SystemExit('Missing required marker: ' + required)

p.write_text(s)
