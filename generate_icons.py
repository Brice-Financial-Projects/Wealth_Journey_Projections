from PIL import Image, ImageDraw, ImageFont
import os

def create_favicon():
    # Create a 32x32 image with a blue background
    img = Image.new('RGBA', (32, 32), (14, 165, 233, 255))
    draw = ImageDraw.Draw(img)
    
    # Draw a simple chart-like icon
    points = [(4, 24), (8, 16), (12, 20), (16, 12), (20, 16), (24, 8), (28, 12)]
    draw.line(points, fill='white', width=2)
    
    # Save as favicon.ico
    img.save('static/images/favicon.ico')
    
    # Save as PNG for other formats
    img.save('static/images/favicon.png')
    img.save('static/images/apple-touch-icon.png')

def create_og_image():
    # Create a 1200x630 image for social media
    img = Image.new('RGB', (1200, 630), (14, 165, 233))
    draw = ImageDraw.Draw(img)
    
    # Add text
    try:
        font = ImageFont.truetype("Arial", 60)
    except:
        font = ImageFont.load_default()
    
    text = "Wealth Journey Projections"
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    
    x = (1200 - text_width) // 2
    y = (630 - text_height) // 2
    
    draw.text((x, y), text, fill='white', font=font)
    
    # Save the image
    img.save('static/images/og-image.jpg')
    img.save('static/images/twitter-image.jpg')

if __name__ == "__main__":
    # Create directories if they don't exist
    os.makedirs('static/images', exist_ok=True)
    
    # Generate icons
    create_favicon()
    create_og_image()
    
    print("Icons generated successfully!") 