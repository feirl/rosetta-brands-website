"""
add_structured_data.py

For each service page:
  1. Injects Service + WebPage + BreadcrumbList JSON-LD before </head>
  2. Appends a FAQ section (HTML + FAQPage JSON-LD) before the footer placeholder
"""

import re

BASE_URL = "https://rosettabrands.co.uk"

PROVIDER = """{"@type": "Organization", "name": "Rosetta Brands", "url": "https://rosettabrands.co.uk"}"""

# ─── Per-page data ─────────────────────────────────────────────────────────────

PAGES = {

    "vendor-access.html": {
        "service": {
            "name": "Vendor Access & Prime",
            "description": "Rosetta Brands provides FMCG brands with enterprise-grade Amazon vendor status, Prime badge access, and the full infrastructure of a managed vendor account — without building it in-house.",
            "serviceType": "Amazon Vendor-as-a-Service",
            "areaServed": ["GB", "IE", "DE", "AU"],
        },
        "webpage": {
            "name": "Vendor Access & Prime | Amazon VaaS | Rosetta Brands",
            "description": "Unlock enterprise-grade Amazon vendor status through Rosetta Brands. Prime badge, fulfilment, advertising and full compliance — without building the infrastructure yourself.",
        },
        "breadcrumbs": [
            {"name": "Home", "url": "/"},
            {"name": "Services", "url": "/#services"},
            {"name": "Vendor Access & Prime", "url": "/vendor-access.html"},
        ],
        "faqs": [
            {
                "q": "What is Vendor-as-a-Service (VaaS)?",
                "a": "Vendor-as-a-Service means Rosetta Brands operates as your Amazon vendor. We hold the vendor account, manage the relationship with Amazon, handle compliance and fulfilment, and share in your growth. You get enterprise-grade vendor infrastructure without the overhead of building or running it yourself."
            },
            {
                "q": "Do I need my own Amazon vendor account to work with Rosetta Brands?",
                "a": "No. Rosetta Brands provides the vendor account infrastructure. You benefit from our established vendor relationships, Prime badge access, and Amazon compliance framework from day one — without needing your own vendor account."
            },
            {
                "q": "Which markets does Rosetta Brands operate in?",
                "a": "We currently operate across the UK, Ireland, Germany, and Australia. Our vendor infrastructure is active in all four markets, allowing brands to expand internationally without managing separate vendor relationships in each territory."
            },
            {
                "q": "What product categories does Rosetta Brands work with?",
                "a": "We specialise in FMCG categories on Amazon, including Grocery & Gourmet, Beer, Wine & Spirits, Health & Personal Care, Pet Supplies, Home & Household, and Garden & Outdoor. If you're an FMCG brand, we likely have deep experience in your category."
            },
            {
                "q": "How long does onboarding take?",
                "a": "Most brands are fully onboarded and live on Amazon within 4–8 weeks. This includes account setup, catalogue migration, compliance checks, content optimisation, and first purchase order processing."
            },
            {
                "q": "Can I use Rosetta Brands alongside my existing Amazon Seller account?",
                "a": "Yes. Many of our partner brands transition from Seller to Vendor through us, while others run both in parallel during the transition period. We'll advise on the right approach based on your current setup and growth objectives."
            },
        ]
    },

    "fulfilment.html": {
        "service": {
            "name": "Fulfilment & Logistics",
            "description": "Rosetta Brands manages the full Amazon fulfilment cycle for FMCG brands — one weekly purchase order, one collection point, consolidated to a single Amazon fulfilment centre using Amazon's own freight network.",
            "serviceType": "Amazon Fulfilment Management",
            "areaServed": ["GB", "IE", "DE", "AU"],
        },
        "webpage": {
            "name": "Fulfilment & Logistics | Amazon VaaS | Rosetta Brands",
            "description": "One weekly order. One fulfilment centre. Zero headaches. Rosetta Brands turns Amazon's complex fulfilment requirements into a simple weekly cycle for FMCG brands.",
        },
        "breadcrumbs": [
            {"name": "Home", "url": "/"},
            {"name": "Services", "url": "/#services"},
            {"name": "Fulfilment & Logistics", "url": "/fulfilment.html"},
        ],
        "faqs": [
            {
                "q": "How does Rosetta Brands simplify Amazon fulfilment?",
                "a": "We consolidate everything into a single weekly cycle. Amazon places one purchase order each week. We generate shipping labels and confirmation, arrange collection from your warehouse via Amazon Freight, and handle all compliance, prep, and last-mile delivery. You ship once a week to one location — we handle the rest."
            },
            {
                "q": "Does Rosetta Brands use Amazon's own freight network?",
                "a": "Yes. We use Amazon Freight to collect directly from your warehouse, which means your stock moves through Amazon's own logistics infrastructure. This reduces handling, improves delivery reliability, and keeps fulfilment costs lower than third-party 3PL alternatives."
            },
            {
                "q": "How many Amazon fulfilment centres do I need to manage?",
                "a": "Just one. Rosetta Brands consolidates all your orders to a single Amazon fulfilment centre, regardless of how many centres Amazon ultimately distributes to. The complexity of Amazon's 31-centre network is invisible to you."
            },
            {
                "q": "What happens with Amazon chargebacks and prep charges?",
                "a": "Chargebacks and prep charges are one of the biggest margin drains for Amazon vendors. Our fulfilment process is built around Amazon's compliance requirements, significantly reducing the frequency of chargebacks. Where disputes arise, we handle them on your behalf."
            },
            {
                "q": "Do I need to change my warehouse or logistics setup?",
                "a": "No. We work with your existing warehouse and dispatch operations. Amazon Freight collects from you directly. The only change is that you ship to us on a weekly cycle rather than managing multiple POs and destinations yourself."
            },
        ]
    },

    "amazon-vendors.html": {
        "service": {
            "name": "Solutions for Amazon Vendors",
            "description": "Rosetta Brands helps established Amazon vendors recover margin, reduce chargebacks, fix compliance issues, and unlock growth programmes that most vendors never access.",
            "serviceType": "Amazon Vendor Optimisation",
            "areaServed": ["GB", "IE", "DE", "AU"],
        },
        "webpage": {
            "name": "Solutions for Amazon Vendors | Rosetta Brands",
            "description": "Already an Amazon vendor losing margin or battling chargebacks? Rosetta Brands helps established vendors protect margin, fix compliance, and scale profitably.",
        },
        "breadcrumbs": [
            {"name": "Home", "url": "/"},
            {"name": "Solutions", "url": "/#solutions"},
            {"name": "Amazon Vendors", "url": "/amazon-vendors.html"},
        ],
        "faqs": [
            {
                "q": "I already have a vendor account — why would I need Rosetta Brands?",
                "a": "Having vendor access is only the starting point. Most brands with vendor accounts are leaving significant margin on the table through chargebacks, poor compliance, unoptimised content, and missed promotional programmes. Rosetta Brands takes over the operational complexity so your vendor account performs at its full potential."
            },
            {
                "q": "How does Rosetta Brands reduce Amazon chargebacks?",
                "a": "We build your fulfilment process around Amazon's exact compliance requirements — correct labelling, accurate ASN submissions, compliant packing, and reliable delivery windows. This eliminates the root causes of most chargebacks rather than just disputing them after the fact."
            },
            {
                "q": "Can Rosetta Brands help recover margin we've already lost?",
                "a": "Yes. We conduct a full account audit when onboarding, identifying historic chargeback patterns, incorrect deductions, and missed dispute windows. Where recoverable amounts exist, we pursue them through Amazon's dispute process on your behalf."
            },
            {
                "q": "What exclusive Amazon programmes can Rosetta Brands unlock for us?",
                "a": "Through our vendor relationships, we can access programmes including Vendor Vine, Subscribe & Save, Amazon Fresh, Amazon Pantry, and exclusive promotional placements. Many of these require a strong compliance track record and established vendor standing — both of which we provide."
            },
            {
                "q": "How is Rosetta Brands different from an Amazon agency?",
                "a": "Agencies manage your account on your behalf. Rosetta Brands operates as the vendor — we take ownership of the commercial relationship with Amazon, the compliance risk, and the fulfilment infrastructure. Our success fee model means our interests are fully aligned with yours."
            },
        ]
    },

    "pricing.html": {
        "service": {
            "name": "Pricing & Partnership Model",
            "description": "Rosetta Brands operates on an outcome-based pricing model: a base component covering infrastructure costs, plus a success fee that only applies when your brand grows beyond its target. No retainers, no upfront fees.",
            "serviceType": "Amazon Vendor-as-a-Service",
            "areaServed": ["GB", "IE", "DE", "AU"],
        },
        "webpage": {
            "name": "Amazon VaaS Pricing & Partnership Model | Rosetta Brands",
            "description": "Rosetta Brands operates on a partnership model: three components working together as one growth engine. No retainers. We only win when you win.",
        },
        "breadcrumbs": [
            {"name": "Home", "url": "/"},
            {"name": "Pricing", "url": "/pricing.html"},
        ],
        "faqs": [
            {
                "q": "How does Rosetta Brands' pricing work?",
                "a": "Our model has three components: a Vendor Access fee covering the infrastructure cost of maintaining your vendor account; a Fulfilment fee based on the volume and complexity of your orders; and a Success Fee that only applies when your Amazon revenue grows beyond an agreed target. The success fee is our primary incentive — we only earn it when you grow."
            },
            {
                "q": "Is there an upfront fee or retainer?",
                "a": "No upfront fees and no retainer. Our base fees cover the operational cost of running your vendor account and fulfilment. Beyond that, our compensation is tied directly to your growth. If you don't grow beyond target, we don't earn the success fee."
            },
            {
                "q": "When does the success fee kick in?",
                "a": "The success fee only applies to revenue above a mutually agreed growth target. The target is set at onboarding based on your current Amazon revenue and realistic growth potential. Anything below that threshold — we absorb the operational cost. Only growth beyond target triggers the success fee."
            },
            {
                "q": "What is included in the base Vendor Access fee?",
                "a": "The Vendor Access fee covers: maintenance of your vendor account relationship with Amazon, compliance management, catalogue management, weekly purchase order processing, and access to our platform technology. It reflects the true cost of operating enterprise-grade vendor infrastructure."
            },
            {
                "q": "Is there a minimum contract length?",
                "a": "We ask for an initial partnership term to allow the account infrastructure to bed in and performance to stabilise — typically six months. After that, the partnership continues on a rolling basis. We're confident in the model; brands that are growing tend to stay."
            },
            {
                "q": "How do you calculate the growth target?",
                "a": "The growth target is agreed collaboratively at onboarding. We look at your current Amazon revenue run rate, category growth rates, the impact of switching to vendor, and realistic timelines. The target should stretch you, but it should also be achievable — we need to earn our success fee, so setting an unachievable target isn't in our interest."
            },
        ]
    },

    "vendor-management-team.html": {
        "service": {
            "name": "Vendor Management Team",
            "description": "Rosetta Brands provides a fully integrated seven-person Amazon vendor management team as a service — client manager, advertising manager, creative designer, onboarding specialist, finance manager, orders coordinator, and partnerships lead.",
            "serviceType": "Amazon Vendor Team Management",
            "areaServed": ["GB", "IE", "DE", "AU"],
        },
        "webpage": {
            "name": "Vendor Management Team | Amazon VaaS | Rosetta Brands",
            "description": "Seven specialist roles. One partnership. Instead of building an Amazon vendor management team in-house, Rosetta's cross-functional team becomes yours from day one.",
        },
        "breadcrumbs": [
            {"name": "Home", "url": "/"},
            {"name": "Services", "url": "/#services"},
            {"name": "Vendor Management Team", "url": "/vendor-management-team.html"},
        ],
        "faqs": [
            {
                "q": "What specialists are included in the Vendor Management Team?",
                "a": "Every Rosetta Brands partnership includes seven dedicated roles: a Client Manager who owns your account relationship; an Advertising Manager running your Amazon PPC; a Creative Designer for content and imagery; an Onboarding & Technical Specialist; a Finance Manager handling deductions and reconciliation; an Orders Coordinator managing weekly POs; and a Partnerships Lead developing your Amazon commercial relationships."
            },
            {
                "q": "Are these dedicated individuals or shared resources?",
                "a": "Each specialist is dedicated to their function but works across a carefully managed portfolio of brands. You get genuine specialist expertise — not an account manager wearing multiple hats. Your Client Manager is your single point of contact and coordinates the full team on your behalf."
            },
            {
                "q": "How does this compare to hiring an in-house Amazon team?",
                "a": "Building these seven roles in-house would cost upwards of £350,000–£500,000 in annual salaries alone, plus recruitment, training, management overhead, and the time to build institutional knowledge. Through Rosetta Brands, you access the same depth of expertise immediately, with costs tied to your commercial performance."
            },
            {
                "q": "How does the team communicate with us day-to-day?",
                "a": "Your Client Manager is your primary contact for day-to-day communication, weekly performance reviews, and strategic planning. Specialist team members join calls when their area is the focus. You have visibility across everything through our client portal, including live analytics, order status, and advertising performance."
            },
            {
                "q": "What happens if a team member leaves Rosetta Brands?",
                "a": "Our team structure is designed for resilience. Each function has internal depth and documented processes, so transitions don't create gaps in your account management. Unlike an in-house hire, there's no notice period or knowledge gap — the institutional expertise stays with Rosetta Brands."
            },
        ]
    },
}


def build_schema_block(page_slug, data):
    url = f"{BASE_URL}/{page_slug}"
    service_url = url
    breadcrumbs = data["breadcrumbs"]
    service = data["service"]
    webpage = data["webpage"]
    faqs = data["faqs"]

    # BreadcrumbList
    crumb_items = ",\n        ".join([
        f'{{"@type":"ListItem","position":{i+1},"name":"{bc["name"]}","item":"{BASE_URL}{bc["url"]}"}}'
        for i, bc in enumerate(breadcrumbs)
    ])

    # FAQPage
    faq_items = ",\n      ".join([
        f'{{"@type":"Question","name":{repr(faq["q"])},"acceptedAnswer":{{"@type":"Answer","text":{repr(faq["a"])}}}}}'
        for faq in faqs
    ])

    block = f"""<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@graph": [
    {{
      "@type": "WebPage",
      "@id": "{url}",
      "url": "{url}",
      "name": "{webpage["name"]}",
      "description": "{webpage["description"]}",
      "inLanguage": "en-GB",
      "isPartOf": {{"@type": "WebSite", "url": "https://rosettabrands.co.uk", "name": "Rosetta Brands"}},
      "breadcrumb": {{"@id": "{url}#breadcrumb"}}
    }},
    {{
      "@type": "BreadcrumbList",
      "@id": "{url}#breadcrumb",
      "itemListElement": [
        {crumb_items}
      ]
    }},
    {{
      "@type": "Service",
      "name": "{service["name"]}",
      "description": "{service["description"]}",
      "serviceType": "{service["serviceType"]}",
      "url": "{service_url}",
      "provider": {{"@type": "Organization", "name": "Rosetta Brands", "url": "https://rosettabrands.co.uk"}},
      "areaServed": {service["areaServed"]}
    }},
    {{
      "@type": "FAQPage",
      "mainEntity": [
      {faq_items}
      ]
    }}
  ]
}}
</script>"""
    return block


def build_faq_html(faqs, accent="orange"):
    items_html = "\n".join([
        f"""        <div class="faq-item fade-in">
          <button class="faq-q" aria-expanded="false">
            {faq["q"]}
            <svg class="faq-chevron" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"/></svg>
          </button>
          <div class="faq-a" hidden>
            <p>{faq["a"]}</p>
          </div>
        </div>"""
        for faq in faqs
    ])

    return f"""
<!-- ═══════════════════════════════════════════
     FAQ SECTION
     ═══════════════════════════════════════════ -->
<section class="faq-section">
  <div class="container">
    <div class="section-header center fade-in">
      <div class="section-tag {accent}">Common Questions</div>
      <h2 class="section-title">Everything you need to know</h2>
      <p class="section-subtitle">Specific questions about this service. For broader questions about how Rosetta Brands works, visit our <a href="faq.html" style="color:var(--orange);text-decoration:none;font-weight:600;">FAQ page</a>.</p>
    </div>
    <div class="faq-list">
{items_html}
    </div>
  </div>
</section>
"""


FAQ_CSS = """
/* ═══════════════════════════════════════════
   FAQ SECTION
   ═══════════════════════════════════════════ */
.faq-section {
  padding: var(--section-pad) 0;
  background: var(--off-white);
}
.faq-list {
  max-width: 760px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 2px;
}
.faq-item {
  background: var(--white);
  border: 1px solid var(--border);
  border-radius: 12px;
  overflow: hidden;
  transition: box-shadow 0.2s ease;
}
.faq-item:hover { box-shadow: 0 2px 12px rgba(45,41,51,0.06); }
.faq-q {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  padding: 20px 24px;
  background: none;
  border: none;
  cursor: pointer;
  font-family: var(--font-display);
  font-size: 16px;
  font-weight: 600;
  color: var(--charcoal);
  text-align: left;
  transition: color 0.2s ease;
}
.faq-q:hover { color: var(--orange); }
.faq-q[aria-expanded="true"] { color: var(--orange); }
.faq-chevron {
  flex-shrink: 0;
  transition: transform 0.25s ease;
  color: var(--charcoal-50);
}
.faq-q[aria-expanded="true"] .faq-chevron {
  transform: rotate(180deg);
  color: var(--orange);
}
.faq-a {
  padding: 0 24px 20px;
  border-top: 1px solid var(--border);
}
.faq-a p {
  font-size: 15px;
  line-height: 1.7;
  color: var(--text-secondary);
  padding-top: 16px;
}
"""

FAQ_JS = """
<script>
(function(){
  document.querySelectorAll('.faq-q').forEach(function(btn){
    btn.addEventListener('click', function(){
      var expanded = this.getAttribute('aria-expanded') === 'true';
      var answer   = this.nextElementSibling;
      this.setAttribute('aria-expanded', String(!expanded));
      if(expanded){ answer.hidden = true; } else { answer.hidden = false; }
    });
  });
})();
</script>"""


import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

for page_slug, data in PAGES.items():
    html = open(page_slug).read()

    # 1. Inject JSON-LD block before </head>
    schema_block = build_schema_block(page_slug, data)
    if 'application/ld+json' not in html:
        html = html.replace('</head>', schema_block + '\n</head>', 1)
    else:
        # Replace existing ld+json block
        html = re.sub(
            r'<script type="application/ld\+json">.*?</script>',
            schema_block,
            html, flags=re.DOTALL, count=1
        )

    # 2. Inject FAQ CSS into the page's <style> block
    if 'faq-section' not in html:
        html = html.replace('</style>', FAQ_CSS + '\n</style>', 1)

    # 3. Inject FAQ HTML before footer placeholder
    faq_html = build_faq_html(data["faqs"])
    if 'faq-section' not in html.split('<style>')[0] + html.split('</style>')[-1]:
        html = html.replace('<div id="footer-placeholder">', faq_html + '\n<div id="footer-placeholder">', 1)
    elif '<section class="faq-section">' not in html:
        html = html.replace('<div id="footer-placeholder">', faq_html + '\n<div id="footer-placeholder">', 1)

    # 4. Inject FAQ JS before </body>
    if 'faq-q' not in html.split('<script')[-1]:
        html = html.replace('</body>', FAQ_JS + '\n</body>', 1)

    open(page_slug, 'w').write(html)
    print(f'✓ {page_slug}  ({len(data["faqs"])} FAQs, schema injected)')
