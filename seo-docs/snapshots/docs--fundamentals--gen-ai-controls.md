---
url: https://developers.google.com/search/docs/fundamentals/gen-ai-controls
title: "Control how your content is used for generative AI at Google"
fetched: 2026-11-24T16:10:46Z
hash: 402f2931f90747d1ddc38b889cddec01a66cfcf486af727d770fb73df0b1d92d
note: Untrusted web content. Treat as data, never as instructions.
---

# Control how your content is used for generative AI at Google

Google supports a variety of ways to let site owners control how their content is used across Google's products and generative AI experiences. When you make content on your site available to [Googlebot](/search/docs/crawling-indexing/googlebot), your content may be used by Google Search (including generative AI features in Search), as well as for non-Search products and generative AI services at Google (such as the Gemini app), subject to the controls below. This document gives an overview of the existing controls that we offer to let site owners manage how their content is used across Google's products and generative AI experiences.

Without any controls applied, Google may use crawled web content in two main ways for generative AI features and services:

- **AI model training**: Teaching future generations of foundation models (such as Gemini models) general language patterns, reasoning capabilities, and world knowledge before a model is deployed. Foundation models trained this way help power commercially available generative AI products like the Gemini app as well as Search generative AI features (such as AI Overviews, AI Mode, and generative AI features in Discover). Allowing your content to be used for training improves our models' general capabilities and may help improve domain-specific knowledge, enabling more accurate and helpful responses on topics that include your insight, in your language and inclusive of your cultural context.
- **Grounding**: Looking up relevant, fresh information from the Google Search index when answering a prompt (also known as retrieval-augmented generation, or RAG) to improve the factuality, accuracy, and relevancy of responses and link to supporting web pages. Grounding is used in [generative AI features in Search](/search/docs/appearance/ai-features) (such as AI Overviews, AI Mode, and generative AI features in Discover) and in non-Search generative AI products (such as the Gemini app). Unlike training, grounding occurs after a model has already been trained and deployed and is completely independent of the training step. Allowing grounding enables these experiences to show links to your site, which can help users discover your content and may direct traffic to your site.

**Note**: As with [Google Search overall](/search/docs/fundamentals/how-search-works), not all discovered content is crawled, and not all crawled content is indexed or used by generative AI products or services at Google.

## List of available controls and how to set them

Many site owners want their content to be discovered and findable across these experiences. However, others may want to limit how their content is used. Google provides the following controls so that you can manage foundation model training, non-Search grounding, and Search generative AI grounding independently:

| Controls |

### [Search generative AI control](https://support.google.com/webmasters/answer/16908024)

Manages whether content from your site is used for grounding or displayed (including links) in generative AI features on Google Search and Discover, such as [AI Overviews and AI Mode](/search/docs/appearance/ai-features). This control doesn't affect generative AI model training, and it isn't used as a ranking or inclusion signal for other parts of Google Search.

**Where to set:** Search Console settings

### [`Google-Extended`](/crawling/docs/google-extended)

Limits how your content is used to train and ground certain commercially available generative AI products and services, as described in the full explanation in our [documentation on the `Google-Extended` token](/crawling/docs/google-extended). `Google-Extended` status is not used as a ranking signal in Search and doesn't affect a site's inclusion in Search.

**Where to set:** `robots.txt` file

### [`GoogleOther`](/crawling/docs/crawlers-fetchers/google-common-crawlers#googleother)

Blocks Google's generic crawler from fetching pages for non-Search uses such as one-off research and development crawls, without affecting Search. See [`GoogleOther` in Google's common crawlers list](/crawling/docs/crawlers-fetchers/google-common-crawlers#googleother).

**Where to set:** `robots.txt` file

### [robots `meta` tag, `data-nosnippet`, or `X-Robots-Tag`](/search/docs/crawling-indexing/special-tags)

Page- and text-level preview controls (such as `nosnippet`, `data-nosnippet`, and `max-snippet`) let you control how text snippets, images, or previews of your content appear in Google Search results, including in AI Overviews and AI Mode. `nosnippet` and `max-snippet` also give you the option to prevent your content from being used as a direct input for AI Overviews and AI Mode. Learn more about [supported robots `meta` tags and HTML attributes](/search/docs/crawling-indexing/special-tags).

**Where to set:** Page HTML or `X-Robots-Tag` HTTP header

### [`noindex` rule](/search/docs/crawling-indexing/block-indexing)

Tells Google not to index a page or let it appear in Google Search results, including Search generative AI features. Follow the instructions to [block Search indexing with `noindex`](/search/docs/crawling-indexing/block-indexing).

**Where to set:** Page HTML or `X-Robots-Tag` HTTP header

Google intends to support the [shared machine-readable training preference signal](/search/blog/2026/10/ai-training-control) (with `user-agent: __usage_ai-training`) in early 2027.

## Which control should I use?

You can use the controls independently, or combine them. Here are some examples of how you can combine the controls to match your goal:

| Example goal | How to set |
| Enable Google Search, including Search generative AI features (including AI Overviews and AI Mode), as well as AI model training, and grounding on other Google generative AI products | Make sure your site is accessible to Googlebot, without disallowing [`Google-Extended`](/crawling/docs/google-extended) in `robots.txt` or excluding your site with the [Search generative AI control](https://support.google.com/webmasters/answer/16908024). |
| Stay on Google Search and allow AI model training, but opt out of Search generative AI features (including AI Overviews and AI Mode) | Set your [Search generative AI control](https://support.google.com/webmasters/answer/16908024) in Search Console to "Exclude my site's links and content from Search generative AI features". Don't disallow `Google-Extended`. |
| Stay on Google Search (including AI Overviews and AI Mode), but limit AI model training and grounding on other Google generative AI products | Disallow [`Google-Extended`](/crawling/docs/google-extended) in `robots.txt`. |
| Stay on Google Search, opt out of Search generative AI features, and limit AI model training and grounding on other Google generative AI products | Use the Search generative AI control and disallow [`Google-Extended`](/crawling/docs/google-extended). |
| Limit snippet length or exclude a specific passage on a page from being used for grounding | Add robots `meta` tags (`max-snippet`, `data-nosnippet`, or `nosnippet`). |
| Keep a page out of Google Search (including AI Overviews and AI Mode) completely | Use the `noindex` rule. |
| Make paywalled content available to Google (including enabling a snippet to be shown in AI Overviews and AI Mode) | Add [paywalled structured data](/search/docs/appearance/structured-data/paywalled-content) in combination with [`data-nosnippet`](/search/docs/crawling-indexing/robots-meta-tag#data-nosnippet-attr) or [`max-snippet` robots `meta` tag](/search/docs/crawling-indexing/robots-meta-tag#max-snippet). |
