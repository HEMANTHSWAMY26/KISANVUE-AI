from PIL import Image
import os

os.makedirs("screenshots/crops", exist_ok=True)

# 1. Farm Snapshot Card from v2_03_crop_diagnosis.png
img = Image.open("screenshots/v2_03_crop_diagnosis.png")
# Crop the Unified Farm Intelligence card
# image size is 1600 x 1100
# Snapshot card is approximately at y: 250 to 580, x: 150 to 1450
w, h = img.size
snapshot_crop = img.crop((160, 260, 1440, 580))
snapshot_crop.save("screenshots/crops/farm_snapshot_card.png")

# 2. Weather & location top banner
weather_banner = img.crop((160, 110, 1440, 240))
weather_banner.save("screenshots/crops/weather_banner.png")

# 3. Verify Again score card from v3_verify_result_full.png
v3 = Image.open("screenshots/v3_verify_result_full.png")
# The verification result panel starts around y: 500 to 1100, x: 150 to 1450
verify_card = v3.crop((160, 500, 1440, 1050))
verify_card.save("screenshots/crops/verify_result_card.png")

# 4. Baseline vs Follow-up comparison images
verify_comparison = v3.crop((160, 70, 1440, 490))
verify_comparison.save("screenshots/crops/verify_comparison_cards.png")

# 5. Architecture card from v2_07_architecture.png
arch = Image.open("screenshots/v2_07_architecture.png")
# Modal center box
arch_card = arch.crop((350, 40, 1250, 950))
arch_card.save("screenshots/crops/architecture_modal_card.png")

# 6. Telugu UI Header & Scanner
telugu = Image.open("screenshots/13_multilingual_telugu.png")
telugu_crop = telugu.crop((150, 10, 1450, 680))
telugu_crop.save("screenshots/crops/telugu_interface_card.png")

print("Cropped cards successfully generated!")
