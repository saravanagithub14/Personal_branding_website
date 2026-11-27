# SEO audit checklist

Written 2026-11-24 from the snapshots in `seo-docs/snapshots/` (first crawl, 172 pages). Used by `/seo-audit`.

- Every rule cites the Google doc page it comes from. No doc URL, no rule.
- Severity: **high** means the docs describe it as blocking indexing or a feature, or as a policy problem, or it
  breaks the page for visitors. **medium** means a documented best practice with a visible effect on this site.
  **low** means optional, cosmetic, or only relevant after launch.
- CLAUDE.md wins over generic doc advice. Rules marked [CLAUDE.md] have a site decision that applies.
- Rules marked [after launch] cannot be checked in the repo. Report them as TODO until the site is live.
- The docs say none of this guarantees crawling, indexing or ranking. Never promise an effect.

## 1. SEO fundamentals

Covers: Introduction, Search Essentials, SEO Starter Guide, Optimizing for generative AI search, How Google
Search works, Do you need an SEO?

| Id | Check | Severity | Doc URL |
| --- | --- | --- | --- |
| INTRO-01 | Every page a visitor should find is content-first and search-friendly: real text, reachable, described. | medium | https://developers.google.com/search/docs |
| ESS-01 | Googlebot is not blocked: no login, no robots block, no `noindex` on any of the 13 pages. | high | https://developers.google.com/search/docs/essentials/technical |
| ESS-02 | Each page is served with HTTP 200 on the live host. [after launch] | high | https://developers.google.com/search/docs/essentials/technical |
| ESS-03 | Each page has indexable text content in a supported file type (HTML). | high | https://developers.google.com/search/docs/essentials/technical |
| ESS-04 | Words people search for appear in the title and main heading, and in alt text and link text where natural. [CLAUDE.md: keyword map; homepage H1 is Saravana's choice] | medium | https://developers.google.com/search/docs/essentials |
| SPAM-01 | No keyword stuffing in copy, titles, alt text or link text. [CLAUDE.md: each keyword two or three times] | high | https://developers.google.com/search/docs/essentials/spam-policies |
| SPAM-02 | No hidden text or links placed only for search engines. Accordions and hover cards that show their text to visitors are fine. | high | https://developers.google.com/search/docs/essentials/spam-policies |
| SPAM-03 | Landing pages are not doorway pages: each one is useful on its own and not substantially similar to another. | medium | https://developers.google.com/search/docs/essentials/spam-policies |
| SPAM-04 | No copied third-party content is published as site pages (this includes `seo-docs/snapshots/`). | medium | https://developers.google.com/search/docs/essentials/spam-policies |
| SPAM-05 | No script interferes with the browser back button or misleads visitors about what a control does. | high | https://developers.google.com/search/docs/essentials/spam-policies |
| HELP-01 | Content shows first-hand experience and makes clear who is behind it (About page, consistent facts). | medium | https://developers.google.com/search/docs/fundamentals/creating-helpful-content |
| HELP-02 | No easily checked factual errors, and facts agree across pages. [CLAUDE.md: facts and open items] | medium | https://developers.google.com/search/docs/fundamentals/creating-helpful-content |
| HELP-03 | Pages look finished: no placeholder labels, empty cards or skeletons shown to visitors. [CLAUDE.md: definition of done] | medium | https://developers.google.com/search/docs/fundamentals/creating-helpful-content |
| HELP-04 | The main heading is a descriptive summary of the page and not exaggerated. | low | https://developers.google.com/search/docs/fundamentals/creating-helpful-content |
| START-01 | Text is easy to read: paragraphs, sections and headings that help people move around. | low | https://developers.google.com/search/docs/fundamentals/seo-starter-guide |
| START-02 | Little duplicate content: the same information should not be repeated across pages without a reason. | medium | https://developers.google.com/search/docs/fundamentals/seo-starter-guide |
| START-03 | Headings: one H1 and a logical order. The docs say order does not matter to Search, it helps screen readers. [CLAUDE.md: one H1 is a site rule] | low | https://developers.google.com/search/docs/fundamentals/seo-starter-guide |
| START-04 | CSS and JavaScript that the page needs are not blocked from Google. | medium | https://developers.google.com/search/docs/fundamentals/seo-starter-guide |
| GEN-01 | Eligible for AI features: the page can be indexed and shown with a snippet (no `nosnippet`, `max-snippet:0`, `noindex`). | high | https://developers.google.com/search/docs/appearance/ai-features |
| GEN-02 | The site is included in Search generative AI features in Search Console settings. [after launch] | medium | https://developers.google.com/search/docs/fundamentals/ai-optimization-guide |
| GEN-03 | Important content is in text, not only in images. | high | https://developers.google.com/search/docs/appearance/ai-features |
| GEN-04 | Content is unique and first-hand, not commodity content that repeats what is already available. | medium | https://developers.google.com/search/docs/fundamentals/ai-optimization-guide |
| GEN-05 | Text is supported by relevant, high-quality images or video where it makes sense. | medium | https://developers.google.com/search/docs/fundamentals/ai-optimization-guide |
| GEN-06 | No effort spent on llms.txt, chunking or special AI markup for Google: not needed and not used. Informational. | low | https://developers.google.com/search/docs/fundamentals/ai-optimization-guide |
| GEN-07 | Any generative AI control (`Google-Extended`, `GoogleOther`, snippet limits) is a deliberate choice, not an accident. | medium | https://developers.google.com/search/docs/fundamentals/gen-ai-controls |
| GEN-08 | AI-assisted copy is accurate and adds value. [CLAUDE.md: copy written by Claude uses only confirmed facts] | medium | https://developers.google.com/search/docs/fundamentals/using-gen-ai-content |
| HOW-01 | Every page can be discovered by links from other pages or the sitemap, then crawled and rendered. | high | https://developers.google.com/search/docs/fundamentals/how-search-works |
| SEOPRO-01 | Advice from SEO vendors or tools is checked against this documentation before it is applied. Informational. | low | https://developers.google.com/search/docs/fundamentals/do-i-need-seo |

## 2. Crawling and indexing

Covers: Sitemaps, robots.txt, Meta tags, Crawler management, Removals, Canonicalization, Redirects, JavaScript SEO.

| Id | Check | Severity | Doc URL |
| --- | --- | --- | --- |
| SITEMAP-01 | `sitemap.xml` is UTF-8, valid XML, at the site root, and lists all 13 pages. | medium | https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap |
| SITEMAP-02 | Sitemap URLs are absolute, use the live domain and equal the canonical URLs. | high | https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap |
| SITEMAP-03 | `<lastmod>` matches the last significant change to each page. | low | https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap |
| SITEMAP-04 | The sitemap is submitted in Search Console or named in robots.txt. [after launch] | low | https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap |
| ROBOTS-01 | `robots.txt` does not block any page, or any CSS, JS or image the pages need. | high | https://developers.google.com/search/docs/crawling-indexing/robots/intro |
| ROBOTS-02 | `robots.txt` has a `Sitemap:` line with the full live URL. | medium | https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap |
| META-01 | `<head>` contains only valid elements, so Google reads all of it. | medium | https://developers.google.com/search/docs/crawling-indexing/valid-page-metadata |
| META-02 | Charset and viewport meta tags are present. | medium | https://developers.google.com/search/docs/crawling-indexing/special-tags |
| META-03 | No accidental `noindex`, `nofollow`, `nosnippet` or `none` in a robots meta tag. `index, follow` is the default and not needed. | high | https://developers.google.com/search/docs/crawling-indexing/robots-meta-tag |
| META-04 | `noindex` is only used on purpose, and never on a URL that robots.txt blocks. | high | https://developers.google.com/search/docs/crawling-indexing/block-indexing |
| META-05 | No `meta keywords`: Google Search does not use it. | low | https://developers.google.com/search/docs/crawling-indexing/special-tags |
| LINK-01 | Links are `<a>` elements with an `href` that resolves. No dead links or dead fragments, no script-only links. | high | https://developers.google.com/search/docs/crawling-indexing/links-crawlable |
| LINK-02 | Anchor text is descriptive and not generic. Icon-only or image links have a name. | medium | https://developers.google.com/search/docs/crawling-indexing/links-crawlable |
| LINK-03 | Every page has at least one internal link pointing to it. | medium | https://developers.google.com/search/docs/crawling-indexing/links-crawlable |
| LINK-04 | `nofollow`, `sponsored` or `ugc` only where they apply (paid, untrusted or user links). | low | https://developers.google.com/search/docs/crawling-indexing/qualify-outbound-links |
| URL-01 | URLs use readable words and hyphens, with no fragments that change content. | low | https://developers.google.com/search/docs/crawling-indexing/url-structure |
| CRAWL-01 | After launch or a large change, request recrawling with URL Inspection or the sitemap. [after launch] | low | https://developers.google.com/search/docs/crawling-indexing/ask-google-to-recrawl |
| CRAWL-02 | No availability errors in the Crawl Stats report. [after launch] | medium | https://developers.google.com/search/docs/crawling-indexing/troubleshoot-crawling-errors |
| CRAWL-03 | Each HTML, CSS and JS file is under the 2 MB that Googlebot reads. | medium | https://developers.google.com/search/docs/crawling-indexing/googlebot |
| MOBILE-01 | Responsive design with the same content, headings and structured data on mobile. | high | https://developers.google.com/search/docs/crawling-indexing/mobile/mobile-sites-mobile-first-indexing |
| MOBILE-02 | Primary content does not need a tap, swipe or typing before it is in the page. | high | https://developers.google.com/search/docs/crawling-indexing/mobile/mobile-sites-mobile-first-indexing |
| REMOVE-01 | Files that should not be public (notes, tools, test pages, doc snapshots) are not deployed, or are kept out of Search. | medium | https://developers.google.com/search/docs/crawling-indexing/control-what-you-share |
| REMOVE-02 | Images that must not appear in Search are blocked with robots.txt or `noindex` headers. | low | https://developers.google.com/search/docs/crawling-indexing/prevent-images-on-your-page |
| CANON-01 | Each page has one self-referencing absolute `rel="canonical"` on the live domain, without a fragment. | high | https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls |
| CANON-02 | Canonical, `og:url` and the sitemap agree on the same URL for each page. | high | https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls |
| CANON-03 | Internal links point to the canonical URL, not to a duplicate. [CLAUDE.md: links use explicit `.html` so pages open from disk] | medium | https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls |
| CANON-04 | JavaScript does not change the canonical set in the HTML. | medium | https://developers.google.com/search/docs/crawling-indexing/javascript/javascript-seo-basics |
| REDIR-01 | One preferred URL per page: HTTP to HTTPS, www or non-www, and `/index.html` to `/` use permanent redirects. [after launch] | medium | https://developers.google.com/search/docs/crawling-indexing/301-redirects |
| REDIR-02 | Any URL that is renamed later gets a permanent redirect from the old address. | medium | https://developers.google.com/search/docs/crawling-indexing/site-move-with-url-changes |
| JS-01 | Main content, titles, descriptions and links are in the HTML, or in the rendered HTML, without user interaction. | high | https://developers.google.com/search/docs/crawling-indexing/javascript/javascript-seo-basics |
| JS-02 | Missing pages return a real 404 status. [after launch] | medium | https://developers.google.com/search/docs/crawling-indexing/javascript/javascript-seo-basics |
| JS-03 | CSS and JS file names change when the content changes (fingerprinting), because Google caches them for a long time. | low | https://developers.google.com/search/docs/crawling-indexing/javascript/fix-search-javascript |
| LAZY-01 | Lazy loading uses the browser or IntersectionObserver and is not used on content visible at first view. | medium | https://developers.google.com/search/docs/crawling-indexing/javascript/lazy-loading |

## 3. Ranking and search appearance

Covers: Visual Elements gallery, Title links, Snippets, Images, Videos, Structured data, Favicons, and ranking.

| Id | Check | Severity | Doc URL |
| --- | --- | --- | --- |
| TITLE-01 | Every page has a `<title>`, unique on the site. | high | https://developers.google.com/search/docs/appearance/title-link |
| TITLE-02 | Titles are descriptive and concise, branded briefly, with no stuffing or boilerplate. There is no length limit in the docs, long titles are cut to fit the device. [CLAUDE.md: landing page title is fixed] | medium | https://developers.google.com/search/docs/appearance/title-link |
| TITLE-03 | One clear main title on the page, in the first visible H1, consistent with the `<title>`. | medium | https://developers.google.com/search/docs/appearance/title-link |
| SNIP-01 | Every page has a meta description, unique on the site. | medium | https://developers.google.com/search/docs/appearance/snippet |
| SNIP-02 | Descriptions summarise the page in sentences, not keyword lists. There is no length limit in the docs, snippets are truncated. [CLAUDE.md: landing page description is fixed] | low | https://developers.google.com/search/docs/appearance/snippet |
| SNIP-03 | No accidental opt-out from featured snippets (`nosnippet`, very low `max-snippet`). | medium | https://developers.google.com/search/docs/appearance/featured-snippets |
| VIS-01 | Attribution elements are provided: favicon, site name, breadcrumb. | low | https://developers.google.com/search/docs/appearance/visual-elements-gallery |
| SITENAME-01 | The homepage has `WebSite` structured data with `name` and `url`, matching `og:site_name`. | medium | https://developers.google.com/search/docs/appearance/site-names |
| FAV-01 | The homepage links a favicon with `rel="icon"` (or an apple-touch-icon), crawlable at a stable URL. | medium | https://developers.google.com/search/docs/appearance/favicon-in-search |
| FAV-02 | The favicon is square, larger than 48x48px, in BMP, GIF, ICO, PNG, JPEG, PPM or TIFF. SVG is not in the supported list. | medium | https://developers.google.com/search/docs/appearance/favicon-in-search |
| IMG-01 | Images that matter use `<img src>`, and the file exists and loads. | high | https://developers.google.com/search/docs/appearance/google-images |
| IMG-02 | Alt text is descriptive and not stuffed. [CLAUDE.md: publication covers are decorative with `alt=""`] | medium | https://developers.google.com/search/docs/appearance/google-images |
| IMG-03 | Supported format (BMP, GIF, JPEG, PNG, WebP, SVG, AVIF) with a matching extension and a descriptive file name. | low | https://developers.google.com/search/docs/appearance/google-images |
| IMG-04 | Images are optimised for speed and quality (size on disk suits the display size, responsive where useful). | medium | https://developers.google.com/search/docs/appearance/google-images |
| IMG-05 | `og:image` points to a real, relevant, high-resolution image on the live domain. | medium | https://developers.google.com/search/docs/appearance/google-images |
| VIDEO-01 | Videos, if any, use standard elements, sit on a page near relevant text and have a stable thumbnail. | medium | https://developers.google.com/search/docs/appearance/video |
| SD-01 | JSON-LD parses, is in a supported format and is placed on the page it describes. | high | https://developers.google.com/search/docs/appearance/structured-data/sd-policies |
| SD-02 | Structured data matches what visitors can see. Nothing invented, hidden or misleading. | high | https://developers.google.com/search/docs/appearance/structured-data/sd-policies |
| SD-03 | All image and page URLs in structured data are real and crawlable. | medium | https://developers.google.com/search/docs/appearance/structured-data/sd-policies |
| SD-04 | Local business markup (`ProfessionalService` is a `LocalBusiness` subtype) has the required `name` and `address`. Recommended properties only when the fact is confirmed. [CLAUDE.md: no phone number] | high | https://developers.google.com/search/docs/appearance/structured-data/local-business |
| SD-05 | Breadcrumb markup has at least two `ListItem`s, each with `position`, `name` and `item` (optional on the last). | medium | https://developers.google.com/search/docs/appearance/structured-data/breadcrumb |
| SD-06 | `FAQPage` markup is not counted on for a rich result: Google stopped showing it on 7 May 2026 and has removed its documentation. [CLAUDE.md: the visible FAQ stays either way] | low | https://developers.google.com/search/updates |
| SD-07 | Types used for a rich result are in the supported gallery. Others (`Service`, `Person`) are allowed but earn none. | low | https://developers.google.com/search/docs/appearance/structured-data/search-gallery |
| SD-08 | Markup added by JavaScript is present in the rendered HTML (Rich Results Test, or URL Inspection for unsupported types). | medium | https://developers.google.com/search/docs/appearance/structured-data/generate-structured-data-with-javascript |
| SD-09 | `QAPage` is not used for the FAQ. | medium | https://developers.google.com/search/docs/appearance/structured-data/qapage |
| SD-10 | Optional: the About page may use `ProfilePage` with a `Person` as `mainEntity`. An "About Me" page is a listed valid use. | low | https://developers.google.com/search/docs/appearance/structured-data/profile-page |
| SD-11 | Review or rating markup only for real reviews. [CLAUDE.md: no testimonials yet] | high | https://developers.google.com/search/docs/appearance/structured-data/review-snippet |
| PX-01 | HTTPS on the live site. [after launch] | high | https://developers.google.com/search/docs/appearance/page-experience |
| PX-02 | Core Web Vitals are good: LCP within 2.5 s, INP under 200 ms, CLS under 0.1. [after launch for field data] | medium | https://developers.google.com/search/docs/appearance/core-web-vitals |
| PX-03 | Local causes of slow loading or layout shift are handled: image width and height, no oversized files, few render-blocking files. | medium | https://developers.google.com/search/docs/appearance/core-web-vitals |
| PX-04 | No intrusive interstitials or dialogs that cover the content on arrival. | medium | https://developers.google.com/search/docs/appearance/avoid-intrusive-interstitials |
| BIZ-01 | Business details are established with Google: Business Profile and verified Search Console. [after launch] | medium | https://developers.google.com/search/docs/appearance/establish-business-details |
| RANK-01 | No claim or plan that relies on a guaranteed position: results are ordered by helpfulness to the query. | low | https://developers.google.com/search/docs/ranking/principles-for-ranking-results |

## 4. Site-specific guides

Covers: Ecommerce, International and multilingual sites.

| Id | Check | Severity | Doc URL |
| --- | --- | --- | --- |
| ECOM-01 | Not a shop: no product or price markup on the site. [CLAUDE.md: no prices] | low | https://developers.google.com/search/docs/specialty/ecommerce |
| ECOM-02 | Important pages are linked from the menu and the homepage, so their importance is clear from links. | medium | https://developers.google.com/search/docs/specialty/ecommerce/help-google-understand-your-ecommerce-site-structure |
| INTL-01 | One obvious language per page. Google reads the visible content, not the `lang` attribute, so `lang` is for browsers and screen readers. | low | https://developers.google.com/search/docs/specialty/international/managing-multi-regional-sites |
| INTL-02 | `hreflang` only if translated versions exist. The site is English only, so none is expected. | low | https://developers.google.com/search/docs/specialty/international/localized-versions |

## 5. Data analysis

Covers: Identify traffic from Google Search, Debug traffic drops, Search Console with Google Analytics, Analyze
social and video platform content. All of these need the live site.

| Id | Check | Severity | Doc URL |
| --- | --- | --- | --- |
| DATA-01 | Site verified in Search Console and checked about once a month. [after launch] | medium | https://developers.google.com/search/docs/monitor-debug/search-console-start |
| DATA-02 | If analytics or server logs are used, Google traffic is identified by the `Referer` header. No analytics on the site now. [after launch] | low | https://developers.google.com/search/docs/monitor-debug/identify-google-search-traffic |
| DATA-03 | If analytics is added, Search Console clicks and Analytics sessions are read together and not expected to be equal. [after launch] | low | https://developers.google.com/search/docs/monitor-debug/google-analytics-search-console |
| DATA-04 | Traffic drops are diagnosed with the Performance report before any page is changed. [after launch] | low | https://developers.google.com/search/docs/monitor-debug/debugging-search-traffic-drops |
| DATA-05 | Optional: add supported social accounts (for example Instagram) as Search Console properties. [after launch] | low | https://developers.google.com/search/docs/monitor-debug/analyze-social-video-content |
| DATA-06 | No security or hacked-content issues in Search Console. [after launch] | high | https://developers.google.com/search/docs/monitor-debug/security |

## Known gaps

- Google has moved its crawler list, robots.txt specification, HTTP status code and crawl budget pages to
  `https://developers.google.com/crawling/docs/`. That is outside the crawl scope in CLAUDE.md, so those pages have
  no snapshot and no rule here. Adding that path to the scope is a decision for Saravana.
- The docs recommend nothing specific about Open Graph tags other than `og:title` (title links), `og:site_name`
  (site names) and `og:image` (images). Any other Open Graph check is a site choice from CLAUDE.md.

## Retired rules

None yet. When a rule is retired, keep its id here with the date and the reason, and do not reuse the id.
