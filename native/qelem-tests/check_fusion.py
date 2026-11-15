"""Static safety/branding checks only: these do not build or test the Android UI."""
from pathlib import Path
import re
import xml.etree.ElementTree as ET
import zipfile

root = Path(__file__).resolve().parents[1]
repo = root.parent
src = root / 'android/app/src/main'
settings = (root / 'android/app/build.gradle.kts').read_text()
assert 'applicationId = "com.qalam.studio.nativepreview"' in settings
assert 'versionName = "1.5-preview"' in settings
assert ET.parse(src / 'res/values/strings.xml').getroot().find("string[@name='app_name']").text == 'Qelem'
theme = (src / 'java/io/github/artcraftandroid/procraft/ui/Theme.kt').read_text()
assert 'Color(0xFFBB5800)' in theme and 'accentGiven ?: BrandAccent' in theme
# Existing selected controls use white ink: the default solid accent must remain legible.
rgb = [int('BB5800'[i:i + 2], 16) / 255 for i in (0, 2, 4)]
linear = [v / 12.92 if v <= .04045 else ((v + .055) / 1.055) ** 2.4 for v in rgb]
luminance = sum(a*b for a,b in zip((.2126, .7152, .0722), linear))
assert 1.05 / (luminance + .05) >= 4.5
assert (root / 'LICENSE-MIT').is_file() and (root / 'LICENSE-APACHE').is_file() and (root / 'NOTICE').is_file() and (root / 'ATTRIBUTION.md').is_file()
with zipfile.ZipFile(repo / 'artifacts/Qelem-7.23-dev-source.zip') as legacy:
    for density in ('mdpi', 'hdpi', 'xhdpi', 'xxhdpi', 'xxxhdpi'):
        name = f'android/res/mipmap-{density}/ic_launcher.png'
        assert (src / f'res/mipmap-{density}/ic_launcher.png').read_bytes() == legacy.read('Qelem-7.23-dev/' + name)
    assert (src / 'res/drawable-nodpi/procraft_mark.png').read_bytes() == legacy.read('Qelem-7.23-dev/android/assets/app/img/icon.png')
assert not (src / 'res/mipmap-anydpi/ic_launcher.xml').exists()
ui = (src / 'java/io/github/artcraftandroid/procraft/ui/AnimationUi.kt').read_text()
vm = (src / 'java/io/github/artcraftandroid/procraft/canvas/CanvasViewModel.kt').read_text()
assert 'Reverse preview only' in ui and 'qelemPreviewOrder(qelemRangeSlots(original, bounds), reverse)' in vm and 'playingSlot = slot' in vm
assert 'Set preview start here' in ui and 'Set preview end here' in ui and 'Preview speed' in ui
assert 'Storyboard PNG' in (src / 'java/io/github/artcraftandroid/procraft/ui/ActionsPanel.kt').read_text()
assert 'Share palette chart PNG' in (src / 'java/io/github/artcraftandroid/procraft/ui/ColorPanel.kt').read_text()
assert re.search(r'fun closeArtwork\(\)\s*\{\s*stopPlaying\(\)\s*reversePreview = false', vm)
# Expanded timeline text must remain legible against its dark surface on both platforms.
def contrast(foreground, background):
    def luminance(hex_color):
        values = [int(hex_color[i:i + 2], 16) / 255 for i in (0, 2, 4)]
        values = [v / 12.92 if v <= .04045 else ((v + .055) / 1.055) ** 2.4 for v in values]
        return sum(a*b for a,b in zip((.2126, .7152, .0722), values))
    high, low = sorted((luminance(foreground), luminance(background)), reverse=True)
    return (high + .05) / (low + .05)
for ink in ('E4EDEF', 'B0C1C4'):
    assert contrast(ink, '091418') >= 4.5
assert contrast('E4EDEF', '263C41') >= 4.5
android_timeline = ui
windows_timeline = (root / 'desktop/src/animation.rs').read_text()
for value in ('FF091418', 'FF15292F', 'FF355058', 'FFE4EDEF', 'FF263C41'):
    assert value in android_timeline and value in windows_timeline
print('Static Qelem fusion safety and branding checks passed (not an Android build)')
