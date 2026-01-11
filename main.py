from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.graphics import Color, RoundedRectangle
import random

# আরও ফাস্ট চেকিংয়ের জন্য সেট (Set) ব্যবহার করা হয়েছে
AD_SERVERS = {
    "googleads.g.doubleclick.net", "ads.facebook.com", "graph.facebook.com",
    "app-measurement.com", "ads.mopub.com", "ads.twitter.com",
    "pagead2.googlesyndication.com", "ads.inmobi.com", "ads.yahoo.com",
    "tracking.adjust.com", "ads.pubmatic.com", "ads.vungle.com"
}

class AdBlockEngine:
    def __init__(self):
        self.blocked = 0
        self.trackers = 0
        self.saved = 0
        self.last = "None"

    def check(self, domain):
        if domain in AD_SERVERS:
            self.blocked += 1
            self.trackers += 1
            self.saved += random.randint(50, 150) # রিয়েলিস্টিক ডেটা সেভিং
            self.last = domain
            return True
        return False

engine = AdBlockEngine()
FAKE_TRAFFIC = list(AD_SERVERS) + ["google.com", "github.com", "wikipedia.org", "openai.com"]

class SlayerAdBlocker(App):
    def build(self):
        # ব্যাকগ্রাউন্ড কালার ডার্ক করার জন্য মেইন লেআউট
        self.root = BoxLayout(orientation="vertical", padding=30, spacing=20)
        
        with self.root.canvas.before:
            Color(0.1, 0.1, 0.1, 1) # ডার্ক গ্রে ব্যাকগ্রাউন্ড
            self.rect = RoundedRectangle(size=self.root.size, pos=self.root.pos)
        self.root.bind(size=self._update_rect, pos=self._update_rect)

        self.title = Label(
            text="[b][color=00FF7F]SLAYER AD-BLOCKER[/color][/b]",
            markup=True, font_size="32sp", size_hint_y=0.2
        )

        self.stats = Label(
            text="Initializing Engine...",
            font_size="18sp",
            halign="center",
            valign="middle",
            markup=True
        )

        self.root.add_widget(self.title)
        self.root.add_widget(self.stats)

        Clock.schedule_interval(self.tick, 0.8) # স্পিড কিছুটা বাড়ানো হয়েছে
        return self.root

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def tick(self, dt):
        domain = random.choice(FAKE_TRAFFIC)
        is_blocked = engine.check(domain)
        
        color = "FF4444" if is_blocked else "FFFFFF"
        
        self.stats.text = (
            f"🚫 [b]Ads Blocked:[/b] {engine.blocked}\n\n"
            f"🕵️ [b]Trackers:[/b] {engine.trackers}\n\n"
            f"💾 [b]Data Saved:[/b] {engine.saved} KB\n\n"
            f"🌐 [b]Scanning:[/b] [color={color}]{domain}[/color]"
        )

if __name__ == "__main__":
    SlayerAdBlocker().run()
