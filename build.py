#!/usr/bin/env python3
"""Bluff Creek Baptist Church — static site generator (Homestead kit).
Run:  python3 build.py   → writes *.html into this folder. Content lives below; layout is shared.
"""
import os, html, datetime, re
from image_helpers import responsive_image
from event_helpers import render_event_rows
from seo_helpers import schema_json, generate_redirects
ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = "https://www.bluffcreekbaptistchurch.org"
APP = "https://app.bluffcreekbaptistchurch.org/"
GIVE = "https://buy.stripe.com/9B600j6Q68IFgK8h13bo400"
YT_CHANNEL_ID = "UC75FUMm1TckzTRpfYHd_ILQ"   # @bluffcreekbc — Bluff Creek Baptist Church (created 2026-09-04)
FACEBOOK = "https://www.facebook.com/bluffcreekbaptist"
WATCH = (f"https://www.youtube.com/channel/{YT_CHANNEL_ID}/live" if YT_CHANNEL_ID else FACEBOOK)
EMAIL = "bluffcreekbaptist@gmail.com"
PHONE = "(225) 218-7902"; PHONE_TEL = "+12252187902"
YEAR = datetime.date.today().year
EVENTS_URL = "https://app.bluffcreekbaptistchurch.org/events.json"
EVENTS_FALLBACK = [
    {"when":"2026-09-06","time":"9:00a","title":"Sunday School","where":"Fellowship Building","tag":"Weekly"},
    {"when":"2026-09-06","time":"10:15a","title":"Sunday Worship","where":"Sanctuary","tag":"Weekly"},
    {"when":"2026-09-06","time":"5:30p","title":"Youth discipleship","where":"Fellowship Building","tag":"Weekly"},
    {"when":"2026-09-06","time":"6:00p","title":"Evening service","where":"Sanctuary","tag":"Weekly"},
    {"when":"2026-09-07","time":"6:30p","title":"Women’s Bible study","where":"Contact church office for location","tag":"Weekly"},
    {"when":"2026-09-08","time":"5:00p","title":"Yoga @ the Creek","where":"Fellowship Building","tag":"Weekly"},
    {"when":"2026-09-09","time":"6:00p","title":"Prayer meeting","where":"Sanctuary","tag":"Weekly"},
    {"when":"2026-09-09","time":"6:00p","title":"Youth @ the Creek — MDWK","where":"Fellowship Building","tag":"Weekly"},
    {"when":"2026-09-10","time":"5:00p","title":"Yoga @ the Creek","where":"Fellowship Building","tag":"Weekly"},
]

NAV = [("about","Our Church"),("ministries","Find Your Place"),
       ("times","This Week"),("watch","Watch"),("give","Give")]

def event_rows(events=EVENTS_FALLBACK, limit=3):
    return render_event_rows(events, limit)

EVENTS_SCRIPT = f'<script src="js/events.js" data-events-url="{html.escape(EVENTS_URL, quote=True)}" defer></script>'

# Interior headings use the brand itself; photos are reserved for useful wayfinding.
HEAD_RE = re.compile(
    r'\s*<section class="sec">\s*<div class="eye">(?P<eye>.*?)</div>\s*<h1>(?P<h1>.*?)</h1>\s*'
    r'(?:<p class="lead">(?P<lead>.*?)</p>\s*)?', re.S)

def page_hero(slug, body):
    """Lift the interior title into a light editorial heading."""
    if slug == "index":
        return "", body
    m = HEAD_RE.match(body)
    if not m:
        return "", body
    lead = f'<p class="lead">{m.group("lead")}</p>' if m.group("lead") else ""
    hero = f"""<section class="interior-heading">
  <a class="breadcrumb" href="index.html">Home <span aria-hidden="true">/</span></a>
  <div class="eye">{m.group('eye')}</div>
  <h1>{m.group('h1')}</h1>
{lead}
  <img class="heading-creek" src="assets/creek-gold.png" alt="" width="372" height="93">
</section>
"""
    return hero, '<section class="sec">' + body[m.end():]

def layout(slug, title, desc, body, extra_head=""):
    nav = "".join(f'<a href="{s}.html"{" aria-current=\"page\"" if s==slug else ""}>{t}</a>' for s,t in NAV)
    hero, body = page_hero(slug, body)
    events_script = EVENTS_SCRIPT + "\n" if 'data-events-feed' in body else ''
    structured_data = '' if slug == '404' else '<script type="application/ld+json">' + schema_json(
        SITE, slug, title, desc, app=APP,
        watch=f'https://www.youtube.com/channel/{YT_CHANNEL_ID}' if YT_CHANNEL_ID else FACEBOOK,
        facebook=FACEBOOK, social_urls=[
            'https://www.instagram.com/bluffcreekbaptistchurch/',
            'https://www.instagram.com/bluffcreekstudents/',
        ],
    ) + '</script>'
    error_head = '''<meta name="robots" content="noindex,follow">
<base href="/">
<script>
(function(){
  if(location.hostname.endsWith('.github.io')){
    document.querySelector('base').setAttribute('href','/bluffcreekbaptistchurch.org/');
  }
  document.addEventListener('DOMContentLoaded',function(){
    document.querySelectorAll('a[href^="#"]').forEach(function(link){
      link.setAttribute('href',location.pathname+location.search+link.getAttribute('href'));
    });
  });
})();
</script>''' if slug == '404' else ''
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
{error_head}
<title>{html.escape(title)} — Bluff Creek Baptist Church</title>
<meta name="description" content="{html.escape(desc)}">
<meta property="og:title" content="{html.escape(title)} — Bluff Creek Baptist Church">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:image" content="{SITE}/assets/social/{slug if slug != '404' else 'index'}.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:type" content="website">
<meta property="og:url" content="{SITE}/{'' if slug=='index' else slug+'.html'}">
<meta property="og:site_name" content="Bluff Creek Baptist Church">
<meta name="twitter:card" content="summary_large_image">
<meta property="og:image:alt" content="{html.escape(title)} — Bluff Creek Baptist Church, Clinton, Louisiana">
<meta name="theme-color" content="#3C5A45">
<link rel="icon" type="image/png" sizes="32x32" href="assets/favicon-32.png">
<link rel="apple-touch-icon" href="assets/apple-touch-icon.png">
<link rel="canonical" href="{SITE}/{'' if slug=='index' else slug+'.html'}">
<link rel="preload" href="assets/fonts/bitter-latin-normal-v42.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="assets/fonts/nunito-sans-latin-normal-v19.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="css/fonts.css">
<link rel="stylesheet" href="css/site.css">
<link rel="stylesheet" href="css/polish.css">
<noscript><style>
#cform{{display:none}}
@media(max-width:1040px){{
  .editorial .top{{position:static}}
  .editorial .top .wrap{{height:auto;min-height:82px;flex-wrap:wrap;padding-top:14px;padding-bottom:14px}}
  .editorial .burger{{display:none}}
  .editorial nav.main{{display:flex;position:static;flex-direction:row;flex-wrap:wrap;width:100%;max-height:none;overflow:visible;border:0;box-shadow:none;padding:0}}
  .editorial nav.main a.cta{{margin:0}}
}}
</style></noscript>
{structured_data}
{extra_head}
</head>
<body class="editorial page-{slug}">
<a class="skip" href="#main">Skip to content</a>
<header class="top" id="top"><div class="wrap">
  <a class="brand" href="index.html" aria-label="Bluff Creek Baptist Church — home">
    <img src="assets/logo.png" alt="" width="930" height="192">
  </a>
  <button class="burger" aria-label="Menu" aria-controls="nav" aria-expanded="false"><span>Menu</span><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round"><path d="M4 7h16M4 12h16M4 17h16"/></svg></button>
  <nav class="main" id="nav" aria-label="Primary">{nav}<a class="cta" href="visit.html"{' aria-current="page"' if slug=='visit' else ''}>Plan a Visit <span aria-hidden="true">↗</span></a></nav>
</div></header>
<main class="wrap" id="main" tabindex="-1">
{hero}
{body}
</main>
<footer>
  <div class="wm" aria-hidden="true">63</div>
  <img class="tex" src="assets/creek-ivory.png" alt="" aria-hidden="true">
  <div class="wrap">
    <div>
      <img class="logo" src="assets/logo-white.png" alt="Bluff Creek Baptist Church" width="1500" height="309" loading="lazy">
      <p style="color:#e6ddc7;max-width:34ch;font-size:15px">A country church on Highway 63 — rooted in the Word, sharing Christ with our community and the world, walking together as one family in Him.</p>
      <div class="byline"><img class="la63" src="assets/la63.svg" alt="">1706 · LA 63 · Clinton</div>
    </div>
    <div><h4>Come see us</h4><a href="visit.html">Plan a visit</a><a href="times.html">When we meet</a><a href="about.html">Who we are</a><a href="beliefs.html">What we believe</a><a href="membership.html">Becoming a member</a></div>
    <div><h4>The Creek</h4><a href="ministries.html">Ministries @ the Creek</a><a href="missions.html">Missions @ the Creek</a><a href="give.html">Give</a><a href="watch.html">Watch</a><a href="contact.html">Contact</a><a href="{APP}">Home @ the Creek — the app</a><h4 style="margin-top:16px">Follow</h4><a href="https://www.facebook.com/bluffcreekbaptist" target="_blank" rel="noopener">Facebook</a><a href="https://www.instagram.com/bluffcreekbaptistchurch/" target="_blank" rel="noopener">Instagram</a><a href="https://www.instagram.com/bluffcreekstudents/" target="_blank" rel="noopener">Students on Instagram</a><a href="webcal://p24-caldav.icloud.com/published/2/MjgxNDIwMTA5MjgxNDIwMZkrrqg7P_e_uOJSEuneGS4QT-quA4OE5lbjyAKZifNVcV3yYLBvdcwT4okvZF-44VCzkvYBgUEuOzihC5igIm4">Subscribe to our calendar</a></div>
    <div class="fine"><span>1706 Highway 63 · Clinton, Louisiana 70722 · <a href="tel:{PHONE_TEL}" style="display:inline;padding:0">{PHONE}</a> · <a href="mailto:{EMAIL}" style="display:inline;padding:0">{EMAIL}</a></span><span>© {YEAR} Bluff Creek Baptist Church · "Go therefore and make disciples of all nations." Matthew 28:19</span></div>
  </div>
</footer>
<script>
(function(){{
  var top=document.getElementById('top');
  var button=top.querySelector('.burger'),nav=document.getElementById('nav');
  function closeMenu(){{nav.classList.remove('open');button.setAttribute('aria-expanded','false');}}
  button.addEventListener('click',function(){{var open=nav.classList.toggle('open');button.setAttribute('aria-expanded',String(open));}});
  nav.addEventListener('click',function(e){{if(e.target.closest('a'))closeMenu();}});
  document.addEventListener('keydown',function(e){{if(e.key==='Escape'&&nav.classList.contains('open')){{closeMenu();button.focus();}}}});
  document.addEventListener('click',function(e){{if(!top.contains(e.target))closeMenu();}});
}})();
</script>
{events_script}</body>
</html>
"""

def lock(name, color="var(--wheat)", size=24):
    return f'<div class="lock" style="font-size:{size}px;--ministry-accent:{color}">{name} <span class="at">@</span> the Creek</div><img class="creek" src="assets/creek-gold.png" alt="" width="372" height="93" style="width:60%;max-width:168px;margin:6px 0 10px">'

PAGES = {}

# ---------------- HOME ----------------
PAGES["index"] = ("Welcome home to the Creek", "A country church in Clinton, Louisiana. Rooted in the Word, growing together, with room for your family.", f"""
<section class="home-hero" aria-labelledby="welcome-title">
  <div class="home-hero-photo" aria-hidden="true">{responsive_image("hero-church.jpg", "", "100vw", "welcome-photo", loading="eager")}</div>
  <div class="wrap home-hero-grid"><div class="home-hero-copy">
    <p class="eye">Bluff Creek Baptist Church</p>
    <h1 id="welcome-title">Welcome home<br>to the Creek.</h1>
    <img class="welcome-creek" src="assets/creek-gold.png" alt="" width="372" height="93">
    <p class="welcome-intro">A country church on Highway 63, rooted in the Word and walking together as one family in Christ.</p>
    <div class="actions"><a class="btn" href="visit.html">Plan a visit <span aria-hidden="true">↗</span></a><a class="hero-secondary" href="#church-family">Meet our church <span aria-hidden="true">↓</span></a></div>
  </div></div>
</section>

<div class="home-wayline"><div class="wrap">
  <a class="home-address" href="contact.html"><img src="assets/la63.svg" alt="" width="32" height="32"><span><b>1706 · LA 63 · Clinton</b><span>A little way down the road. A place to call home.</span></span><span class="wayline-arrow" aria-hidden="true">↗</span></a>
  <a class="home-scroll" href="#church-family">Discover life at the Creek <span aria-hidden="true">↓</span></a>
</div></div>

<section class="band home-story" id="church-family" aria-labelledby="church-family-title">
  <div class="home-story-backdrop" aria-hidden="true">{responsive_image("sign.jpg", "", "(max-width: 760px) 100vw, 62vw", "home-story-photo")}</div>
  <div class="wrap home-story-grid">
    <div class="home-story-heading"><p class="eye">This is Bluff Creek</p><h2 id="church-family-title">A country church.<br>A church family.</h2><p class="home-roots">Rooted here, on Highway 63.</p></div>
    <div class="home-story-copy"><p class="home-purpose">We exist to glorify God<br>and enjoy Him forever.</p><p>We’re a traditional Southern Baptist church. You’ll hear hymns with deep roots, prayer from the heart, and preaching straight from Scripture.</p><p>And after the service? We’ll probably still be talking.</p><a class="textlink" href="about.html">Get to know our church <span aria-hidden="true">↗</span></a></div>
  </div>
</section>

<section class="band home-belong" id="find-your-place" aria-labelledby="belong-title"><div class="wrap home-belong-grid">
  <div class="home-belong-intro"><p class="eye">Life together</p><h2 id="belong-title">A place for<br>your family.</h2><p>Little ones. Growing students. Every age and season of life. There’s a place to learn God’s Word and walk with others here.</p><a class="textlink" href="ministries.html">Explore our ministries <span aria-hidden="true">↗</span></a></div>
  <div class="home-ministry-list">
    <a class="home-ministry" href="ministries.html#kidz"><div><span class="micro">Birth through 5th grade</span>{lock("Kidz")}<p>A loving place for little ones to learn God’s Word.</p></div><span class="ministry-arrow" aria-hidden="true">↗</span></a>
    <a class="home-ministry" href="ministries.html#youth"><div><span class="micro">6th through 12th grade</span>{lock("Youth")}<p>Good friends. Honest questions. Faith that grows.</p></div><span class="ministry-arrow" aria-hidden="true">↗</span></a>
    <a class="home-ministry" href="ministries.html#adults"><div><span class="micro">Every age. Every season.</span>{lock("Adults")}<p>Open the Bible, find your class, and do life together.</p></div><span class="ministry-arrow" aria-hidden="true">↗</span></a>
  </div>
</div></section>

<section class="band word-band home-worship"><div class="wrap word-grid">
  <div class="word-heading"><p class="eye">Worship @ the Creek</p><h2>Straight from<br>the Word.</h2><img class="creek" src="assets/creek-gold.png" width="372" height="93" alt=""></div>
  <div class="word-copy"><p>Theologically rich hymns. Time in prayer. A word for the kids. A message that opens the Bible and walks through the text.</p><p class="word-time">Sunday worship · 10:15a</p><a class="btn" href="watch.html"><span class="play-symbol" aria-hidden="true">▶</span> Watch with us</a><a class="word-secondary" href="beliefs.html">What we believe <span aria-hidden="true">↗</span></a></div>
</div></section>

<section class="band week-band"><div class="wrap week-grid">
  <div class="week-intro"><p class="eye">Gather with us</p><h2>This week<br> at the Creek.</h2><p>Make a little room<br> for life together.</p><a class="textlink" href="times.html">All service &amp; meeting times <span aria-hidden="true">↗</span></a><div class="wednesday-note"><div class="place-rule"><b>6 on the 63</b></div><span>Wednesday prayer &amp; youth · 6:00p</span></div></div>
  <div class="event-feed" data-events-feed="3">{event_rows()}</div>
</div></section>

<section class="band first-visit home-visit" aria-labelledby="first-visit-title"><div class="wrap visit-grid">
  <div><p class="eye">First stop on the 63</p><h2 id="first-visit-title">Your first Sunday,<br>made simple.</h2><p class="lead">A few things to know.<br>A warm welcome when you get here.</p><a class="btn pine" href="visit.html">Plan your first visit <span aria-hidden="true">↗</span></a></div>
  <div class="faq">
    <details><summary>Where do I park?</summary><div class="a"><p>Use either parking lot at the corner of Highways 959 and 63. Head to the fellowship building for Sunday School at 9:00a, or the sanctuary for worship at 10:15a.</p></div></details>
    <details><summary>What about my kids?</summary><div class="a"><p>Your kids are welcome in worship. We also have a nursery during Sunday School and both Sunday services. Use it as much or as little as you like.</p></div></details>
    <details><summary>Do I need to dress up?</summary><div class="a"><p>Jeans, boots, or Sunday best—you’ll fit right in. Comfortable is what matters.</p></div></details>
    <details><summary>What is the service like?</summary><div class="a"><p>Hymns, prayer, a special word for the children, and a 30–40 minute message straight from Scripture. We’re a traditional Southern Baptist church, and we’d love to meet you.</p></div></details>
  </div>
</div><div class="wrap">
  <section class="sunday-strip" aria-label="Sunday service times and location">
    <div class="sunday-label"><span class="micro">Make yourself at home</span><b>See you Sunday.</b></div>
    <div><span class="micro">Sunday School</span><b>9:00 <small>AM</small></b></div>
    <div><span class="micro">Morning worship</span><b>10:15 <small>AM</small></b></div>
    <a class="sunday-location" href="contact.html"><span>1706 Highway 63<br><strong>Find your way here <span aria-hidden="true">↗</span></strong></span></a>
  </section>
  <aside class="home-pastor-note"><p class="eye">A note from our pastor</p><blockquote>“I’d love to sit across a table from you with a cup of coffee and hear your story.”</blockquote><p>— Cole Permenter, Pastor</p><a class="textlink" href="contact.html">Say hello <span aria-hidden="true">↗</span></a></aside>
</div></section>

<section class="band next-steps"><div class="wrap">
  <p class="eye">Keep walking with us</p>
  <div class="next-grid"><a href="missions.html"><h3>Serve our neighbors.</h3><p>Across the street and around the world.</p><span aria-hidden="true">↗</span></a><a href="give.html"><h3>Give with purpose.</h3><p>Support the ministry of Bluff Creek.</p><span aria-hidden="true">↗</span></a><a href="{APP}"><h3>Take the Creek with you.</h3><p>Prayer, events, and connection in our app.</p><span aria-hidden="true">↗</span></a></div>
</div></section>

""")

# ---------------- PLAN A VISIT ----------------
PAGES["visit"] = ("Plan a Visit", "Your first Sunday at Bluff Creek Baptist Church — where to park, when to arrive, what to do with your kids, and what the service is like.", f"""
<section class="sec">
  <div class="eye">First stop on the 63</div>
  <h1>Plan a visit.</h1>
  <p class="lead">We want your first Sunday to feel like your tenth. Here's everything people usually wonder about — and the honest answers.</p>
  <p class="visit-quicklinks"><a href="#visit-times">Service times</a><span aria-hidden="true"> · </span><a href="contact.html">Directions</a></p>
  <div class="faq">
    <details open><summary>Where do I park?</summary><div class="a"><p>We have two large parking lots. The church sits at the corner of Highways 959 and 63 — you can get to a lot from either side.</p></div></details>
    <details><summary>What time do I arrive?</summary><div class="a"><p>Sunday School starts at 9:00 for all ages. Our Sunday morning service begins at 10:15, the Sunday evening service at 6:00, and Wednesday night at 6:00. Kids' and youth activities start at various times — see <a href="ministries.html">Ministries</a> for all the ways they can plug in.</p></div></details>
    <details><summary>Where do I go?</summary><div class="a"><p>If you're here for 9:00, park and head to the fellowship building — if you're looking at the sanctuary, it's the "little sanctuary" on the right. Sunday School classes for every age are in that building and the courtyard beside it.</p><p>If you're here for 10:15 or 6:00, head to the sanctuary for "big church" — use any door you like. Sit wherever. No one truly has assigned seating, and if they "usually" sit where you choose, they'd love to sit with you. We're flexible here.</p><p>Here for a youth event? Head to the fellowship hall, the youth room in the courtyard — or most likely the pickleball court in the courtyard.</p></div></details>
    <details><summary>What do I do with my kids?</summary><div class="a"><p>Include them as much or as little as you'd like. We have a nursery for the little ones during Sunday School and both Sunday services — but don't feel obligated to use it if you'd rather have your kids in the service with you. It's really up to your family.</p><p>We're patient while kids learn the rhythm of church, and every family here is at a different place on that journey. We promise your kids will probably never do anything more distracting than our own pastor's kids have already done. Any "looks" you get will be in solidarity — we've <em>all</em> been there.</p><p>Birth to 3 meet in the nursery for Sunday School. Pre-K through high school meet in the classes next to the courtyard, off the "little sanctuary" we call the fellowship hall.</p></div></details>
    <details><summary>Where do I find the coffee?</summary><div class="a"><p>Before Sunday School there's coffee in the fellowship building's kitchen. Head on in and make yourself a cup.</p></div></details>
    <details><summary>Do I need to dress up?</summary><div class="a"><p>That's your call. As long as you're clothed, you'll fit right in. Some folks wear a suit or a dress; others prefer their Wranglers and boots. We've seen overalls right off the tractor and camo right off the stand. Comfortable is what matters.</p></div></details>
    <details><summary>What if I have special needs?</summary><div class="a"><p>Tell us how we can serve you best. If you or your family have any special needs, <a href="mailto:{EMAIL}">email us</a> and we'll do whatever we can to accommodate you.</p></div></details>
    <details><summary>What is the service like?</summary><div class="a"><p>We're a pretty traditional Southern Baptist church. In a normal service we sing theologically rich, doctrinally sound hymns, spend time in prayer, have a special word for our children (with treats!), and then our pastor preaches a 30–40 minute expositional message straight from the text. If your kids are headed to the nursery, they can go to the back foyer after the children's time.</p></div></details>
    <details><summary>What happens after the service?</summary><div class="a"><p>That's your call — but we'll probably be hanging out until they turn the lights off on us. People will want to meet you; our folks are genuinely charming and genuinely want to know you. Fill out a contact card and drop it in the offering, and our pastor will reach out during the week. He'd love to meet you for coffee — or his family would love to share a meal with yours.</p></div></details>
  </div>
  <section class="visit-times" id="visit-times" aria-labelledby="visit-times-heading"><h2 id="visit-times-heading">When we gather.</h2>
  <div class="times" style="margin:18px 0 26px">
    <div class="t" style="background:var(--surface);border-color:var(--line)"><small style="color:var(--wheat)">Sunday School</small><b style="color:var(--ink)">9:00a</b></div>
    <div class="t" style="background:var(--surface);border-color:var(--line)"><small style="color:var(--wheat)">Worship</small><b style="color:var(--ink)">10:15a</b></div>
    <div class="t" style="background:var(--surface);border-color:var(--line)"><small style="color:var(--wheat)">Sunday Evening</small><b style="color:var(--ink)">6:00p</b></div>
    <div class="t" style="background:var(--surface);border-color:var(--line)"><small style="color:var(--wheat)">Wednesday</small><b style="color:var(--ink)">6:00p</b></div>
  </div>
  </section>
  <div class="panel" style="margin-top:26px"><img class="sign" src="assets/la63.svg" alt="" aria-hidden="true"><div class="eye">Before you come</div><h3>Tell us you're coming — or just show up.</h3><p>Either way is perfect. If you'd like someone watching for you at the door, send a note and we'll be there.</p><a class="btn" href="contact.html">Say hello</a> <a class="btn ghost" href="{APP}" style="margin-left:8px">Get the app</a></div>
</section>
""")

# ---------------- WHO WE ARE ----------------
def person(name, role, text, photo=None, tall=False, initials=None):
    ph = f'<div class="ph{" tall" if tall else ""}">{responsive_image(photo, name, "92px", "staff-photo")}</div>' if photo else f'<div class="ph"><span class="init">{initials or "".join(w[0] for w in name.split()[:2])}</span></div>'
    return f'<div class="card person">{ph}<div><b>{name}</b><div class="role">{role}</div><p>{text}</p></div></div>'

PAGES["about"] = ("Who We Are", "The mission, vision, and people of Bluff Creek Baptist Church — a Southern Baptist church in Clinton, Louisiana.", f"""
<section class="sec">
  <div class="eye">Who we are</div>
  <h1>We exist to glorify God and enjoy Him forever.</h1>
  <p class="lead">Bluff Creek is a traditional Southern Baptist congregation on Highway 63 in Clinton, Louisiana. We're rooted in the Word, we cooperate with Louisiana Baptists and the Southern Baptist Convention, and we take the Great Commission personally.</p>
  <div class="word" style="max-width:760px;margin:18px 0 8px"><blockquote>"…and thus I make it my ambition to preach the gospel, not where Christ has already been named, lest I build on someone else's foundation, but as it is written, 'Those who have never been told of him will see, and those who have never heard will understand.'"</blockquote><cite>Romans 15:20–21 (ESV)</cite></div>
</section>

<section class="sec">
  <div class="sec-h"><div><div class="eye">The people</div><h2>Our staff &amp; team</h2></div></div>
  <div class="grid g3">
    {person("Cole Permenter","Senior Pastor","Pastor of Bluff Creek since 2015 — and our youth pastor before that (2012–14). Louisiana Tech (Communication) and New Orleans Baptist Theological Seminary (M.Div.). Married to Rikki; dad to Hudson and Magnolia. Retired MMA fighter, surfer, golfer, scuba diver, woodworker. He'd love to meet you for coffee.","cole-headshot.jpg")}
    {person("Julie Stevens","Children's Time · Kidz @ the Creek","A Clinton native, married to Joey for 20+ years, mom to Jackson and D'Lanie, and principal of Central Intermediate School. Julie leads the children's time in our services.",initials="JS")}
    {person("Ashleigh Pierce","Kidz @ the Creek Director","Ashleigh leads Kidz @ the Creek. Daughter of a former youth minister, married to Denver, and mom to Berlin, Ryker, Ruth, and Gabriel.","ashleigh-pierce.jpg")}
    {person("Janice McNabb","Church Secretary","Born and raised in Bluff Creek, married to Allen since 1978, mom to Alison and Jamie — and more than 30 years of faithful service keeping this church running.","janice-mcnabb.jpg",tall=True)}
    {person("Jackie Brian","Church Treasurer","Born and raised in Bluff Creek and a member for 45+ years. Sunday School and VBS teacher; mom to Kaitlin, Parker, and Preston.","jackie-brian.jpg",tall=True)}
    <div class="card person"><div class="ph"><span class="init">♪</span></div><div><b>Worship @ the Creek</b><div class="role">Music ministry team</div><p>A team of musicians leads our worship every Sunday — theologically rich, doctrinally sound hymns. All musical talents are welcome; come sing or play with us.</p></div></div>
  </div>
  <div class="card" style="margin-top:16px;border-left:4px solid var(--wheat)"><h3 style="margin:0 0 6px">We're praying for our next youth minister.</h3><p class="muted" style="margin:0">Bluff Creek is searching for the leader God has for Youth @ the Creek. If that's you — or someone you know — <a href="contact.html">we'd love to hear from you</a>.</p></div>
</section>

<section class="sec">
  <div class="grid g2">
    <div class="card"><div class="eye">Doctrine</div><h3>What we believe</h3><p>We affirm the Bible as God's inspired Word and hold to the Baptist Faith &amp; Message (2000).</p><p><a href="beliefs.html">Read our beliefs →</a></p></div>
    <div class="card"><div class="eye">Join the family</div><h3>Becoming a member</h3><p>By profession of faith and baptism, by letter, or by statement — during the invitation at the end of any Sunday morning service.</p><p><a href="membership.html">How membership works →</a></p></div>
  </div>
</section>
""")

# ---------------- BELIEFS ----------------
ART = [
 ("The Scriptures","The Holy Bible was written by men divinely inspired and is God's revelation of Himself to man — truth without any mixture of error, the true center of Christian union, and the supreme standard by which all conduct, creeds, and opinions are tried. All Scripture testifies to Christ."),
 ("God","There is one and only one living and true God — Creator, Redeemer, Preserver, and Ruler of the universe — who reveals Himself as Father, Son, and Holy Spirit, with distinct personal attributes but without division of nature, essence, or being."),
 ("God the Father","God as Father reigns with providential care over His universe, His creatures, and the flow of human history according to the purposes of His grace. He is Father in truth to those who become His children through faith in Jesus Christ."),
 ("God the Son","Christ is the eternal Son of God. Conceived of the Holy Spirit and born of the virgin Mary, He perfectly revealed and did the will of God, died a substitutionary death on the cross for our sins, rose bodily, ascended, and now reigns as the one Mediator, fully God and fully man. He will return in power and glory."),
 ("God the Holy Spirit","The Holy Spirit is fully divine. He inspired the Scriptures, convicts of sin, calls people to the Savior, effects regeneration, baptizes every believer into the body of Christ, seals them unto the day of redemption, and empowers the church for worship, evangelism, and service."),
 ("Man","Man is the special creation of God, made in His own image, male and female. Through free choice man sinned and fell, so that his posterity inherit a nature inclined toward sin. Yet every person of every race possesses full dignity and is worthy of respect and Christian love."),
 ("Salvation","Salvation involves the redemption of the whole man and is offered freely to all who accept Jesus Christ as Lord and Savior. It includes regeneration, justification, sanctification, and glorification. There is no salvation apart from personal faith in Jesus Christ as Lord."),
 ("God's Purpose of Grace","Election is the gracious purpose of God, consistent with the free agency of man, that excludes boasting and promotes humility. All true believers endure to the end — kept by the power of God through faith unto salvation."),
 ("The Church","A New Testament church is an autonomous local congregation of baptized believers, associated by covenant, observing the two ordinances of Christ and seeking to extend the gospel to the ends of the earth. Its scriptural officers are pastors and deacons; the office of pastor is limited to men as qualified by Scripture."),
 ("Baptism and the Lord's Supper","Baptism is the immersion of a believer in water in the name of the Father, the Son, and the Holy Spirit — an act of obedience symbolizing faith in a crucified, buried, and risen Savior. The Lord's Supper memorializes the death of the Redeemer and anticipates His second coming."),
 ("The Lord's Day","The first day of the week is the Lord's Day, commemorating the resurrection of Christ — set apart for worship and spiritual devotion, public and private."),
 ("The Kingdom","The Kingdom of God includes His general sovereignty over the universe and His particular kingship over those who acknowledge Him as King. Christians pray and labor for the Kingdom to come; its full consummation awaits the return of Jesus Christ."),
 ("Last Things","God will bring the world to its appropriate end. Jesus Christ will return personally and visibly; the dead will be raised; Christ will judge all people in righteousness. The unrighteous will be consigned to hell; the righteous will dwell forever in heaven with the Lord."),
 ("Evangelism and Missions","It is the duty and privilege of every follower of Christ and every church to make disciples of all nations — to win the lost to Christ by verbal witness undergirded by a Christian lifestyle."),
 ("Education","Christianity is the faith of enlightenment and intelligence. All sound learning is part of our Christian heritage, and Christian education is co-ordinate with missions and benevolence in the Kingdom of Christ."),
 ("Stewardship","God is the source of all blessings. Christians are stewards of their time, talents, and possessions, and should give cheerfully, regularly, systematically, proportionately, and liberally for the advancement of the Redeemer's cause."),
 ("Cooperation","Christ's people should organize associations and conventions to cooperate for the great objects of the Kingdom — voluntary, advisory bodies with no authority over the churches."),
 ("The Christian and the Social Order","All Christians are under obligation to make the will of Christ supreme in their own lives and in society — opposing racism, greed, and every form of sexual immorality; caring for the orphaned, the needy, the abused, the aged, and the sick; and contending for the sanctity of all human life from conception to natural death."),
 ("Peace and War","It is the duty of Christians to seek peace with all people on principles of righteousness. The true remedy for the war spirit is the gospel of our Lord."),
 ("Religious Liberty","God alone is Lord of the conscience. Church and state should be separate. A free church in a free state is the Christian ideal."),
 ("The Family","God has ordained the family as the foundational institution of human society. Marriage is the uniting of one man and one woman in covenant commitment for a lifetime. Children, from the moment of conception, are a blessing and heritage from the Lord."),
]
PAGES["beliefs"] = ("What We Believe", "Bluff Creek Baptist Church affirms the Bible as God's Word and holds to the Baptist Faith and Message (2000).", f"""
<section class="sec">
  <div class="eye">What we believe</div>
  <h1>Rooted in the Word.</h1>
  <p class="lead">Bluff Creek is a traditional Southern Baptist congregation. We affirm the Holy Bible as the inspired Word of God and the basis for our beliefs, and we subscribe to <a href="https://bfm.sbc.net/bfm2000/" target="_blank" rel="noopener">The Baptist Faith &amp; Message (2000)</a>. Below is each article in a sentence or two — the full statement, with every Scripture reference, is one click away.</p>
  <div class="grid g2 beliefs" style="margin-top:20px">
    {"".join(f'<div class="card"><div class="eye">{i+1}</div><h3>{t}</h3><p>{d}</p></div>' for i,(t,d) in enumerate(ART))}
  </div>
  <div class="word" style="margin-top:22px"><blockquote>"Wrong ideas about God are not only the fountain from which the polluted waters of idolatry flow; they themselves are idolatrous."</blockquote><cite>A. W. Tozer, <em>The Knowledge of the Holy</em></cite></div>
  <p style="margin-top:22px"><a class="btn pine" href="https://bfm.sbc.net/bfm2000/" target="_blank" rel="noopener">Read the full Baptist Faith &amp; Message</a></p>
</section>
""")

# ---------------- WHEN WE MEET ----------------
PAGES["times"] = ("When We Meet", "Service and meeting times at Bluff Creek Baptist Church — Sunday School 9:00, worship 10:15 and 6:00, Wednesday 6:00, and weekly ministries.", f"""
<section class="sec">
  <div class="eye">When we meet</div>
  <h1>Every week at the Creek.</h1>
  <p class="lead">1706 Highway 63, Clinton — at the corner of Highways 959 and 63. Two parking lots, one from each side.</p>
  <div class="tablewrap"><table class="sched">
    <tr><th>Sunday</th><td><b>9:00–10:00a</b> Sunday School — all ages (fellowship building)<br><b>10:15–11:30a</b> Morning worship (sanctuary)<br><b>5:30–7:00p</b> Youth discipleship (fellowship building)<br><b>6:00–7:00p</b> Evening service (sanctuary)</td></tr>
    <tr><th>Monday</th><td><b>6:30–8:00p</b> Women's Bible study — currently walking through Esther (contact Rikki for the location)</td></tr>
    <tr><th>Tuesday</th><td><b>5:00–5:45p</b> Yoga @ the Creek (fellowship building) · <b>3rd Tuesday, 6:00p</b> WMU (fellowship hall)</td></tr>
    <tr><th>Wednesday</th><td><b>6:00–6:30p</b> Prayer meeting (sanctuary)<br><b>6:00–8:00p</b> Youth @ the Creek — MDWK (fellowship building) · <span class="chip gold">6 on the 63</span></td></tr>
    <tr><th>Thursday</th><td><b>5:00–5:45p</b> Yoga @ the Creek (fellowship building)</td></tr>
  </table></div>
  <div class="events-inline">
    <div class="sec-h"><div><div class="eye">Coming up</div><h2>This week at the Creek</h2></div></div>
    <div class="event-feed" data-events-feed="3">{event_rows()}</div>
  </div>
  <div class="grid g2" style="margin-top:22px">
    <div class="card"><div class="eye">In your pocket</div><h3>The week, in the app</h3><p>This week's schedule and events, updated as they change — plus prayer, giving, and a way to connect.</p><p><a href="{APP}">Open Home @ the Creek →</a></p></div>
    <div class="card"><div class="eye">On your calendar</div><h3>Subscribe to the church calendar</h3><p>Every service, meeting, and event — straight into the calendar on your phone or computer, updated automatically.</p><p><a href="webcal://p24-caldav.icloud.com/published/2/MjgxNDIwMTA5MjgxNDIwMZkrrqg7P_e_uOJSEuneGS4QT-quA4OE5lbjyAKZifNVcV3yYLBvdcwT4okvZF-44VCzkvYBgUEuOzihC5igIm4">Subscribe →</a> · <a href="visit.html">Plan a visit →</a></p></div>
  </div>
</section>
""")

# ---------------- MINISTRIES ----------------
PAGES["ministries"] = ("Ministries @ the Creek", "Kidz, Youth, Adults, Women, WMU, Yoga, and Worship @ the Creek — every ministry at Bluff Creek Baptist Church.", f"""
<section class="sec">
  <div class="eye">One church, one family</div>
  <h1>Ministries @ the Creek.</h1>
  <p class="lead">Every ministry here is the Creek — different ages, same family, same mission: to help each other glorify God and enjoy Him forever.</p>
</section>

<section class="sec" id="kidz" style="padding-top:10px">
  <div class="grid g2" style="align-items:start">
    <div class="card">{lock("Kidz","var(--moss)",30)}<span class="chip moss">Birth – 5th grade</span><p style="margin-top:12px"><b>Big or small — your kids are welcome here.</b> We partner with parents, who are the primary disciple-makers, to help children glorify God and enjoy Him forever.</p><p>Sunday School meets at <b>9:00a</b> in the fellowship building (birth–3 in the nursery). In services we have a children's time with treats, clipboards, and crayons; the nursery has a nursing space, changing facilities, and quiet toys — and it's always your call whether to use it.</p><p>Through the year: Vacation Bible School, the back-to-school carnival, the fall festival, pumpkin carving, Easter, and Christmas.</p><p class="small">Questions about curriculum, baby dedication, or baptism? Contact Ashleigh Pierce through the <a href="contact.html">church office</a>.</p></div>
    <div class="card" id="youth">{lock("Youth","var(--creekblue)",30)}<span class="chip blue">6th – 12th grade</span><p style="margin-top:12px">Students gather <b>Sunday mornings at 9:00</b>, <b>Sunday nights at 5:30</b>, and every <b>Wednesday at 6:00 for MDWK</b> — <b>6 on the 63</b>. Summer brings weekly events and camp; the school year brings Disciple Now and the fall retreat.</p><p>Bring a friend. Head to the fellowship hall, the youth room in the courtyard — or the pickleball court.</p><div class="card" style="margin-top:14px;padding:14px;border-left:4px solid var(--wheat);box-shadow:none"><b>We're praying for our next youth minister.</b><p class="small" style="margin:4px 0 0">If God's leading you toward Youth @ the Creek, <a href="contact.html">talk to us</a>.</p></div></div>
  </div>
</section>

<section class="sec" id="adults">
  <div class="sec-h"><div><div class="eye">Grown-ups, too</div><h2>Adults @ the Creek</h2></div></div>
  <div class="grid g3">
    <div class="card"><h3>Sunday School · 9:00a</h3><p>A Men's class, a Ladies' class, two Adult classes, and a Young Adults class (coffee provided) — no age stipulations, all in the fellowship building. Find one that fits.</p><p class="small">Young adults: contact Rikki at <a href="mailto:riikkipermenter@gmail.com">riikkipermenter@gmail.com</a>.</p></div>
    <div class="card"><h3>Women's study · Mondays 6:30p</h3><p>Our women meet to dive into Scripture together — right now, the book of Esther. Contact Rikki for the location.</p></div>
    <div class="card"><h3>Wednesday prayer · 6:00p</h3><p>The heartbeat of the week: the church gathers in the sanctuary to pray, Wednesdays 6:00–6:30.</p></div>
    <div class="card">{lock("Yoga","var(--pine)",20)}<p>We're trying to be the best stewards of our bodies we can. A beginners' class — stretching and a gentle flow led by Leslie Barnes — <b>Tuesdays &amp; Thursdays, 5:00–5:45p</b> in the fellowship hall. $5; bring a mat or towel. All ages and abilities welcome.</p></div>
    <div class="card"><h3>WMU · 3rd Tuesdays 6:00p</h3><p>Our Women's Missionary Union meets monthly to fellowship, eat, pray, study Scripture, and take on hands-on missions projects. Fellowship hall — come join them.</p></div>
    <div class="card">{lock("Worship","var(--wheat)",20)}<p>Theologically rich, doctrinally sound hymns, led by a team of musicians every Sunday. All musical talents welcome — come sing or play with us.</p></div>
  </div>
</section>
""")

# ---------------- MISSIONS ----------------
PAGES["missions"] = ("Missions @ the Creek", "Our mission runs across campus, across the street, across the country, and across the world — Bluff Creek Baptist Church.", f"""
<section class="sec">
  <div class="eye">Across campus · the street · the country · the world</div>
  <h1>Missions @ the Creek.</h1>
  <p class="lead">Our mission is to glorify God and enjoy Him forever — and that mission takes us across our campus, across the street, across the country, and across the world.</p>
  <div class="grid g2" style="margin-top:20px">
    <div class="card"><span class="chip">Across campus</span><h3 style="margin-top:12px">Serve here</h3><p>Use the talents and gifts God gave you: Kidz @ the Creek, facilities, student ministry, audio &amp; video, worship. There's a place for you.</p></div>
    <div class="card"><span class="chip gold">Across the street</span><h3 style="margin-top:12px">Our community</h3><p>Sign-up sheets for local opportunities are in the sanctuary foyer. Every quarter we take a team to <b>The LOT Project</b> in North Baton Rouge.</p></div>
    <div class="card"><span class="chip blue">Across the country</span><h3 style="margin-top:12px">Louisiana &amp; beyond</h3><p>We partner with the <b>Louisiana Baptist Children's Home</b> (contact Rikki), and when hurricanes come, our campus serves as a <b>FEMA base camp</b> for disaster relief.</p></div>
    <div class="card"><span class="chip clay">Across the world</span><h3 style="margin-top:12px">The nations</h3><p>We pray for and support <b>Ebenezer Ministries in India</b> under Pastor Sparjan, and our <b>IMB partners serving in Northern Italy</b>. Ask us how to pray with them.</p></div>
  </div>
  <div class="panel" style="margin-top:22px"><img class="sign" src="assets/la63.svg" alt="" aria-hidden="true"><div class="eye">Down the 63</div><h3>Want to go?</h3><p>Trips, outings, and missions on the road — tell us you're interested and we'll get you on the list.</p><a class="btn" href="contact.html">I want to serve</a></div>
</section>
""")

# ---------------- MEMBERSHIP ----------------
PAGES["membership"] = ("Becoming a Member", "How to join Bluff Creek Baptist Church — by profession of faith and baptism, by letter, or by statement.", f"""
<section class="sec">
  <div class="eye">Join the family</div>
  <h1>Becoming a member.</h1>
  <p class="lead">You can join our faith family in formal membership during the invitation at the end of any Sunday morning service. Before you walk forward, we'd love for you to meet with our pastor so he can answer any questions.</p>
  <div class="grid g2" style="margin-top:20px">
    <div class="card"><h3>Four ways home</h3><ol style="padding-left:20px;margin:0;color:var(--ink2)"><li style="margin:6px 0"><b>By profession of faith and baptism</b> — you've received Christ and want to follow Him in believer's baptism.</li><li style="margin:6px 0"><b>By letter</b> — you're coming from another Baptist church.</li><li style="margin:6px 0"><b>By statement</b> — you've been converted and baptized in a Baptist church but a letter isn't available.</li><li style="margin:6px 0"><b>By baptism</b> if you come from a non-Baptist background and haven't been baptized by immersion.</li></ol></div>
    <div class="card"><h3>What membership means</h3><ul style="padding-left:20px;margin:0;color:var(--ink2)"><li style="margin:6px 0">Members 16 and older vote in church conference; members 18 and older may serve in elected offices.</li><li style="margin:6px 0">We commit to the church covenant, to growing in Christ, to serving, and to giving regularly — the tithe is our biblical starting point.</li><li style="margin:6px 0">We're a family. If you ever move away, we'll help you find a church home there.</li></ul></div>
  </div>
  <div class="panel" style="margin-top:22px"><img class="sign" src="assets/la63.svg" alt="" aria-hidden="true"><div class="eye">Good coffee, good conversation</div><h3>Talk with the pastor first.</h3><p>Cole would love to meet you one-on-one, answer your questions, and hear your story.</p><a class="btn" href="contact.html">Set up a coffee</a></div>
</section>
""")

# ---------------- GIVE ----------------
PAGES["give"] = ("Give", "Give to Bluff Creek Baptist Church online, in person, or by mail.", f"""
<section class="sec">
  <div class="eye">Cheerfully &amp; regularly</div>
  <h1>Give @ the Creek.</h1>
  <p class="lead">Your giving sustains worship, discipleship, missions, and the care of our people and our community. Every gift is recorded by the church treasurer for your year-end statement.</p>
  <div class="grid g3" style="margin-top:20px">
    <div class="card" style="border-top:4px solid var(--wheat)"><h3>Online</h3><p>Secure giving by card, Apple Pay, or Link — any amount, in about a minute.</p><a class="btn" href="{GIVE}" target="_blank" rel="noopener">Give online</a></div>
    <div class="card"><h3>In person</h3><p>Checks or cash in the offering during any service. Contact cards go in the same plate.</p></div>
    <div class="card"><h3>By mail</h3><p>Checks payable to Bluff Creek Baptist Church<br>1706 Highway 63<br>Clinton, LA 70722</p></div>
  </div>
  <div class="word" style="margin-top:22px"><blockquote>"Each one must give as he has decided in his heart, not reluctantly or under compulsion, for God loves a cheerful giver."</blockquote><cite>2 Corinthians 9:7</cite></div>
</section>
""")

# ---------------- WATCH ----------------
PAGES["watch"] = ("Watch", "Watch Bluff Creek Baptist Church online — Sunday worship live.", f"""
<section class="sec">
  <div class="eye">Can't make it in person?</div>
  <h1>Watch the Creek.</h1>
  <p class="lead">Sunday morning worship streams live at <b>10:15a</b>, and past services are there any time.</p>
  {('<div class="embed" style="margin-top:20px"><iframe src="https://www.youtube.com/embed/live_stream?channel='+YT_CHANNEL_ID+'&autoplay=0" title="Bluff Creek Baptist Church — live" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe></div>') if YT_CHANNEL_ID else ''}
  <div class="grid g2" style="margin-top:20px">
    <div class="panel"><img class="sign" src="assets/la63.svg" alt="" aria-hidden="true"><div class="eye">Live &amp; on demand</div><h3>{"Bluff Creek on YouTube" if YT_CHANNEL_ID else "Bluff Creek live on Facebook"}</h3><p>{"Subscribe and turn on notifications so Sunday finds you wherever you are." if YT_CHANNEL_ID else "Sunday morning worship streams live on our Facebook page, and past services are there any time. Follow the page so Sunday finds you wherever you are."}</p><a class="btn" href="{WATCH}" target="_blank" rel="noopener">{"Watch on YouTube" if YT_CHANNEL_ID else "Watch on Facebook"}</a>{('<p class="small" style="margin-top:12px"><a href="'+FACEBOOK+'" target="_blank" rel="noopener">Also on Facebook →</a></p>') if YT_CHANNEL_ID else ''}</div>
    <div class="card"><h3>What you'll hear</h3><p>Theologically rich hymns, prayer, a word for the kids, and a 30–40 minute expositional message straight from the text — the same service we have in the room.</p><p><a href="visit.html">Then come see us in person →</a></p></div>
  </div>
</section>
""")

# ---------------- CONTACT ----------------
PAGES["contact"] = ("Contact", "Find and contact Bluff Creek Baptist Church — 1706 Highway 63, Clinton, Louisiana.", f"""
<section class="sec">
  <div class="eye">You know where to find us</div>
  <h1>Find us on the 63.</h1>
  <div class="grid g2" style="margin-top:20px;align-items:start">
    <div class="card">
      <div class="contact-card"><img src="assets/la63.svg" alt="Louisiana Highway 63" style="width:72px"><div><b style="font-family:Bitter,serif;font-size:19px">Bluff Creek Baptist Church</b><div class="muted">1706 Highway 63<br>Clinton, Louisiana 70722<br><span class="small">Corner of Highways 959 and 63</span></div></div></div>
      <p style="margin:18px 0 6px"><a class="btn pine" href="https://maps.apple.com/?q=1706+Highway+63,+Clinton,+LA+70722" target="_blank" rel="noopener">Directions</a></p>
      <p style="margin:16px 0 0"><b>Pastor Cole Permenter</b><br><a href="tel:{PHONE_TEL}">{PHONE}</a><br><a href="mailto:{EMAIL}">{EMAIL}</a></p>
      <p class="small" style="margin-top:12px">We'd love to get to know you. Email us so we can better understand how to serve you.</p>
    </div>
    <div class="card">
      <h3>Say hello</h3>
      <noscript><p>Email <a href="mailto:{EMAIL}">{EMAIL}</a> with your question or a note about your visit.</p></noscript>
      <form id="cform" aria-describedby="contact-help">
        <div class="field"><label for="cn">Your name</label><input id="cn" required autocomplete="name"></div>
        <div class="field"><label for="ce">Email or phone</label><input id="ce" required></div>
        <div class="field"><label for="cm">Message</label><textarea id="cm" required placeholder="A question, a prayer request, or just 'we're coming Sunday'…"></textarea></div>
        <button class="btn" type="submit" style="border:0;cursor:pointer;font-family:inherit">Open email draft</button>
        <p class="small" id="contact-help" style="margin:10px 0 0">Review and send your message in your email app. You can also email <a href="mailto:{EMAIL}">{EMAIL}</a> directly.</p>
      </form>
      <div class="ok" id="cok" role="status" aria-live="polite" hidden style="margin-top:16px">If your email app opened, review the draft and send it there. If nothing opened, <a href="mailto:{EMAIL}">email the church office directly</a>. Your message stays here until you leave this page.</div>
    </div>
  </div>
  <div style="margin-top:22px"><iframe class="map" loading="lazy" referrerpolicy="no-referrer-when-downgrade" src="https://www.google.com/maps?q=1706+Highway+63,+Clinton,+LA+70722&amp;output=embed" title="Map to Bluff Creek Baptist Church"></iframe></div>
</section>
<script>
(function(){{
  var form=document.getElementById('cform');
  var fields=['cn','ce','cm'].map(function(id){{return document.getElementById(id);}});
  fields.forEach(function(field){{field.addEventListener('input',function(){{field.setCustomValidity('');}});}});
  form.addEventListener('submit',function(e){{
    e.preventDefault();
    fields.forEach(function(field){{field.setCustomValidity(field.value.trim()?'':'Please complete this field.');}});
    if(!form.reportValidity())return;
    var n=fields[0].value.trim(),c=fields[1].value.trim(),m=fields[2].value.trim();
    var body='From: '+n+'\\nContact: '+c+'\\n\\n'+m;
    document.getElementById('cok').hidden=false;
    location.href='mailto:{EMAIL}?subject='+encodeURIComponent('Hello from the website — '+n)+'&body='+encodeURIComponent(body);
  }});
}})();
</script>
""")

# ---------------- 404 ----------------
PAGES["404"] = ("Page not found", "That page isn't on the 63.", """
<section class="sec"><div class="eye">Hmm</div><h1>That page isn't on the 63.</h1><p class="lead">The link may be old. Try the menu — or head home.</p><p><a class="btn" href="index.html">Back home</a></p></section>
""")

def main():
    for slug,(title,desc,body) in PAGES.items():
        out = layout(slug,title,desc,body)
        with open(os.path.join(ROOT, f"{slug}.html"),"w",encoding="utf-8") as f: f.write(out)
    urls = [SITE+"/"] + [f"{SITE}/{s}.html" for s in PAGES if s not in ("index","404")]
    with open(os.path.join(ROOT,"sitemap.xml"),"w") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+"".join(f"  <url><loc>{u}</loc></url>\n" for u in urls)+"</urlset>\n")
    with open(os.path.join(ROOT,"robots.txt"),"w") as f: f.write(f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n")
    redirects = generate_redirects(ROOT, SITE)
    print("built", ", ".join(f"{s}.html" for s in PAGES), "+ sitemap.xml, robots.txt,", len(redirects), "legacy redirects")

if __name__ == "__main__": main()
