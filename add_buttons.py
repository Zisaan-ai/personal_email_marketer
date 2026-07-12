import sys
with open('frontend/assets/app.js', encoding='utf-8') as f:
    lines = f.readlines()

def add_button(input_id):
    for i, line in enumerate(lines):
        if f'id="{input_id}"' in line:
            btn = f'<button type="button" onclick="openGalleryModal(\'{input_id}\')" class="secondary-btn" style="padding:6px 12px;font-size:12px;margin-top:6px;width:100%;background:#f1f5f9;border:1px solid #cbd5e1;border-radius:6px;color:#475569;cursor:pointer;"><i class="fa-solid fa-images"></i> Browse Gallery</button>'
            if '</label><input' in line:
                # Need to wrap input and button in a div so they stack properly if needed, but the button is width:100% block
                lines[i] = line.replace('</label><input', '</label><div><input').replace('"></div>', '">' + btn + '</div></div>')
                # If there's no "></div>" at the end, just append after input
                if '</div>' not in line[line.find('<input'):]:
                    lines[i] = line.replace('">', '">' + btn)
            else:
                lines[i] = line.replace('">', '">' + btn)
            print(f'Added button for {input_id}')
            break

add_button('prop-img-src')
add_button('prop-video-thumb')
add_button('prop-header-img')
add_button('prop-prod-img')
add_button('prop-img1-src')
add_button('prop-img2-src')

with open('frontend/assets/app.js', 'w', encoding='utf-8') as f:
    f.writelines(lines)
