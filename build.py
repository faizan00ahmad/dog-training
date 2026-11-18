# -*- coding: utf-8 -*-
"""Static site generator for Paws & Path Dog Training.

Run:  python build.py
Writes every page as <folder>/index.html, plus sitemap.xml and robots.txt.
Edit SITE / TRACKING below, then rebuild.
"""
import html
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))
from blog_data import BLOG  # noqa: E402

ROOT = Path(__file__).parent

# ----------------------------------------------------------------------------
# Settings
# ----------------------------------------------------------------------------
SITE = {
    "url": "https://www.pawspath.example",   # replace with the real domain before launch
    "name": "Paws & Path Dog Training",
    "short": "Paws & Path",
    "city": "Austin",
    "region": "TX",
    "phone": "(555) 012-3456",
    "phone_e164": "+15550123456",
    "email": "hello@pawspath.example",
    "hours": "Mon-Sat, 8am-6pm",
    "areas": ["Austin", "Round Rock", "Cedar Park", "Pflugerville"],
    "og_image": "/assets/obedience.jpg",
}

# Paste real IDs here. Anything containing YOUR_ or XXXX is treated as "not set" and sends nothing.
TRACKING = {
    "META_PIXEL_ID": "YOUR_META_PIXEL_ID",
    "GA4_ID": "G-XXXXXXXXXX",
    "GADS_ID": "AW-XXXXXXXXX",
    "GADS_LEAD_LABEL": "",   # Google Ads conversion label for form leads
    "GADS_CALL_LABEL": "",   # Google Ads conversion label for call clicks
}

PAW = ('<svg viewBox="0 0 24 24"><ellipse cx="5.5" cy="11" rx="2.2" ry="2.9"/><ellipse cx="10" cy="6.6" rx="2.2" ry="2.9"/>'
       '<ellipse cx="15.2" cy="6.6" rx="2.2" ry="2.9"/><ellipse cx="19.4" cy="11" rx="2.2" ry="2.9"/>'
       '<path d="M12.4 11.2c-3 0-5.6 3.1-5.6 5.8 0 2 1.5 3 3.2 3 1 0 1.5-.4 2.4-.4s1.4.4 2.4.4c1.7 0 3.2-1 3.2-3 0-2.7-2.6-5.8-5.6-5.8z"/></svg>')

NAV = [("About", "/about/"), ("Services", "/services/"), ("Blog", "/blog/"), ("FAQ", "/faq/"), ("Contact", "/contact/")]

# ----------------------------------------------------------------------------
# Content: services
# ----------------------------------------------------------------------------
SERVICES = {
    "obedience": {
        "path": "/services/obedience-training-austin/",
        "name": "Obedience Training",
        "title": "Dog Obedience Training Austin TX | In-Home | Paws & Path",
        "h1": "Dog obedience training in Austin, TX",
        "description": "In-home dog obedience training in Austin. Loose-leash walking, sit, stay, recall and calm manners taught on your own street. Force-free. From $120.",
        "keywords": "dog obedience training Austin, in-home dog training Austin TX, dog trainer near me, loose leash walking Austin, dog recall training Austin, private dog training Austin",
        "lead": "Walk without being dragged. Come when you call. Settle when guests arrive. We teach obedience in your home and on your own streets, so it works in real life and not only in a classroom.",
        "image": "obedience.jpg", "alt": "Person walking a golden retriever on a loose leash along an Austin street",
        "price": 120, "price_note": "per two-hour session",
        "sections": [
            ("Who obedience training is for", """<p>Most of the families we see aren't chasing show-ring perfection. They want a dog who doesn't pull their arm off, who comes back at the park, and who can be calm when the doorbell rings. If that sounds like you, this is the right place to start.</p>
<p>It suits adult dogs, adolescent dogs (the 8 to 18 month stage can be a handful) and rescue dogs settling into a new home.</p>"""),
            ("What we teach", """<ul>
<li><strong>Loose-leash walking</strong> on the routes you actually use, whether that's a quiet Mueller street or the Lady Bird Lake trail.</li>
<li><strong>Sit, down, stay and wait</strong>, including at doors and car doors.</li>
<li><strong>Recall.</strong> A "come" that survives squirrels and other dogs. See our <a href="/blog/dog-recall-training-come-when-called/">recall training guide</a>.</li>
<li><strong>Settle on a mat</strong> so your dog can relax while you eat, work or have visitors.</li>
<li><strong>Leave it and drop it</strong> for the things your dog shouldn't have.</li>
<li><strong>Polite greetings</strong>, with no jumping up on people.</li>
</ul>"""),
            ("How a session works", """<ol>
<li><strong>We talk first.</strong> Before we visit we hear about your dog on a free 15-minute call.</li>
<li><strong>We train in your home.</strong> About two hours, with everyone in the household welcome.</li>
<li><strong>You get a written plan.</strong> Simple steps, short practice sessions, and what to do when things go wrong.</li>
<li><strong>Support afterwards.</strong> Phone and email help for the life of your dog.</li>
</ol>
<p>Everything we do is reward-based. No prong, choke or shock collars. If you want to know why, read our <a href="/blog/how-to-stop-dog-pulling-on-leash/">guide to stopping leash pulling</a>.</p>"""),
            ("Pricing", """<p>Obedience sessions start at <strong>$120 per two-hour visit</strong>. Many dogs make clear progress in a single session and keep improving with the practice plan. Packages are available if you'd like ongoing coaching. For a full breakdown of what dog training costs around Austin, see our <a href="/blog/dog-training-cost-austin-tx/">price guide</a>.</p>"""),
        ],
        "faqs": [
            ("How long does dog obedience training take?", "Most dogs show clear improvement after one session and keep progressing over two to six weeks of regular practice. Strong habits or high-distraction areas can take longer."),
            ("Do you train dogs at my home in Austin?", "Yes. We train in your home and on your normal walking routes across Austin, Round Rock, Cedar Park and Pflugerville."),
            ("What age can a dog start obedience training?", "Puppies can start learning basics from 8 weeks. Adult and senior dogs can learn too, at any age."),
            ("Do you use treats or collars?", "We use rewards such as treats, toys and praise. We never use prong, choke or shock collars."),
        ],
        "related": ["how-to-stop-dog-pulling-on-leash", "dog-recall-training-come-when-called", "in-home-vs-group-dog-training"],
    },
    "behaviour": {
        "path": "/services/behaviour-training-austin/",
        "name": "Behaviour Training",
        "title": "Dog Behavior Training Austin TX | Reactivity | Paws & Path",
        "h1": "Dog behaviour training and reactivity help in Austin, TX",
        "description": "Austin dog behaviour training for leash reactivity, barking, resource guarding and anxiety. Force-free, in-home assessment and plan. From $150.",
        "keywords": "dog behavior training Austin, leash reactive dog trainer Austin, dog reactivity training Austin, dog barking trainer Austin, resource guarding dog trainer, separation anxiety dog trainer Austin",
        "lead": "Lunging at other dogs. Barking at the doorbell. Growling over a bone. These aren't bad dogs. They're dogs struggling with something, and we find out what before we change anything.",
        "image": "behaviour.jpg", "alt": "Handler calmly holding a black and white dog outdoors",
        "price": 150, "price_note": "assessment and first session",
        "sections": [
            ("Problems we help with", """<ul>
<li><strong>Leash reactivity.</strong> Barking, lunging or spinning when other dogs, bikes or people pass. Start with our <a href="/blog/leash-reactive-dog-training/">leash reactivity guide</a>.</li>
<li><strong>Barking.</strong> Doorbell, visitors, windows, delivery drivers. See <a href="/blog/stop-dog-barking-at-visitors-and-doorbell/">six fixes for door barking</a>.</li>
<li><strong>Resource guarding</strong> of food, toys, beds or people.</li>
<li><strong>Separation anxiety</strong> and distress when left alone. Read <a href="/blog/dog-separation-anxiety-vs-boredom/">anxiety or boredom?</a></li>
<li><strong>Fear and nervousness</strong> around strangers, noises or new places.</li>
<li><strong>Jumping up, nipping and over-excitement.</strong></li>
</ul>"""),
            ("Why we start with an assessment", """<p>The same behaviour can come from very different causes. A dog barking at visitors might be excited, protective or scared, and each needs a different plan. So the first visit is a proper look: your dog's history, their body language, the triggers and the layout of your home.</p>
<p>If we suspect pain or a medical problem, we'll ask you to check with your vet before going any further. Behaviour and health are closely linked.</p>"""),
            ("What you can expect", """<ol>
<li><strong>Free 15-minute call</strong> to decide whether we're the right fit. If your case is beyond us (for example, serious aggression) we'll say so and point you to a veterinary behaviourist.</li>
<li><strong>In-home assessment and first session</strong>, with a written plan.</li>
<li><strong>Coaching on real triggers</strong> in your home and on your walks.</li>
<li><strong>Follow-up support</strong> by phone and email between visits.</li>
</ol>
<p>Training is reward-based and paced to your dog. We never push a dog past what they can handle, and we never use fear, pain or intimidation.</p>"""),
            ("Pricing", """<p>An assessment plus first session starts at <strong>$150</strong>. Behaviour cases often benefit from follow-up sessions or a package, and we'll give you an honest estimate after the first visit.</p>"""),
        ],
        "faqs": [
            ("Can you help with an aggressive dog?", "We help with many reactive and fearful dogs. If a dog has bitten or is likely to cause serious harm, we'll refer you to a veterinary behaviourist and work alongside them where appropriate."),
            ("Why is my dog only reactive on a leash?", "A leash stops a dog from moving away or greeting normally, which can create fear or frustration. Reward-based desensitisation helps."),
            ("Will my dog need medication?", "Sometimes. That's a decision for your vet. We'll tell you if we think a vet visit is worth it."),
            ("How long will behaviour training take?", "It depends on the dog and the problem. Many families see progress within weeks, though deeply rooted fears take longer."),
        ],
        "related": ["leash-reactive-dog-training", "stop-dog-barking-at-visitors-and-doorbell", "dog-separation-anxiety-vs-boredom"],
    },
    "puppy": {
        "path": "/services/puppy-training-austin/",
        "name": "Puppy Training",
        "title": "Puppy Training Austin TX | In-Home | Paws & Path",
        "h1": "Puppy training in Austin, TX",
        "description": "In-home puppy training in Austin for house training, biting, crate routines and socialisation. Force-free. Group classes capped at six puppies. From $110.",
        "keywords": "puppy training Austin TX, puppy classes Austin, house training puppy Austin, puppy biting training, puppy socialization Austin, in-home puppy trainer Austin",
        "lead": "The first six months set up the next ten years. We help you get house training, biting, handling and early socialisation right from day one, in your own home.",
        "image": "puppy.jpg", "alt": "Trainer crouching on grass holding a white puppy",
        "price": 110, "price_note": "per session",
        "sections": [
            ("What puppy training covers", """<ul>
<li><strong>House training and crate routines.</strong> Our <a href="/blog/potty-train-puppy-apartment-austin/">7-day apartment plan</a> is a good start.</li>
<li><strong>Biting and chewing.</strong> Why it happens and how to stop it, in our <a href="/blog/how-to-stop-puppy-biting/">puppy biting guide</a>.</li>
<li><strong>Handling and grooming practice</strong> so vet visits aren't a battle.</li>
<li><strong>Meeting people, dogs and new places</strong> without fear.</li>
<li><strong>Names, sit, down, come</strong> and the start of loose-leash walking.</li>
<li><strong>Settling and sleeping routines</strong> for the whole household.</li>
</ul>"""),
            ("Private sessions or group classes?", """<p>Private in-home sessions are ideal for the practical stuff: house training, nipping and routines. Small group classes (six puppies at most) are great for socialisation once your puppy has had their vaccinations. Many families do one private visit first, then a class. Not sure which is right? Read <a href="/blog/in-home-vs-group-dog-training/">in-home vs group training</a>.</p>"""),
            ("When to start", """<p>As early as 8 weeks. The socialisation window matters, so the earlier we help you plan safe experiences, the better. If your puppy is older than six months, don't worry. Adolescent dogs benefit from our <a href="/services/obedience-training-austin/">obedience</a> sessions.</p>"""),
            ("Pricing", """<p>Puppy sessions start at <strong>$110</strong>. Group classes are priced per course, and we'll send the current dates when you get in touch.</p>"""),
        ],
        "faqs": [
            ("When should I start training my puppy?", "From the day you bring them home, usually around 8 weeks. Early habits are far easier to shape than to change."),
            ("Can my puppy go to class before finishing vaccinations?", "Check with your vet. Many puppy classes require at least the first vaccinations, and private in-home sessions are a safe way to start earlier."),
            ("How long does house training take?", "Many puppies are mostly reliable in 4 to 8 weeks with a consistent routine, though full reliability can take a few months."),
            ("Do you offer puppy classes in Austin?", "Yes, small group classes capped at six puppies. Get in touch for the next dates."),
        ],
        "related": ["how-to-stop-puppy-biting", "potty-train-puppy-apartment-austin", "in-home-vs-group-dog-training"],
    },
}

HOME_FAQS = [
    ("Should the whole family come to the session?", "Ideally, yes. Everyone who handles the dog should use the same cues. If that isn't possible, one person can attend and we'll write a plan to share."),
    ("Do you train reactive dogs at home?", "Yes. Reactive dogs are a big part of the work. We keep your dog below the point where they react and never push past what they can handle."),
    ("How many sessions will my dog need?", "Many households see a big change after one two-hour session. Complex cases may need a few follow-ups. We'll tell you honestly after the first visit."),
    ("What if it rains or I need to reschedule?", "We move outdoor work under cover or indoors where we can. Give us 24 hours' notice to reschedule for free."),
    ("Do you offer refunds?", "Training depends on practice at home, so we can't promise a fixed result. If you're unhappy after the first month, we'll change the plan or refund unused sessions."),
]

FAQ_PAGE = [
    ("About our training", HOME_FAQS + [
        ("What training methods do you use?", "Reward-based, force-free methods only. We use treats, toys and praise, and never prong, choke or shock collars."),
        ("Are you certified and insured?", "Alex Morgan holds the CPDT-KA credential and we carry liability insurance and bonding for in-home work."),
    ]),
    ("Pricing and booking", [
        ("How much does dog training cost in Austin?", "Private in-home sessions across Austin generally run $100 to $200. Ours start at $110 for puppies, $120 for obedience and $150 for a behaviour assessment plus session. See our full <a href='/blog/dog-training-cost-austin-tx/'>price guide</a>."),
        ("Is there a travel fee?", "No travel fee within Austin, Round Rock, Cedar Park and Pflugerville. We'll tell you before booking if you're outside our area."),
        ("How do I book?", "Book a free 15-minute call using the form on our <a href='/contact/'>contact page</a>, or phone us. We'll recommend the best first step."),
    ]),
    ("Puppies and behaviour", [
        ("When should I start puppy training?", "From the day you bring your puppy home, usually around 8 weeks."),
        ("Can you help with a dog that bites?", "If a dog has bitten, we start with a free call and may refer you to a veterinary behaviourist. Safety comes first."),
        ("My dog barks at everything. Can you help?", "Yes. We find out why they bark and teach a calmer alternative. See our guide to <a href='/blog/stop-dog-barking-at-visitors-and-doorbell/'>door barking</a>."),
    ]),
]

# ----------------------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------------------
def esc(s):
    return html.escape(s, quote=True)


def url(path):
    return SITE["url"] + path


def slugify(text):
    return re.sub(r"[^a-z0-9]+", "-", re.sub(r"<[^>]+>", "", text).lower()).strip("-")


def write(path, content):
    p = ROOT / path.lstrip("/")
    if path.endswith("/"):
        p = p / "index.html"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")


def ld(obj):
    return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False) + "</script>"


def is_real(v):
    return bool(v) and not re.search(r"YOUR_|XXXX", v)


def breadcrumb_ld(trail):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": url(p)} for i, (n, p) in enumerate(trail)]}


def faq_ld(faqs):
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": re.sub(r"<[^>]+>", "", a)}} for q, a in faqs]}


def local_business_ld():
    return {"@context": "https://schema.org", "@type": ["LocalBusiness", "ProfessionalService"], "@id": url("/#business"),
            "name": SITE["name"], "url": url("/"), "telephone": SITE["phone_e164"], "email": SITE["email"],
            "image": url(SITE["og_image"]), "priceRange": "$$",
            "description": "Force-free, in-home dog training in Austin, TX: obedience, behaviour, reactivity and puppy training.",
            "address": {"@type": "PostalAddress", "addressLocality": SITE["city"], "addressRegion": SITE["region"], "addressCountry": "US"},
            "areaServed": [{"@type": "City", "name": a} for a in SITE["areas"]],
            "openingHoursSpecification": [{"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"], "opens": "08:00", "closes": "18:00"}],
            "founder": {"@type": "Person", "name": "Alex Morgan", "jobTitle": "Certified Professional Dog Trainer (CPDT-KA)"},
            "aggregateRating": {"@type": "AggregateRating", "ratingValue": "4.9", "reviewCount": "120"},
            "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Dog training services", "itemListElement": [
                {"@type": "Offer", "itemOffered": {"@type": "Service", "name": s["name"], "url": url(s["path"])}} for s in SERVICES.values()]}}


def head(title, description, path, keywords="", extra="", og_type="website", og_image=None, page_type="page", page_title=""):
    cfg = {k: v for k, v in TRACKING.items()}
    noscript = ""
    if is_real(TRACKING["META_PIXEL_ID"]):
        noscript = ('<noscript><img height="1" width="1" style="display:none" alt="" '
                    'src="https://www.facebook.com/tr?id=%s&ev=PageView&noscript=1"/></noscript>' % esc(TRACKING["META_PIXEL_ID"]))
    img = url(og_image or SITE["og_image"])
    return f"""<!doctype html>
<html lang="en" data-theme="light">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(description)}">
{f'<meta name="keywords" content="{esc(keywords)}">' if keywords else ''}
<link rel="canonical" href="{url(path)}">
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">
<meta name="theme-color" content="#0b5a3a">
<meta name="geo.region" content="US-TX">
<meta name="geo.placename" content="Austin">
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="{esc(SITE['name'])}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(description)}">
<meta property="og:url" content="{url(path)}">
<meta property="og:image" content="{img}">
<meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(title)}">
<meta name="twitter:description" content="{esc(description)}">
<meta name="twitter:image" content="{img}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,700&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/site.css">
<script>window.PP_CONFIG={json.dumps(cfg)};</script>
<script src="/assets/tracking.js"></script>
{extra}
</head>
<body data-page-type="{page_type}" data-page-title="{esc(page_title or title)}">
{noscript}
<div class="aurora" aria-hidden="true"><i></i><i></i><i></i></div>
"""


def header(active=""):
    links = "".join(
        f'<a href="{p}"{" aria-current=\"page\"" if p == active else ""}>{n}</a>' for n, p in NAV)
    return f"""<header class="header">
  <div class="header-in">
    <a class="brand" href="/" aria-label="{esc(SITE['short'])} home"><span class="brand-mark" aria-hidden="true">{PAW}</span><span>{esc(SITE['short'])}</span></a>
    <nav class="nav" id="nav" aria-label="Primary">{links}</nav>
    <button class="theme-btn" id="themeBtn" type="button" aria-label="Switch to dark mode" title="Switch to dark mode"></button>
    <a class="btn btn-primary btn-sm" href="/contact/">Book a Free Call</a>
    <button class="menu-btn" id="menuBtn" aria-controls="nav" aria-expanded="false" aria-label="Open menu">☰</button>
  </div>
</header>
"""


def footer():
    svc = "".join(f'<a href="{s["path"]}">{s["name"]}</a>' for s in SERVICES.values())
    posts = "".join(f'<a href="/blog/{p["slug"]}/">{esc(p["h1"].split(":")[0][:48])}</a>' for p in BLOG[:4])
    return f"""<footer>
  <div class="wrap">
    <div class="glass">
      <div class="footer-grid">
        <div>
          <a class="brand" href="/"><span class="brand-mark" aria-hidden="true">{PAW}</span><span>{esc(SITE['short'])}</span></a>
          <p style="margin-top:12px; max-width:320px">In-home, force-free dog training in Austin, TX, Round Rock, Cedar Park and Pflugerville.</p>
          <p style="font-size:.9rem">Serving: {', '.join(SITE['areas'])}</p>
        </div>
        <div><h4>Services</h4>{svc}<a href="/services/">All services</a></div>
        <div><h4>Learn</h4>{posts}<a href="/blog/">All articles</a></div>
        <div><h4>Contact</h4><a href="tel:{SITE['phone_e164']}">{SITE['phone']}</a><a href="mailto:{SITE['email']}">{SITE['email']}</a><a href="/about/">About</a><a href="/faq/">FAQ</a><a href="/contact/">Book a call</a></div>
      </div>
      <div class="footer-bottom">
        <span>© <span id="year"></span> {esc(SITE['name'])} · Insured &amp; bonded</span>
        <span><a href="/privacy/" style="color:inherit">Privacy</a> · <a href="#" data-cookie-settings style="color:inherit">Cookie settings</a></span>
      </div>
    </div>
  </div>
</footer>

<div class="call-bar" id="callBar">
  <a class="btn btn-glass" href="tel:{SITE['phone_e164']}">Call</a>
  <a class="btn btn-primary" href="/contact/">Book Free Call</a>
</div>
<script src="/assets/site.js"></script>
</body>
</html>
"""


def lead_form(idx=""):
    return """<form class="glass form lead-form" novalidate>
  <div class="row">
    <label>Your name <input name="name" type="text" autocomplete="name" required></label>
    <label>Email <input name="email" type="email" autocomplete="email" required></label>
  </div>
  <label>Phone (optional) <input name="phone" type="tel" autocomplete="tel"></label>
  <label>Dog's name &amp; breed <input name="dog" type="text" placeholder="e.g. Biscuit, Labrador mix" required></label>
  <label>Main challenge
    <select name="need" required>
      <option value="">Choose one…</option>
      <option>Pulling or leash walking</option>
      <option>Reactivity to dogs or people</option>
      <option>Barking, jumping or visitors</option>
      <option>Puppy training</option>
      <option>Recall or off-leash</option>
      <option>Separation anxiety</option>
      <option>Something else</option>
    </select>
  </label>
  <label>Anything else? <textarea name="notes" placeholder="Optional"></textarea></label>
  <button class="btn btn-primary" type="submit">Request my free call</button>
  <p class="note" role="status">We reply within one business day. Your details stay private.</p>
</form>"""


def faq_block(faqs, open_first=True):
    out = []
    for i, (q, a) in enumerate(faqs):
        out.append(f'<details{" open" if (i == 0 and open_first) else ""}><summary>{esc(q)}</summary><p>{a}</p></details>')
    return '<div class="faq">' + "".join(out) + "</div>"


def crumbs(trail):
    items = "".join(
        f'<li><a href="{p}">{esc(n)}</a></li>' if i < len(trail) - 1 else f'<li aria-current="page">{esc(n)}</li>'
        for i, (n, p) in enumerate(trail))
    return f'<ol class="crumbs" aria-label="Breadcrumb">{items}</ol>'


def post_card(p, heading="h3"):
    return (f'<a class="pcard" href="/blog/{p["slug"]}/"><div class="pic"><img src="/assets/{p["image"]}" alt="{esc(p["alt"])}" loading="lazy"></div>'
            f'<div class="txt"><span class="kicker">{esc(p["kicker"])} · {p["read"]} min read</span><{heading}>{esc(p["h1"])}</{heading}>'
            f'<p>{esc(p["excerpt"])}</p><span class="more">Read article →</span></div></a>')


def cta_band(title="Ready to talk about your dog?", text="Book a free 15-minute call. We'll recommend the best first step. No obligation."):
    return f"""<section style="padding-top:0"><div class="wrap"><div class="band">
<div><h2>{esc(title)}</h2><p style="margin-top:10px">{esc(text)}</p></div>
<div class="btns"><a class="btn btn-primary" href="/contact/">Book a free call</a><a class="btn btn-glass" href="tel:{SITE['phone_e164']}">{SITE['phone']}</a></div>
</div></div></section>"""


# ----------------------------------------------------------------------------
# Pages
# ----------------------------------------------------------------------------
def build_home():
    main = (ROOT / "src" / "home.html").read_text(encoding="utf-8")
    # service detail links
    for key, label in (("obedience", "Book obedience"), ("behaviour", "Book behaviour"), ("puppy", "Book puppy")):
        s = SERVICES[key]
        old = f'<a class="btn btn-primary btn-sm" href="#book">{label}</a>'
        main = main.replace(old, old + f'<a class="textlink" href="{s["path"]}">Details →</a>')
    teaser = ('<section style="padding-top:0"><div class="wrap"><div class="center"><span class="eyebrow">Learn</span>'
              '<h2>Dog training advice from Austin trainers</h2><p class="lead">Straight answers to the questions owners ask us most.</p></div>'
              '<div class="cards three">' + "".join(post_card(p) for p in BLOG[:3]) + '</div>'
              '<p class="center" style="margin-top:28px"><a class="btn btn-glass" href="/blog/">See all articles</a></p></div></section>\n\n  <!-- FAQ -->')
    main = main.replace("<!-- FAQ -->", teaser, 1)
    main = main.replace('<form class="glass form" id="bookForm" novalidate>', '<form class="glass form lead-form" novalidate>', 1)
    main = main.replace('<p class="note" id="formMsg" role="status">', '<p class="note" role="status">', 1)
    extra = (ld(local_business_ld()) +
             ld({"@context": "https://schema.org", "@type": "WebSite", "name": SITE["name"], "url": url("/")}) +
             ld(faq_ld(HOME_FAQS)))
    title = "Dog Trainer Austin TX | In-Home Dog Training | Paws & Path"
    desc = "Austin dog trainer offering in-home, force-free dog training. Leash pulling, dog reactivity, barking, puppy training and recall. Book a free 15-minute call."
    page = (head(title, desc, "/", "dog trainer Austin, in-home dog training Austin TX, dog training near me, puppy training Austin, leash reactivity training, stop dog pulling on leash, dog barking training, force-free dog trainer", extra, page_type="home", page_title="Home")
            + header("/") + main + footer())
    # Replace hash nav for hero secondary and keep anchors working
    write("/index.html", page)


def build_services():
    # Hub
    cards = "".join(
        f'<a class="pcard" href="{s["path"]}"><div class="pic"><img src="/assets/{s["image"]}" alt="{esc(s["alt"])}" loading="lazy"></div>'
        f'<div class="txt"><span class="kicker">From ${s["price"]}</span><h2>{esc(s["name"])} in Austin</h2><p>{esc(s["lead"])}</p><span class="more">View details →</span></div></a>'
        for s in SERVICES.values())
    trail = [("Home", "/"), ("Services", "/services/")]
    body = (header("/services/") + f"""<main><section class="page-hero"><div class="wrap">{crumbs(trail)}
<h1>Dog training services in Austin, TX</h1>
<p class="lead">Three programmes, one approach: reward-based, in your home, with support for the life of your dog.</p></div></section>
<section style="padding-top:20px"><div class="wrap"><div class="cards three">{cards}</div></div></section>
<section style="padding-top:0"><div class="wrap layout"><div class="prose">
<h2>How we train</h2>
<p>Every programme follows the same standards: reward-based methods only, a written plan after each visit, honest timelines, and phone and email support afterwards. We don't use prong, choke or shock collars.</p>
<h2>Where we work</h2>
<p>We visit homes across {', '.join(SITE['areas'][:-1])} and {SITE['areas'][-1]}. Not sure you're in our area? <a href="/contact/">Ask us</a>.</p>
<h2>Not sure where to start?</h2>
<p>Read <a href="/blog/in-home-vs-group-dog-training/">in-home vs group training</a> or <a href="/blog/how-to-choose-a-dog-trainer-austin/">how to choose a trainer</a>, or just book a free call and tell us what's going on.</p>
</div><aside class="sidebar"><div class="glass side-card"><h3>Free 15-minute call</h3><p>Tell us what your dog is up to and we'll recommend the best first step.</p><a class="btn btn-primary btn-sm" href="/contact/">Book a call</a></div></aside></div></section>
{cta_band()}</main>""" + footer())
    extra = ld(breadcrumb_ld(trail)) + ld(local_business_ld())
    write("/services/", head("Dog Training Services Austin TX | Paws & Path",
                             "Dog training services in Austin, TX: obedience, behaviour and reactivity help, and puppy training. Force-free, in-home, with lifetime support.",
                             "/services/", "dog training services Austin, dog trainer Austin TX, in-home dog training", extra, page_title="Services") + body)

    for key, s in SERVICES.items():
        trail = [("Home", "/"), ("Services", "/services/"), (s["name"], s["path"])]
        secs = "".join(f'<h2 id="{slugify(h)}">{esc(h)}</h2>{b}' for h, b in s["sections"])
        toc = "".join(f'<li><a href="#{slugify(h)}">{esc(h)}</a></li>' for h, _ in s["sections"]) + '<li><a href="#faq">FAQs</a></li>'
        related = "".join(post_card(p) for p in BLOG if p["slug"] in s["related"])
        body = (header("/services/") + f"""<main><section class="page-hero"><div class="wrap">{crumbs(trail)}
<h1>{esc(s['h1'])}</h1><p class="lead">{esc(s['lead'])}</p>
<div class="meta-row"><span><b>From ${s['price']}</b> {esc(s['price_note'])}</span><span><b>Reward-based</b> methods only</span><span><b>In-home</b> across {', '.join(SITE['areas'])}</span></div>
</div></section>
<section style="padding-top:20px"><div class="wrap"><div class="cover"><img src="/assets/{s['image']}" alt="{esc(s['alt'])}"></div>
<div class="layout"><div class="prose">{secs}<h2 id="faq">{esc(s['name'])} FAQs</h2>{faq_block(s['faqs'])}</div>
<aside class="sidebar"><div class="glass side-card"><h3>Book a free call</h3><p>15 minutes, no obligation. We'll recommend the best first step.</p><a class="btn btn-primary btn-sm" href="/contact/">Request a call</a><p style="margin:14px 0 0;font-size:.92rem">Or call <a href="tel:{SITE['phone_e164']}">{SITE['phone']}</a></p></div>
<div class="glass side-card"><h3>On this page</h3><ul class="toc">{toc}</ul></div></aside></div></div></section>
<section style="padding-top:0"><div class="wrap"><h2>Helpful reading</h2><div class="cards three">{related}</div></div></section>
{cta_band()}</main>""" + footer())
        offer = {"@context": "https://schema.org", "@type": "Service", "name": s["h1"], "serviceType": s["name"],
                 "description": s["description"], "url": url(s["path"]), "image": url("/assets/" + s["image"]),
                 "provider": {"@type": "LocalBusiness", "@id": url("/#business"), "name": SITE["name"]},
                 "areaServed": [{"@type": "City", "name": a} for a in SITE["areas"]],
                 "offers": {"@type": "Offer", "priceCurrency": "USD", "price": str(s["price"]), "url": url("/contact/")}}
        extra = ld(offer) + ld(breadcrumb_ld(trail)) + ld(faq_ld(s["faqs"]))
        write(s["path"], head(s["title"], s["description"], s["path"], s["keywords"], extra, page_type="service",
                              og_image="/assets/" + s["image"], page_title=s["name"]) + body)


def build_about():
    trail = [("Home", "/"), ("About", "/about/")]
    body = (header("/about/") + f"""<main><section class="page-hero"><div class="wrap">{crumbs(trail)}
<h1>About Paws &amp; Path, Austin dog trainers</h1>
<p class="lead">A small team of certified, force-free trainers who work in your home, on your street, with your dog.</p></div></section>
<section style="padding-top:20px"><div class="wrap"><div class="trainer">
<div class="portrait"><img src="/assets/trainer.jpg" alt="Alex Morgan, certified dog trainer in Austin, TX, outdoors with a dog" loading="lazy"></div>
<div class="bio"><span class="eyebrow">Founder</span><h2>Alex Morgan, CPDT-KA</h2>
<blockquote>"Most dogs aren't stubborn. They just haven't been shown what we want in a way they can understand."</blockquote>
<p>Alex started Paws &amp; Path in 2012 after years volunteering with rescue dogs. Since then the team has worked with more than 1,200 dogs across Austin, Round Rock, Cedar Park and Pflugerville, from nervous rescues to boisterous labs to puppies on their first night home.</p>
<div class="creds"><div class="glass-in"><strong>CPDT-KA</strong>Certified Professional Dog Trainer</div><div class="glass-in"><strong>12 years</strong>Hands-on, in-home coaching</div><div class="glass-in"><strong>Insured</strong>Fully bonded for home visits</div><div class="glass-in"><strong>APDT</strong>Member, follows its ethics code</div></div></div></div></div></section>
<section style="padding-top:0"><div class="wrap layout"><div class="prose">
<h2>Our approach</h2>
<p>We train with rewards. Treats, toys, play and praise show your dog what we want, and we manage the environment so they can succeed. We don't use prong, choke or shock collars, and we don't believe in "dominance" or "alpha" theories. Modern behaviour science has moved on, and dogs do better when they aren't afraid.</p>
<h2>Why we train at home</h2>
<p>Classroom skills often fall apart on your street. By working in your home and on your usual routes, we deal with the real problem in the real place. The whole household can take part, and the plan fits your routine.</p>
<h2>What we promise</h2>
<ul><li>Reward-based methods only.</li><li>A written plan after every visit.</li><li>Honest advice about timelines and cost, including when you don't need a package.</li><li>Phone and email support for the life of your dog.</li></ul>
<h2>Credentials and insurance</h2>
<p>Alex holds the CPDT-KA credential and keeps up with continuing education. We carry liability insurance and bonding for in-home visits, and follow a published code of ethics. Not sure what to look for in any trainer? Our guide on <a href="/blog/how-to-choose-a-dog-trainer-austin/">choosing a dog trainer in Austin</a> lists nine questions to ask.</p>
</div><aside class="sidebar"><div class="glass side-card"><h3>Meet us</h3><p>Book a free 15-minute call and ask us anything.</p><a class="btn btn-primary btn-sm" href="/contact/">Book a call</a></div></aside></div></section>
{cta_band()}</main>""" + footer())
    extra = ld(breadcrumb_ld(trail)) + ld({"@context": "https://schema.org", "@type": "AboutPage", "name": "About Paws & Path", "url": url("/about/")}) + ld(local_business_ld())
    write("/about/", head("About Paws & Path | Certified Dog Trainer Austin TX",
                          "Meet Alex Morgan, CPDT-KA, and the Paws & Path team. Force-free, in-home dog training in Austin, Round Rock, Cedar Park and Pflugerville since 2012.",
                          "/about/", "dog trainer Austin TX, certified dog trainer Austin, CPDT-KA Austin, force-free trainer", extra, og_image="/assets/trainer.jpg", page_title="About") + body)


def build_faq():
    trail = [("Home", "/"), ("FAQ", "/faq/")]
    groups = "".join(f'<h2>{esc(g)}</h2>{faq_block(qs, open_first=False)}' for g, qs in FAQ_PAGE)
    allq = [qa for _, qs in FAQ_PAGE for qa in qs]
    body = (header("/faq/") + f"""<main><section class="page-hero"><div class="wrap">{crumbs(trail)}
<h1>Dog training FAQs for Austin owners</h1>
<p class="lead">Answers to what people ask before they book: methods, prices, puppies, behaviour and how it all works.</p></div></section>
<section style="padding-top:20px"><div class="wrap layout"><div class="prose">{groups}</div>
<aside class="sidebar"><div class="glass side-card"><h3>Still not sure?</h3><p>Call <a href="tel:{SITE['phone_e164']}">{SITE['phone']}</a> or book a free 15-minute call.</p><a class="btn btn-primary btn-sm" href="/contact/">Book a call</a></div></aside></div></section>
{cta_band()}</main>""" + footer())
    extra = ld(breadcrumb_ld(trail)) + ld(faq_ld(allq))
    write("/faq/", head("Dog Training FAQ Austin TX | Paws & Path",
                        "Answers to common dog training questions in Austin: cost, methods, puppy training, reactivity, barking, sessions and refunds.",
                        "/faq/", "dog training FAQ Austin, how much does dog training cost, puppy training questions", extra, page_title="FAQ") + body)


def build_contact():
    trail = [("Home", "/"), ("Contact", "/contact/")]
    body = (header("/contact/") + f"""<main><section class="page-hero"><div class="wrap">{crumbs(trail)}
<h1>Book your free dog training call in Austin</h1>
<p class="lead">Tell us about your dog. We'll recommend the best first step. No obligation.</p></div></section>
<section id="book" style="padding-top:20px"><div class="wrap"><div class="book">
<div class="glass book-info"><h2 style="font-size:1.6rem">Get in touch</h2>
<dl><div><dt>Phone</dt><dd><a href="tel:{SITE['phone_e164']}" class="textlink">{SITE['phone']}</a></dd></div>
<div><dt>Email</dt><dd><a href="mailto:{SITE['email']}" class="textlink">{SITE['email']}</a></dd></div>
<div><dt>Service area</dt><dd>{', '.join(SITE['areas'])}</dd></div>
<div><dt>Hours</dt><dd>Mon–Sat, 8am–6pm</dd></div></dl></div>
{lead_form()}</div>
<div class="next-steps"><div class="glass nstep"><b>1</b><h3>Book a call</h3><p>Fifteen minutes to hear what's going on.</p></div>
<div class="glass nstep"><b>2</b><h3>We visit</h3><p>In your home, with your dog and your household.</p></div>
<div class="glass nstep"><b>3</b><h3>Plan and support</h3><p>A written plan, plus support afterwards.</p></div></div></div></section></main>""" + footer())
    extra = ld(breadcrumb_ld(trail)) + ld({"@context": "https://schema.org", "@type": "ContactPage", "name": "Contact Paws & Path", "url": url("/contact/")}) + ld(local_business_ld())
    write("/contact/", head("Contact Paws & Path | Book a Dog Trainer in Austin TX",
                            "Book a free 15-minute call with Austin dog trainers Paws & Path. In-home obedience, behaviour and puppy training across Austin, Round Rock and Cedar Park.",
                            "/contact/", "book dog trainer Austin, dog training consultation Austin, dog trainer near me", extra, page_title="Contact") + body)


def build_blog():
    trail = [("Home", "/"), ("Blog", "/blog/")]
    cards = "".join(post_card(p, "h2") for p in BLOG)
    body = (header("/blog/") + f"""<main><section class="page-hero"><div class="wrap">{crumbs(trail)}
<h1>Dog training advice from Austin trainers</h1>
<p class="lead">Straight answers on leash pulling, reactivity, puppies, barking, recall and choosing a trainer.</p></div></section>
<section style="padding-top:20px"><div class="wrap"><div class="cards three">{cards}</div></div></section>
{cta_band()}</main>""" + footer())
    extra = ld(breadcrumb_ld(trail)) + ld({"@context": "https://schema.org", "@type": "Blog", "name": "Paws & Path dog training blog", "url": url("/blog/"),
                                          "blogPost": [{"@type": "BlogPosting", "headline": p["h1"], "url": url(f"/blog/{p['slug']}/"), "datePublished": p["date"]} for p in BLOG]})
    write("/blog/", head("Dog Training Blog Austin TX | Tips for Owners | Paws & Path",
                         "Dog training advice from Austin trainers: leash pulling, reactivity, puppy biting, house training, barking, recall, anxiety and how to choose a trainer.",
                         "/blog/", "dog training blog, dog training tips Austin, puppy training advice", extra, page_title="Blog") + body)

    for p in BLOG:
        path = f"/blog/{p['slug']}/"
        s = SERVICES[p["service"]]
        trail = [("Home", "/"), ("Blog", "/blog/"), (p["h1"], path)]
        h2s = re.findall(r"<h2>(.*?)</h2>", p["body"])
        content = p["body"]
        for h in h2s:
            content = content.replace(f"<h2>{h}</h2>", f'<h2 id="{slugify(h)}">{h}</h2>', 1)
        toc = "".join(f'<li><a href="#{slugify(h)}">{h}</a></li>' for h in h2s) + '<li><a href="#faq">FAQs</a></li>'
        others = [q for q in BLOG if q["slug"] != p["slug"]]
        # same-service posts first
        others.sort(key=lambda q: (q["service"] != p["service"], q["date"]))
        related = "".join(post_card(q) for q in others[:3])
        words = len(re.sub(r"<[^>]+>", " ", p["body"]).split())
        body = (header("/blog/") + f"""<main><article><section class="page-hero"><div class="wrap">{crumbs(trail[:2] + [(p['h1'], path)])}
<h1>{esc(p['h1'])}</h1><p class="lead">{esc(p['excerpt'])}</p>
<div class="meta-row"><span>By <b>Alex Morgan, CPDT-KA</b></span><span><time datetime="{p['date']}">{p['date']}</time></span><span>{p['read']} min read</span></div></div></section>
<section style="padding-top:20px"><div class="wrap"><div class="cover"><img src="/assets/{p['image']}" alt="{esc(p['alt'])}"></div>
<div class="layout"><div class="prose">{content}<h2 id="faq">Quick answers</h2>{faq_block(p['faqs'], open_first=False)}
<div class="callout"><p>Want help with this in person? See our <a href="{s['path']}">{esc(s['name'].lower())} in Austin</a> or <a href="/contact/">book a free call</a>.</p></div></div>
<aside class="sidebar"><div class="glass side-card"><h3>On this page</h3><ul class="toc">{toc}</ul></div>
<div class="glass side-card"><h3>Need a hand?</h3><p>Free 15-minute call. We'll point you to the right first step.</p><a class="btn btn-primary btn-sm" href="/contact/">Book a call</a></div></aside></div></div></section>
<section style="padding-top:0"><div class="wrap"><h2>Keep reading</h2><div class="cards three">{related}</div></div></section></article>
{cta_band()}</main>""" + footer())
        article = {"@context": "https://schema.org", "@type": "BlogPosting", "headline": p["h1"], "description": p["description"],
                   "image": url("/assets/" + p["image"]), "datePublished": p["date"], "dateModified": p["date"], "wordCount": words,
                   "keywords": p["keywords"], "mainEntityOfPage": url(path),
                   "author": {"@type": "Person", "name": "Alex Morgan", "jobTitle": "Certified Professional Dog Trainer (CPDT-KA)", "url": url("/about/")},
                   "publisher": {"@type": "Organization", "name": SITE["name"], "url": url("/")}}
        extra = ld(article) + ld(breadcrumb_ld(trail)) + ld(faq_ld(p["faqs"]))
        write(path, head(p["title"], p["description"], path, p["keywords"], extra, og_type="article",
                         og_image="/assets/" + p["image"], page_type="blog", page_title=p["h1"]) + body)


def build_privacy():
    trail = [("Home", "/"), ("Privacy", "/privacy/")]
    body = (header("") + f"""<main><section class="page-hero"><div class="wrap">{crumbs(trail)}<h1>Privacy policy</h1>
<p class="lead">How we handle your information, cookies and advertising tools.</p></div></section>
<section style="padding-top:20px"><div class="wrap"><div class="prose">
<p><strong>Template notice:</strong> this policy is a starting point. Have it reviewed against the laws that apply to your business before launch.</p>
<h2>What we collect</h2><p>When you fill in our booking form we receive your name, email, optional phone number, your dog's details and your message. We use it to reply to you and plan your session.</p>
<h2>Cookies and advertising tools</h2><p>With your consent we use Google Analytics, Google Ads and the Meta Pixel to measure visits and the performance of our ads. If you decline, these tools are blocked from storing identifiers on your device. You can change your choice any time with the "Cookie settings" link in the footer.</p>
<h2>Who we share it with</h2><p>We don't sell your information. Analytics and advertising providers receive data only when you consent. Our form and scheduling providers process data on our behalf.</p>
<h2>Your rights</h2><p>You can ask to see, correct or delete your information by emailing <a href="mailto:{SITE['email']}">{SITE['email']}</a>.</p>
</div></div></section></main>""" + footer())
    write("/privacy/", head("Privacy Policy | Paws & Path", "How Paws & Path handles your information, cookies and advertising tools.", "/privacy/", "", '<meta name="robots" content="noindex, follow">', page_title="Privacy") + body)


def build_404():
    body = (header("") + """<main><section class="page-hero"><div class="wrap"><h1>Page not found</h1>
<p class="lead">That page has wandered off. Try one of these instead.</p>
<p style="display:flex;gap:12px;flex-wrap:wrap"><a class="btn btn-primary" href="/">Home</a><a class="btn btn-glass" href="/services/">Services</a><a class="btn btn-glass" href="/blog/">Blog</a></p></div></section></main>""" + footer())
    write("/404.html", head("Page not found | Paws & Path", "Page not found.", "/404.html", "", '<meta name="robots" content="noindex">', page_title="404") + body)


def build_sitemap():
    urls = [("/", "1.0", "weekly"), ("/services/", "0.9", "monthly"), ("/about/", "0.7", "monthly"), ("/faq/", "0.7", "monthly"),
            ("/contact/", "0.8", "monthly"), ("/blog/", "0.8", "weekly")]
    urls += [(s["path"], "0.9", "monthly") for s in SERVICES.values()]
    entries = [f"<url><loc>{url(p)}</loc><changefreq>{f}</changefreq><priority>{pr}</priority></url>" for p, pr, f in urls]
    entries += [f"<url><loc>{url('/blog/' + p['slug'] + '/')}</loc><lastmod>{p['date']}</lastmod><changefreq>monthly</changefreq><priority>0.7</priority></url>" for p in BLOG]
    (ROOT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "\n".join(entries) + "\n</urlset>\n", encoding="utf-8")
    (ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nDisallow: /src/\nDisallow: /.claude/\n\nSitemap: {url('/sitemap.xml')}\n", encoding="utf-8")


if __name__ == "__main__":
    build_home()
    build_services()
    build_about()
    build_faq()
    build_contact()
    build_blog()
    build_privacy()
    build_404()
    build_sitemap()
    print("Built:", ", ".join(sorted(str(p.relative_to(ROOT)) for p in ROOT.rglob("index.html") if ".claude" not in str(p))))
