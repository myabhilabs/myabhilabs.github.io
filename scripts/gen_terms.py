"""Generate every app's Terms & Conditions page (terms/<slug>/index.html).

This script is the single source of truth for the terms pages. Edit the
text here, then regenerate:

    python3 scripts/gen_terms.py

Do not hand-edit the generated pages: the next run overwrites them.

The page shell (the <head>, header, footer and scripts) is read from the
current terms/abhinow/index.html, so site-wide footer or header changes made
there carry over to every page on the next run.

When you change a page's wording, update DATE and add a line to that app's
"history" list so the "Changes to These Terms" section stays accurate.
"""
import re, sys, pathlib

ROOT = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else pathlib.Path(__file__).resolve().parent.parent
TPL = (ROOT / "terms/abhinow/index.html").read_text()
DATE = "November 5, 2026"

head_end = TPL.index('  <section class="privacy-hero"')
tail_start = TPL.index("</main>")
HEAD, TAIL = TPL[:head_end], TPL[tail_start:]

# Reuse section icons from the template, keyed by section id.
ICON = dict(re.findall(
    r'<section class="privacy-section" id="([a-z-]+)">.*?(<span class="privacy-section__icon".*?</span>)',
    TPL, re.S))
def svg(body):
    return ('<span class="privacy-section__icon" aria-hidden="true"><svg width="20" height="20" viewBox="0 0 24 24" '
            'fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">'
            + body + '</svg></span>')
ICON.update({
    "price": svg('<path d="M20.59 13.41l-7.17 7.17a2 2 0 0 1-2.83 0L2 12V2h10l8.59 8.59a2 2 0 0 1 0 2.82z"/><line x1="7" y1="7" x2="7.01" y2="7"/>'),
    "ads": svg('<rect x="2" y="5" width="20" height="14" rx="2"/><path d="M7 15l2.5-6 2.5 6M7.8 13h3.4M15 9v6h1.5a2.5 2.5 0 0 0 0-5H15"/>'),
    "data": svg('<ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3"/><path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"/>'),
    "content": svg('<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/>'),
    "warning": svg('<path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/>'),
    "volume": svg('<polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"/><path d="M15.54 8.46a5 5 0 0 1 0 7.07"/>'),
    "link": svg('<path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/>'),
    "lock": svg('<rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/>'),
    "export": svg('<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" y1="3" x2="12" y2="15"/>'),
})

def P(*paras):
    return "\n".join(f"        <p>{p}</p>" for p in paras)
def UL(*items):
    return "        <ul>\n" + "\n".join(f"          <li>{i}</li>" for i in items) + "\n        </ul>"

# ---------- shared sections ----------
def common_pre(a):
    n = a["name"]
    return [
        ("eligibility", "Eligibility", "Eligibility", "eligibility", P(
            f"You must be at least 13 years old to use {n}. If you are under the age of majority where you live, you may use the app only if a parent or legal guardian agrees to these Terms on your behalf.")),
        ("license", "License", "License", "license", P(
            f"We grant you a personal, non-exclusive, non-transferable, revocable license to use {n} for personal, non-commercial purposes on Android devices you own or control, subject to these Terms and the Google Play Terms of Service.")),
    ]

def price(a):
    n = a["name"]
    if a.get("ads"):
        first = f"{n} is free to download and use. It has no in-app purchases and no subscriptions. It is supported by ads (see Advertising)."
    else:
        first = f"{n} is free to download and use. It shows no ads and has no in-app purchases or subscriptions."
    return ("price", "Price", "Price", "price", P(
        first,
        "If we ever introduce paid features, we will update these Terms before they become available. Any purchase would be processed by Google Play under its own terms, and we would never receive your payment details."))

def ads(a, where):
    n = a["name"]
    return ("ads", "Advertising", "Advertising", "ads", P(
        f"{n} displays ads served by Google AdMob{where}. Ads are provided by third parties. We do not control or endorse the products, services or websites they promote, and any dealings you have with an advertiser are between you and that advertiser.",
        "In the EEA and UK, a consent form from Google's User Messaging Platform (UMP) is shown at first launch, and personalized ads are shown only with your consent. What AdMob collects is described in our "
        f'<a href="/privacy/{a["slug"]}/">Privacy Policy</a>.'))

def local_data(a, what):
    n = a["name"]
    return ("data", "Your Data on Your Device", "Your Data", "data", P(
        f"{what} are stored only on your device. We do not run servers that hold a copy, and {n} has no cloud backup.",
        f"Deleting items, clearing the app's data or uninstalling {n} removes that data permanently, and we cannot recover it. You are responsible for keeping your own copies of anything important."))

def common_post(a):
    n, slug = a["name"], a["slug"]
    ip_extra = a.get("ip_extra", "")
    term_extra = a.get("termination_extra", "")
    disclaim = a.get("disclaim", "that its results will be accurate in every case")
    ip_what = a.get("ip_what", "design, text, graphics, and code")
    history = UL(*[f"<strong>{d}</strong> — {t}" for d, t in a["history"]])
    return [
        ("privacy", "Privacy", "Privacy", "privacy", P(
            f'Our handling of data is described in the <a href="/privacy/{slug}/">{n} Privacy Policy</a>, which forms part of these Terms.')),
        ("ip", "Intellectual Property", "IP", "ip", P(
            f"{n}, including its {ip_what}, is owned by Abhi Labs and protected by applicable intellectual-property laws. You may not copy, modify, distribute, sell, or reverse-engineer the app, except to the extent permitted by applicable law or by open-source licenses covering third-party components{ip_extra}.")),
        ("disclaimers", "Disclaimers", "Disclaimers", "disclaimers", P(
            f'{n} is provided "as is" and "as available", without warranties of any kind, express or implied, including fitness for a particular purpose, merchantability, and non-infringement. We do not warrant that the app will be uninterrupted, error-free, or {disclaim}.')),
        ("liability", "Limitation of Liability", "Liability", "liability", P(
            "To the maximum extent permitted by law, Abhi Labs is not liable for indirect, incidental, special, consequential, or punitive damages, or for loss of data, profits, or goodwill, arising from your use of or inability to use the app. To the extent permitted by law, our total liability for any claim relating to the app is limited to the greater of (a) the amount you paid us for the app in the 12 months before the claim arose, or (b) INR 1,000.")),
        ("statutory", "Statutory Rights", "Statutory Rights", "statutory", P(
            "Nothing in these Terms limits rights you have under mandatory consumer-protection laws in your country of residence. Where these Terms conflict with such laws, the laws prevail.")),
        ("termination", "Termination", "Termination", "termination", P(
            f"These Terms apply for as long as you use the app. Your license ends automatically if you materially breach these Terms. You may stop using {n} at any time by uninstalling it.{term_extra} The sections on Intellectual Property, Disclaimers, Limitation of Liability, Statutory Rights, Governing Law and General survive termination.")),
        ("changes", "Changes to These Terms", "Changes", "changes", P(
            "We may update these Terms. Material changes will be posted on this page with a new effective date. Your continued use of the app after changes take effect constitutes acceptance.",
            "Version history:") + "\n" + history),
        ("law", "Governing Law and Disputes", "Governing Law", "law", P(
            'These Terms are governed by the laws of India, without regard to conflict-of-laws principles. Subject to any mandatory consumer-protection rules that let you bring claims where you live, the courts of Bengaluru, Karnataka, India have jurisdiction. If you have a dispute, please contact us first at <a href="mailto:contact@abhilabs.app">contact@abhilabs.app</a> — most issues can be resolved quickly and informally.')),
        ("general", "General", "General", "general", P(
            "If any provision of these Terms is found unenforceable, the remaining provisions remain in effect. These Terms, together with the Privacy Policy, are the entire agreement between you and Abhi Labs regarding the app. We may assign these Terms in connection with a merger, acquisition, or sale of assets; you may not assign them.")),
        ("contact", "Contact", "Contact", "contact",
            '        <p>Abhi Labs<br>\n        Bangalore, India<br>\n        Email: <a href="mailto:contact@abhilabs.app">contact@abhilabs.app</a><br>\n        Website: <a href="https://abhilabs.app">https://abhilabs.app</a></p>'),
    ]

# ---------- per-app sections ----------
def scanner(a):
    n = a["name"]
    return [
        ("what-it-is", f"What {n} Is (and Is Not)", "What It Is", "what-it-is",
         P(f"{n} is an offline document scanner. It captures pages with your camera, crops and enhances them, extracts text (OCR) and saves PDFs — all on your device.")
         + "\n" + P(
            "<strong>Not a certified copy.</strong> Scans, PDFs and extracted text are made for your convenience. They are not certified or notarised copies, and we do not promise they will be accepted for any legal, official or institutional purpose.",
            "<strong>Best-effort processing.</strong> Edge detection, enhancement and OCR can be inaccurate, especially with poor lighting, handwriting or unusual fonts. Check important documents against the original before you rely on them.")),
        ("accessibility", "Permissions", "Permissions", "accessibility", P(
            f"{n} uses the Camera to scan and the Android Storage Access Framework to save files where you choose. You can revoke these permissions in Android settings at any time; scanning or saving will stop working without them.")),
        ("content", "Your Content", "Your Content", "content", P(
            "You own the documents you scan. We never receive a copy of them.",
            "You are responsible for having the right to scan, store and share each document, including copyrighted material and other people's personal or identity documents. Do not use the app to forge, alter or misrepresent documents, or for any unlawful purpose.")),
        local_data(a, "Your scans, PDFs and extracted text"),
        price(a),
    ]

def app_scan(a):  return scanner(a)

def app_nidra(a):
    n = a["name"]
    return [
        ("what-it-is", f"What {n} Is (and Is Not)", "What It Is", "what-it-is",
         P(f"{n} plays sleep sounds, white noise and mixes offline, with sleep timers, an optional Adaptive Volume feature and a sleep journal.")
         + "\n" + P(
            f"<strong>Not medical.</strong> {n} is not a medical device. It does not diagnose, treat or prevent insomnia, sleep apnea or any other condition. If you have ongoing sleep problems, consult a qualified healthcare professional.",
            f"<strong>Not a baby monitor.</strong> {n} does not watch over, monitor or alert you about a baby or anyone else. Never rely on it for a child's safety.")),
        ("safe-listening", "Safe Listening", "Safe Listening", "volume", P(
            "Listening at high volume for long periods can damage hearing. Keep the volume moderate, especially with headphones or overnight.",
            "If you play sounds for an infant, keep the volume low, place the phone well away from the cot or crib (never inside it), and follow your pediatrician's advice.")),
        ("accessibility", "Microphone and Background Playback", "Permissions", "accessibility", P(
            "The microphone is used only if you turn on Adaptive Volume, to measure ambient noise on your device. Audio is never recorded, stored or sent anywhere.",
            "Playback runs as a foreground service with a visible notification so sounds continue with the screen off. This uses battery. Battery optimization or manufacturer settings can stop or delay playback, and we cannot guarantee uninterrupted playback on every device.")),
        local_data(a, "Your custom presets, sleep journal and session history"),
        price(a),
    ]

def app_qr(a):
    n = a["name"]
    return [
        ("what-it-is", f"What {n} Is", "What It Is", "what-it-is", P(
            f"{n} scans QR codes and barcodes, lets you create QR codes, keeps a scan history and favourites, and runs on-device safety checks using Google ML Kit.")),
        ("safety", "Safety Checks Are Not a Guarantee", "Safety Checks", "warning", P(
            "Safety checks run on your device and help spot suspicious links, but they can miss harmful or phishing content and can flag safe content by mistake.",
            "Before you open a link, join a WiFi network, save a contact, place a call or make a payment from a scanned code, check where it leads. You decide what to open or act on, and you are responsible for that decision.")),
        ("third-party", "Third-Party Destinations", "Third Parties", "link", P(
            "Scanned codes can lead to websites, apps, networks and payment pages that we do not own or control. Their own terms and privacy policies apply, and we are not responsible for their content, availability or practices.")),
        ("accessibility", "Permissions", "Permissions", "accessibility", P(
            "The app uses the Camera to scan, Location and WiFi State only so Android can connect you to a WiFi network from a scanned WiFi code, Vibration for scan feedback, and Internet to show ads. You can revoke permissions in Android settings; the related features will stop working.")),
        ("content", "QR Codes You Create", "Codes You Create", "content", P(
            "You are responsible for the content of QR codes you create and share. Do not create codes that link to phishing, malware, fraud, or illegal content, or that infringe anyone's rights.")),
        ads(a, ""),
        local_data(a, "Your scan history, favourites and created codes"),
        price(a),
    ]

def app_lunavi(a):
    n = a["name"]
    return [
        ("what-it-is", f"What {n} Is", "What It Is", "what-it-is", P(
            f"{n} is a personal wellness tracker for periods, ovulation and symptoms. It works fully offline and estimates future periods and fertile windows from what you log.")),
        ("not-medical", "Not Medical Advice", "Not Medical", "warning", P(
            f"{n} is not a medical device. It does not diagnose, treat, cure or prevent any medical condition, and it does not replace advice from a doctor or other qualified healthcare professional. If you have symptoms that worry you, or need urgent help, contact a healthcare provider or emergency services.")),
        ("not-contraception", "Not Contraception", "Not Contraception", "warning", P(
            f"<strong>Do not use {n} as a method of contraception or birth control.</strong> Period, ovulation and fertile-window predictions are estimates. Cycles vary, and predictions can be wrong even when your logs are complete.",
            f"{n} also does not guarantee conception. If you are trying to conceive or to avoid pregnancy, talk to a healthcare professional about suitable methods.")),
        ("accuracy", "Accuracy and Your Logs", "Accuracy", "disclaimers", P(
            "Predictions depend on what you enter. Missing or incorrect entries reduce accuracy. The OPK strip scanner reads a photo of your test and can misread it; always read the test according to its own instructions.",
            "Reminders, including pill reminders, are created on your device and can be delayed or blocked by battery settings, notification settings or restarts. Do not rely on them alone to take medication on time.")),
        ("app-lock", "App Lock, PIN and Recovery Key", "App Lock", "lock", P(
            "If you turn on App Lock, keep your PIN and recovery key safe. There is no account and no server, so if you lose both you may be unable to open your data, and we cannot reset it for you.")),
        ("export", "Export and Sharing", "Export", "export", P(
            "Export files (JSON, CSV, ICS, PDF) are not encrypted. Once you save or share a file, you are responsible for who can access it, and the receiving app's own terms apply. To change phones, export a JSON file and import it on the new device.")),
        local_data(a, "Your cycle, symptom and health logs"),
        price(a),
    ]

CALLOUT_ICON = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3l7 3v5c0 4.5-3 7.6-7 9-4-1.4-7-4.5-7-9V6l7-3z"/><path d="M9 12l2 2 4-4"/></svg>'
def CALLOUT(text):
    return f'        <div class="privacy-callout" role="note">\n          {CALLOUT_ICON}\n          <p>{text}</p>\n        </div>'

def app_now(a):
    return [
        ("what-it-is", "What AbhiNow Is (and Is Not)", "What It Is", "what-it-is",
         P("AbhiNow is a screen-time and focus tool. When you open an app you have chosen to shield, it shows a brief on-screen pause before you decide to continue or walk away.")
         + "\n" + UL(
            "<strong>Not medical.</strong> AbhiNow is not a medical device and does not provide medical, psychological, or health advice, diagnosis, or treatment. If you have concerns about your wellbeing, consult a qualified professional.",
            "<strong>Not a guarantee.</strong> Blocking is best-effort. Device settings and manufacturer behavior — such as force-stopping the app, aggressive battery optimization, revoking permissions, or system navigation gestures — can prevent, delay, or bypass the pause screen. You remain responsible for how you use your device.",
            "<strong>Not for emergencies.</strong> Do not shield apps you may need in an emergency (for example, your phone or messaging apps). You are solely responsible for which apps you choose to shield and for your commitment-lock settings, including locks that cannot be ended early.")),
        ("accessibility", "Accessibility Service and Permissions", "Accessibility", "accessibility", P(
            'AbhiNow uses Android\'s Accessibility Service, with your explicit consent, to detect which app is in the foreground so it can show the pause screen. You can disable it at any time in your device settings; core features will stop working without it. How we handle data is described in our <a href="/privacy/abhinow/">Privacy Policy</a>.')),
        ("features", "Free and Premium Features", "Free &amp; Premium", "features",
         P("AbhiNow's core features are free, including the full blocking engine, all presence tasks, Deep Focus, and insights, for one connected set of apps.",
           "AbhiNow Premium additionally unlocks:")
         + "\n" + UL("multiple independent app sets,", "all themes,", "the full Timeline history,", "saving custom mantras.")
         + "\n" + P("We may change which features are free or Premium over time; changes will not remove features you have already paid for during a period you have paid for.")),
        ("purchases", "Purchases, Subscriptions, and Trials", "Purchases", "purchases",
         P("Premium is offered through Google Play as:")
         + "\n" + UL("a <strong>Yearly subscription</strong> (auto-renewing, and may include a free trial), and",
                     "a <strong>Lifetime purchase</strong> (one-time payment, no renewal).")
         + "\n" + P(
            "Auto-renewing subscriptions renew automatically at the then-current price unless you cancel at least 24 hours before the end of the current billing period. If your subscription includes a free trial, it converts to a paid subscription unless you cancel before the trial ends. If a subscription price increases, Google Play will notify you in advance and, where required, ask for your consent; you can cancel before the increase takes effect.",
            "You can cancel anytime in Google Play → Payments &amp; subscriptions → Subscriptions. Cancellation takes effect at the end of the current billing period; you keep Premium until then. Uninstalling the app does not cancel a subscription.")
         + "\n" + CALLOUT("All payments are processed by Google Play. We do not receive or store your payment details.")),
        ("refunds", "Refunds", "Refunds", "refunds", P(
            "Refunds are handled by Google Play in accordance with the Google Play refund policy. If you are in the EEA or UK, you may have a 14-day right of withdrawal for digital purchases; by starting your purchase and receiving immediate access to Premium, you consent to immediate performance and acknowledge that this may affect the withdrawal right to the extent permitted by law. Nothing in this section limits your statutory rights.")),
        ("premium-ends", "When Premium Ends", "When Premium Ends", "premium-ends",
         P("If your subscription expires or is refunded, Premium features lock again: additional app sets deactivate (your largest set stays active), Premium themes revert to the default, the Timeline re-gates, and custom mantras are no longer used by the pause screen.")
         + "\n" + CALLOUT("Your data is not deleted — it remains on your device, and your drafts and history are retained.")),
        ("responsibilities", "Your Responsibilities", "Your Responsibilities", "responsibilities", P(
            "You choose which apps to shield and how firm your settings are. You are responsible for maintaining the permissions and device settings the app needs, and for the consequences of your own configuration, including commitment locks with no early exit. Conditions at the device level (manufacturer battery management, force-stop, OS restrictions) are outside our control.")),
    ]

FIRST = [(DATE, "Initial terms published.")]

APPS = [
    dict(slug="abhinow", app="abhinow", name="AbhiNow", cls="app-abhinow",
         logo="/apps/abhinow/assets/applogo.png", pkg="com.abhilabs.abhinow",
         desc="focus app", sections=app_now,
         meta="AbhiNow Terms &amp; Conditions. License, Premium subscriptions, disclaimers, and your rights when using the AbhiNow focus app.",
         ip_extra=" (see the in-app Licenses screen)",
         disclaim="that it will block any app in all circumstances",
         termination_extra=" Subscriptions and refunds remain governed by Google Play.",
         tagline="Reclaim your focus. Private by default — your shields, settings, and history never leave your device.",
         history=[(DATE, "Limitation of Liability now caps our liability at the greater of what you paid us in the previous 12 months or INR 1,000. Added this version history."),
                  ("July 5, 2026", "Initial terms published.")]),
    dict(slug="abhiscan", app="abhi-scan", name="AbhiScan", cls="app-abhiscan",
         logo="/apps/abhi-scan/assets/applogo.png", pkg="com.abhilabs.pdfscanner",
         desc="scanner app", sections=app_scan,
         tagline="Professional offline scanner. Turn off airplane mode and it still works perfectly.", history=FIRST),
    dict(slug="abhiscan-lite", app="abhi-scan-lite", name="AbhiScan Lite", cls="app-abhiscan",
         logo="/apps/abhi-scan-lite/assets/play_store_icon.png", pkg="com.abhilabs.pdfscanner.lite",
         desc="lightweight scanner app", sections=app_scan,
         tagline="Full scanner power in a featherweight 5 MB install. Turn on airplane mode — it still works.", history=FIRST),
    dict(slug="abhinidra", app="abhinidra", name="AbhiNidra", cls="app-abhinidra",
         logo="/apps/abhinidra/assets/applogo.png", pkg="com.abhilabs.abhinidra", ip_what="design, text, graphics, sounds, and code",
         desc="sleep sounds app", sections=app_nidra,
         tagline="Sleep sounds that respect your privacy. No ads, no data, ever.", history=FIRST),
    dict(slug="ai-qr-barcode", app="ai-qr-barcode", name="AI QR Barcode Scanner", cls="app-ai-qr",
         logo="/apps/ai-qr-barcode/assets/applogo.png", pkg="com.abhilabs.aiqrbarcodescanner", ads=True,
         desc="QR and barcode scanner app", sections=app_qr,
         tagline="Fast, smart QR and barcode scanning. Safety verified on-device. Your scans stay yours.", history=FIRST),
    dict(slug="lunavi", app="lunavi", name="Lunavi", cls="app-lunavi",
         logo="/apps/lunavi/assets/applogo.png", pkg="com.abhilabs.lunavi",
         desc="period and ovulation tracker", sections=app_lunavi,
         tagline="Your cycle, your data. Ovulation predictions that stay on your device.", history=FIRST),
]

PRIV_ICON = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3l7 3v5c0 4.5-3 7.6-7 9-4-1.4-7-4.5-7-9V6l7-3z"/></svg>'
BACK_ICON = '<svg width="14" height="14" viewBox="0 0 14 14" fill="none" aria-hidden="true"><path d="M12 7H2M6 3l-4 4 4 4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>'
PLAY_ICON = '<svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M3 1l18 11L3 23V1z"/></svg>'
DOC_ICON = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg>'

def build(a):
    n, slug = a["name"], a["slug"]
    secs = common_pre(a) + a["sections"](a) + common_post(a)
    ids = [s[0] for s in secs]
    assert len(ids) == len(set(ids)), ids
    url = f"https://abhilabs.app/terms/{slug}/"
    desc = a.get("meta") or f"{n} Terms &amp; Conditions. License, disclaimers, and your rights when using the {n} {a['desc']}."
    title = f"Terms &amp; Conditions — {n} | Abhi Labs"
    h = HEAD
    h = h.replace('class="app-abhinow"', f'class="{a["cls"]}"')
    h = re.sub(r"<title>.*?</title>", f"<title>{title}</title>", h)
    h = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{desc}">', h)
    h = re.sub(r'<meta property="og:description" content="[^"]*">', f'<meta property="og:description" content="{desc}">', h)
    h = re.sub(r'<meta property="og:title" content="[^"]*">', f'<meta property="og:title" content="{title}">', h)
    h = h.replace("https://abhilabs.app/terms/abhinow/", url)
    h = h.replace("https://abhilabs.app/apps/abhinow/assets/applogo.png", "https://abhilabs.app" + a["logo"])
    if slug != "abhinow":
        assert "abhinow" not in h.lower(), "leftover AbhiNow text in head"

    promise = f"By downloading or using {n}, you agree to these Terms. If you do not agree, do not use the app."
    out = [h]
    out.append(f'''  <section class="privacy-hero" aria-label="Terms overview">
    <div class="privacy-hero__orb" aria-hidden="true"></div>
    <div class="privacy-hero__inner">
      <img src="{a["logo"]}" alt="{n} app icon" class="privacy-hero__icon" width="72" height="72">
      <p class="privacy-hero__label">
        {DOC_ICON}
        Terms &amp; Conditions
      </p>
      <h1 class="privacy-hero__title">{n}</h1>
      <p class="privacy-hero__promise">{promise}</p>
      <p class="privacy-hero__updated">Effective: {DATE} · Last updated: {DATE}</p>
    </div>
  </section>

  <nav class="privacy-chips" id="privacy-chips" aria-label="Jump to section">''')
    for sid, _t, chip, _i, _b in secs:
        out.append(f'    <a href="#{sid}" class="privacy-chip">{chip}</a>')
    out.append('''  </nav>

  <div class="privacy-layout">
    <aside class="privacy-toc" aria-label="Table of contents">
      <p class="privacy-toc__label">Contents</p>''')
    for sid, t, _c, _i, _b in secs:
        out.append(f'      <a href="#{sid}">{t.replace(" (and Is Not)", "")}</a>')
    out.append('''    </aside>

    <div class="privacy-content">
''')
    for i, (sid, t, _c, icon, body) in enumerate(secs, 1):
        out.append(f'''      <section class="privacy-section" id="{sid}">
        <span class="privacy-section__num" aria-hidden="true">{i:02d}</span>
        <div class="privacy-section__head">
          {ICON[icon]}
          <h2 class="privacy-section__title">{t}</h2>
        </div>
{body}
      </section>
''')
    out.append(f'''    </div>
  </div>

  <div class="privacy-app-cta">
    <div class="privacy-app-cta__card">
      <img src="{a["logo"]}" alt="{n} app icon" class="privacy-app-cta__icon" width="64" height="64">
      <p class="privacy-app-cta__name">{n}</p>
      <p class="privacy-app-cta__tagline">{a["tagline"]}</p>
      <div class="privacy-app-cta__actions">
        <a href="https://play.google.com/store/apps/details?id={a["pkg"]}" class="privacy-app-cta__play" target="_blank" rel="noopener noreferrer">
          {PLAY_ICON}
          Get on Google Play
        </a>
        <a href="/privacy/{slug}/" class="privacy-app-cta__back">
          {PRIV_ICON}
          Privacy Policy
        </a>
        <a href="/apps/{a["app"]}/" class="privacy-app-cta__back">
          {BACK_ICON}
          View app page
        </a>
      </div>
    </div>
  </div>

''')
    out.append(TAIL)
    html = "\n".join(out)
    dest = ROOT / "terms" / slug / "index.html"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(html)
    print(dest.relative_to(ROOT), len(secs), "sections")


# Order of cards on the /legal/ hub (matches the footer's Apps column).
LEGAL_ORDER = ["abhiscan", "abhiscan-lite", "lunavi", "abhinidra", "abhinow", "ai-qr-barcode"]

def build_legal():
    """Write legal/index.html: one card per app linking its Privacy Policy and Terms."""
    title = "Legal — Privacy Policies &amp; Terms | Abhi Labs"
    desc = "Privacy policies and terms &amp; conditions for every Abhi Labs Android app."
    h = HEAD.replace(' class="app-abhinow"', "")
    h = re.sub(r"<title>.*?</title>", f"<title>{title}</title>", h)
    for prop in ("og:title",):
        h = re.sub(rf'<meta property="{prop}" content="[^"]*">', f'<meta property="{prop}" content="{title}">', h)
    h = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{desc}">', h)
    h = re.sub(r'<meta property="og:description" content="[^"]*">', f'<meta property="og:description" content="{desc}">', h)
    h = h.replace("https://abhilabs.app/terms/abhinow/", "https://abhilabs.app/legal/")
    h = h.replace("https://abhilabs.app/apps/abhinow/assets/applogo.png", "https://abhilabs.app/assets/developer_logo.png")
    assert "abhinow" not in h.lower(), "leftover AbhiNow text in legal head"

    by_slug = {a["slug"]: a for a in APPS}
    assert sorted(by_slug) == sorted(LEGAL_ORDER), "LEGAL_ORDER must list every app"
    cards = []
    for slug in LEGAL_ORDER:
        a = by_slug[slug]
        cards.append(f'''    <article class="legal-card {a["cls"]}">
      <div class="legal-card__head">
        <img src="{a["logo"]}" alt="" class="legal-card__icon" width="48" height="48" aria-hidden="true">
        <a href="/apps/{a["app"]}/" class="legal-card__name">{a["name"]}</a>
      </div>
      <div class="legal-card__links">
        <a href="/privacy/{slug}/" class="legal-card__link">{PRIV_ICON} Privacy Policy</a>
        <a href="/terms/{slug}/" class="legal-card__link">{DOC_ICON} Terms &amp; Conditions</a>
      </div>
    </article>''')
    body = f'''  <section class="privacy-hero" aria-label="Legal overview">
    <div class="privacy-hero__orb" aria-hidden="true"></div>
    <div class="privacy-hero__inner">
      <img src="/assets/developer_logo.png" alt="Abhi Labs logo" class="privacy-hero__icon" width="72" height="72">
      <p class="privacy-hero__label">
        {DOC_ICON}
        Legal
      </p>
      <h1 class="privacy-hero__title">Privacy &amp; Terms</h1>
      <p class="privacy-hero__promise">The privacy policy and terms &amp; conditions for every Abhi Labs app, in one place.</p>
    </div>
  </section>

  <div class="legal-grid">
{chr(10).join(cards)}
  </div>

'''
    dest = ROOT / "legal" / "index.html"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(h + body + TAIL)
    print(dest.relative_to(ROOT), len(cards), "apps")

for a in APPS:
    build(a)
build_legal()
